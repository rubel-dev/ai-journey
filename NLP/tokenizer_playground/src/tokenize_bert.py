from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def bert_toeknize(text: str, max_length: int = 16):

    encoded = tokenizer(
        text,
        padding = "max_length",
        truncation = True,
        max_length = max_length,
        return_tensors= 'pt'

    )

    input_ids = encoded['input_ids'][0].tolist()
    attention_mask = encoded['attention_mask'][0].tolist()
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    return {
        'max_length': max_length,
        'tokens': tokens,
        'input_ids': input_ids,
        'attention_mask':attention_mask,
    }