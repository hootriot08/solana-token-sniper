from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# last notes done 05-10-25 7:37 PM CST
class SentimentAnalyzer:
    def __init__(self):
        # Analyzer object
        self._vd = SentimentIntensityAnalyzer() 

    def sentiment(self, text: str) -> float:
        # returns neg (negative), neu (neutral), pos (positive), compound (composite) values
        return self._vd.polarity_scores(text)['compound'] 
        
     # returns a float; parameters are parts of a tweet and associated type
    def hype_score(self, likes: int, retweets: int, text: str) -> float:
        # compound score from earlier
        s = self.sentiment(text) 
        # formula
        return (likes * 0.6 + retweets * 1.2) * s 
