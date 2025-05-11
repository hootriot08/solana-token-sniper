import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# last note update: 05-10-25 @ 7:45 PM CST
_stop = set(stopwords.words('english')) # nltk gives us some english fluff words (e.g. this, the, a, and) and groups it in a set

def clean_text(text: str) -> str:
    text = re.sub(r'http\\S+|@\\w+|#', '', text) # remove URLs (http\S+), Twitter handles (@\w+), and hashtags (#) from the text.
    text = re.sub(r'[^A-Za-z0-9\\$ ]+', '', text) # removes all characters except uppercase and lowercase letters, digits, dollar signs ($), and spaces.
    # text -> lowercase, tokenizes into indiv words, filters out words in _stop, joins the filtered tokens back into a string
    return ' '.join(w for w in word_tokenize(text.lower()) if w not in _stop)

def extract_tokens(text: str) -> list:
    return re.findall(r'\\$\\w+', text.upper()) #  returns a list of tokens eg $BONK, $SOL, etc
