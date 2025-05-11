#!/usr/bin/env python3
import sys
import os

# notes updated 05-10-25 @ 8:24 PM CST

# Ensure `utils/` is on the import path
sys.path.append(os.path.dirname(__file__))

import logging
from datetime import datetime, timedelta

import pandas as pd
import snscrape.modules.twitter as sntwitter
import fire

from utils.text_cleaner import clean_text, extract_tokens
from utils.sentiment import SentimentAnalyzer

def main(days_back=1, max_tweets=50, output='output.csv'):
    """
    Scrape recent tweets containing specific Solana‐slang phrases, compute
    a custom ‘hype score’, and save results to CSV.

    Args:
        days_back (int): how many days in the past to include (default: 1)
        max_tweets (int): max tweets to fetch per phrase (default: 50)
        output (str): path to write the CSV (default: 'output.csv')
    """

    # ─── 1) Configure the root logger ─────────────────────────────────────────
    # basicConfig() initializes logging only once. Here we:
    #  • set level=INFO so that INFO, WARNING, ERROR, etc. all appear
    #  • choose a format: timestamp, log‐level, then our message
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    # ─── 2) Compute the “since” date string ───────────────────────────────────
    # datetime.now() gives current date/time.
    # Subtracting timedelta(days=days_back) backs up N days.
    # strftime('%Y-%m-%d') formats as 'YYYY-MM-DD', which snscrape needs.
    since = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    # ─── 3) Instantiate your sentiment analyzer ───────────────────────────────
    # This wraps VADER or similar; gives .sentiment(text) and .hype_score(...)
    analyzer = SentimentAnalyzer()

    # ─── 4) Define the list of slang phrases to search for ────────────────────
    phrases = [
        "just aped", "low cap gem", "next bonk", "100x", "dev doxxed",
        "airdrop incoming", "presale", "based dev", "hidden gem", "melt faces",
        "10x", ".sol", "#solana"
    ]

    # ─── 5) Prepare a list to hold each tweet’s processed data ───────────────
    records = []

    # ─── 6) Loop over each target phrase and scrape tweets ───────────────────
    for phrase in phrases:
        # Build an exact‐match query in English since our target date
        query = f'"{phrase}" lang:en since:{since}'
        logging.info(f"Scraping phrase: '{phrase}' (query: {query})")

        # TwitterSearchScraper(query).get_items() yields Tweet objects
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            # Stop once we hit the max for this phrase
            if i >= max_tweets:
                break

            try:
                # ─── 6a) Clean the raw text ─────────────────────────────
                # e.g. remove URLs, lower‐case, strip punctuation
                text = clean_text(tweet.content)

                # ─── 6b) Extract tokens ─────────────────────────────────
                # e.g. split into words, filter stopwords, maybe stem/lemmatize
                tokens = extract_tokens(text)

                # ─── 6c) Compute your custom hype score ─────────────────
                # (likes * 0.6 + retweets * 1.2) * sentiment_compound
                score = analyzer.hype_score(
                    tweet.likeCount,
                    tweet.retweetCount,
                    text
                )

                # ─── 6d) Append this tweet’s details to our records list ─
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
                # If anything goes wrong (bad regex, rate‐limit hiccup, etc.), skip
                logging.warning(f"Skipping tweet #{i} for '{phrase}': {e}")
                continue

    # ─── 7) Build a DataFrame from all records ────────────────────────────────
    df = pd.DataFrame(records)

    # If nothing got scraped, log and exit cleanly
    if df.empty:
        logging.info("No tweets scraped—exiting.")
        return

    # ─── 8) Explode token lists into individual rows ─────────────────────────
    # Converts each row with ['foo','bar'] into two rows, one per token.
    df_exploded = df.explode('tokens')

    # ─── 9) Group by token, sum hype scores, and pick top 10 ────────────────
    top_tokens = (
        df_exploded
        .groupby('tokens')['hype_score']
        .sum()
        .nlargest(10)
    )

    # ─── 10) Log the top tokens & their scores ──────────────────────────────
    logging.info("Top 10 tokens by summed hype score:")
    for token, score in top_tokens.items():
        logging.info(f"{token!r}: {score}")

    # ─── 11) Save the full DataFrame to CSV ──────────────────────────────────
    # encoding='utf-8-sig' writes a BOM so Excel on Windows reads UTF-8 correctly.
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f"Saved {len(df)} tweets to {output}")

if __name__ == '__main__':
    fire.Fire(main)
