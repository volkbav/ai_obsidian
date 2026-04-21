#!/bin/bash

cd /home/alex/it/ai_obsidian
source .venv/bin/activate  # если используешь venv (если нет — убери)

python search.py "$1"