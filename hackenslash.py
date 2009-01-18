####################################################
##
## Hacknslash.py
##
## Main Game Program...
##
####################################################
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


import sys,pygame
pygame.init()
import pygame.time
import DisplayInfo
import Room
import ImageData
import MiniDungeon
import jtext
import Barks
import random
import PlayerData
import Menu
import Monster
import MonsterDisplay
import TextBox
import dice



 


def LoadWallGraphics(graphicsData):
    #graphicsData.LoadTexture("walls","art\\brick32.png")
    graphicsData.LoadTexture("walls","art\\walls.png")
    graphicsData.spriteRects["walls"].append(pygame.rect.Rect(0,0,32,32))
    graphicsData.spriteRects["walls"].append(pygame.rect.Rect(32,0,32,32))
    graphicsData.spriteRects["walls"].append(pygame.rect.Rect(0,32,32,32))
    graphicsData.spriteRects["walls"].append(pygame.rect.Rect(32,32,32,32))
    

def LoadTitleGraphics(graphicsData):
    graphicsData.LoadTexture("hacktitle","art\\hacktitle.png")
 


def LoadItemsGraphics(graphicsData):
    graphicsData.LoadTexture("items1","art\\items1.png")
    for y in range(0,8):
        for x in range(0,8):
            graphicsData.spriteRects["items1"].append(pygame.rect.Rect(x*32,y*32,32,32))    

def LoadFloorGraphics(graphicsData):
    graphicsData.LoadTexture("floors","art\\floors.png")
    for y in range(0,4):
        for x in range(0,4):
            graphicsData.spriteRects["floors"].append(pygame.rect.Rect(x*32,y*32,32,32))    

def LoadMonsterGraphics(graphicsData):
    graphicsData.LoadTexture("monsters1","art\\monsters1.png")
    for y in range(0,4):
        for x in range(0,4):
            graphicsData.spriteRects["monsters1"].append(pygame.rect.Rect(x*32,y*32,32,32))   



def LoadFeaturesGraphics(graphicsData):
    graphicsData.LoadTexture("features","art\\features.png")
    for y in range(0,8):
        for x in range(0,8):
            graphicsData.spriteRects["features"].append(pygame.rect.Rect(x*32,y*32,32,32))


    features1 = pygame.transform.rotate(graphicsData.textures["features"][0],90)
    features2 = pygame.transform.rotate(graphicsData.textures["features"][0],180)
    features3 = pygame.transform.rotate(graphicsData.textures["features"][0],270)

    graphicsData.AssignTexture("features1",features1)
    graphicsData.AssignTexture("features2",features2)
    graphicsData.AssignTexture("features3",features3)

    
    # Now set up the appropriate rects for all 3 rotations
    for origY in range(0,8):
        for origX in range(0,8):
            # 90 degree turn: X0-7 maps to Y7-0, Y0-7 maps to X0-7
            x = origY
            y = 7 - origX
            graphicsData.spriteRects["features1"].append(pygame.rect.Rect(x*32,y*32,32,32))

            # 180 degree turn: X0-7 maps to X7-0, Y0-7 maps to Y0-7
            x = 7 - origX
            y = 7 - origY
            graphicsData.spriteRects["features2"].append(pygame.rect.Rect(x*32,y*32,32,32))
            
            # 270 degree turn: X0-7 maps to Y0-7, Y0-7 maps to X7-0
            x = 7 - origY
            y = origX
            graphicsData.spriteRects["features3"].append(pygame.rect.Rect(x*32,y*32,32,32))


class GameLoop:
    def __init__(self):
        self.DisplayInitialized = 0
        self.exitGame = 0
        self.stage = 0
        self.quitFlag = 0
        self.timePerFrame = 1.0 / 60.0
        self.updatecount = 0
        self.display = DisplayInfo.DisplayInfo()
        self.timer = pygame.time.Clock()
        self.timer.tick(120)
        self.Player = PlayerData.PlayerData()
        self.playerMoveTo = (0,0)
        self.escapeDebounceFlag = 0
        self.SelectedAction = None
        self.ActiveAI = []
        self.TurnType = 0  # 0 = Player turn, 1 = AI turn

        

    def InitDisplay(self):
        self.display.CreateScreen()
        self.DisplayInitilized = 1
        self.TextureManager = ImageData.ImageData()
        LoadTitleGraphics(self.TextureManager)
        LoadWallGraphics(self.TextureManager)
        PlayerData.LoadPlayerGraphics(self.TextureManager)
        LoadFeaturesGraphics(self.TextureManager)
        LoadItemsGraphics(self.TextureManager)
        LoadFloorGraphics(self.TextureManager)
        LoadMonsterGraphics(self.TextureManager)
        self.map = MiniDungeon.CreateDungeon()



    def ResetDungeon(self):
        MiniDungeon.StockDungeon(self.map, self.Player.PC.GetLevel())
        self.Player.map = self.map
        

    def InitPlayer(self):
        self.Player = PlayerData.PlayerData()
        self.SetPlayerScreenPos(self.display.GetScreenWidth()/2, self.display.GetScreenHeight()/2)        
        self.Player.SetInitialGamePosition()
        self.Player.PC.SetMoney(100)
        self.Player.PC.potionCount["Healing"] = 3
        self.Player.PC.potionCount["Essence"] = 3
        


    def HandlePlayerInput(self):
        # Check for player quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quitFlag = 1
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.HandleMouseClick(event)
                if event.type == pygame.MOUSEMOTION:
                    self.HandleMouseMovement(event)
                
        self.keyInfo = pygame.key.get_pressed()

        try:
            if (self.keyInfo[pygame.K_ESCAPE]):
                #self.quitFlag = 1
                if (self.escapeDebounceFlag == 0):
                    if (Menu.MasterMenu.GetMenuCount()>0):
                        Menu.MasterMenu.DropMenu()
                    else:                          
                        if (self.Player.PC.GetCurrentHitPoints()<1):
                            deathComments = ["You are now an ex-adventurer. Deceased. Ceased to Be.",
                                        "Pushing up daisies. Kaput. Finished. There's not much else",
                                        "to do except to quit the game or restart.",
                                        "YOUR FINAL SCORE IS: %d"%(self.Player.PC.GetMoney()+self.Player.PC.GetExperience())
                                        ]                             
                            Menu.CreateMainMenu(self.display, deathComments)
                        else:
                            Menu.CreateMainMenu(self.display)
                        
                    self.escapeDebounceFlag = 1
            else:
                self.escapeDebounceFlag = 0
                
                    
        finally:
            pass


    def HandleMouseMovement(self, event):
        posX = event.dict["pos"][0]
        posY = event.dict["pos"][1]

        # Menus trumps ALL        
        if (Menu.MasterMenu.GetMenuCount()>0):
            Menu.MasterMenu.CheckUserInteraction(0,posX,posY)
            return


       # Next: Check Monsters for MonsterDisplay
        for monster in self.ActiveAI:
            if (monster.isVisible) and (monster.MouseOnMe(self.display,posX,posY)>0):
                MonsterDisplay.MonsterWindow.SetMonster(monster)
                
        # If we don't have a menu up, turn the player to face the arrow.




        if (self.Player.IsSettled()) and (not self.IsDesiredMoveAvailable()):
            relPos = self.GetRelativeMovement(posX,posY)
            self.Player.SetFacingFromMovement(relPos)
        


    def HandleMenuEvent(self,menu,menuSelection):
        if (menuSelection=="CANCEL"):
            Menu.MasterMenu.DropMenu()
            return
            
        if (menu.Title.lower()=="main menu"):
            if (menuSelection.lower()=="exit"):
                self.quitFlag = 1
            return

        if (menu.type=="item"):
            desiredMoveTo = (menu.object.position.X - self.Player.PC.position.X,
                                  menu.object.position.Y - self.Player.PC.position.Y)
            self.SetPlayerAction(1,menu.menuID,menuSelection,desiredMoveTo,menu.object)
            Menu.MasterMenu.DropMenu()
            return

        if (menu.type=="monster"):
            desiredMoveTo= (menu.object.position.X - self.Player.PC.position.X,
                                  menu.object.position.Y - self.Player.PC.position.Y)
            prox = 1
            if (menuSelection=="Negotiate") or (menuSelection=="Cast Spell"):
                prox = 3
            
            if not (menu.menuID==0):
                prox = 3
            self.SetPlayerAction(prox,menu.menuID,menuSelection,desiredMoveTo,menu.object)
            Menu.MasterMenu.DropMenu()
            return            

        if (menu.type=="player"):
            menuID = menu.menuID
            menuObject = menu.object
            Menu.MasterMenu.DropMenu()
            if (menuID==0) and (menuSelection.lower()=="main menu"):
                Menu.CreateMainMenu(self.display)
                return
            self.SetPlayerAction(3,menu.menuID,menuSelection,(0,0),menuObject)
            #menuObject.RespondToMenu(menuID,self.Player,menuSelection)
            return

                        
                

    def HandleMouseClick(self,event):
        # Read location and which buttons are down...
        buttonPressed = event.dict["button"]
        posX = event.dict["pos"][0]
        posY = event.dict["pos"][1]
        
        # First: Check Menus. Menus trump all.
        if (Menu.MasterMenu.GetMenuCount()>0):
            menuResult = Menu.MasterMenu.CheckUserInteraction(buttonPressed,posX,posY)
            if not (menuResult[1] == None):
                self.HandleMenuEvent(menuResult[0],menuResult[1])
            return
                
        # Next: Check Objects
        if (self.CheckClickOnItems(posX,posY)>0):
            return

        # Next: Check Monsters
        for monster in self.ActiveAI:
            if (monster.isVisible) and (monster.MouseOnMe(self.display,posX,posY)>0):
                menu = monster.MakeMenu(0)
                Menu.MasterMenu.AddMenu(menu)
                return
        

        # Next: Check clicking on self
        if self.Player.MouseOnMe(self.display,posX,posY):
            if (self.Player.PC.GetCurrentHitPoints()<1):
                deathComments = ["You are now an ex-adventurer. Deceased. Ceased to Be.",
                            "Pushing up daisies. Kaput. Finished. There's not much else",
                            "to do except to quit the game or restart.",
                            "YOUR FINAL SCORE IS: %d"%(self.Player.PC.GetMoney()+self.Player.PC.GetExperience())
                            ]                   
                Menu.CreateMainMenu(self.display, deathComments)                
            else:            
                menu = self.Player.MakeMenu(0)
                Menu.MasterMenu.AddMenu(menu)
            return
            
            

        # Finally: Check Locations
        pos = self.GetMouseToRoomPosition(posX,posY)
        self.SetPlayerAction(0,0,"move",pos,None)



    def CheckClickOnItems(self,posX, posY):
        blockSize = 32 * self.display.GetSizeMod()
        roomOffset = self.Player.GetRoomOffset(blockSize)
        mX = int ((posX - roomOffset[0]) / blockSize)
        mY = int ((posY - roomOffset[1]) / blockSize)

        room = self.map.FindRoom(self.Player.GetPlayerRoom())
        itemList = room.GetItemsAtLocation(mX,mY)
        if (len(itemList)<1):
            return 0

        # Create a menu
        menu = itemList[0].MakeMenu(self.Player)
        menu.ResizeForBestFit()
        menu.SetPosition((mX + 1)*blockSize + roomOffset[0]+4, (mY -1)*blockSize + roomOffset[1])     

        
        Menu.MasterMenu.AddMenu(menu)
        return 1
            
        
        
    def SetPlayerScreenPos(self, posX, posY):
        self.Player.SetScreenPosition(posX, posY)
   
            
    def GetRelativeMovement(self, posX, posY):
        offX = posX - self.Player.screenPosX
        offY = posY - self.Player.screenPosY
        blockSize = 32 * self.display.GetSizeMod()

        if (abs(offX)<blockSize * 0.5):
            offX = 0
        if (abs(offY)<blockSize * 0.5):
            offY = 0

        # Are we clicking on ourselves?
        if (offX == 0) and (offY == 0):
            return (0,0)
        
        # Check for pure horizontal movement
        if (abs(offX) > 2*abs(offY)):
            if (offX < 0):
                return (-1,0)
            elif (offX > 0):
                return (1,0)
            else:
                return (0,0)
        # Check for pure vertical
        elif (abs(offY) > 2*abs(offX)):
            if (offY < 0):
                return (0, -1)
            elif (offY > 0):
                return (0, 1)
            else:
                return (0,0)

        # Must be diagonal
        if (offY > 0):
            offY = 1
        elif (offY < 0):
            offY = -1

        if (offX > 0):
            offX = 1
        elif (offX < 0):
            offX = -1

        return (offX, offY)
        

    def GetMouseToRoomPosition(self,posX,posY):
        blockSize = 32 * self.display.GetSizeMod()
        roomOffset = self.Player.GetRoomOffset(blockSize)
        mX = (posX - roomOffset[0])
        mY = (posY - roomOffset[1])

        if (mX<0):
            mX -= blockSize
        if (mY<0):
            mY -= blockSize

        mX = int(mX / blockSize)
        mY = int(mY / blockSize)
        
        desiredMoveTo = (mX - self.Player.PC.position.X, mY - self.Player.PC.position.Y)
        return desiredMoveTo
        
        
        

    def SetPlayerAction(self,moveRequirement,menuID,actionString,actionLocation,actionObject):
        # MoveRequirement: 0: Move ONLY (actionLocation is direct location), 1=Move Proximate, 2=Move On Top Of
        self.SelectedAction = [moveRequirement,menuID,actionString,actionLocation,actionObject]





    def IsDesiredMoveAvailable(self):
        # Calculate whether or not we have a move planned
        if (self.SelectedAction == None):
            return 0
        return 1


    def GetMoveToAction(self):
        "Finds out if the player still needs to move to perform an action, and tells him which square to move to next"
        if (self.SelectedAction == None):
            return (0,0)
        offset = self.SelectedAction[3]
        proximity = self.SelectedAction[0]
        if (proximity==1) and (abs(offset[0])<2) and (abs(offset[1])<2):
             return (0,0)
        if (proximity == 3):
            return (0,0)
        moveX = 0
        moveY = 0
        if (offset[0]<0):
            moveX = -1
        elif (offset[0]>0):
            moveX = 1
        if (offset[1]<0):
            moveY = -1
        elif (offset[1]>0):
            moveY = 1

        self.SelectedAction[3] = (offset[0]-moveX,offset[1]-moveY)
        return (moveX,moveY)
   

    def UpdatePlayerMove(self):
        if not self.Player.IsSettled():
            return 0
        
        if not (self.IsDesiredMoveAvailable()):
                return 0
        movement = self.GetMoveToAction()
        if (movement[0]==0) and (movement[1]==0):
            return self.ExecutePlayerAction()


        #self.desiredMoveTo = (self.desiredMoveTo[0] - posX, self.desiredMoveTo[1] - posY)
        self.playerMoveTo = movement
        return self.IncrementTurn()


    def ExecutePlayerAction(self):
        "If we're close enough, execute the actual."
        bRun = 0
        if (self.SelectedAction[0]>0): # Only if we had more to do than move
            bRun = self.SelectedAction[4].RespondToMenu(self.SelectedAction[1],
                                             self.Player,
                                             self.SelectedAction[2]
                                             )
                  
        # Better get rid of that selected action!       
        self.SelectedAction = None
        return bRun
        
        

    def IncrementTurn(self):
        bPlayerMove = 0
        iPlayerRoom = self.Player.GetPlayerRoom()
        moveX,moveY = self.playerMoveTo

        if (not (moveX == 0)) or (not(moveY ==0)):
            endX = self.Player.PC.position.X + moveX
            endY = self.Player.PC.position.Y + moveY

            room = self.map.FindRoom(self.Player.GetPlayerRoom())
            allowed,portal = room.AllowedMove((self.Player.PC.position.X,self.Player.PC.position.Y),
                                              (endX,endY),1, self.ActiveAI)
            if (allowed):
                self.Player.StartMove(moveX,moveY)
                return 1
            else:
                # Cancel previous move
                self.SelectedAction = None
                return 0
        return 0

            
    

    def UpdatePlayerNonTurnBased(self, timeDelta):
        "Perform per-frame housekeeping on Player"
        if (not self.Player.IsSettled()):            
            self.Player.ContinueMovement(timeDelta*4,self.map)
        if (self.Player.TookItem):
            self.Player.TookItem = 0
            # Warn all monsters in the room that the player stole something
            for x in self.ActiveAI:
                if x.position.roomID == self.Player.PC.position.roomID:
                    hidden = dice.StandardRoll(self.Player.PC.GetStealSkill()+self.Player.GetBonusForAction("thievery"),
                                               x.GetPerception()+x.GetBonusForAction("search"))
                    if not hidden:
                        TextBox.MainText.AddText("%s sees player steal something!"%x.name)
                        x.attitude = -1
                    else:
                        TextBox.MainText.AddText("%s doesn't notice your actions."%x.name)
        
                    
        
    
    def UpdatePlayerTurnBased(self):
        "Execute a player move."
        if self.Player.IsDead():
            return
        self.TurnType = self.UpdatePlayerMove()
        #self.TurnType = 1
        if (self.TurnType):
            self.Player.PC.UpdateTurn()

    def UpdateMonstersNonTurnBased(self, timeDelta):
        "Perform per-frame housekeeping on Monsters"
        deletionList = []
        for monster in self.ActiveAI:
            if MonsterDisplay.MonsterWindow.monster == monster:
                if not (monster.position.roomID == self.Player.PC.position.roomID):
                    MonsterDisplay.MonsterWindow.ClearMonster()
            if (monster.GetCurrentHitPoints()<1):
                deletionList.append(monster)
                self.HandleDeadMonster(monster)
                if (MonsterDisplay.MonsterWindow.monster == monster):
                    MonsterDisplay.MonsterWindow.ClearMonster()

        for x in deletionList:
            self.ActiveAI.remove(x)
            

    def UpdateMonstersTurnBased(self):
        "Execute the monster's move."
        deactivatedMonsters = []
        for monster in self.ActiveAI:
            if (monster.GetCurrentHitPoints()>0):
                monster.AIRunAI(self.map,self.Player)
                monster.UpdateTurn()
                if (monster.inactive):
                    room = self.map.FindRoom(monster.position.roomID)
                    if not (room==None):
                        room.monsters.append(monster)
                        deactivatedMonsters.append(monster)
                    else:
                        print "Can't find room %d to deactivate monster"%monster.position.roomID
        for monster in deactivatedMonsters:
            self.ActiveAI.remove(monster)
                    
        
        self.TurnType = 0
    



    def UpdateWorld(self):
        timeDelta = self.timer.tick(60)*0.001
        self.updatecount +=1
        
        self.UpdateBarks(timeDelta)
        self.UpdatePlayerNonTurnBased(timeDelta)
        self.UpdateMonstersNonTurnBased(timeDelta)
        if (self.TurnType==0):
            self.UpdatePlayerTurnBased()
        elif (self.TurnType==1):
            self.UpdateMonstersTurnBased()
        # Activate monsters in room
        room = self.map.FindRoom(self.Player.PC.position.roomID)
        if (len(room.monsters)>0):
            self.ActiveAI += room.monsters
            room.monsters = []

        if (self.Player.RestFlag):
            self.ResetDungeon()
            self.Player.RestFlag = 0
            self.ActiveAI = []
            
        

    def DrawWorld(self):
        if (self.display.GetScreen() is not None):
            self.display.GetScreen().fill((0,0,0))

            # Only display rooms in a 600 x 600 window
            fullWindow = self.display.GetWindow()
            roomWindow = self.display.SetWindow(0,0,600*self.display.GetSizeMod(),600*self.display.GetSizeMod())
            curRoom = self.Player.GetPlayerRoom()
            roomOffset = self.Player.GetRoomOffset(32 * self.display.GetSizeMod())                       
            roomOffsetDict = self.map.FindRoom(curRoom).DisplayCentral(roomOffset[0],roomOffset[1],self.display,self.TextureManager)

            for monster in self.ActiveAI:
                if (roomOffsetDict.has_key(monster.GetRoom())):
                    off = roomOffsetDict[monster.GetRoom()]
                    monster.GenerateScreenPosition(self.display,off[0],off[1])
                    monster.isVisible = 1
                    monster.Display(self.display,self.TextureManager)
                else:
                    monster.isVisible = 0
                    
            Barks.DisplayBarks(self.display.GetScreen())                
            
        
            # Now re-open the window to display everything
            self.display.SetWindow(0,0,self.display.GetScreenWidth(), self.display.GetScreenHeight())
            self.Player.Display(self.display,self.TextureManager)
            jtext.PrintTextAt("Room #%d: %s"%(curRoom,self.map.FindRoom(curRoom).name),self.display.GetScreen(),10,10,(255,255,255,255))
            #jtext.PrintTextAt("Hit Points: 20",self.display.GetScreen(),
            #                  384 - 32, 284 - 32, (255,255,255,255))
            # Display the title
            self.display.GetScreen().blit(self.TextureManager.textures["hacktitle"][0],
                                          (599,200))
            MonsterDisplay.MonsterWindow.Display(self.display)
            TextBox.MainText.Display(self.display.GetScreen())
            

            Menu.MasterMenu.Display(self.display)
            
            
                                              

    def FlipScreenBuffer(self):
        pygame.display.flip()



    def UpdateBarks(self, timeDelta):
##        try:
##            self.barkTime -= timeDelta
##        except:
##            self.barkTime = -1.0
##
##        # Add potential New Barks....            
##        if (self.barkTime < 0):
##            self.barkTime = random.randint(1,8) * 0.125
##            nextBark = random.randint(0,4)
##
##            # Create a new bark
##            myBark = Barks.Bark()
##            if (random.randint(1,2)==1):
##                myBark.Spin(random.randint(90,720), 720)
##            if (random.randint(0,2)>0):
##                myBark.movement = [0,-random.randint(20,40)]
##            if (random.randint(0,5)==1):
##                myBark.SetScaleFactor(0.5,2.0,1.0)
##                myBark.SetCentered(1,myBark.centered[1])
##                
##            myBark.duration = 2.0
##
##            if (nextBark==0):
##                myBark.Create("WOW!",random.randint(20,720),
##                              random.randint(30,500))
##            elif (nextBark==1):
##                myBark.Create("Cool.",random.randint(20,720),random.randint(30,500))
##            elif (nextBark==2):
##                myBark.Create("Critical Hit",random.randint(20,720),random.randint(30,500))
##            elif (nextBark==3):
##               myBark.Create("%d Gold"%(random.randint(1,120)),random.randint(20,720),random.randint(30,500))
##            else:
##                myBark.Create("%d damage"%(random.randint(1,200)),random.randint(20,720),random.randint(30,500))            
##                              
##            Barks.AddBark(myBark)
            
        # Update existing barks
        Barks.UpdateBarks(timeDelta)
        
                
    def HandleDeadMonster(self,monster):
        # Award XP to player.
        self.Player.GiveXP(20)
        TextBox.MainText.AddText("%s is toast."%(monster.name))

        # Drop Items
        room = self.map.FindRoom(monster.GetRoom())
        monster.DropItems(room)

        # Print congrats message        
        if (monster.isVisible) and (not self.Player.PC.LevelupFlag):
            myBark = Barks.Bark()
            myBark.Spin(720,720)
            myBark.SetScaleFactor(1.0,2.0,1.0)
            myBark.SetCentered(1,1)
            myBark.duration = 2.5
            myBark.Create("%s Killed!"%monster.name,monster.screenPosX, monster.screenPosY,(255,0,0))
            Barks.AddBark(myBark)

        if (self.Player.PC.LevelupFlag):
            myBark = Barks.Bark()
            myBark.Spin(720,720)
            myBark.SetScaleFactor(1.0,2.0,1.0)
            myBark.SetCentered(1,1)
            myBark.duration = 3
            myBark.Create("DING! You have gained a level!",self.Player.screenPosX, self.Player.screenPosY, (255,220,0))
            myBark.movement = [0,-20]
            Barks.AddBark(myBark)            
            
            
            

            

    def Mainloop(self):
        if (self.DisplayInitialized==0):
            self.InitDisplay()
        self.InitPlayer()
        self.ResetDungeon()
        timer = pygame.time.get_ticks()
        timer2 = timer
        timeOffset = 0.00        

        while not self.quitFlag:
            self.HandlePlayerInput()
            self.UpdateWorld()
            self.DrawWorld()
            self.FlipScreenBuffer()
            
            
            
        


if __name__=="__main__":

    game = GameLoop()
    print "Default Font: %s"%(pygame.font.get_default_font())
    print "All fonts:\n-------------"
    print pygame.font.get_fonts()
    game.Mainloop()

    