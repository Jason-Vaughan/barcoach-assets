#!/usr/bin/env python3
"""
Build figures_index.json from page_data JSON files.

Scans docs/page_data/*.json and extracts image information to create
a comprehensive figures index for fast visual search.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def get_manual_page(page_data_file):
    """Map page_data filename to manual page filename."""
    mapping = {
        'bookmarks.json': 'bookmarks.htm',
        'content-fixed.json': 'content-fixed.htm',
        'content.json': 'content.htm',
        'headings.json': 'headings.htm',
        'index.json': 'index.html'
    }
    return mapping.get(page_data_file, page_data_file.replace('.json', '.htm'))


def normalize_src(src):
    """Normalize image src path to ensure it starts with images/."""
    if not src.startswith('images/'):
        return f'images/{src}'
    return src


def extract_figures_from_page_data(page_data_path):
    """Extract figure information from a single page_data JSON file."""
    figures = []

    try:
        with open(page_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        manual_page = get_manual_page(os.path.basename(page_data_path))

        if 'images' in data and isinstance(data['images'], list):
            for image in data['images']:
                if 'src' not in image:
                    continue

                figure = {
                    'file': manual_page,
                    'src': normalize_src(image['src']),
                    'caption': image.get('caption', ''),
                    'alt': image.get('alt', ''),
                    'context': image.get('context', '')
                }

                figures.append(figure)

    except Exception as e:
        print(f"Error processing {page_data_path}: {e}")

    return figures


def build_figures_index():
    """Build the complete figures index from all page_data files."""
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / 'docs'
    page_data_dir = docs_dir / 'page_data'

    if not page_data_dir.exists():
        print(f"Error: {page_data_dir} does not exist")
        return None

    all_figures = []

    # Process all JSON files in page_data directory
    for json_file in page_data_dir.glob('*.json'):
        figures = extract_figures_from_page_data(json_file)
        all_figures.extend(figures)
        print(f"Processed {json_file.name}: {len(figures)} figures")

    # Create the final structure
    figures_index = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'count': len(all_figures),
        'figures': all_figures
    }

    return figures_index


def write_figures_index(figures_index, output_path):
    """Write the figures index to JSON file (compact format)."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(figures_index, f, separators=(',', ':'), ensure_ascii=False)


def update_figures_html(json_path, html_path):
    """Update the figures.html wrapper with the new JSON content."""
    # Read the JSON content
    with open(json_path, 'r', encoding='utf-8') as f:
        json_content = f.read()

    # Create the HTML wrapper
    html_content = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>figures index wrapper</title>
  <meta name="robots" content="noindex,follow">
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 2rem; line-height: 1.5; }}
    h1 {{ margin-bottom: .5rem; }}
    code {{ font-family: ui-monospace, Menlo, Consolas, monospace; }}
  </style>
</head>
<body>
  <h1>figures_index.json (HTML wrapper)</h1>
  <p>Embedded JSON for BarCoach Gen2 fast figure search.</p>
  <script id="figures-json" type="application/json">
{json_content}
  </script>
</body>
</html>'''

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / 'docs'
    figures_json_path = docs_dir / 'figures_index.json'
    figures_html_path = docs_dir / 'figures.html'

    print("Building figures index...")

    figures_index = build_figures_index()
    if figures_index is None:
        return 1

    print(f"Total figures found: {figures_index['count']}")

    # Write the JSON file
    write_figures_index(figures_index, figures_json_path)
    print(f"Written: {figures_json_path}")

    # Update the HTML wrapper
    update_figures_html(figures_json_path, figures_html_path)
    print(f"Updated: {figures_html_path}")

    # Show first 3 figures as requested
    if figures_index['figures']:
        print("\nFirst 3 figures:")
        for i, fig in enumerate(figures_index['figures'][:3]):
            print(f"  {i+1}. {fig['file']} -> {fig['src']}")

    print("\nDone!")
    return 0


if __name__ == '__main__':
    exit(main())
