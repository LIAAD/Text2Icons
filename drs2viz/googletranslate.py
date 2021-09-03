# Translation using Google Translate API

from googletrans import Translator

translator = Translator()

def toEnglish(actors):
    actors_translated = {}

    for key, value in actors.items():
        translation = translator.translate(value, src='pt', dest='en')
        actors_translated[key] = ''.join(translation.text)
    
    return actors_translated