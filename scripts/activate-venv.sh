#!/usr/bin/env bash

if [ -z "${VIRTUAL_ENV:-}" ]; then
  if [ -f "apps/backend/.venv/Scripts/activate" ]; then
    . "apps/backend/.venv/Scripts/activate"
  elif [ -f "apps/backend/.venv/bin/activate" ]; then
    . "apps/backend/.venv/bin/activate"
  else
    echo "No virtual environment activation script found." >&2
    exit 1
  fi
fi