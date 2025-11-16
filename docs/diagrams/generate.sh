#!/bin/bash

# Script to generate PNG and SVG images from Mermaid source files
# Requires: @mermaid-js/mermaid-cli (npm install -g @mermaid-js/mermaid-cli)

set -e

SOURCE_DIR="source"
OUTPUT_DIR="../assets/images"

echo "Generating diagrams from Mermaid source files..."

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Generate each diagram
for mmd_file in "$SOURCE_DIR"/*.mmd; do
    filename=$(basename "$mmd_file" .mmd)
    echo "  Generating $filename..."

    # Generate PNG (for GitHub README, documentation)
    mmdc -i "$mmd_file" -o "$OUTPUT_DIR/${filename}.png" -w 1200 -H 800 -b transparent

    # Generate SVG (scalable, for web)
    mmdc -i "$mmd_file" -o "$OUTPUT_DIR/${filename}.svg" -w 1200 -H 800 -b transparent
done

echo "✓ All diagrams generated successfully!"
echo "  PNG files: $OUTPUT_DIR/*.png"
echo "  SVG files: $OUTPUT_DIR/*.svg"
