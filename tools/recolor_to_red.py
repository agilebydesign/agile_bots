"""
Recolor orange icons to Scotiabank red (#EC111A)

Usage:
    python tools/recolor_to_red.py [input_dir] [output_dir]
    
    If no arguments, processes src/panel/img/scotia/ in place.
"""
from PIL import Image
import colorsys
import os
import sys

# Scotiabank red in RGB
SCOTIA_RED = (236, 17, 26)  # #EC111A

def rgb_to_hls(r, g, b):
    """Convert RGB (0-255) to HLS (0-1)"""
    return colorsys.rgb_to_hls(r/255, g/255, b/255)

def hls_to_rgb(h, l, s):
    """Convert HLS (0-1) to RGB (0-255)"""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)

def recolor_orange_to_red(image_path, output_path):
    """Recolor orange pixels to Scotiabank red"""
    img = Image.open(image_path).convert('RGBA')
    pixels = img.load()
    
    # Get target red's HLS
    target_h, target_l, target_s = rgb_to_hls(*SCOTIA_RED)
    
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # Skip transparent pixels
            if a < 10:
                continue
            
            # Skip pure black/white/gray pixels
            if abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15:
                continue
            
            # Convert to HLS
            h, l, s = rgb_to_hls(r, g, b)
            
            # Orange hue is roughly 0.05-0.15 (18-54 degrees)
            # Red hue is 0-0.03 or 0.97-1.0
            # Only recolor if it's in the orange/yellow range
            if 0.02 < h < 0.18 and s > 0.2:
                # Shift to red (hue ~0)
                new_h = target_h
                # Keep similar saturation but boost it slightly
                new_s = min(1.0, s * 1.1)
                # Keep lightness
                new_l = l
                
                new_r, new_g, new_b = hls_to_rgb(new_h, new_l, new_s)
                pixels[x, y] = (new_r, new_g, new_b, a)
    
    img.save(output_path)
    print(f"Recolored: {os.path.basename(image_path)}")

def main():
    # Default directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    default_input = os.path.join(repo_root, 'src', 'panel', 'img', 'scotia')
    
    input_dir = sys.argv[1] if len(sys.argv) > 1 else default_input
    output_dir = sys.argv[2] if len(sys.argv) > 2 else input_dir
    
    if not os.path.exists(input_dir):
        print(f"Directory not found: {input_dir}")
        return 1
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    count = 0
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            recolor_orange_to_red(input_path, output_path)
            count += 1
    
    print(f"\nDone! Recolored {count} icons to Scotiabank red.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
