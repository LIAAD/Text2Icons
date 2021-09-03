# Open Emoji API

from Constants import *
from Functions import *
from fastText import *

import requests
import json
from PIL import Image

# semi-automatic search - user choice
def semi(term,icon_type):
    KEY = '90a343bc319fb955bb6892bc6cfc98d9bc8162b7'
    parameters = {'search': term,'access_key': KEY}
    r = requests.get('https://emoji-api.com/emojis?', params=parameters)
 
    data = r.json()
    icon_list = [] 
    for d in data:
        icon_list.append(d['slug'])

    if not icon_list:
        return None

    print('Search results for icons with the term',term,':')
    jprint(icon_list)
 
    # request input of the name of the chosen icon from the list of matched icons
    icon_name = input('Type name of chosen icon: ')
    #parameters = {'access_key': KEY}
    source = 'https://emoji-api.com/emojis/' + icon_name + 'access_key'

    return source, icon_name, icon_type

# automatic search using fastText
def auto(term,type,icon_type):
    KEY = '90a343bc319fb955bb6892bc6cfc98d9bc8162b7'
    parameters = {'search': term,'access_key': KEY}
    r = requests.get('https://emoji-api.com/emojis?', params=parameters)
 
    data = r.json()
    icon_list = [] 
    for d in data:
        icon_list.append(d['slug'])

    if not icon_list:
        return None

    jprint(icon_list)

    if type == 'opposite':
        if icon_type == 'least':
            icon_name = getLeastSimilar(term,icon_list)
        else:
            icon_name = get2MostSimilar(term,icon_list)
    else:
        icon_name = getMostSimilar(term,icon_list)

    print('Icon chosen by fastText: ', icon_name)

    #parameters = {'access_key': KEY}
    source = 'https://emoji-api.com/emojis/' + icon_name + 'access_key'

    return source, icon_name, icon_type

def searchOpenEmoji(term,type,icon_type):
    if type == 'semi':
        return semi(term,icon_type)
        
    # auto and opposite go through here
    else:
        return auto(term,type,icon_type)

#r = requests.get('https://emoji-api.com/emojis/person', params=parameters)
#jprint(r.json())
#print(r.json()[0]['character'])

#data = '\ud83e\uddd1'
#data = u'\U0001F9D1'
#data = 'U+1F600'

#img = Image.new("RGB", (800, 1280), (255, 255, 255))
#img.save("image.png", "PNG")

#data = r.json()[0]['character']
#utf8data = data.encode('UTF-8')
#open('image.png', 'wb').write(utf8data)

