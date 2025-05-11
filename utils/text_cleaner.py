import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# last note update: 05-10-25 @ 7:45 PM CST
_stop = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    # remove URLs, Twitter handles, and entire hashtags
    text = re.sub(r'http\S+|@\w+|#\w*', '', text)
    # allow only letters, digits, dollar-signs, and spaces
    text = re.sub(r'[^A-Za-z0-9\$ ]+', '', text)
    # lowercase → tokenize → drop stopwords → rejoin
    tokens = word_tokenize(text.lower())
    filtered = [w for w in tokens if w not in _stop]
    return ' '.join(filtered)

def extract_tokens(text: str) -> list:
    # normalize to uppercase, then pull out $TICKER-style tokens
    return re.findall(r'\$\w+', text.upper())
