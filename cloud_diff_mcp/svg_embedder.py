"""
SVG icon embedder - Converts external image references to base64 data URIs.
"""

import base64
import re
from pathlib import Path
from typing import Dict


def embed_icons_in_svg(svg_path: str) -> str:
    """
    Convert external image references in SVG to embedded base64 data URIs.
    This makes the SVG self-contained and displayable in browsers without external files.
    
    Args:
        svg_path: Path to the SVG file
    
    Returns:
        Path to the updated SVG file with embedded icons
    """
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
    
    # Find all xlink:href references to PNG files
    pattern = r'xlink:href="([^"]+\.png)"'
    matches = re.findall(pattern, svg_content)
    
    # Cache for already encoded images
    encoded_cache: Dict[str, str] = {}
    
    # Replace each image reference with base64 data URI
    for image_path in set(matches):  # Use set to avoid duplicate processing
        if image_path in encoded_cache:
            continue
        
        # Check if file exists
        if not Path(image_path).exists():
            print(f"⚠️  Warning: Icon file not found: {image_path}")
            continue
        
        try:
            # Read and encode the image
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                base64_data = base64.b64encode(img_data).decode('utf-8')
                data_uri = f"data:image/png;base64,{base64_data}"
                encoded_cache[image_path] = data_uri
        except Exception as e:
            print(f"⚠️  Warning: Could not encode {image_path}: {e}")
            continue
    
    # Replace all image paths with data URIs
    for image_path, data_uri in encoded_cache.items():
        svg_content = svg_content.replace(f'xlink:href="{image_path}"', f'xlink:href="{data_uri}"')
    
    # Write the updated SVG
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"✅ Embedded {len(encoded_cache)} unique icons as base64 data URIs")
    
    return svg_path
