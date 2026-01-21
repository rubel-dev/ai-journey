import json
from preprocess import normalize_text, word_tokenize
from tokenize_bert import bert_toeknize

def run(text:str):
    cleaned = normalize_text(text)
    words = word_tokenize(text)

    bert_16 = bert_toeknize(text, max_length=16)
    bert_8 = bert_toeknize(text, max_length=8)


    result = {
        'raw_text':text,
        'cleaned_text': cleaned,
        'words_tokens':words,
        'bert_maxlen_16':bert_16,
        'bert_maxlen_8':bert_8
    }

    print(json.dumps(result, indent = 2))

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    
if __name__ == '__main__':
    sample = "I LOVE NLP!!! 😍  Tokenization is cooool, right?"
    run(sample)