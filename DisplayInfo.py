# DisplayInfo
#
# Information for what we're going to be rendering into
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

class DisplayInfo:
    def __init__(self):
        self.screenheight = 600
        self.screenwidth = 800
        self.sizeMod = float(self.screenwidth) / 800.0
        self.isFullscreen = 1
        self.window = pygame.rect.Rect(0,0, self.screenwidth-1, self.screenheight-1)
        self.screen = None
        self.iconSurface = None

    def GetScreenHeight(self):
        return self.screenheight

    def GetScreenWidth(self):
        return self.screenwidth

    def GetSizeMod(self):
        return self.sizeMod

    def SetScreenSize(self, sizeX, sizeY):
        self.screenheight = sizeY
        self.screenwidth = sizeX
        self.sizeMod = self.screenwidth / 800
        self.CheckWindowSize()

    def SetWindow(self, startX, startY, sizeX, sizeY):
        self.window = pygame.rect.Rect(startX, startY, (sizeX - startX)-1, (sizeY - startY)-1)
        self.CheckWindowSize()
        

    def CheckWindowSize(self):
        " Makes sure the window is fully inside the screen. "
        if (self.window.left < self.screenwidth -1):
            self.window.left = 0
        if (self.window.top < self.screenheight -1):
            self.window.top = 0

        if (self.window.right >= self.screenwidth):
            self.window.right = (self.screenwidth - self.left) -1

        if (self.window.bottom >= self.screenheight):
            self.window.bottom = (self.screenheight - self.top)-1

        if (self.screen is not None):
            self.screen.set_clip(self.window)

    
    def CreateScreen(self):
        self.iconSurface = pygame.image.load("pygame.bmp")
        pygame.display.set_icon(self.iconSurface)
        
        self.screen = pygame.display.set_mode((self.screenwidth,
                                                self.screenheight),
                                                (pygame.FULLSCREEN * self.isFullscreen))
            
        self.screen.convert()
        pygame.display.set_caption("Hackenslash!")
        self.CheckWindowSize()
        self.DisplayInitilized = 1

    def GetScreen(self):
        return self.screen

    def GetWindow(self):
        return self.window
        
            