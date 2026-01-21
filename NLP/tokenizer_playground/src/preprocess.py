import re 
import string

def normalize_text(text: str) -> str:

    if not isinstance(text, str):
        raise TypeError ("text must be string")
    
    text = text.lower().strip()
     # remove emojis / non-ascii
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    # remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # normalize multiple spaces -> single space
    text = re.sub(r"\s+", " ", text).strip()

    return text

def word_tokenize(text: str) -> list[str]:
    text = normalize_text(text)
    return text.split()