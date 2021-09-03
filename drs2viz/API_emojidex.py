# emojidex API
# search using predicates - query for codes which contain the specified term
# cont - contains: search term somewhere in the code

from Constants import *
from Functions import *
from fastText import *

import requests
import json

# API authentication using username and token
parameters = {
    'username': 'JoValente',
    'token': '59881669aea5ada2cda17ab572721cf03a57ecc8f5602f2f'
}

r = requests.get('http://www.emojidex.com/api/v1/users/authenticate', params=parameters)

# semi-automatic search - user choice
def semi(term,icon_type):
    param = {'code_cont': term}
    r = requests.get('https://www.emojidex.com/api/v1/search/emoji', params=param)
    r.status_code

    data = r.json()['emoji']
    icon_list = [] 
    for d in data:
        icon_list.append(d['base'])

    if not icon_list:
        return None
    
    print('Search results for icons with the term',term,':')
    jprint(icon_list)
 
    # request input of the name of the chosen icon from the list of matched icons
    icon_name = input('Type name of chosen icon: ')

    source = 'https://cdn.emojidex.com/emoji/px256/' + icon_name + '.png'

    return source, icon_name, icon_type

# automatic search using fastText
def auto(term,type,icon_type):
    param = {'code_cont': term}
    r = requests.get('https://www.emojidex.com/api/v1/search/emoji', params=param)
    r.status_code

    data = r.json()['emoji']
    icon_list = [] 
    for d in data:
        icon_list.append(d['base'])

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

    source = 'https://cdn.emojidex.com/emoji/px256/' + icon_name + '.png'

    return source, icon_name, icon_type

def searchEmojidex(term,type,icon_type):
    if type == 'semi':
        return semi(term,icon_type)
        
    # auto and opposite go through here
    else:
        return auto(term,type,icon_type)