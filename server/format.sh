#!/bin/bash
# Python code formatting script
echo "Formatting Python code..."
cd "$(dirname "$0")"
.venv/bin/isort app/ tests/ --profile black
.venv/bin/black app/ tests/ --line-length 88
echo "✅ Python code formatting complete!"