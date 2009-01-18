# MENU.PY
# For interactive menus in PyGame
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
import jtext

class Menu:
    def __init__(self):
        self.position = (0,0)
        self.size = (128,128)
        self.color = (16,16,48)
        self.TitleBackgroundColor = (48,48,96)
        self.OutOfFocusBorderColor = (128,128,196)
        self.InFocusBorderColor = (255,255,128)
        self.MenuOptions = []
        self.TopMenuOption = []
        self.highlightedOption = -1
        self.InFocus = 1
        self.ChosenOption = None
        self.Title = "New menu"
        self.TextHighlightColor = (255,255,255)
        self.TextNormalColor = (200,240,240)
        self.centeredText = 1
        self.type = "general"
        self.object = None
        self.msgText = []
        self.msgSize = 0
        self.menuID = 0
        
        

    def CheckUserInteraction(self, mouseButtonClick, mousePosX, mousePosY):
        # Step 1: Make sure cursor is within the menu boundaries
        if (mousePosX<self.position[0]) or (mousePosX>=self.position[0] + self.size[0]):
            self.ChosenOption = None
            return None
        if (mousePosY<self.position[1]) or (mousePosY >= self.position[1] + self.size[1]):
            self.ChosenOption = None
            return None

        # Find out who is selected...
        if (mousePosY >= self.position[1] + self.size[1] - 16):
            self.ChosenOption = "CANCEL"
            if (mouseButtonClick>0):
                return "CANCEL"
            return None

        # Title Bar and message area never do anything
        if (mousePosY < self.position[1]+16+self.msgSize):
            self.ChosenOption = None
            return None

        

        menuItem = (mousePosY - (self.position[1]+16+self.msgSize))/16
        if (menuItem >= len(self.MenuOptions)):
            self.ChosenOption = None
            return None


        menuItem = int(menuItem)
        self.ChosenOption = self.MenuOptions[menuItem]

            
        if (mouseButtonClick>0):
            return self.ChosenOption
        

                    

    def AddMessage(self, strMessage):
        self.msgText.append(strMessage)
        self.msgSize = 16 * len(self.msgText)


    def SetMessages(self,strMessageList):
        self.msgText = strMessageList
        self.msgSize = 16 * len(self.msgText)
            
    def SetFocus(self, bInFocus):
        "Sets whether or not this menu is the one currently in focus"
        self.InFocus = bInFocus

    def SetSize(self, iSizeX, iSizeY):
        if (iSizeX < 80):
            iSizeX = 80
        if (iSizeY < 64):
            iSizeY = 64
        self.size = (iSizeX, iSizeY)

    def SetPosition(self, posX, posY):
        if (posX < 0):
            posX = 0
        if (posY < 0):
            posY = 0
        self.position = (posX, posY)

    def SetTitle(self, titleString):
        self.Title = titleString

    def SetMenuOptions(self, optionList):
        self.MenuOptions = optionList        


    def Locate(self, posX, posY, sizeX, sizeY):
        self.SetPosition(posX, posY)
        self.SetSize(sizeX, sizeY)

    def GetSelected(self):
        return self.ChosenOption

    def ResizeForBestFit(self):
        longestString = jtext.GetTextSize("CANCEL")[0]
        titleLength = jtext.GetTextSize(self.Title)[0]
        if (titleLength>longestString):
            longestString = titleLength
        for x in self.MenuOptions:
            tempLen = jtext.GetTextSize(x)[0]
            if (tempLen>longestString):
                longestString = tempLen

        for x in self.msgText:
            tempLen = jtext.GetTextSize(x)[0]
            if (tempLen>longestString):
                longestString = tempLen                

        height = len(self.MenuOptions) * 16 + self.msgSize + 32
        self.SetSize(longestString + 6, height)

    def RepositionAtScreenCenter(self,display):
        centerX = (display.GetScreenWidth() - self.size[0])/2
        centerY = (display.GetScreenHeight() - self.size[1])/2
        self.SetPosition(centerX, centerY)                     



    def Display(self,display):
        screen = display.GetScreen()
        if (self.InFocus):
            borderColor = self.InFocusBorderColor
        else:
            borderColor = self.OutOfFocusBorderColor
            
        # Draw Title background
        pygame.draw.polygon(screen,self.TitleBackgroundColor,
                            [(self.position[0],self.position[1]),
                             (self.position[0]+self.size[0],self.position[1]),
                             (self.position[0]+self.size[0],self.position[1]+16),
                             (self.position[0],self.position[1]+16)],
                            0)
        pygame.draw.polygon(screen,borderColor,
                            [(self.position[0]+1,self.position[1]+1),
                             (self.position[0]+self.size[0]-2,self.position[1]+1),
                             (self.position[0]+self.size[0]-2,self.position[1]+16),
                             (self.position[0]+1,self.position[1]+16)],
                            1)

        jtext.PrintTextCentered(self.Title,screen,self.position[0]+1,self.position[1]+2,
                                self.position[0]+self.size[0]-1, self.position[1]+16,
                                (255,255,255))
        
      

        # Draw Cancel Background
        if (self.ChosenOption=="CANCEL"):
            cancelColor = (255,255,128)
            cancelBGColor = self.TitleBackgroundColor
        else:
            #print "Chosen Option = "+str(self.ChosenOption)
            cancelColor = (255,255,64)
            cancelBGColor = self.color
            
        pygame.draw.polygon(screen,cancelBGColor,
                            [(self.position[0],self.position[1]+self.size[1]-15),
                             (self.position[0]+self.size[0],self.position[1]+self.size[1]-15),
                             (self.position[0]+self.size[0],self.position[1]+self.size[1]),
                             (self.position[0],self.position[1]+self.size[1])],
                            0)
        pygame.draw.polygon(screen,borderColor,
                            [(self.position[0]+1,self.position[1]+self.size[1]-16),
                             (self.position[0]+self.size[0]-2,self.position[1]+self.size[1]-16),
                             (self.position[0]+self.size[0]-2,self.position[1]+self.size[1]-1),
                             (self.position[0]+1,self.position[1]+self.size[1]-1)],
                            1)

            
        jtext.PrintTextCentered("CANCEL",screen,self.position[0]+1,self.position[1]+self.size[1]-15,
                                self.position[0]+self.size[0]-1, self.position[1]+self.size[1],
                                cancelColor)
        

        # Draw Main Menu Area
        pygame.draw.polygon(screen,self.color,
                            [(self.position[0],self.position[1]+17),
                             (self.position[0]+self.size[0],self.position[1]+17),
                             (self.position[0]+self.size[0],self.position[1]+self.size[1]-17),
                             (self.position[0],self.position[1]+self.size[1]-17)],
                            0)        
        pygame.draw.line(screen,borderColor,(self.position[0]+1,self.position[1]+16),
                         (self.position[0]+1,self.position[1]+self.size[1]-16),1)
        pygame.draw.line(screen,borderColor,(self.position[0]+self.size[0]-2,self.position[1]+16),
                         (self.position[0]+self.size[0]-2,self.position[1]+self.size[1]-16),1)

        # If there are messages, draw them.
        drawLoc = self.position[1] + 16
        if (self.msgSize>0):
            for message in self.msgText:
                jtext.PrintTextAt(message,screen, self.position[0]+3, drawLoc,(255,255,255))
                drawLoc += 16
                
        pygame.draw.line(screen,borderColor,(self.position[0]+1,self.position[1]+self.msgSize+16),
                         (self.position[0]+self.size[0]-2,self.position[1]+self.msgSize+16),1)



        # Now draw the selection text...
        drawLoc = self.position[1] + 18 + self.msgSize
        for x in self.MenuOptions:
            if (self.InFocus) and (x == self.ChosenOption) :
                curColor = self.TextHighlightColor
            else:
                curColor = self.TextNormalColor
            
            if self.centeredText:
                jtext.PrintTextCentered(x,screen, self.position[0]+3, drawLoc,
                                        self.position[0]+self.size[0]-3,drawLoc + 16,
                                        curColor)
            else:
                jtext.PrintTextAt(x,screen, self.position[0]+3, drawLoc,curColor)
  
            drawLoc += 16                
                
                


class MenuMaster:
    def __init__(self):
        self.MenuList = []

    def AddMenu(self, menuItem):
        for x in self.MenuList:
            x.SetFocus(0)
        menuItem.SetFocus(1)
        self.MenuList.append(menuItem)

    def DropMenu(self):
        try:
            self.MenuList.pop()
            menuCount = len(self.MenuList)            
            if (menuCount>0):
                for x in self.MenuList[0:menuCount-1]:
                    x.SetFocus(0)
                self.MenuList[menuCount-1].SetFocus(1)                                       
        except:
            return 0
            

    def Display(self,display):
        # This order makes sure they are properly overlapped.
        for x in self.MenuList:
            x.Display(display)

    def GetMenuCount(self):
        return len(self.MenuList)

    def CheckUserInteraction(self, mouseButtonClick, mousePosX, mousePosY):
        menuCount = len(self.MenuList)
        if (menuCount > 0):
            return (self.MenuList[menuCount-1],self.MenuList[menuCount-1].CheckUserInteraction(mouseButtonClick, mousePosX, mousePosY))


def CreateMainMenu(display, comments = []):
    mainMenu = Menu()
    mainMenu.msgText = comments
    mainMenu.msgSize = 16 * len(mainMenu.msgText)    
    mainMenu.SetTitle("Main Menu")
    mainMenu.SetMenuOptions(["New game","Exit"])
    mainMenu.Locate(300,300,256,256)
    mainMenu.ResizeForBestFit()
    mainMenu.RepositionAtScreenCenter(display)
    MasterMenu.AddMenu(mainMenu)    
    
    


# Global handler            

MasterMenu = MenuMaster()



        
        
        