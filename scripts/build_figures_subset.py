#!/usr/bin/env python3
"""
Build figures_adjust.json - filtered subset of figures_index.json.

Filters figures where caption or alt matches (?i)(rotate|rotation|adjust).
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path


def matches_rotation_pattern(text):
    """Check if text matches rotation/adjust pattern."""
    if not text:
        return False
    pattern = r'(?i)(rotate|rotation|adjust)'
    return bool(re.search(pattern, text))


def filter_figures(figures_data):
    """Filter figures that match the rotation/adjust pattern."""
    filtered = []

    for figure in figures_data.get('figures', []):
        caption = figure.get('caption', '')
        alt = figure.get('alt', '')

        if matches_rotation_pattern(caption) or matches_rotation_pattern(alt):
            filtered.append(figure)

    return filtered


def main():
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / 'docs'

    input_file = docs_dir / 'figures_index.json'
    output_file = docs_dir / 'figures_adjust.json'

    print("Building filtered figures subset...")

    # Read the input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            figures_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return 1

    # Filter the figures
    filtered_figures = filter_figures(figures_data)

    # Create the output structure
    output_data = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'count': len(filtered_figures),
        'figures': filtered_figures
    }

    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, separators=(',', ':'), ensure_ascii=False)

    print(f"Filtered {len(filtered_figures)} figures matching rotation/adjust pattern")
    print(f"Written: {output_file}")

    # Show results
    if filtered_figures:
        print("\nFirst 3 entries:")
        for i, fig in enumerate(filtered_figures[:3]):
            print(f"  {i+1}. {fig['file']} -> {fig['src']}")
            print(f"     Caption: {fig.get('caption', 'N/A')}")
            print(f"     Alt: {fig.get('alt', 'N/A')}")

    return 0


if __name__ == '__main__':
    exit(main())
