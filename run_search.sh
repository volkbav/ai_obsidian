#!/bin/bash

cd /home/alex/sync/obsidian/alex/ai_obsidian || exit 1

/home/alex/sync/obsidian/alex/ai_obsidian/.venv/bin/python search.py "$@"