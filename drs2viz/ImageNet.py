# ImageNet dataset
# http://image-net.org/download-images

from Constants import *
from Functions import *
from fastText import *

import string
import glob
import os
import re

def get_image_folders(path=IMAGENET_IMAGES_DIR):
    path = r"{}".format(path)
    all_folders = os.listdir(path)
    return all_folders   

def get_image_files(path):
    path = r"{}".format(path)
    all_files = glob.glob(path + "/*.JPEG")
    return all_files

def read_index():
    d = {}
    with open(IMAGENET_INDEX_DIR) as f:
        d = dict(x.rstrip().split(None, 1) for x in f)
    return d

def updateIndex():
    folders = get_image_folders()
    index = read_index()
    index_updated = {}
    for folder in folders:
        if folder in index:
            index_updated[folder] = index[folder]
    return index_updated

def searchTerm(index, term):
    icon_list = []
    numbers = []
    for n in index:
        words = index[n]
        list = [word.strip(string.punctuation) for word in words.split()]
        if term in list:
            icon_list.append(index[n])
            numbers.append(n)
    return numbers, icon_list

# semi-automatic search - user choice
def semi(term,icon_type):

    # get index of words/terms in the dataset
    index = updateIndex()

    # get folder numbers and icon list of matched terms
    numbers, icon_list = searchTerm(index, term)
    
    if not icon_list:
        return None
    
    print('Search results for icons with the term',term,':')
    jprint(icon_list)

    # request input of the name of the chosen icon from the list of matched icons
    icon_name = input('Type name of chosen icon: ')

    # get folder number from list of matched numbers
    i = icon_list.index(icon_name)
    number = numbers[i]

    source = IMAGENET_IMAGES_DIR + number + '/images'
    images = get_image_files(source)
    
    return images, term, icon_type

# automatic search using fastText
def auto(term,type,icon_type):

    # get index of words/terms in the dataset
    index = updateIndex()

    # get folder numbers and icon list of matched terms
    numbers, icon_list = searchTerm(index, term)
    
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

    # get folder number from list of matched numbers
    i = icon_list.index(icon_name)
    number = numbers[i]

    source = IMAGENET_IMAGES_DIR + number + '/images'
    images = get_image_files(source)
    
    return images, term, icon_type

def searchImageNet(term,type,icon_type):
    if type == 'semi':
        return semi(term,icon_type)
        
    # auto and opposite go through here
    else:
        return auto(term,type,icon_type)