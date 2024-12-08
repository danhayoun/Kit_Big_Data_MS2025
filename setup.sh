#!/bin/bash
# Installer Poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"

# Installer les dépendances avec Poetry
poetry install
