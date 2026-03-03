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

print_state() {
  local -n _revealed_ref=$1
  local out=""
  local i
  for ((i=0; i<${#_revealed_ref[@]}; i++)); do
    if [[ $i -gt 0 ]]; then out+=" "; fi
    out+="${_revealed_ref[$i]}"
  done
  echo "State: ${out}"
}

interactive_mode() {
  local word="bash"
  local max_wrong=6
  local wrong=0

  local -a letters
  local -a revealed
  local i
  for ((i=0; i<${#word}; i++)); do
    letters+=("${word:i:1}")
    revealed+=("_")
  done

  echo "Word: _ _ _ _"

  local guess
  while IFS= read -r guess; do
    # Only consider the first character; ignore empty lines.
    guess="${guess:0:1}"
    if [[ -z "${guess}" ]]; then
      continue
    fi

    echo "Guess: ${guess}"

    local hit=0
    for ((i=0; i<${#letters[@]}; i++)); do
      if [[ "${letters[$i]}" == "${guess}" ]]; then
        revealed[$i]="${guess}"
        hit=1
      fi
    done

    if [[ $hit -eq 0 ]]; then
      wrong=$((wrong+1))
    fi

    print_state revealed

    local all=1
    for ((i=0; i<${#revealed[@]}; i++)); do
      if [[ "${revealed[$i]}" == "_" ]]; then
        all=0
        break
      fi
    done

    if [[ $all -eq 1 ]]; then
      echo "Result: win"
      return 0
    fi

    if [[ $wrong -ge $max_wrong ]]; then
      echo "Result: lose"
      return 0
    fi
  done

  # If stdin ends before a result, decide based on current state.
  local all=1
  for ((i=0; i<${#revealed[@]}; i++)); do
    if [[ "${revealed[$i]}" == "_" ]]; then
      all=0
      break
    fi
  done
  if [[ $all -eq 1 ]]; then
    echo "Result: win"
  elif [[ $wrong -ge $max_wrong ]]; then
    echo "Result: lose"
  fi
}

if [[ $# -eq 1 && "${1:-}" == "--help" ]]; then
  print_help
  exit 0
fi

if [[ $# -eq 1 && "${1:-}" == "--demo" ]]; then
  demo_mode
  exit 0
fi

if [[ $# -eq 0 ]]; then
  interactive_mode
  exit 0
fi

echo "Error: unsupported arguments. Run: bash hangman.sh --help" >&2
exit 1
