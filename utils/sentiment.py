from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# last notes done 05-10-25 7:37 PM CST
class SentimentAnalyzer:
    def __init__(self):
        self._vd = SentimentIntensityAnalyzer() #analyzer object

    def sentiment(self, text: str) -> float:
        return self._vd.polarity_scores(text)['compound'] # returns neg (negative), neu (neutral), pos (positive), compound (composite) values

    def hype_score(self, likes: int, retweets: int, text: str) -> float: # returns a float; parameters are parts of a tweet and associated type
        s = self.sentiment(text) # compound score from earlier
        return (likes * 0.6 + retweets * 1.2) * s # formula
