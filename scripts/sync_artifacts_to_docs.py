#!/usr/bin/env python3
"""
Sync artifact images to docs/images for Jekyll site.

This script copies relevant simulation images from artifacts/*/sim/ to docs/images/
to ensure they're available for the Jekyll site build.
"""

import shutil
from pathlib import Path

# Repository root
REPO_ROOT = Path(__file__).parent.parent
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
DOCS_IMAGES_DIR = REPO_ROOT / "docs" / "images"


def sync_artifact_images():
    """Copy simulation images from artifacts to docs/images."""
    print("=" * 80)
    print("Syncing Artifact Images to Docs")
    print("=" * 80)
    print()

    if not ARTIFACTS_DIR.exists():
        print("❌ Artifacts directory not found!")
        return

    # Ensure docs/images exists
    DOCS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0

    # Find all simulation images
    for artifact_img in ARTIFACTS_DIR.rglob("*.png"):
        # Only sync images from sim/ subdirectories
        if "sim" not in artifact_img.parts:
            continue

        # Get the invention name (parent of sim/)
        invention_name = None
        for i, part in enumerate(artifact_img.parts):
            if part == "sim" and i > 0:
                invention_name = artifact_img.parts[i - 1]
                break

        if not invention_name:
            continue

        # Create destination filename: invention_name_filename.png
        dest_filename = f"{invention_name}_{artifact_img.name}"
        dest_path = DOCS_IMAGES_DIR / dest_filename

        # Check if we need to update
        if dest_path.exists():
            src_mtime = artifact_img.stat().st_mtime
            dest_mtime = dest_path.stat().st_mtime
            if src_mtime <= dest_mtime:
                skipped += 1
                continue

        # Copy the file
        try:
            shutil.copy2(artifact_img, dest_path)
            print(f"✅ {invention_name}/{artifact_img.name} → docs/images/{dest_filename}")
            copied += 1
        except Exception as e:
            print(f"❌ Failed to copy {artifact_img}: {e}")

    print()
    print(f"📊 Summary: {copied} images copied, {skipped} up-to-date")
    print()
    print("=" * 80)


def main():
    """Main entry point."""
    sync_artifact_images()


if __name__ == '__main__':
    main()

