#################################################
##
## ImageData.py
##
## Load of all Images (pictures / textures)
##
#################################################
#
# (c) 2005 Rampant Games
#
# This software is provided as-is, with no warranty expressed or implied. It was thrown together
# in a matter of hours, so any resemblance to useful or readable code is purely coincidental
#
# Permission is granted to use this software for any legal purpose, provided you acknowledge the
# contribution of code by Jay Barnson or Rampant Games somewhere in the documentation. 
# If you do manage to construct something for distribution with this code, it would be nice
# (but not required) to include a link back to http://www.rampantgames.com

import pygame,sys

class ImageData:
    def __init__(self):
        self.textures = dict()
        self.spriteRects = dict()

    def LoadTexture(self, dictionaryEntry, textureFilename):
        try:
            texture = pygame.image.load(textureFilename)
            sheetRect = texture.get_rect()
            self.textures[dictionaryEntry] = [texture,sheetRect]
            self.spriteRects[dictionaryEntry] = [sheetRect]  # Sprite 0 = whole page
            #print "Successfully loaded texture file '%s' (%s)."%(textureFilename,str(sheetRect))
        except:
            print "Failed to load texture file '%s'!"%textureFilename
            return


    def AssignTexture(self, dictionaryEntry, surface):
        sheetRect = surface.get_rect()
        self.textures[dictionaryEntry] = [surface,sheetRect]
        self.spriteRects[dictionaryEntry] = [sheetRect]
        

                

                    

                    
            
        
        
        