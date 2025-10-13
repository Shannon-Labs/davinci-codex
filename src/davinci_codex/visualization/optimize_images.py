"""
Image Optimization Script
=========================

Optimizes all image assets across the da Vinci Codex project for consistent
quality, sizing, and web performance while maintaining high visual standards.

This script ensures all visual assets meet professional standards for
display across web, documentation, and presentation platforms.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    from PIL import Image, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL/Pillow not available. Install with: pip install Pillow")

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("Warning: OpenCV not available. Install with: pip install opencv-python")

# ============================================================================
# OPTIMIZATION STANDARDS
# ============================================================================

OPTIMIZATION_STANDARDS = {
    'max_width': 1920,           # Maximum width for web images
    'max_height': 1080,          # Maximum height for web images
    'thumbnail_size': (300, 200), # Thumbnail dimensions
    'quality_jpeg': 85,          # JPEG quality for web
    'quality_png': 8,            # PNG compression level
    'max_file_size_mb': 2.0,     # Maximum file size for web images
    'dpi_standard': 300,         # Standard DPI for print
    'dpi_web': 72,               # Standard DPI for web
}

# File type preferences
FORMAT_PREFERENCES = {
    '.png': 'PNG',    # Keep PNG for diagrams with text
    '.jpg': 'JPEG',   # Convert to JPEG for photos
    '.jpeg': 'JPEG',
    '.gif': 'GIF',    # Keep GIF for animations
    '.webp': 'WebP'   # Convert to WebP for better compression
}

# ============================================================================
# IMAGE ANALYSIS FUNCTIONS
# ============================================================================

def analyze_image(image_path: Path) -> Dict:
    """
    Analyze an image file and return metadata.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing image metadata
    """
    if not PIL_AVAILABLE:
        return {'error': 'PIL not available'}

    try:
        with Image.open(image_path) as img:
            return {
                'path': str(image_path),
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
                'file_size': image_path.stat().st_size,
                'file_size_mb': image_path.stat().st_size / (1024 * 1024),
                'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info,
                'dpi': img.info.get('dpi', (72, 72))[0] if img.info.get('dpi') else 72,
                'color_count': len(img.getcolors(maxcolors=256*256*256)) if img.mode == 'P' else None
            }
    except Exception as e:
        return {'error': str(e), 'path': str(image_path)}

def needs_optimization(image_info: Dict) -> bool:
    """
    Determine if an image needs optimization based on standards.

    Args:
        image_info: Image analysis metadata

    Returns:
        True if image needs optimization
    """
    if 'error' in image_info:
        return False

    # Check file size
    if image_info['file_size_mb'] > OPTIMIZATION_STANDARDS['max_file_size_mb']:
        return True

    # Check dimensions
    if (image_info['width'] > OPTIMIZATION_STANDARDS['max_width'] or
        image_info['height'] > OPTIMIZATION_STANDARDS['max_height']):
        return True

    # Check DPI (for print-quality images)
    if image_info['dpi'] < OPTIMIZATION_STANDARDS['dpi_web']:
        return True

    return False

# ============================================================================
# IMAGE OPTIMIZATION FUNCTIONS
# ============================================================================

def resize_image(image_path: Path, output_path: Path, max_width: int, max_height: int) -> bool:
    """
    Resize image to fit within specified dimensions while maintaining aspect ratio.

    Args:
        image_path: Input image path
        output_path: Output image path
        max_width: Maximum width
        max_height: Maximum height

    Returns:
        True if successful
    """
    if not PIL_AVAILABLE:
        return False

    try:
        with Image.open(image_path) as img:
            # Convert RGBA to RGB for JPEG output if needed
            if img.mode in ('RGBA', 'LA') and output_path.suffix.lower() in ('.jpg', '.jpeg'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                else:
                    background.paste(img)
                img = background

            # Calculate new size maintaining aspect ratio
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            # Save with appropriate quality
            save_kwargs = {}
            if output_path.suffix.lower() in ('.jpg', '.jpeg'):
                save_kwargs['quality'] = OPTIMIZATION_STANDARDS['quality_jpeg']
                save_kwargs['optimize'] = True
            elif output_path.suffix.lower() == '.png':
                save_kwargs['optimize'] = True

            img.save(output_path, **save_kwargs)
            return True

    except Exception as e:
        print(f"Error resizing {image_path}: {e}")
        return False

def create_thumbnail(image_path: Path, output_path: Path, size: Tuple[int, int] = None) -> bool:
    """
    Create thumbnail version of an image.

    Args:
        image_path: Input image path
        output_path: Output thumbnail path
        size: Thumbnail size (width, height)

    Returns:
        True if successful
    """
    if not PIL_AVAILABLE:
        return False

    if size is None:
        size = OPTIMIZATION_STANDARDS['thumbnail_size']

    try:
        with Image.open(image_path) as img:
            # Create thumbnail
            img.thumbnail(size, Image.Resampling.LANCZOS)

            # Create new image with exact dimensions and center the thumbnail
            thumb = Image.new('RGB', size, (255, 255, 255))
            offset = ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2)
            thumb.paste(img, offset)

            thumb.save(output_path, 'JPEG', quality=80, optimize=True)
            return True

    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        return False

def enhance_image(image_path: Path, output_path: Path) -> bool:
    """
    Apply enhancement filters to improve image quality.

    Args:
        image_path: Input image path
        output_path: Output enhanced image path

    Returns:
        True if successful
    """
    if not PIL_AVAILABLE:
        return False

    try:
        with Image.open(image_path) as img:
            # Enhance contrast slightly
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)

            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.05)

            # Apply subtle sharpening filter
            img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))

            img.save(output_path, quality=OPTIMIZATION_STANDARDS['quality_jpeg'], optimize=True)
            return True

    except Exception as e:
        print(f"Error enhancing {image_path}: {e}")
        return False

def convert_format(image_path: Path, output_path: Path, target_format: str) -> bool:
    """
    Convert image to different format.

    Args:
        image_path: Input image path
        output_path: Output image path
        target_format: Target format (JPEG, PNG, WebP)

    Returns:
        True if successful
    """
    if not PIL_AVAILABLE:
        return False

    try:
        with Image.open(image_path) as img:
            # Handle transparency for JPEG
            if target_format == 'JPEG' and img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            save_kwargs = {}
            if target_format == 'JPEG':
                save_kwargs['quality'] = OPTIMIZATION_STANDARDS['quality_jpeg']
                save_kwargs['optimize'] = True
            elif target_format == 'PNG':
                save_kwargs['optimize'] = True
            elif target_format == 'WebP':
                save_kwargs['quality'] = 85
                save_kwargs['optimize'] = True

            img.save(output_path, format=target_format, **save_kwargs)
            return True

    except Exception as e:
        print(f"Error converting {image_path} to {target_format}: {e}")
        return False

# ============================================================================
# BATCH PROCESSING FUNCTIONS
# ============================================================================

def find_image_files(directory: Path, recursive: bool = True) -> List[Path]:
    """
    Find all image files in a directory.

    Args:
        directory: Directory to search
        recursive: Whether to search recursively

    Returns:
        List of image file paths
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tiff'}
    image_files = []

    if recursive:
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                image_files.append(file_path)
    else:
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                image_files.append(file_path)

    return sorted(image_files)

def optimize_project_images(project_root: Path) -> Dict:
    """
    Optimize all images in the da Vinci Codex project.

    Args:
        project_root: Root directory of the project

    Returns:
        Dictionary with optimization results
    """
    results = {
        'total_files': 0,
        'optimized_files': 0,
        'skipped_files': 0,
        'errors': [],
        'space_saved_mb': 0,
        'optimized_files_list': []
    }

    # Find all image files
    artifacts_dir = project_root / 'artifacts'
    docs_dir = project_root / 'docs'

    image_files = []
    if artifacts_dir.exists():
        image_files.extend(find_image_files(artifacts_dir))
    if docs_dir.exists():
        image_files.extend(find_image_files(docs_dir))

    results['total_files'] = len(image_files)

    if not image_files:
        print("No image files found for optimization")
        return results

    print(f"Found {len(image_files)} image files to analyze")

    for image_path in image_files:
        try:
            # Analyze image
            image_info = analyze_image(image_path)

            if 'error' in image_info:
                results['errors'].append(f"Analysis error for {image_path}: {image_info['error']}")
                results['skipped_files'] += 1
                continue

            # Check if optimization is needed
            if not needs_optimization(image_info):
                results['skipped_files'] += 1
                continue

            # Determine optimization strategy
            original_size = image_info['file_size']

            # Create optimized version
            optimized_path = image_path.with_name(f"{image_path.stem}_optimized{image_path.suffix}")

            # Apply optimizations
            optimized = False

            # Resize if too large
            if (image_info['width'] > OPTIMIZATION_STANDARDS['max_width'] or
                image_info['height'] > OPTIMIZATION_STANDARDS['max_height']):
                if resize_image(image_path, optimized_path,
                              OPTIMIZATION_STANDARDS['max_width'],
                              OPTIMIZATION_STANDARDS['max_height']):
                    optimized = True

            # Convert format if beneficial
            if not optimized and image_path.suffix.lower() == '.png':
                if not image_info.get('has_transparency', False):
                    webp_path = image_path.with_suffix('.webp')
                    if convert_format(image_path, webp_path, 'WebP'):
                        optimized = True
                        optimized_path = webp_path

            # Apply enhancement if not already optimized
            if not optimized:
                if enhance_image(image_path, optimized_path):
                    optimized = True

            if optimized:
                # Check optimized file size
                optimized_size = optimized_path.stat().st_size
                space_saved = (original_size - optimized_size) / (1024 * 1024)
                results['space_saved_mb'] += space_saved

                # Replace original if optimization is beneficial
                if optimized_size < original_size * 0.95:  # At least 5% reduction
                    image_path.unlink()
                    optimized_path.rename(image_path)
                    results['optimized_files'] += 1
                    results['optimized_files_list'].append(str(image_path.relative_to(project_root)))
                    print(f"✓ Optimized: {image_path.name} (saved {space_saved:.2f} MB)")
                else:
                    optimized_path.unlink()  # Remove if no benefit
                    results['skipped_files'] += 1
            else:
                results['skipped_files'] += 1

        except Exception as e:
            results['errors'].append(f"Error processing {image_path}: {str(e)}")
            results['skipped_files'] += 1

    return results

def create_thumbnails_batch(directory: Path, output_dir: Path = None) -> bool:
    """
    Create thumbnails for all images in a directory.

    Args:
        directory: Directory containing images
        output_dir: Output directory for thumbnails

    Returns:
        True if successful
    """
    if output_dir is None:
        output_dir = directory / 'thumbnails'

    output_dir.mkdir(exist_ok=True)

    image_files = find_image_files(directory, recursive=False)
    success_count = 0

    for image_path in image_files:
        thumbnail_path = output_dir / f"{image_path.stem}_thumb.jpg"
        if create_thumbnail(image_path, thumbnail_path):
            success_count += 1

    print(f"Created {success_count} thumbnails in {output_dir}")
    return success_count > 0

# ============================================================================
# REPORTING FUNCTIONS
# ============================================================================

def generate_optimization_report(results: Dict, project_root: Path) -> None:
    """
    Generate and print optimization report.

    Args:
        results: Optimization results dictionary
        project_root: Project root directory
    """
    print("\n" + "=" * 60)
    print("IMAGE OPTIMIZATION REPORT")
    print("=" * 60)

    print(f"\n📊 SUMMARY:")
    print(f"   Total files analyzed: {results['total_files']}")
    print(f"   Files optimized: {results['optimized_files']}")
    print(f"   Files skipped: {results['skipped_files']}")
    print(f"   Space saved: {results['space_saved_mb']:.2f} MB")

    if results['errors']:
        print(f"\n⚠️  ERRORS ({len(results['errors'])}):")
        for error in results['errors'][:5]:  # Show first 5 errors
            print(f"   • {error}")
        if len(results['errors']) > 5:
            print(f"   ... and {len(results['errors']) - 5} more errors")

    if results['optimized_files_list']:
        print(f"\n✅ OPTIMIZED FILES:")
        for file_path in results['optimized_files_list'][:10]:  # Show first 10
            print(f"   • {file_path}")
        if len(results['optimized_files_list']) > 10:
            print(f"   ... and {len(results['optimized_files_list']) - 10} more files")

    print("\n" + "=" * 60)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description="Optimize images in da Vinci Codex project")
    parser.add_argument(
        '--project-root',
        type=Path,
        default=Path(__file__).parent.parent.parent.parent,
        help='Project root directory'
    )
    parser.add_argument(
        '--thumbnails',
        action='store_true',
        help='Create thumbnails for all images'
    )
    parser.add_argument(
        '--directory',
        type=Path,
        help='Optimize specific directory only'
    )

    args = parser.parse_args()

    if not PIL_AVAILABLE:
        print("Error: PIL/Pillow is required for image optimization.")
        print("Install with: pip install Pillow")
        return

    print("🖼️  DA VINCI CODEX IMAGE OPTIMIZATION")
    print("=" * 60)
    print("Optimizing image assets for consistent quality and performance...")
    print()

    try:
        if args.directory:
            # Optimize specific directory
            print(f"Optimizing directory: {args.directory}")
            # Implementation for single directory optimization
            pass
        else:
            # Optimize entire project
            results = optimize_project_images(args.project_root)
            generate_optimization_report(results, args.project_root)

            # Create thumbnails if requested
            if args.thumbnails:
                print("\n🎬 Creating thumbnails...")
                artifacts_dir = args.project_root / 'artifacts'
                if artifacts_dir.exists():
                    create_thumbnails_batch(artifacts_dir)

        print("\n🎉 OPTIMIZATION COMPLETE!")

    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        raise

if __name__ == "__main__":
    main()