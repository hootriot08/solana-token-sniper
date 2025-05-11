#!/usr/bin/env python3

import sys
import os

# Ensure project root (where utils/ lives) is on PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import logging
from datetime import datetime, timedelta

import pandas as pd
import snscrape.modules.twitter as sntwitter
import fire

from utils.text_cleaner import clean_text, extract_tokens
from utils.sentiment import SentimentAnalyzer

def main(days_back=1, max_tweets=50):
    """
    Scrape recent tweets containing Solana‐slang phrases, compute a hype score,
    and print both the raw tweets and the top tokens by hype score.
    """
    # ─── Configure logging ────────────────────────────────────────────────────
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    # ─── Compute the “since” date ─────────────────────────────────────────────
    since = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    analyzer = SentimentAnalyzer()
    phrases = [
        "just aped", "low cap gem", "next bonk", "100x", "dev doxxed",
        "airdrop incoming", "presale", "based dev", "hidden gem", "melt faces",
        "10x", ".sol", "#solana"
    ]

    records = []
    for phrase in phrases:
        query = f'"{phrase}" lang:en since:{since}'
        logging.info(f"Scraping phrase: '{phrase}'")
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= max_tweets:
                break
            try:
                # Clean text and extract tokens
                text = clean_text(tweet.content)
                tokens = extract_tokens(text)
                # Compute hype score
                score = analyzer.hype_score(tweet.likeCount, tweet.retweetCount, text)

                records.append({
                    'date': tweet.date,
                    'user': tweet.user.username,
                    'followers': tweet.user.followersCount,
                    'content': tweet.content,
                    'likes': tweet.likeCount,
                    'retweets': tweet.retweetCount,
                    'sentiment': analyzer.sentiment(text),
                    'tokens': tokens,
                    'hype_score': score
                })
            except Exception as e:
                logging.warning(f"Skipping tweet #{i} for '{phrase}': {e}")
                continue

    # ─── Build DataFrame ──────────────────────────────────────────────────────
    df = pd.DataFrame(records)
    if df.empty:
        logging.info("No tweets scraped—exiting.")
        return

    # ─── Explode token lists for grouping ────────────────────────────────────
    df_exploded = df.explode('tokens')

    # ─── Compute top tokens by hype score ────────────────────────────────────
    top_tokens = (
        df_exploded
        .groupby('tokens')['hype_score']
        .sum()
        .nlargest(10)
    )

    # ─── Print results to terminal ───────────────────────────────────────────
    print("\n=== All scraped tweets ===")
    print(df.to_string(index=False))

    print("\n=== Top 10 tokens by hype score ===")
    print(top_tokens.to_string())

if __name__ == '__main__':
    fire.Fire(main)
