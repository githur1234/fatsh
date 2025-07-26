#!/bin/bash
pip install -r requirements.txt
CURRENT_DIR="$(pwd)/fatsh/"
SHELL_NAME=$(basename "$SHELL")
if [ "$SHELL_NAME" = "bash" ]; then
  RC_FILE="$HOME/.bashrc"
elif [ "$SHELL_NAME" = "zsh" ]; then
  RC_FILE="$HOME/.zshrc"
else
  echo "Your shell is not zsh or bash. Skipping global installation of fatsh."
  exit 1
fi
echo "export PATH=\"\$PATH:$CURRENT_DIR\"" >> "$RC_FILE"
source "$RC_FILE"
python3 "$CURRENT_DIR/fatsh.py"
