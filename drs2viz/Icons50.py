# Icons-50 dataset
# https://www.kaggle.com/danhendrycks/icons50?select=Icons-50.npy

'''
     Dictionary with keys: 
     'class', with 10000 elements in {0,1,…,49}; 
     'style', with 10000 elements in {'microsoft', 'apple', …, 'facebook'}; 
     'image' with 10000 3x32x32 images representing the icons; 
     'rendition' , with 10000 strings where each indicates the icon's version; 
     'subtype', with 10000 elements which specify the subtype of a class such as 'whale' or 'shark' for the marine animals class.
'''

from Constants import *
from Functions import *
from fastText import *

import numpy as np
import glob
import os

def get_image_folders(path=ICONS50_IMAGES_DIR):
    path = r"{}".format(path)
    all_folders = os.listdir(path)
    all_folders.remove('README.txt')
    all_folders.remove('.DS_Store')
    all_folders.sort()
    return all_folders 

def get_image_files(path):
    path = r"{}".format(path)
    all_files = glob.glob(path + "/*.png")
    return all_files

def searchTerm(dict,class_names,term):
    icon_list = []

    # term matches class names
    for c_name in class_names:
        if term in c_name.split('_'):
            icon_list.append(c_name)

    # term matches subtype names
    for s_name in dict['subtype']:
        if term in s_name.split('_'):
            icon_list.append(s_name)

    return icon_list

def get_key(dict,icon_name):
    if icon_name in dict['subtype']:
        key = 'subtype'
    else:
        key = 'class'
    return key

def split_at(file, delimiter, n):
        words = file.split(delimiter)
        return delimiter.join(words[n:])

def searchSource(class_names,class_data,subtype_names,icon_name):

    # find folder where the searched subtype is located
    for c, s in zip(class_data, subtype_names):
        if icon_name == s:
            folder_number = c

    folder = class_names[folder_number]
    
    # find image file name among images in folder
    path = ICONS50_IMAGES_DIR + folder
    imgs = get_image_files(path)

    for img in imgs:
        img_name = split_at(img, '/', 4)       # split at fourth bar
        pic_name = split_at(img_name, '_', 2)  # split at second underscore
        name, ext = os.path.splitext(pic_name)

        if icon_name == name:
            break

    return folder, img_name

# semi-automatic search - user choice
def semi(term,icon_type):

    icons_dict = np.load(ICONS50_NPY_DIR, allow_pickle=True).item()
    
    # get 'class' names
    class_names = get_image_folders()

    # get 'class' data in dict
    class_data = icons_dict['class']
    class_data = list(class_data)

    # get 'subtype' names
    subtype_names = icons_dict['subtype']
    subtype_names = list(subtype_names)
    
    icon_list = searchTerm(icons_dict,class_names,term)

    if not icon_list:
        return None
    
    print('Search results for icons with the term',term,':')
    jprint(icon_list)

    # request input of the name of the chosen icon from the list of matched icons
    icon_name = input('Type name of chosen icon: ')
    
    # key of chosen icon
    key = get_key(icons_dict,icon_name)
    
    # by default, if matched icon with class name, search for first icon in folder
    if key == 'class':
        imgs = get_image_files(ICONS50_IMAGES_DIR + icon_name)
        pic_name = imgs[0]
        source = ICONS50_IMAGES_DIR + icon_name + pic_name
    else:
        folder, pic_name = searchSource(class_names,class_data,subtype_names,icon_name)
        source = ICONS50_IMAGES_DIR + folder + '/' + pic_name

    return source, icon_name, icon_type

# automatic search using fastText
def auto(term,type,icon_type):
    icons_dict = np.load(ICONS50_NPY_DIR, allow_pickle=True).item()
    
    # get 'class' names
    class_names = get_image_folders()

    # get 'class' data in dict
    class_data = icons_dict['class']
    class_data = list(class_data)

    # get 'subtype' names
    subtype_names = icons_dict['subtype']
    subtype_names = list(subtype_names)
    
    icon_list = searchTerm(icons_dict,class_names,term)

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
    
    # key of chosen icon
    key = get_key(icons_dict,icon_name)
    
    # by default, if matched icon with class name, search for first icon in folder
    if key == 'class':
        imgs = get_image_files(ICONS50_IMAGES_DIR + icon_name)
        pic_name = imgs[0]
        source = ICONS50_IMAGES_DIR + icon_name + pic_name
    else:
        folder, pic_name = searchSource(class_names,class_data,subtype_names,icon_name)
        source = ICONS50_IMAGES_DIR + folder + '/' + pic_name

    return source, icon_name, icon_type

def searchIcons50(term,type,icon_type):
    if type == 'semi':
        return semi(term,icon_type)
        
    # auto and opposite go through here
    else:
        return auto(term,type,icon_type)