#!/bin/bash

# Gereksinimleri yükle
pip install -r requirements.txt

# fatsh dizin yolu (pwd altındaki fatsh)
CURRENT_DIR="$(pwd)/fatsh"

# fatsh dizini var mı kontrol et
if [ ! -d "$CURRENT_DIR" ]; then
  echo "❌ Directory $CURRENT_DIR does not exist!"
  exit 1
fi

# Aktif shell'i tespit et
CURRENT_SHELL=$(ps -p $$ -o comm=)

if [[ "$CURRENT_SHELL" == "bash" ]]; then
  RC_FILE="$HOME/.bashrc"
elif [[ "$CURRENT_SHELL" == "zsh" ]]; then
  RC_FILE="$HOME/.zshrc"
else
  echo "⚠️ Your shell is not bash or zsh. Skipping PATH modification."
  exit 1
fi

# PATH içinde var mı kontrol et, yoksa ekle
if ! grep -Fxq "export PATH=\"\$PATH:$CURRENT_DIR\"" "$RC_FILE"; then
  echo "export PATH=\"\$PATH:$CURRENT_DIR\"" >> "$RC_FILE"
  echo "✔️ Added $CURRENT_DIR to PATH in $RC_FILE"
else
  echo "ℹ️ PATH already contains $CURRENT_DIR"
fi

echo "🔄 Please restart your terminal or run: source $RC_FILE"

# fatsh.py var mı kontrol et, varsa çalıştır
if [ -f "$CURRENT_DIR/fatsh.py" ]; then
  python3 "$CURRENT_DIR/fatsh.py"
else
  echo "❌ fatsh.py not found in $CURRENT_DIR"
fi
