"""
Change black backgrounds to VS Code dark grey (#1E1E1E) in PNG images.

Usage:
    python tools/change_bg_to_vscode_grey.py [input_dir] [output_dir]
    
    If no arguments, processes src/panel/img/ace/ in place.
"""
from PIL import Image
import os
import sys

# VS Code dark grey
VSCODE_GREY = (30, 30, 30)  # #1E1E1E

def change_black_to_grey(image_path, output_path):
    """Change black/near-black pixels to VS Code grey"""
    img = Image.open(image_path).convert('RGBA')
    pixels = img.load()
    
    width, height = img.size
    changed = 0
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # Skip transparent pixels
            if a < 10:
                continue
            
            # Check if pixel is black or near-black (all RGB values < 20)
            if r < 20 and g < 20 and b < 20:
                # Change to VS Code grey, keep alpha
                pixels[x, y] = (VSCODE_GREY[0], VSCODE_GREY[1], VSCODE_GREY[2], a)
                changed += 1
    
    img.save(output_path)
    print(f"Changed {changed} pixels: {os.path.basename(image_path)}")

def main():
    # Default directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    default_input = os.path.join(repo_root, 'src', 'panel', 'img', 'ace')
    
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
            change_black_to_grey(input_path, output_path)
            count += 1
    
    print(f"\nDone! Processed {count} icons (black → #1E1E1E).")
    return 0

if __name__ == '__main__':
    sys.exit(main())
