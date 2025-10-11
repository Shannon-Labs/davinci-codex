#!/usr/bin/env python3
"""Generate brand assets for da Vinci Codex site."""

from PIL import Image, ImageDraw, ImageFont
import os

# Brand colors
COLORS = {
    'base': '#0D0D0D',
    'surface': 'rgba(16,16,20,0.92)',
    'accent': '#C8A061',
    'ink': '#F4F1EB',
    'secondary': 'rgba(244,241,235,0.72)'
}

# Convert rgba to RGB for PIL
def rgba_to_rgb(rgba_str):
    """Convert rgba string to RGB tuple for PIL."""
    if rgba_str.startswith('#'):
        hex_color = rgba_str.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    elif rgba_str.startswith('rgba'):
        parts = rgba_str.replace('rgba(', '').replace(')', '').split(',')
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    return (0, 0, 0)


def create_swatch(color_key, color_value, output_path):
    """Create a color swatch image."""
    width, height = 120, 60
    img = Image.new('RGB', (width, height), rgba_to_rgb(color_value))
    
    # Add subtle border
    draw = ImageDraw.Draw(img)
    border_color = rgba_to_rgb(COLORS['accent'])
    draw.rectangle([0, 0, width-1, height-1], outline=border_color, width=2)
    
    img.save(output_path)
    print(f"Created {output_path}")


def create_social_preview(output_path):
    """Create social media preview image (1200x630)."""
    width, height = 1200, 630
    
    # Create gradient background
    img = Image.new('RGB', (width, height), rgba_to_rgb(COLORS['base']))
    draw = ImageDraw.Draw(img)
    
    # Add radial gradient effect (simplified)
    center_x, center_y = width // 2, height // 3
    for radius in range(400, 0, -10):
        opacity = int(255 * (radius / 400) * 0.15)
        color = (16 + opacity//4, 16 + opacity//4, 20 + opacity//4)
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            fill=color
        )
    
    # Add title text
    try:
        # Try to use a nice font
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 36)
    except:
        # Fallback to default
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    title_text = "The da Vinci Codex"
    subtitle_text = "Computational archaeology of Renaissance mechanical engineering"
    
    text_color = rgba_to_rgb(COLORS['ink'])
    accent_color = rgba_to_rgb(COLORS['accent'])
    
    # Draw title
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 200), title_text, fill=text_color, font=title_font)
    
    # Draw accent line
    line_y = 320
    line_width = 400
    draw.rectangle(
        [(width - line_width) // 2, line_y, (width + line_width) // 2, line_y + 3],
        fill=accent_color
    )
    
    # Draw subtitle
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 370), subtitle_text, fill=text_color, font=subtitle_font)
    
    img.save(output_path)
    print(f"Created {output_path}")


def create_hero_texture(output_path):
    """Create subtle vellum texture for hero background."""
    width, height = 1920, 400
    img = Image.new('RGB', (width, height), rgba_to_rgb(COLORS['base']))
    draw = ImageDraw.Draw(img)
    
    # Add subtle noise/grain pattern
    import random
    random.seed(42)
    
    for _ in range(5000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        brightness = random.randint(5, 20)
        color = (13 + brightness, 13 + brightness, 13 + brightness)
        draw.point((x, y), fill=color)
    
    # Add vignette effect
    for y in range(height):
        for x in range(0, width, 50):
            dist_from_center = ((x - width/2)**2 + (y - height/2)**2) ** 0.5
            max_dist = ((width/2)**2 + (height/2)**2) ** 0.5
            vignette = 1 - (dist_from_center / max_dist) * 0.3
            
    img.save(output_path, quality=85)
    print(f"Created {output_path}")


def main():
    """Generate all brand assets."""
    # Create palette directory
    palette_dir = '/Volumes/VIXinSSD/davinci-codex/docs/images/palette'
    os.makedirs(palette_dir, exist_ok=True)
    
    # Create swatches
    for color_key, color_value in COLORS.items():
        output_path = os.path.join(palette_dir, f'{color_key}.png')
        create_swatch(color_key, color_value, output_path)
    
    # Create social preview
    create_social_preview('/Volumes/VIXinSSD/davinci-codex/docs/images/codex_social_preview.png')
    
    # Create hero texture
    create_hero_texture('/Volumes/VIXinSSD/davinci-codex/docs/images/hero-texture.png')
    
    print("\nAll brand assets generated successfully!")


if __name__ == '__main__':
    main()

