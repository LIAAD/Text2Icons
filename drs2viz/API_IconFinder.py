# IconFinder API

from Constants import *
from Functions import *
from fastText import *

import requests
import json

# semi-automatic search - user choice
def semi(term,icon_type):
    url = 'https://api.iconfinder.com/v4/icons/search'
    param = {'query':term, 'count':'20'}
    headers = {'Authorization': 'Bearer h0ELKEfFjOBivPdb9jx6t6IsT2brKCU7GySs53qyYqzuZ2ohXygwYnBn3ijEOJi2'}

    # returns a list of Icon objects in icons and the total count of icons returned
    response = requests.request('GET', url, headers=headers, params=param)

    # convert to dictionary 
    r = json.loads(response.text)

    data = r['icons']
    icon_list = [] # list of icon names
    icon_id = []   # list of icon ids
    for d in data:
        icon_id.append(d['icon_id'])        
        if len(d['tags']) == 1:
            name = name = d['tags'][0]
        else:
            name = d['tags'][0] + '_' + d['tags'][1]
        icon_list.append(name)

    if not icon_list:
        return None
    
    print('Search results for icons with the term',term,':')
    jprint(icon_list)

    # request input of the name of the chosen icon from the list of matched icons
    icon_name = input('Type name of chosen icon: ')
        
    # search for icon by id
    i = icon_list.index(icon_name)
    for d in data:
        if(d['icon_id'] == icon_id[i]):
            if len(d['raster_sizes']) < 8:
                sources = d['raster_sizes'][0]
            else:
                sources = d['raster_sizes'][7]
    
    s = sources['formats']
    source = s[0]['preview_url']

    return source, icon_name, icon_type

# automatic search using fastText
def auto(term,type,icon_type):
    url = 'https://api.iconfinder.com/v4/icons/search'
    param = {'query':term, 'count':'20'}
    headers = {'Authorization': 'Bearer h0ELKEfFjOBivPdb9jx6t6IsT2brKCU7GySs53qyYqzuZ2ohXygwYnBn3ijEOJi2'}

    # returns a list of Icon objects in icons and the total count of icons returned
    response = requests.request('GET', url, headers=headers, params=param)

    # convert to dictionary 
    r = json.loads(response.text)

    data = r['icons']
    icon_list = [] # list of icon names
    icon_id = []   # list of icon ids
    for d in data:
        icon_id.append(d['icon_id'])        
        if len(d['tags']) == 1:
            name = name = d['tags'][0]
        else:
            name = d['tags'][0] + '_' + d['tags'][1]
        icon_list.append(name)

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
        
    # search for icon by id
    i = icon_list.index(icon_name)
    for d in data:
        if(d['icon_id'] == icon_id[i]):
            if len(d['raster_sizes']) < 8:
                sources = d['raster_sizes'][0]
            else:
                sources = d['raster_sizes'][7]
    
    s = sources['formats']
    source = s[0]['preview_url']

    return source, icon_name, icon_type

def searchIconFinder(term,type,icon_type):
    if type == 'semi':
        return semi(term,icon_type)
        
    # auto and opposite go through here
    else:
        return auto(term,type,icon_type)