# JTEXT.PY
# For displaying text objects
#
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

import pygame


class cTextManager:
    def __init__(self):
        pygame.font.init()
        self.BaseFont10 = pygame.font.Font(None,14)
        self.BaseFont12 = pygame.font.Font(None,20)

    def GetSmallFont(self):
        return self.BaseFont10

    def GetLargeFont(self):
        return self.BaseFont12
            

TextManager = cTextManager()

def GetTextSize(strMessage, isLarge = 1):
    if (isLarge):
        return TextManager.GetLargeFont().size(strMessage)
    else:
        return TextManager.GetSmallFont().size(strMessage)
    
    

def PrintTextAt(strMessage, screen, posX, posY, color):
    message = TextManager.GetLargeFont().render(strMessage,1,color)
    screen.blit(message,(posX,posY))

def PrintTextCentered(strMessage, screen, posX, posY, endPosX, endPosY, color):
    msgLen = TextManager.GetLargeFont().size(strMessage)
    middle = (posX + (endPosX - posX)/2, posY + (endPosY - posY)/2)
    middle = (middle[0] - ((msgLen[0]+1)/2), middle[1] - ((msgLen[1]+1)/2))
    
    message = TextManager.GetLargeFont().render(strMessage,1,color)
    screen.blit(message,(middle[0],middle[1]))    

def PrintSmallTextAt(strMessage, screen, posX, posY, color):
    message = TextManager.GetSmallFont().render(strMessage,1,color)
    screen.blit(message,(posX,posY))    

def GetMessageSprite(strMessage,color):
    message = TextManager.GetLargeFont().render(strMessage,1,color)
    return message
    
    
    



