import re
#import pyttsx3
import os
import wikipedia

wikipedia.set_lang('ru')

'''tts = pyttsx3.init()
rate = tts.getProperty('rate') #Скорость произношения
tts.setProperty('rate', rate-50)

volume = tts.getProperty('volume') #Громкость голоса
tts.setProperty('volume', volume+0.9)

voices = tts.getProperty('voices')

# Задать голос по умолчанию
tts.setProperty('voice', 'ru')
tts.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Anna")'''

'''
def gen_ogg(text):
    tts.save_to_file(text, 'media/file.ogg')
    tts.runAndWait()
    return'''

def wiki_search(text):
    try:
        rez = wikipedia.page(text)
        pre = rez.content.split('\n\n\n')
        pics = rez.images
        my_regex = "\(\D*\)\s|\(\D*\)|\[\d\]"
        text = re.sub(my_regex, "", pre[0])
    except Exception as er:
        return([False,])

    return([text, pics, ])

if __name__ == "__main__":
    wiki_search('паук')