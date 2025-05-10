import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

_stop = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    text = re.sub(r'http\\S+|@\\w+|#', '', text)
    text = re.sub(r'[^A-Za-z0-9\\$ ]+', '', text)
    return ' '.join(w for w in word_tokenize(text.lower()) if w not in _stop)

def extract_tokens(text: str) -> list:
    return re.findall(r'\\$\\w+', text.upper())
