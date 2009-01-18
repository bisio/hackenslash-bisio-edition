# TEXTBOX
#
# Displays text information in a scrolling display
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
import jtext


class TextBox:
    def __init__(self):
        self.position = (599,363)
        self.size = (200,599-self.position[1])
        self.textData = []
        self.maxLines = (self.size[1]/12)
        self.displaySurface = None
        self.needsUpdating = 1
        self.textColor = (200,220,255)
        self.borderColor = (199,176,0)

    def AddText(self,textLine):
        leftovers = None
        lineLength = jtext.GetTextSize(textLine)  
        self.textData.append(textLine)
        if len(self.textData)>self.maxLines:
            self.textData = self.textData[1:]
        self.needsUpdating = 1


    def CreateSurface(self):
        self.displaySurface = pygame.Surface((self.size[0],self.size[1])) 
        

    def Draw(self, screen):
        pygame.draw.polygon(self.displaySurface,(16,16,48),
                            [(0,0),(self.size[0]-1,0),(self.size[0]-1,self.size[1]-1),(0,self.size[1]-1)])
        # Frame it all        
        pygame.draw.polygon(self.displaySurface,self.borderColor,
                            [(0,0),(self.size[0]-1,0),(self.size[0]-1,self.size[1]-1),(0,self.size[1]-1)],
                            1)
        posX = 2
        posY = 1
        for x in self.textData:
            jtext.PrintSmallTextAt(x, self.displaySurface, posX, posY, self.textColor)
            posY += 12
        self.needsUpdating = 0          


    def Display(self,screen):
        if (self.displaySurface==None):
            self.CreateSurface()
        if (self.needsUpdating):
            self.Draw(screen)
        screen.blit(self.displaySurface,self.position)

        
        


MainText = TextBox()    
        
    