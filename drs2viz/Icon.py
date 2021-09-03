#--------------------------------------------------
# Class Icon - get the icon image using Icon object
#--------------------------------------------------

from Constants import *

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import filetype


class Icon(object):

    def __init__(self,term,img_path):
        self.term = term
        # chech if the load file is an image
        if filetype.is_image(img_path):
            # create image surface from image path
            self.img_surface = pygame.image.load(img_path)
        else:
            raise Exception('The path provided is not an existing image!')
    
    def __str__(self):
        return '{self.term}'.format(self=self)

    # define display to show icon image
    def displayIcon(self):
        pygame.init() 
        white = (255, 255, 255) 

        # create display for surface object with X and Y dimensions
        X = 400
        Y = 400
        display_surface = pygame.display.set_mode((X,Y)) 
        pygame.display.set_caption(self.term) 

        # get surface object of icon from dictionary
        image = self.img_surface

        while True : 
            display_surface.fill(white) 
            display_surface.blit(image,(0,0)) 

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                    quit() 
                pygame.display.update()
