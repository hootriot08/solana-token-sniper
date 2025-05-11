Solana Token Sniper

A Twitter scraper and hype‑score analyzer for Solana‑specific slang phrases. Uses snscrape, pandas, and VADER sentiment analysis to track on‑chain memes and airdrop chatter.

Features

Scrape recent tweets containing a list of predefined Solana‑slang phrases

Clean tweet text and extract meaningful tokens

Compute a custom hype score weighted by likes, retweets, and sentiment

Export results to CSV with UTF‑8 BOM for maximum compatibility

Configure look‑back window and tweet limit per phrase via CLI flags

Robust error handling and detailed logging

Prerequisites

Python 3.8 or higher

pip package manager

Installation

Clone the repository

git clone https://github.com/hootriot08/solana-token-sniper.git
cd solana-token-sniper

Install dependencies

pip install -r requirements.txt

Download NLTK data (required for tokenization)

python -m nltk.downloader punkt stopwords

Usage

Command‑line

Run the scraper with your desired settings:

python3 scripts/scraper.py \
  --days-back 1 \
  --max-tweets 50 \
  --output output.csv

--days-back: Number of days in the past to include (default: 1)

--max-tweets: Max tweets to fetch per phrase (default: 50)

--output: Path to the output CSV (default: output.csv)

Example Runner

Use the provided example script for a quick demonstration:

chmod +x examples/run_example.sh
bash examples/run_example.sh

This example scrapes the last day of tweets, up to 100 per phrase, and writes the results to example.csv.

Project Structure

solana-token-sniper/
├── examples/                 # Example runner scripts
│   └── run_example.sh
├── scripts/                  # Main scraper CLI
│   └── scraper.py
├── utils/                    # Shared utilities
│   ├── __init__.py           # Package initializer
│   ├── text_cleaner.py       # Text cleaning functions
│   └── sentiment.py          # SentimentAnalyzer wrapper
├── README.md                 # Project documentation (this file)
└── requirements.txt          # Python dependencies

Testing & Linting (Optional)

Install dev tools

pip install pytest flake8

Run tests

pytest

Check style

flake8 .

Contributing

Contributions are welcome! Please open issues or pull requests for bug fixes and new features. For major changes, open an issue first to discuss the proposal.

License

Add your preferred open source license here.

JIAA
