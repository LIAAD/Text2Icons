#-----------------------------------------
#------------ Icon Dictionary ------------
#-----------------------------------------

from Icon import *
from Dictionary import *

if __name__ == '__main__':

    # search icon by term to add to the dictionary
    d = Dictionary()
    d.updateIcons()

    d.search2Add('computer','semi','most')
    #d.search2Add('icon','auto','most') 

    # search opposite icon to add to the opposites dictionary
    # d = Dictionary()
    # d.updateOpposites()

    # d.search2Add('dog','opposite','least') 
    # d.search2Add('dog','opposite','2most') 