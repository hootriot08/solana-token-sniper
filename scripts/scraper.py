import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
from datetime import datetime, timedelta
from utils.text_cleaner import clean_text, extract_tokens
from utils.sentiment import SentimentAnalyzer

def main(days_back=1, max_tweets=50, output='output.csv'):
    since = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    analyzer = SentimentAnalyzer()
    phrases = [
        "just aped", "low cap gem", "next bonk", "100x", "dev doxxed", 
        "airdrop incoming","presale","based dev","hidden gem","melt faces",
        "10x",".sol","#solana"
    ]

    records = []
    for phrase in phrases:
        query = f'"{phrase}" lang:en since:{since}'
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= max_tweets: break
            text = clean_text(tweet.content)
            tokens = extract_tokens(text)
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

    df = pd.DataFrame(records)
    df.to_csv(output, index=False)
    print(df.groupby('tokens')['hype_score'].sum().nlargest(10))

if __name__ == '__main__':
    import fire
    fire.Fire(main)
