"""
Normal Map Generator for 3D Reliefs - Dynamic Version
"""

from PIL import Image
import numpy as np
import os
import argparse
from pathlib import Path

# Default Configuration
INPUT_COLOR_TEXTURE = "Update_Color.png"
# Initialized to None to enable dynamic naming logic in main()
OUTPUT_NORMAL_MAP = None

DEFAULT_INTENSITY = 2.5

def convert_to_height_map(image):
    gray = image.convert('L')
    height_map = np.array(gray, dtype=np.float32)
    return height_map

def apply_sobel_filter(height_map):
    # Sobel kernels
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
    
    try:
        from scipy import signal
        gradient_x = signal.convolve2d(height_map, sobel_x, mode='same', boundary='symm')
        gradient_y = signal.convolve2d(height_map, sobel_y, mode='same', boundary='symm')
    except ImportError:
        print("  Note: scipy not installed, falling back to alternative method...")
        top = np.roll(height_map, 1, axis=0)
        bottom = np.roll(height_map, -1, axis=0)
        left = np.roll(height_map, 1, axis=1)
        right = np.roll(height_map, -1, axis=1)
        top_left = np.roll(top, 1, axis=1)
        top_right = np.roll(top, -1, axis=1)
        bottom_left = np.roll(bottom, 1, axis=1)
        bottom_right = np.roll(bottom, -1, axis=1)
        
        gradient_x = (-top_left + top_right - 2*left + 2*right - bottom_left + bottom_right)
        gradient_y = (-top_left - 2*top - top_right + bottom_left + 2*bottom + bottom_right)
        
        for g in [gradient_x, gradient_y]:
            g[0, :], g[-1, :], g[:, 0], g[:, -1] = 0, 0, 0, 0
            
    return gradient_x, gradient_y

def load_image_with_alpha(input_path):
    img = Image.open(input_path)
    alpha_mask = None
    if img.mode == 'RGBA':
        alpha_mask = np.array(img.getchannel('A'), dtype=np.uint8)
    elif img.mode == 'P' and 'transparency' in img.info:
        img = img.convert('RGBA')
        alpha_mask = np.array(img.getchannel('A'), dtype=np.uint8)
    else:
        img = img.convert('RGB')
    return img, alpha_mask

def generate_normal_map(input_path, output_path, intensity=DEFAULT_INTENSITY):
    if not os.path.exists(input_path):
        print(f"Error: Source texture '{input_path}' does not exist!")
        return False
    
    color_img, alpha_mask = load_image_with_alpha(input_path)
    width, height = color_img.size
    
    height_map = convert_to_height_map(color_img)
    gradient_x, gradient_y = apply_sobel_filter(height_map)
    
    gx = gradient_x * intensity
    gy = gradient_y * intensity
    
    normal_r = np.clip(gx + 127.5, 0, 255).astype(np.uint8)
    normal_g = np.clip(gy + 127.5, 0, 255).astype(np.uint8)
    normal_b = np.full((height, width), 255, dtype=np.uint8)
    
    if alpha_mask is not None:
        fifa_normal = np.stack([normal_r, normal_g, normal_b, alpha_mask], axis=2)
        normal_img = Image.fromarray(fifa_normal, 'RGBA')
    else:
        fifa_normal = np.stack([normal_r, normal_g, normal_b], axis=2)
        normal_img = Image.fromarray(fifa_normal, 'RGB')
    
    normal_img.save(output_path)
    print(f"Success! Generated file: {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Normal Map Generator - FIFA/EAFC Format")
    parser.add_argument('--intensity', '-i', type=float, default=DEFAULT_INTENSITY)
    parser.add_argument('--input', '-in', type=str, default=INPUT_COLOR_TEXTURE)
    parser.add_argument('--output', '-out', type=str, default=OUTPUT_NORMAL_MAP)
    
    args = parser.parse_args()

    # Dynamic naming logic
    input_p = Path(args.input)
    if args.output is None:
        # Generates name: [Filename] + _-layer + [Extension]
        args.output = f"{input_p.stem}_-layer{input_p.suffix}"
    
    print("=" * 60)
    print(f"Input : {args.input}")
    print(f"Output : {args.output}")
    print(f"Intensity : {args.intensity}")
    print("=" * 60)
    
    success = generate_normal_map(args.input, args.output, args.intensity)
    if not success:
        exit(1)

if __name__ == "__main__":
    main()