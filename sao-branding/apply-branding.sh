#!/bin/bash
# Apply AfyaConnect branding into a SAO checkout / Docker image layer.
# Usage: bash sao-branding/apply-branding.sh [SAO_DIR]
set -eu
SAO_DIR="${1:-/usr/local/share/sao}"
BRAND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$SAO_DIR/custom"
cp "$BRAND_DIR/css/afyaconnect.css" "$BRAND_DIR/css/dark-mode.css" "$SAO_DIR/custom/"
cp "$BRAND_DIR/js/afyaconnect-theme.js" "$SAO_DIR/custom/"
cp "$BRAND_DIR/assets/logo-afya.svg" "$BRAND_DIR/assets/favicon.svg" "$SAO_DIR/custom/"
echo "AfyaConnect branding applied to $SAO_DIR/custom"
