# Translation using Hugging Face Transformers

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# load model (downloads on first call, then uses cached)
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-roa-en")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-roa-en")

# run the text through the model, and decode resulting embedding ids
def runModel(txt):
    res = model.generate(**tokenizer(txt, return_tensors="pt", padding=True))
    translation = [tokenizer.decode(t, skip_special_tokens=True) for t in res]
    return translation

def toEnglish(actors):
    actors_translated = {}

    for key, value in actors.items():
        translation = runModel(value)
        actors_translated[key] = ''.join(translation)
    
    return actors_translated