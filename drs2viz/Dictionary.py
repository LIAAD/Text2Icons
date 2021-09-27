#----------------------------------------------------------------
# Class Dictionary - search terms and add icons to the dictionary 
#----------------------------------------------------------------

from Constants import *
from Functions import *
from fastText import *
from Icon import *

# APIs
from API_emojidex import *
from API_OpenEmoji import *
from API_Icons8 import *
from API_IconFinder import *

# Datasets
from Icons50 import *
from ImageNet import *

from nltk.corpus import wordnet
from cairosvg import svg2png
from shutil import copyfile
import urllib.request
import validators
import json
import os


class Dictionary(object):

    # define dictionary and JSON file for true and opposite icons
    def __init__(self):
        self.icons = dict()
        self.opposites = dict()

        with open('icon_info.json', 'r') as j:
            self.jsonFile = json.load(j)
        self.icon_data = self.jsonFile['icons']

        with open('icon_opposite_info.json', 'r') as k:
            self.jsonOpposite = json.load(k)
        self.opposite_data = self.jsonOpposite['opposites']

    # how to represent the dictionary when displayed
    def __str__(self):
        display = 'Dictionary:\n'
        for k,v in self.icons.items():
            display += '{}: {}.png\n'.format(k,self.icons[k])
        return display

    # update icons from folder to dictionary
    def updateIcons(self):
        for img in os.listdir(IMAGES_DIR):
            if img.split(".")[-1] in ['png']:
                self.icons[img.split('.')[0]] = Icon(img.split('.')[0], os.path.join(IMAGES_DIR,img))

    # list all icons in dictionary
    def getDictionary(self):
        return print(self.icons.keys())

    # show icons info in JSON file 
    def showJson(self):
        return jprint(self.jsonFile)

    # show icon info
    def iconInfo(self,term):
        data_by_icon = {}
        for d in self.icon_data:
            data_by_icon[d['keyTerm']] = d
        return print('Info for',term,'icon:'), jprint(data_by_icon[term])
    
    # show alternative icons
    def alternativeIcons(self,term):
        data_by_icon = {}
        for d in self.icon_data:
            data_by_icon[d['keyTerm']] = d
        return print('Alternative icons for',term,'icon: ', data_by_icon[term]['variants'])

    # show icon - check if exists in dictionary
    def showIcon(self,term):
        if term in self.icons:
            return self.icons[term].displayIcon()
        else:
            raise Exception('The icon does not belong to the dictionary!')
    
    # function that returns a list of synonyms of a word
    def findSyn(self,term):
        if not wordnet.synsets(term):
            return []
        else:
            syn = wordnet.synsets(term)[0]
            return [x.lower() for x in syn.lemma_names()]
            

    # search icon - check if exists
    def search(self,term):
        data_by_icon = {}
        for icon in self.icon_data:
            data_by_icon[icon['keyTerm']] = icon

        # search term in terms
        if term in data_by_icon:
            print('The', term ,'icon belongs to the dictionary.')
            return data_by_icon[term]

        else:
            # if icon does not belong to the dictionary, search in variants
            for icon in self.icon_data:
                for var in icon['variants']:
                    if var == term:
                        print('The term', term ,' matches the icon', icon['keyTerm'],' variants', icon['variants'],' in the dictionary.')
                        return self.icons[icon['keyTerm']]
            return print('The icon for the term: ', term ,'does not exist in the dictionary and does not match any icon variants!')

    def searchImg(self,term):
        data_by_icon = {}
        for icon in self.icon_data:
            data_by_icon[icon['keyTerm']] = icon

        # search term in keyterms
        if term in data_by_icon:
            return data_by_icon[term]['img']
        
        return ''

    # get icon image name - to show in browser (search with most similar in dict - fastext)
    def searchImgName(self,term): 
        match = []
        data_by_icon = {}

        for icon in self.icon_data:
            data_by_icon[icon['keyTerm']] = icon

        # search term in keyterms
        if term in data_by_icon:
            match.append(data_by_icon[term]['keyTerm'])

        # search term in variants
        for icon in self.icon_data:
            for var in icon['variants']:
                if var == term:
                    if data_by_icon[icon['keyTerm']]['keyTerm'] not in match:
                        match.append(data_by_icon[icon['keyTerm']]['keyTerm'])          
                
        if not match:
            return ''

        else:
            icon_name = getMostSimilar(term,match)
            img = self.searchImg(icon_name)
 
            return img

    # update JSON file when adding new icon
    def updateJson(self,keyTerm,variants,img,source,icon_type):

        def write_json(data, file='icon_info.json'): 
            with open(file,'w') as j: 
                json.dump(data,j,indent=4) 

        data = self.jsonFile
        temp = data['icons'] 

        # new icon data
        new_icon = {'keyTerm':keyTerm, 
                    'variants':variants, 
                    'img':img,
                    'source': source,
                    'icon_type': icon_type
                    } 

        temp.append(new_icon)
        write_json(data)

#########################
#       OPPOSITES       #

    # update opposite icons from folder to dictionary
    def updateOpposites(self):
        for img in os.listdir(OPPOSITES_DIR):
            if img.split(".")[-1] in ['png']:
                self.opposites[img.split('.')[0]] = Icon(img.split('.')[0], os.path.join(OPPOSITES_DIR,img))

    # search opposite - check if exists in opposites
    def searchOp(self,term,icon_type):
        data_by_icon = {}
        for icon in self.opposite_data:
            data_by_icon[icon['term']] = icon

        # search term in terms
        if term in data_by_icon:
            if data_by_icon[term]['icon_type'] == icon_type :
                #print('The', term ,'icon belongs to the opposites dictionary.')
                return data_by_icon[term]
            else:
                return print('The icon for the term: ', term ,'does not have an icon with the icon type: ', icon_type,' in the opposites dictionary!')
        else:
            return print('The icon for the term: ', term ,'does not exist in the opposites dictionary!')

    def searchImgOp(self,term):
        data_by_icon = {}
        for icon in self.opposite_data:
            data_by_icon[icon['term']] = icon

        # search term in keyterms
        for op in data_by_icon:
            if term == data_by_icon[op]['keyTerm']:
                return data_by_icon[op]['img']
        
        return ''

    # get opposite icon image name - to show in browser
    def searchImgNameOp(self,term,icon_type):
        match = []
        data_by_icon = {}

        for icon in self.opposite_data:
            data_by_icon[icon['term']] = icon

        # search term in terms
        if term in data_by_icon:
            if data_by_icon[term]['icon_type'] == icon_type :
                match.append(data_by_icon[term]['keyTerm'])

        if not match:
            return ''
            
        else:
            if icon_type == 'least':
                icon_name = getLeastSimilar(term,match)
            else:
                icon_name = get2MostSimilar(term,match)

            img = self.searchImgOp(icon_name)

            return img     
 
            
    # update JSON file when adding new opposite icon
    def updateJsonOp(self,term,keyTerm,img,source,icon_type):

        def write_json(data, file='icon_opposite_info.json'): 
            with open(file,'w') as j: 
                json.dump(data,j,indent=4) 

        data = self.jsonOpposite
        temp = data['opposites'] 

        # new icon data
        new_icon = {'term': term,
                    'keyTerm':keyTerm, 
                    'img':img,
                    'source': source,
                    'icon_type': icon_type
                    } 

        temp.append(new_icon)
        write_json(data)

########################

    # dynamically add icon to dictionary
    # when there is no icon for a specific term, search the available sources
    # allows to choose the type of search (semi-automatic, automatic or opposite) 
    def search2Add(self,term,type,icon_type):
        if type == 'opposite':
            if not self.searchOp(term,icon_type):
                for source in ['IconFinder','Emojidex','Icons-50','Icons8']:
                    self.addIcon(term,source,type,icon_type)
        else:
            if not self.search(term):
                for source in ['IconFinder','Emojidex','Icons-50','Icons8']:
                    self.addIcon(term,source,type,icon_type)

    def addIcon(self,term,source,type,icon_type):

        # from URL
        if validators.url(source):
            self.saveURL(source,term,term,'URL entered',type,r[2])

        # from API search - using emojidex
        elif(source == 'Emojidex'):
            r = searchEmojidex(term,type,icon_type)
            if not r:
                print('No results for icon search in emojidex API.')
            else:
                self.saveURL(r[0],term,r[1],source,type,r[2])

        # from API search - using Open Emoji
        # not saving images yet
        elif(source == 'Open Emoji'):
            r = searchOpenEmoji(term,type,icon_type)
            if not r:
                print('No results for icon search in OpenEmoji API.')
            else:
                self.saveURL(r[0],term,r[1],source,type,r[2])

        # from API search - using Icons8
        # no longer have access to the API - low number of icons available for download for free
        elif(source == 'Icons8'):
            r = searchIcons8(term,type,icon_type)
            if not r:
                print('No results for icon search in Icons8 API.')
            else:
                self.saveSVG(r[0],term,r[1],source,type,r[2])

        # from API search - using IconFinder
        elif(source == 'IconFinder'):
            r = searchIconFinder(term,type,icon_type)
            if not r:
                print('No results for icon search in IconFinder API.')
            else:
                self.saveURL(r[0],term,r[1],source,type,r[2])

        # from local dataset - using Icon-50
        elif(source == 'Icons-50'):
            r = searchIcons50(term,type,icon_type)
            if not r:
                print('No results for icon search in Icons-50.')
            else:
                self.saveLOCAL50(r[0],r[1],term,source,type,r[2])
            
        # from local dataset - using ImageNet
        elif(source == 'ImageNet'):
            r = searchImageNet(term,type,icon_type)
            if not r:
                print('No results for icon search in ImageNet.')
            else:
                self.saveLOCAL(r[0],r[1],source,type,r[2])

        # from unicode
        #elif():

        else:
            raise Exception('Not a recognized source!')

    # SAVE NEW ICONS:
    # save new icon to dictionary
    # update image folder with new icon image
    # update json file with new icon info
    
    # depending on whether they are true or opposite icons, save in different folders

    # from url to png
    def saveURL(self,url,term,keyterm,source,type,icon_type):
        if type == 'opposite':
            img_path = OPPOSITES_DIR + keyterm + '.png'
            img = keyterm + '.png'
            urllib.request.urlretrieve(url,img_path)
            self.updateOpposites()
            self.updateJsonOp(term,keyterm,img,source,icon_type)
        else:
            img_path = IMAGES_DIR + keyterm + '.png'
            img = keyterm + '.png'
            urllib.request.urlretrieve(url,img_path)
            self.updateIcons()
            self.updateJson(keyterm,self.findSyn(term),img,source,icon_type)

    # from svg to png
    def saveSVG(self,svg_code,term,keyterm,source,type,icon_type):
        if type == 'opposite':
            img_path = OPPOSITES_DIR + keyterm + '.png'
            img = keyterm + '.png'
            svg2png(bytestring=svg_code,write_to=img_path)
            self.updateOpposites()
            self.updateJsonOp(term,keyterm,img,source,icon_type)
        else:
            img_path = IMAGES_DIR + keyterm + '.png'
            img = keyterm + '.png'
            svg2png(bytestring=svg_code,write_to=img_path)
            self.updateIcons()
            self.updateJson(keyterm,self.findSyn(term),img,source,icon_type)

    # from local dataset (ImageNet) to image folder
    # by default, it searches for the first image in the list of images
    def saveLOCAL(self,imgs,term,source,type,icon_type):
        if type == 'opposite':
            img_path = imgs[0]
            img = term + '.jpg'
            copyfile(img_path, os.path.join(OPPOSITES_DIR,img))
            self.updateOpposites()
            self.updateJsonOp(term,keyterm,img,source,icon_type)
        else:
            img_path = imgs[0]
            img = term + '.jpg'
            copyfile(img_path, os.path.join(IMAGES_DIR,img))
            self.updateIcons()
            self.updateJson(term,self.findSyn(term),img,source,icon_type)
    
    # from local dataset (Icons-50) to image folder
    def saveLOCAL50(self,path,keyterm,term,source,type,icon_type):
        if type == 'opposite':
            img = keyterm + '.jpg'
            copyfile(path, os.path.join(OPPOSITES_DIR,img))
            self.updateOpposites()
            self.updateJsonOp(term,keyterm,img,source,icon_type)
        else:
            img = keyterm + '.jpg'
            copyfile(path, os.path.join(IMAGES_DIR,img))
            self.updateIcons()
            self.updateJson(keyterm,self.findSyn(term),img,source,icon_type)