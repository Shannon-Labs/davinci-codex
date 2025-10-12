#!/usr/bin/env python3
"""
Validate internal links in the da Vinci Codex documentation.

This script checks all internal links in markdown files to ensure they
point to existing files and reports broken links.
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from urllib.parse import urlparse

# Repository root
REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"
README_FILE = REPO_ROOT / "README.md"


def find_markdown_links(file_path: Path) -> List[Tuple[str, str, int]]:
    """Find all markdown links in a file."""
    links = []
    
    if not file_path.exists():
        return links
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Find markdown links: [text](url)
            md_links = re.findall(r'\[([^\]]*)\]\(([^\)]+)\)', line)
            for text, url in md_links:
                links.append((text, url, line_num))
            
            # Find HTML href links: href="url"
            html_links = re.findall(r'href=["\']([^"\']+)["\']', line)
            for url in html_links:
                links.append(("", url, line_num))
    
    return links


def is_external_link(url: str) -> bool:
    """Check if a URL is external."""
    if url.startswith(('http://', 'https://', '//', 'mailto:', '#')):
        return True
    parsed = urlparse(url)
    return bool(parsed.scheme or parsed.netloc)


def check_link_exists(link_url: str, base_file: Path) -> Tuple[bool, str]:
    """
    Check if a link points to an existing file.
    
    Returns (exists, message)
    """
    # Skip external links
    if is_external_link(link_url):
        return True, "external"
    
    # Clean up the URL
    clean_url = link_url.split('?')[0].split('#')[0]
    
    if not clean_url:
        return True, "anchor only"
    
    # Try to resolve the path
    possible_paths = []
    
    # Relative to the file
    possible_paths.append(base_file.parent / clean_url)
    
    # Relative to repo root
    possible_paths.append(REPO_ROOT / clean_url)
    
    # Relative to docs
    possible_paths.append(DOCS_DIR / clean_url)
    
    # Try with .md extension if missing
    if not clean_url.endswith(('.md', '.html', '.png', '.jpg', '.svg', '.gif')):
        possible_paths.append(base_file.parent / f"{clean_url}.md")
        possible_paths.append(DOCS_DIR / f"{clean_url}.md")
        possible_paths.append(DOCS_DIR / f"{clean_url}.html")
    
    # Check if any path exists
    for path in possible_paths:
        if path.exists():
            return True, f"found at {path.relative_to(REPO_ROOT)}"
    
    return False, f"not found (tried {len(possible_paths)} locations)"


def validate_file(file_path: Path) -> Dict:
    """Validate all links in a file."""
    result = {
        'file': str(file_path.relative_to(REPO_ROOT)),
        'total_links': 0,
        'external_links': 0,
        'internal_links': 0,
        'broken_links': [],
        'ok_links': []
    }
    
    links = find_markdown_links(file_path)
    result['total_links'] = len(links)
    
    for text, url, line_num in links:
        if is_external_link(url):
            result['external_links'] += 1
            continue
        
        result['internal_links'] += 1
        exists, message = check_link_exists(url, file_path)
        
        if exists:
            result['ok_links'].append({
                'text': text,
                'url': url,
                'line': line_num,
                'message': message
            })
        else:
            result['broken_links'].append({
                'text': text,
                'url': url,
                'line': line_num,
                'message': message
            })
    
    return result


def main():
    """Main validation function."""
    print("=" * 80)
    print("da Vinci Codex - Link Validation Report")
    print("=" * 80)
    print()
    
    # Files to validate
    files_to_validate = [README_FILE]
    
    # Add all markdown files in docs/
    for md_file in DOCS_DIR.rglob('*.md'):
        if '_site' not in str(md_file) and '_build' not in str(md_file):
            files_to_validate.append(md_file)
    
    print(f"📄 Validating {len(files_to_validate)} markdown files...")
    print()
    
    # Validate each file
    all_results = []
    total_broken = 0
    
    for file_path in files_to_validate:
        result = validate_file(file_path)
        if result['broken_links']:
            all_results.append(result)
            total_broken += len(result['broken_links'])
    
    # Print results
    if not all_results:
        print("✅ No broken internal links found!")
        print()
        
        # Print summary
        total_links = sum(validate_file(f)['total_links'] for f in files_to_validate)
        total_internal = sum(validate_file(f)['internal_links'] for f in files_to_validate)
        total_external = sum(validate_file(f)['external_links'] for f in files_to_validate)
        
        print(f"📊 Summary:")
        print(f"   Total links checked: {total_links}")
        print(f"   Internal links: {total_internal}")
        print(f"   External links: {total_external} (not validated)")
        return
    
    print(f"⚠️  Found {total_broken} broken links in {len(all_results)} files")
    print()
    
    for result in all_results:
        print(f"📝 {result['file']}")
        print(f"   Total links: {result['total_links']}")
        print(f"   Broken: {len(result['broken_links'])}")
        
        for broken in result['broken_links']:
            text_display = f'"{broken["text"]}"' if broken['text'] else "(no text)"
            print(f"   ❌ Line {broken['line']}: {text_display}")
            print(f"      URL: {broken['url']}")
            print(f"      Issue: {broken['message']}")
        print()
    
    print("=" * 80)


if __name__ == '__main__':
    main()

