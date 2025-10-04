#!/usr/bin/env bash
# Simple launcher for POS_System for Git Bash / WSL
# Run from project root: ./run_app.sh
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
# If a python virtualenv exists in ./venv, try to use it
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
fi
python run.py
