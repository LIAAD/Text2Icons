# Icons8 API - Icons by Icon8.com

from Constants import *
from Functions import *
from fastText import *

import requests
import json

# semi-automatic search - user choice
def semi(term,icon_type):
    API_KEY = 'boEYa5VlJbfomUpIv1HXnjlg7LNRzhVhBGvSjLOW'
    param = {'term': term, 'token':API_KEY}

    # search for icons that match the term
    r = requests.get('https://search.icons8.com/api/iconsets/v5/search?', params=param)
    
    #jprint(r.json())
    data = r.json()['icons']
    icon_list = [] 
    for d in data:
        icon_list.append(d['commonName'])
    
    if not icon_list:
        return None
    
    print('Search results for icons with the term',term,':')
    jprint(icon_list)

    # request input of the name of the chosen icon from the list of matched icons
    icon_name = input('Type name of chosen icon: ')

    for d in data:
        if(d['commonName'] == icon_name):
            icon_id = d['id']
        
    # search for icon by id
    param_id = {'id': icon_id, 'token':API_KEY}
    r_icon = requests.get('https://api-icons.icons8.com/publicApi/icons/icon?', params=param_id)
    
    icon = r_icon.json()['icon']
    svg_code = icon['svg']

    return svg_code, icon_name, icon_type

# automatic search using fastText
def auto(term,type,icon_type):
    API_KEY = 'boEYa5VlJbfomUpIv1HXnjlg7LNRzhVhBGvSjLOW'
    param = {'term': term, 'token':API_KEY}

    # search for icons that match the term
    r = requests.get('https://search.icons8.com/api/iconsets/v5/search?', params=param)
    
    #jprint(r.json())
    data = r.json()['icons']
    icon_list = [] 
    for d in data:
        icon_list.append(d['commonName'])
    
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

    for d in data:
        if(d['commonName'] == icon_name):
            icon_id = d['id']
        
    # search for icon by id
    param_id = {'id': icon_id, 'token':API_KEY}
    r_icon = requests.get('https://api-icons.icons8.com/publicApi/icons/icon?', params=param_id)
    
    icon = r_icon.json()['icon']
    svg_code = icon['svg']

    return svg_code, icon_name, icon_type

def searchIcons8(term,type,icon_type):
    if type == 'semi':
        return semi(term,icon_type)
        
    # auto and opposite go through here
    else:
        return auto(term,type,icon_type)