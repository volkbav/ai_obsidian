#!/bin/bash

# 📍 директория, где лежит сам скрипт
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 📍 переходим в неё
cd "$SCRIPT_DIR" || exit 1

# 🐍 python из локального venv
PYTHON="$SCRIPT_DIR/.venv/bin/python"

# 🔍 проверка
if [ ! -f "$PYTHON" ]; then
  echo "Python not found in .venv"
  exit 1
fi

# 🚀 запуск
"$PYTHON" search.py "$@"