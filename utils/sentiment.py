from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self._vd = SentimentIntensityAnalyzer()

    def sentiment(self, text: str) -> float:
        return self._vd.polarity_scores(text)['compound']

    def hype_score(self, likes: int, retweets: int, text: str) -> float:
        s = self.sentiment(text)
        return (likes * 0.6 + retweets * 1.2) * s
