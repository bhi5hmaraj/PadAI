#!/bin/bash

# Alternative script to generate diagrams using mermaid.ink online service
# Doesn't require local installation of mermaid-cli

set -e

SOURCE_DIR="source"
OUTPUT_DIR="../assets/images"

echo "Generating diagrams using mermaid.ink..."

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to URL-encode the diagram
url_encode() {
    local string="${1}"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            * ) printf -v o '%%%02x' "'$c"
        esac
        encoded+="${o}"
    done
    echo "${encoded}"
}

# Function to generate diagram from mermaid.ink
generate_diagram() {
    local mmd_file="$1"
    local filename=$(basename "$mmd_file" .mmd)

    echo "  Generating $filename..."

    # Read mermaid content
    content=$(<"$mmd_file")

    # Encode content for URL
    # Using base64 encoding which mermaid.ink supports
    encoded=$(echo -n "$content" | base64 | tr -d '\n' | tr '+/' '-_' | tr -d '=')

    # Download PNG from mermaid.ink
    curl -s "https://mermaid.ink/img/$encoded?type=png" -o "$OUTPUT_DIR/${filename}.png"

    # Download SVG from mermaid.ink
    curl -s "https://mermaid.ink/svg/$encoded" -o "$OUTPUT_DIR/${filename}.svg"

    echo "    ✓ ${filename}.png"
    echo "    ✓ ${filename}.svg"
}

# Generate each diagram
for mmd_file in "$SOURCE_DIR"/*.mmd; do
    generate_diagram "$mmd_file"
done

echo ""
echo "✓ All diagrams generated successfully using mermaid.ink!"
echo "  PNG files: $OUTPUT_DIR/*.png"
echo "  SVG files: $OUTPUT_DIR/*.svg"
