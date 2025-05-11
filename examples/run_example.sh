#!/usr/bin/env bash
set -euo pipefail

python3 scripts/scraper.py \
  --days-back=1 \
  --max-tweets=100 \
  --output=example.csv

echo "Done! Output in example.csv"
