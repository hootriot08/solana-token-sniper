# Solana Token Sniper

A Python-based Twitter scraper that snipes early hype around Solana meme tokens—so you can catch 10×–100× pumps before they happen.

## 🔭 Features
- Scrapes tweets matching degen key phrases (e.g. “just aped”, “low cap gem”, “next bonk”)
- Filters English‑language tweets since a configurable date
- Cleans and tokenizes tweet text
- Extracts $TOKEN mentions via regex
- Runs VADER sentiment analysis
- Calculates a **hype score**:
  ```python
  hype_score = (likes * 0.6 + retweets * 1.2) * sentiment_score
  ```
- Aggregates and ranks tokens by total hype
- Outputs results to CSV and prints top candidates

## 🛠️ Installation

1. Clone the repo  
   ```bash
   git clone https://github.com/YOUR_USERNAME/solana-token-sniper.git
   cd solana-token-sniper
   ```

2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

3. Download NLTK data  
   ```bash
   python -m nltk.downloader punkt stopwords
   ```

## 🚀 Usage

```bash
bash examples/run_example.sh
```

Or directly:

```bash
python scripts/scraper.py   --days-back 1   --max-tweets 100   --output solana_hype.csv
```

