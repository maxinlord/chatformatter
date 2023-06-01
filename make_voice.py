from gtts import gTTS

def make_voice(text, lang, id_user):
    tts = gTTS(text, lang=lang)
    name_file = f'voices/{id_user}.mp3'
    tts.save(name_file)
