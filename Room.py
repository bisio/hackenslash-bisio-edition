# ROOM
# Handles - rooms
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

from gameobject import GameObject
import pygame

baseWallSize = 32


class Portal(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        # Start Position is the top or left of the portal
        self.startPosition = 0
        self.size = 0
        # Destination is where the player goes if he goes PAST this portal.
        # destination: Container ID, Room ID, X offset, Y Offset
        # Destination is the offset from the portal's position in the first room to the portal's
        # equivalent position on the other side.
        self.destination = (0,0,0,0)
        self.doorID = -1 # No door = -1
        self.secret = 0  # 1= secret, 2 = illusionary
        self.stateData = []  # For saved-game info

    def Save(self, filePtr):
        if (len(self.stateData)>0):
            filePtr.write(str(self.stateData))
            
    def Load(self,filePtr):
        strStateData = filePtr.read(1024)
        # Do something with it.

    def IsVisible(self):
        if self.secret:
            if self.stateData.Count < 1:
                return 0
            if (self.stateData[0] == 0):
                return 0
            return 1
        return 1
    
        
###########################################################################
##
## Wall Stuff
##
###########################################################################
    

class Wall(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.orientation = -1   # 0 = horizontal, 1=vertical
        self.graphic = 0
        self.startPosition = [0,0]
        self.length = 0
        self.portalList = []
        self.wallExists = []
        self.exteriorWallID = -1
        

    def Generate (self,graphic, orientation, startX, startY, len, exteriorWallID = -1):
        self.orientation = orientation
        self.graphic = graphic
        self.startPosition = (startX,startY)
        self.length = len
        self.exteriorWallID = exteriorWallID

    def UpdatePortalRange(self):
        self.wallExists = []
        for x in range(self.length):
            self.wallExists.append(1)            
        for x in self.portalList:
            if x.IsVisible():
                for i in range(x.startPosition,x.startPosition + x.size):
                    self.wallExists[i] = 0            



    def WallCollision(self, posX, posY):
        "Returns 1 if there's a wall on this square, 0 if not"
        # If the portal range has never been updated for this wall, do it now.        
        if (len(self.wallExists) < self.length-1):
            self.UpdatePortalRange()
        if (self.orientation == 0):
            # Check for collision against a horizontal wall
            if not (posY == self.startPosition[1]):
                return 0
            # If we're to the left or right of the wall, return false
            if (posX < self.startPosition[0]) or (posX >= self.startPosition[0]+self.length):
                return 0
            # Are we on a portal?
            try:
                if (self.wallExists[posX - self.startPosition[0]]):
                    return 1
            except:
                # In case something bad happens.
                return 0
            return 0
            
            
        else:
            # Check for collision against a vertical wall
            if not (posX == self.startPosition[0]):
                return 0
            # If we're above or below the wall, return false
            if (posY < self.startPosition[1]) or (posY >= self.startPosition[1]+self.length):
                return 0
            # Are we on a portal?
            try:
                if (self.wallExists[posY - self.startPosition[1]]):
                    return 1
            except:
                # In case something bad happens
                return 0
            return 0
        return 0            
            


    def PortalAt(self, posX, posY):
        # If the portal range has never been updated for this wall, do it now.        
        if (len(self.wallExists) < self.length-1):
            self.UpdatePortalRange()
        if (self.orientation == 0):
            # Check for portal on a horizontal wall
            if not (posY == self.startPosition[1]):
                return None
            # If we're to the left or right of the wall, return false
            if (posX < self.startPosition[0]) or (posX >= self.startPosition[0]+self.length):
                return None
            # Are we on a portal?
            squarePos = posX - self.startPosition[0]
            for portal in self.portalList:
                if not (portal.secret == 1):   # Ignore secret, undiscovered portals
                    if (squarePos>=portal.startPosition) and (squarePos < portal.startPosition + portal.size):
                            return portal              

        else:
            # Check for portal on a vertical wall
            if not (posX == self.startPosition[0]):
                return None
            # If we're above or below the wall, return false
            if (posY < self.startPosition[1]) or (posY >= self.startPosition[1]+self.length):
                return None
            # Are we on a portal?
            squarePos = posY - self.startPosition[1]
            for portal in self.portalList:
                if not (portal.secret == 1):   # Ignore secret, undiscovered portals
                    if (squarePos>=portal.startPosition) and (squarePos < portal.startPosition + portal.size):
                            return portal              

        return None                    
        
        
        

    def Display(self, offsetX, offsetY, displayInfo, graphicsData):

        # If the portal range has never been updated for this wall, do it now.        
        if (len(self.wallExists) < self.length-1):
            self.UpdatePortalRange()

        # Early opt-out        
        wallSize = baseWallSize * displayInfo.GetSizeMod()
        halfWallSize = wallSize * 0.5
        if (offsetX + self.startPosition[0] * wallSize > displayInfo.GetWindow().right):
            return
        if (offsetY + self.startPosition[1] * wallSize > displayInfo.GetWindow().bottom):
            return

        if (self.orientation == 0):
            rightExtent = offsetX + (self.startPosition[0] + self.length ) * wallSize 
            bottomExtent = offsetY + (self.startPosition[1]+ 1) * wallSize
        else:
            rightExtent = offsetX + (self.startPosition[0]+1) * wallSize
            bottomExtent = offsetY + (self.startPosition[1]+ self.length ) * wallSize 
      
        if (rightExtent < displayInfo.GetWindow().left):
            return
        if (bottomExtent < displayInfo.GetWindow().top):
            return

        # Prepare for drawing
        drawX = offsetX + (self.startPosition[0]) * wallSize
        drawY = offsetY + (self.startPosition[1]) * wallSize  
        spritePage = graphicsData.textures["walls"][0]
        spriteRect = graphicsData.spriteRects["walls"][self.graphic]

    
    
        
        # Draw only a half-wall if we're drawing an exterior wall
        if (self.exteriorWallID==-1):
            firstRect= spriteRect
            lastRect = spriteRect         
        elif (self.exteriorWallID==0): # North wall
            drawY += halfWallSize
            firstRect= pygame.rect.Rect(spriteRect.left + spriteRect.width/2,spriteRect.top + spriteRect.height/2,
                                          spriteRect.width/2,spriteRect.height/2)
            lastRect= pygame.rect.Rect(spriteRect.left,spriteRect.top + spriteRect.height/2,
                                          spriteRect.width/2,spriteRect.height/2)            
            spriteRect = pygame.rect.Rect(spriteRect.left,spriteRect.top + spriteRect.height/2,
                                          spriteRect.width,spriteRect.height/2)
        elif (self.exteriorWallID==1): # East wall
            firstRect= pygame.rect.Rect(spriteRect.left,spriteRect.top + spriteRect.height/2,
                                          spriteRect.width/2,spriteRect.height/2)
            lastRect= pygame.rect.Rect(spriteRect.left,spriteRect.top,
                                          spriteRect.width/2,spriteRect.height/2)             
            spriteRect = pygame.rect.Rect(spriteRect.left,spriteRect.top,
                                          spriteRect.width/2,spriteRect.height)
        elif (self.exteriorWallID==2): # South wall
            firstRect= pygame.rect.Rect(spriteRect.left + spriteRect.width/2,spriteRect.top,
                                          spriteRect.width/2,spriteRect.height/2)
            lastRect= pygame.rect.Rect(spriteRect.left,spriteRect.top,
                                          spriteRect.width/2,spriteRect.height/2)             
            spriteRect = pygame.rect.Rect(spriteRect.left,spriteRect.top,
                                          spriteRect.width,spriteRect.height/2)
        elif (self.exteriorWallID==3): # West wall
            drawX += halfWallSize
            firstRect= pygame.rect.Rect(spriteRect.left + spriteRect.width/2,spriteRect.top + spriteRect.height/2,
                                          spriteRect.width/2,spriteRect.height/2)
            lastRect= pygame.rect.Rect(spriteRect.left+ spriteRect.width/2,spriteRect.top,
                                          spriteRect.width/2,spriteRect.height/2)             
            spriteRect = pygame.rect.Rect((spriteRect.left+spriteRect.width/2),spriteRect.top,
                                          spriteRect.width/2,spriteRect.height)

        # Now draw this sucker...
        screen = displayInfo.GetScreen()
        # Draw edges
        tempDrawX = drawX
        tempDrawY = drawY
        if (self.orientation==0):
            tempDrawX += halfWallSize
        else:
            tempDrawY += halfWallSize        
        screen.blit(spritePage,(tempDrawX,tempDrawY),firstRect)
        if (self.orientation==0):
            tempDrawX += wallSize * (self.length-1) - halfWallSize
        else:
            tempDrawY += wallSize* (self.length-1) - halfWallSize

        screen.blit(spritePage,(tempDrawX,tempDrawY),lastRect)
            
        

        if (self.orientation==0):
            drawX += wallSize
        else:
            drawY += wallSize
        for x in range(1,self.length-1):
            # Only draw it if there's not non-hidden portal there
            if (self.wallExists[x]):
                screen.blit(spritePage,(drawX,drawY),spriteRect)
            if (self.orientation == 0):
                drawX += wallSize
            else:
                drawY += wallSize

    def Save(self, filePtr):
        # Save all states of portals
        pass

    def Load(self, filePtr):
        pass

      
            
            
            
        
##########################################################################
##
## ROOM STUFF
##
##########################################################################
        
        

class Room(GameObject):
    def __init__(self):
        self.height = 0
        self.width = 0
        self.floorGraphic = 0
        self.wall = []
        self.roomID = 0
        self.features = []
        self.monsters = []
        GameObject.__init__(self)
        self.map = None
        self.safeRoom = 0
        self.name = "Dungeon Room"


    def GetRoomID(self):
        return self.roomID


    def GetItemsAtLocation(self, posX, posY):
        itemList = []
        for item in self.contents:
            if (item.position.X == posX) and (item.position.Y == posY):
                itemList.append(item)

        return itemList                
        

    def AllowedMove(self,startPos, endPos, isPlayer, monsterList = []):
        #"Returns 1 or a negative if the entity is allowed to move from startPos to endPos, otherwise 0. StartPos and endPos should be an x,y tuple. The second value is the portal you are exiting (if from the right direction)"
        # If it's more than 1 square away, return a zero... it's too big of a hop.
        if abs(startPos[0] - endPos[0])>1:
            return (0, None)
        if abs(startPos[1] - endPos[1])>1:
            return(0,None)
            
        #if (endPos[0]<0) or (endPos[0]>=self.width) or (endPos[1]<0) or (endPos[1]>=self.height):
            # Check for portal
            # else
            #return (0, None)
        
        for wall in self.wall:
            if wall.WallCollision(endPos[0],endPos[1])>0:
                return (0,None)

        # Check for features not allowing travel in this direction...
        for feature in self.features:
            eData = feature.EntryAllowed(startPos,endPos)
            if (eData[0]==0):
                return (0,None)


        # Check for items / monsters blocking traffic...        
        for item in self.contents:
            try:
                if (item.position.X == endPos[0]) and (item.position.Y == endPos[1]):
                    if (item.itemType.size>2):
                        return (0,item)
            except:
            #    print e
                pass

        for monster in monsterList:
            if monster.GetRoom()==self.roomID:
                if (monster.position.X == endPos[0]) and (monster.position.Y == endPos[1]):
                    return (0,monster)


        # Guess we're clear...
        return (1,None)
        


    def GetFeatureBlockAtPosition(self, posX, posY):
        eData = []
        for feature in self.features:
            eData = feature.GetAllFeatures(posX, posY)
        return eData

    def GetPortal(self, posX, posY):
        "returns the portal covering position posX, posY"
        for x in self.wall:
            portal = x.PortalAt(posX,posY)
            if not (portal == None):
                return portal
        return None


    def FindPortalToRoom(self, roomID):
        "Returns a portal (if any) from this room to room roomID"
        for y in self.wall:
            for x in y.portalList:
                if x.destination[1] == roomID:
                    return (y,x)
        return None
    

    

    def BuildRoom(self,sizeX,sizeY,wallType,floorType):
        self.height = sizeY
        self.width = sizeX
        self.floorGraphic = floorType

        # Do N,E,S,W Walls
        self.wall = [Wall(),Wall(),Wall(),Wall()]
        self.wall[0].Generate(wallType,0,0,0,sizeX, 0)
        self.wall[1].Generate(wallType,1,sizeX-1,0,sizeY, 1)
        self.wall[2].Generate(wallType,0,0,sizeY-1,sizeX, 2)
        self.wall[3].Generate(wallType,1,0,0,sizeY, 3)      



    def Display(self, offsetX, offsetY, displayInfo, graphicsData):
        # First - draw floor and major features
        wallSize = baseWallSize * displayInfo.GetSizeMod()
        halfWallSize = wallSize * 0.5
        
        spritePage = graphicsData.textures["floors"][0]
        screen = displayInfo.GetScreen()
        if (self.floorGraphic>0):
            drawY = offsetY+wallSize
            spriteRect = graphicsData.spriteRects["floors"][self.floorGraphic]
            # Draw corners
##            # Topleft
##            tempRect = pygame.rect.Rect(spriteRect.left+spriteRect.width/2, spriteRect.top + spriteRect.height/2,
##                                        spriteRect.width/2,spriteRect.height/2)
##            screen.blit(spritePage,(offsetX+halfWallSize,offsetY+halfWallSize),tempRect)
##            # TopRight
##            tempRect = pygame.rect.Rect(spriteRect.left, spriteRect.top + spriteRect.height/2, 
##                                        spriteRect.width/2,spriteRect.height/2)
##            screen.blit(spritePage,(offsetX+halfWallSize+(self.width-2)*wallSize,offsetY+halfWallSize),tempRect)
##            # BottomLeft
##            tempRect = pygame.rect.Rect( spriteRect.left+spriteRect.width/2,spriteRect.top,
##                                        spriteRect.width/2,spriteRect.height/2)
##            screen.blit(spritePage,(offsetX+halfWallSize,offsetY+halfWallSize+(self.height-2)*wallSize),tempRect)
##            # BottomRight
##            tempRect = pygame.rect.Rect(spriteRect.left,spriteRect.top, 
##                                        spriteRect.width/2,spriteRect.height/2)
##            screen.blit(spritePage,(offsetX+halfWallSize+(self.width-2)*wallSize,offsetY+halfWallSize+(self.height-2)*wallSize),tempRect)
            

            # Draw edges
            # Top & bottom
            drawX = offsetX+wallSize
            drawY = offsetY+halfWallSize
            drawY2 = offsetY + (self.height-1)*wallSize
            tempRectTop = pygame.rect.Rect(spriteRect.left,spriteRect.top + spriteRect.height/2, 
                                        spriteRect.width,spriteRect.height/2)
            tempRectBottom = pygame.rect.Rect(spriteRect.left,spriteRect.top, 
                                        spriteRect.width,spriteRect.height/2)             
            for x in range(1,self.width-1):                
                screen.blit(spritePage,(drawX,drawY),tempRectTop)
                screen.blit(spritePage,(drawX,drawY2),tempRectBottom)
                drawX += wallSize

            # Right & left
            drawX = offsetX+halfWallSize
            drawY = offsetY+wallSize            
            drawX2 = offsetX + (self.width -1)*wallSize
            tempRectLeft = pygame.rect.Rect(spriteRect.left+spriteRect.width/2,spriteRect.top, 
                                        spriteRect.width,spriteRect.height)            
            tempRectRight = pygame.rect.Rect(spriteRect.left,spriteRect.top, 
                                        spriteRect.width/2,spriteRect.height)
            for y in range(1,self.height-1):                
                screen.blit(spritePage,(drawX,drawY),tempRectLeft)
                screen.blit(spritePage,(drawX2,drawY),tempRectRight)
                drawY += wallSize                      
                
            # Now draw the internals
            drawY = offsetY+wallSize            
            for y in range(1,self.height-1):
                drawX = offsetX+wallSize
                for x in range(1,self.width-1):
                    screen.blit(spritePage,(drawX,drawY),spriteRect)
                    drawX += wallSize
                drawY += wallSize
                

        
        for x in self.features:
            x.Display(offsetX, offsetY, displayInfo, graphicsData)

                
        # Next: Draw all walls.        
        for x in self.wall:
            x.Display(offsetX, offsetY, displayInfo, graphicsData)

        # Next: Draw Contents (items and monsters)
        contentRemovalList = []
        for x in self.contents:
            if (x.position.containerID<0):
                contentRemovalList.append(x)
            else:
                x.Display(offsetX, offsetY, displayInfo, graphicsData)
        for x in contentRemovalList:
            self.contents.remove(x)
            



    def DisplayCentral(self, offsetX, offsetY, displayInfo, graphicsData):
        "Displays this as the main room, and displays all portaled rooms as well."
        roomOffsets = dict()
        roomOffsets[self.roomID] = (offsetX,offsetY)
        wallSize = baseWallSize * displayInfo.GetSizeMod()
        for w in self.wall:
            for p in w.portalList:
                mapID = p.destination[0]
                try:
                    # What do we do if it's not on the same map...
                    if not mapID==0:
                        rm = self.map.GetMapMaster().FindMap(mapID).FindRoom(p.destination[1])
                        rm.Display(offsetX + p.destination[2]*wallSize, offsetY + p.destination[3]*wallSize,
                                   displayInfo, graphicsData)
                        roomOffsets[rm.roomID] = (offsetX + p.destination[2]*wallSize, offsetY + p.destination[3]*wallSize)
                    # And here's what we do for a room on the same map
                    else:
                        rm = self.map.FindRoom(p.destination[1])
                        rm.Display(offsetX + p.destination[2]*wallSize,
                                   offsetY + p.destination[3]*wallSize,
                                   displayInfo,graphicsData)
                        roomOffsets[rm.roomID] = (offsetX + p.destination[2]*wallSize,offsetY + p.destination[3]*wallSize)
                        
                except:
                    # For some reason - the room or the map or the mapmaster was just WRONG.
                    # For now - just skip it. Log error later
                    pass
                                                                    
        # Now display THIS room
        self.Display(offsetX, offsetY, displayInfo, graphicsData)
        return roomOffsets
                        

    def AddFeature(self,newFeature):
        self.features.append(newFeature)                    
                

    def SetRoomID(self, newRoomID, map):
        if (self.roomID > 0):
            map.UnregisterRoom(self)
        self.roomID = newRoomID
        if (self.roomID > 0):
            map.RegisterRoom(self)
        self.map = map

        
            
        
        
            
        
    

        