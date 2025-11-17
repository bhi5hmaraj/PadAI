#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(git rev-parse --show-toplevel)
HOOKS_DIR="$ROOT_DIR/.githooks"
mkdir -p "$HOOKS_DIR"

cat > "$HOOKS_DIR/pre-push" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
"$(git rev-parse --show-toplevel)"/scripts/prepush_checks.sh
EOF

chmod +x "$HOOKS_DIR/pre-push"
git config core.hooksPath "$HOOKS_DIR"
echo "Installed pre-push hook to run scripts/prepush_checks.sh"

