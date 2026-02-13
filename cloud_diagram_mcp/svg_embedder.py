"""
SVG icon embedder - Converts external image references to base64 data URIs.
"""

import base64
import re
from pathlib import Path
from typing import Dict


def embed_icons_in_svg_content(svg_content: str) -> str:
    """
    Convert external image references in SVG content to embedded base64 data URIs.

    Args:
        svg_content: SVG content as a string

    Returns:
        SVG content with all icons embedded as base64 data URIs
    """
    pattern = r'xlink:href="([^"]+\.png)"'
    matches = re.findall(pattern, svg_content)

    encoded_cache: Dict[str, str] = {}

    for image_path in set(matches):
        if image_path in encoded_cache:
            continue

        if not Path(image_path).exists():
            continue

        try:
            with open(image_path, "rb") as img_file:
                img_data = img_file.read()
                base64_data = base64.b64encode(img_data).decode("utf-8")
                encoded_cache[image_path] = f"data:image/png;base64,{base64_data}"
        except Exception:
            continue

    for image_path, data_uri in encoded_cache.items():
        svg_content = svg_content.replace(f'xlink:href="{image_path}"', f'xlink:href="{data_uri}"')

    return svg_content
