"""
SRS Texture Generator for Coupe du Trône Trophy (Trophy_1004)

This script generates an SRS (Smoothness, Roughness, Metalness) texture map
for the trophy based on the color texture.

Channel Mapping:
- Red Channel (Metalness): 255 for gold areas, 0 for base
- Green Channel: Unused (0)
- Blue Channel (Smoothness): 255 for high-gloss gold, 40 for matte base
- Alpha Channel: Unused (255)

Usage:
    python generate_srs_texture.py
"""

from PIL import Image
import os

# Configuration
INPUT_COLOR_TEXTURE = "main.png"
OUTPUT_SRS_TEXTURE = "trophy_1004_srs.png"

# SRS Values
METALNESS_GOLD = 255      # Red channel for gold areas
METALNESS_BASE = 0        # Red channel for base (non-gold)
SMOOTHNESS_GOLD = 255    # Blue channel for high-gloss gold
SMOOTHNESS_BASE = 40      # Blue channel for matte base


def is_gold_color(r, g, b):
    """
    Determine if a pixel represents gold based on its color.
    Gold is typically characterized by high yellow tones.
    
    Args:
        r, g, b: Color values (0-255)
    
    Returns:
        True if the color is gold, False otherwise
    """
    # Gold detection: High red, high green, low-medium blue
    # Typical gold colors have R > 150, G > 150, B < 200
    # Also check for bright yellows which are common in gold textures
    if r > 150 and g > 150 and b < 220:
        return True
    # Check for desaturated gold/bright yellow
    if r > 180 and g > 180 and b < 100:
        return True
    return False


def generate_srs_texture(input_path, output_path):
    """
    Generate SRS texture from color texture.
    
    Args:
        input_path: Path to input color texture
        output_path: Path to output SRS texture
    """
    if not os.path.exists(input_path):
        print(f"Error: Input texture '{input_path}' not found!")
        print("Please ensure the color texture exists in the same directory.")
        return False
    
    print(f"Loading color texture: {input_path}")
    color_img = Image.open(input_path)
    
    # Convert to RGB if necessary
    if color_img.mode != 'RGB':
        color_img = color_img.convert('RGB')
    
    width, height = color_img.size
    print(f"Texture size: {width}x{height}")
    
    # Create new RGBA image for SRS
    srs_img = Image.new('RGBA', (width, height))
    srs_pixels = srs_img.load()
    color_pixels = color_img.load()
    
    gold_count = 0
    base_count = 0
    
    print("Generating SRS texture...")
    for y in range(height):
        for x in range(width):
            r, g, b = color_pixels[x, y]
            
            if is_gold_color(r, g, b):
                # Gold area: High metalness, high smoothness
                srs_pixels[x, y] = (METALNESS_GOLD, 0, SMOOTHNESS_GOLD, 255)
                gold_count += 1
            else:
                # Base area: No metalness, matte finish
                srs_pixels[x, y] = (METALNESS_BASE, 0, SMOOTHNESS_BASE, 255)
                base_count += 1
    
    # Save the SRS texture
    srs_img.save(output_path)
    print(f"SRS texture saved to: {output_path}")
    
    # Print statistics
    total_pixels = width * height
    gold_percent = (gold_count / total_pixels) * 100
    base_percent = (base_count / total_pixels) * 100
    
    print(f"\nStatistics:")
    print(f"  Gold areas: {gold_count} pixels ({gold_percent:.1f}%)")
    print(f"  Base areas: {base_count} pixels ({base_percent:.1f}%)")
    print(f"\nSRS Values:")
    print(f"  Gold - Metalness: {METALNESS_GOLD}, Smoothness: {SMOOTHNESS_GOLD}")
    print(f"  Base - Metalness: {METALNESS_BASE}, Smoothness: {SMOOTHNESS_BASE}")
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("SRS Texture Generator for Coupe du Trône Trophy")
    print("=" * 60)
    print()
    
    success = generate_srs_texture(INPUT_COLOR_TEXTURE, OUTPUT_SRS_TEXTURE)
    
    if success:
        print("\nTexture generation completed successfully!")
    else:
        print("\nTexture generation failed!")
        exit(1)

