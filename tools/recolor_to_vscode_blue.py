"""
Recolor orange icons to VS Code blue (#569CD6) for ACE branding

Usage:
    python tools/recolor_to_vscode_blue.py [input_dir] [output_dir]
    
    If no arguments, copies from src/panel/img/ to src/panel/img/ace/ and recolors.
"""
from PIL import Image
import colorsys
import os
import sys
import shutil

# VS Code blue in RGB
VSCODE_BLUE = (86, 156, 214)  # #569CD6

def rgb_to_hls(r, g, b):
    """Convert RGB (0-255) to HLS (0-1)"""
    return colorsys.rgb_to_hls(r/255, g/255, b/255)

def hls_to_rgb(h, l, s):
    """Convert HLS (0-1) to RGB (0-255)"""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)

def recolor_orange_to_blue(image_path, output_path):
    """Recolor orange pixels to VS Code blue"""
    img = Image.open(image_path).convert('RGBA')
    pixels = img.load()
    
    # Get target blue's HLS
    target_h, target_l, target_s = rgb_to_hls(*VSCODE_BLUE)
    
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
            # We want to convert orange to VS Code blue
            if 0.02 < h < 0.18 and s > 0.3:
                # Keep same lightness and saturation, change hue to blue
                new_r, new_g, new_b = hls_to_rgb(target_h, l, target_s)
                pixels[x, y] = (new_r, new_g, new_b, a)
    
    img.save(output_path)
    print(f"  Recolored: {os.path.basename(output_path)}")

def process_directory(input_dir, output_dir):
    """Process all PNG files in directory"""
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            # Skip subdirectories
            if os.path.isdir(input_path):
                continue
                
            recolor_orange_to_blue(input_path, output_path)

def main():
    if len(sys.argv) == 3:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        # Default: copy from img/ to img/ace/
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(script_dir)
        input_dir = os.path.join(repo_root, 'src', 'panel', 'img')
        output_dir = os.path.join(repo_root, 'src', 'panel', 'img', 'ace')
    
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print("Recoloring orange to VS Code blue (#569CD6)...")
    
    process_directory(input_dir, output_dir)
    print("Done!")

if __name__ == '__main__':
    main()
