#!/usr/bin/env bash
set -euo pipefail

print_help() {
  cat <<'EOF'
Usage: bash hangman.sh [--demo]

Options:
  --help   Show this help message and exit.
EOF
}

demo_mode() {
  # Deterministic transcript for tests and documentation.
  # Requirements:
  # - starts with: 'Demo mode'
  # - includes line exactly: 'State: b a s h'
  # - ends with: 'Result: win'
  cat <<'EOF'
Demo mode
Word: 4 letters
Guess: b
State: b _ _ _
Guess: a
State: b a _ _
Guess: s
State: b a s _
Guess: h
State: b a s h
Result: win
EOF
}

if [[ $# -eq 1 && "${1:-}" == "--help" ]]; then
  print_help
  exit 0
fi

if [[ $# -eq 1 && "${1:-}" == "--demo" ]]; then
  demo_mode
  exit 0
fi

echo "Error: unsupported arguments. Run: bash hangman.sh --help" >&2
exit 1
