#!/usr/bin/env bash
set -euo pipefail

print_help() {
  cat <<'EOF'
Usage: bash hangman.sh [--demo]

Options:
  --help   Show this help message and exit.
EOF
}

if [[ $# -eq 1 && "${1:-}" == "--help" ]]; then
  print_help
  exit 0
fi

echo "Error: unsupported arguments. Run: bash hangman.sh --help" >&2
exit 1
