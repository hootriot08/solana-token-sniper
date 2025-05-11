#!/usr/bin/env bash
# examples/run_example.sh

set -euo pipefail

# Example: scrape tweets from the last day, 100 per phrase, write to example.csv
python3 scraper.py --days_back=1 --max_tweets=100 --output=example.csv
echo "Done! Output in example.csv"
