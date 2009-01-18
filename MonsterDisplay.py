# MonsterDisplay
#
# shows monster information in a display
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
import Monster
import jtext

class MonsterDisplay:
    def __init__(self):
        self.position = (599,263)
        self.size = (200,100)
        self.monster = None
        self.borderColor = (199,176,0)
        self.displaySurface = None
        
                
                        

    def SetMonster(self,monster):
        self.monster = monster

    def ClearMonster(self):
        self.monster = None

    def GenerateDisplaySurface(self):
        self.displaySurface = pygame.Surface((self.size[0],self.size[1])) 

    def Draw(self):        
        pygame.draw.polygon(self.displaySurface,(16,16,48),
                            [(0,0),(self.size[0]-1,0),(self.size[0]-1,self.size[1]-1),(0,self.size[1]-1)])
        # Frame it all        
        pygame.draw.polygon(self.displaySurface,self.borderColor,
                            [(0,0),(self.size[0]-1,0),(self.size[0]-1,self.size[1]-1),(0,self.size[1]-1)],
                            1)
        if (self.monster==None):
            # We're done
            return
        if (self.monster.inactive):
            # We're also done
            self.monster = None
            return
        
        posX = 2
        posY = 1
        
        jtext.PrintTextAt("%s"%self.monster.name,
                          self.displaySurface,
                          posX, posY,(255,200,32))
        posY += 16
        jtext.PrintTextAt("Level: %d"%self.monster.Attributes.GetLevel(),
                          self.displaySurface,
                          posX, posY,(255,200,32))

        attitude = "Neutral Aggressive"
        if (self.monster.attitude<0):
            attitude = "Angrified"
        if (self.monster.attitude>0):
            attitude = "Non-Hostile."

        posY += 16
        jtext.PrintTextAt("Attitude: %s"%attitude,
                          self.displaySurface,
                          posX, posY,(255,200,32))            

        
        posY += 16
        jtext.PrintTextAt("Hit Points: %d"%self.monster.GetCurrentHitPoints(),
                          self.displaySurface,
                          posX, posY,(255,200,32))
        posY += 16
        jtext.PrintTextAt("Magic Points: %d"%self.monster.GetCurrentMagicPoints(),
                          self.displaySurface,
                          posX, posY,(255,200,32))          
        



    def Display(self, display):
        if (self.displaySurface==None):
            self.GenerateDisplaySurface()

        # Draw Background
        self.Draw()
        display.GetScreen().blit(self.displaySurface,self.position)
        


MonsterWindow = MonsterDisplay()
