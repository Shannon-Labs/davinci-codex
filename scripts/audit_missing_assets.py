#!/usr/bin/env python3
"""
Audit missing assets in the da Vinci Codex repository.

This script scans markdown files for image references and checks if they exist,
suggesting available alternatives from artifacts/ and docs/images/.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Repository root
REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
README_FILE = REPO_ROOT / "README.md"


def find_image_references(file_path: Path) -> List[Tuple[str, int]]:
    """Find all image references in a markdown file."""
    references = []

    if not file_path.exists():
        return references

    with open(file_path, encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Find markdown image syntax: ![alt](path)
            md_images = re.findall(r'!\[([^\]]*)\]\(([^\)]+)\)', line)
            for _alt, path in md_images:
                references.append((path, line_num))

            # Find HTML img tags: <img src="path" />
            html_images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', line)
            for path in html_images:
                references.append((path, line_num))

    return references


def check_image_exists(image_path: str, base_dir: Path) -> bool:
    """Check if an image file exists relative to base directory."""
    # Handle URLs
    if image_path.startswith(('http://', 'https://', '//')):
        return True  # Assume external URLs are valid

    # Clean up the path
    clean_path = image_path.split('?')[0].split('#')[0]

    # Try multiple possible locations
    possible_paths = [
        base_dir / clean_path,
        REPO_ROOT / clean_path,
        DOCS_DIR / clean_path,
    ]

    return any(p.exists() for p in possible_paths)


def find_available_images() -> Dict[str, List[Path]]:
    """Find all available images in docs/images and artifacts/."""
    available = {
        'docs': [],
        'artifacts': []
    }

    # Scan docs/images
    docs_images_dir = DOCS_DIR / "images"
    if docs_images_dir.exists():
        for img in docs_images_dir.rglob('*'):
            if img.is_file() and img.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
                available['docs'].append(img)

    # Scan artifacts
    if ARTIFACTS_DIR.exists():
        for img in ARTIFACTS_DIR.rglob('*.png'):
            if '/sim/' in str(img) or img.parent.name == 'sim':
                available['artifacts'].append(img)

    return available


def suggest_alternatives(missing_path: str, available: Dict[str, List[Path]]) -> List[str]:
    """Suggest alternative images based on filename similarity."""
    suggestions = []
    missing_name = Path(missing_path).stem.lower()

    # Look for similar names
    for category, images in available.items():
        for img in images:
            img_name = img.stem.lower()
            # Check for partial matches
            if missing_name in img_name or img_name in missing_name:
                rel_path = img.relative_to(REPO_ROOT)
                suggestions.append(f"{rel_path} (from {category})")

    return suggestions[:3]  # Top 3 suggestions


def audit_file(file_path: Path, available_images: Dict[str, List[Path]]) -> Dict:
    """Audit a single markdown file."""
    result = {
        'file': str(file_path.relative_to(REPO_ROOT)),
        'total_images': 0,
        'missing_images': [],
        'ok_images': []
    }

    references = find_image_references(file_path)
    result['total_images'] = len(references)

    for img_path, line_num in references:
        if check_image_exists(img_path, file_path.parent):
            result['ok_images'].append({
                'path': img_path,
                'line': line_num
            })
        else:
            suggestions = suggest_alternatives(img_path, available_images)
            result['missing_images'].append({
                'path': img_path,
                'line': line_num,
                'suggestions': suggestions
            })

    return result


def main():
    """Main audit function."""
    print("=" * 80)
    print("da Vinci Codex - Asset Audit Report")
    print("=" * 80)
    print()

    # Find available images
    print("📸 Scanning for available images...")
    available_images = find_available_images()
    print(f"   Found {len(available_images['docs'])} images in docs/images/")
    print(f"   Found {len(available_images['artifacts'])} images in artifacts/*/sim/")
    print()

    # Files to audit
    files_to_audit = [README_FILE]

    # Add all markdown files in docs/
    for md_file in DOCS_DIR.rglob('*.md'):
        if '_site' not in str(md_file) and '_build' not in str(md_file):
            files_to_audit.append(md_file)

    print(f"📄 Auditing {len(files_to_audit)} markdown files...")
    print()

    # Audit each file
    all_results = []
    total_missing = 0

    for file_path in files_to_audit:
        result = audit_file(file_path, available_images)
        if result['missing_images']:
            all_results.append(result)
            total_missing += len(result['missing_images'])

    # Print results
    if not all_results:
        print("✅ No missing images found!")
        return

    print(f"⚠️  Found {total_missing} missing image references in {len(all_results)} files")
    print()

    for result in all_results:
        print(f"📝 {result['file']}")
        print(f"   Total images: {result['total_images']}")
        print(f"   Missing: {len(result['missing_images'])}")

        for missing in result['missing_images']:
            print(f"   ❌ Line {missing['line']}: {missing['path']}")
            if missing['suggestions']:
                print("      💡 Suggestions:")
                for suggestion in missing['suggestions']:
                    print(f"         - {suggestion}")
        print()

    # Save detailed report
    report_path = REPO_ROOT / "asset_audit_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            'summary': {
                'total_files_audited': len(files_to_audit),
                'files_with_missing_images': len(all_results),
                'total_missing_images': total_missing
            },
            'available_images': {
                'docs_count': len(available_images['docs']),
                'artifacts_count': len(available_images['artifacts'])
            },
            'results': all_results
        }, f, indent=2)

    print(f"📊 Detailed report saved to: {report_path}")
    print()
    print("=" * 80)


if __name__ == '__main__':
    main()

