import string
import re

def preprocess(text):
    text = text.lower()
    text = text.strip()
    text = re.sub(r'[^\x00-\x7F]+', '', text) 
    text = text.translate(str.maketrans("","", string.punctuation))
    tokens = text.split()
    return tokens

text = "   I LOVE   NLP!!! 😍 "
print(preprocess(text))