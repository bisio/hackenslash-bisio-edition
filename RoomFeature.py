# RoomFeature.py
#
# Room Features - such as stairs, columns, and other static objects
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

import gameobject
import Position

RotationLookup = {'n':0,'e':1,'s':2,'w':3, 0:'n', 1:'e', 2:'s', 3:'w'}

FeatureBlockMasterList = dict()

Block2x2Locations = {0:[(0,0),(1,0),(0,1),(1,1)],
                   1:[(0,1),(0,0),(1,1),(1,0)],
                   2:[(1,1),(0,1),(1,0),(0,0)],
                   3:[(1,0),(1,1),(0,0),(0,1)]}

Block3x2Locations = {0:[(0,0), (1,0), (2,0), (0,1), (1,1), (2,1)],
                   1:[(0,2), (0,1), (0,0), (1,2), (1,1), (1,0)],
                   2:[(2,1), (1,1), (0,1), (2,0), (1,0), (0,0)],
                   3:[(1,0), (1,1), (1,2), (0,0), (0,1), (0,2)]}

Block4x2Locations = {0:[(0,0), (1,0), (2,0), (3,0), (0,1), (1,1), (2,1), (3,1)],
                     1:[(0,3), (0,2), (0,1), (0,0), (1,3), (1,2), (1,1), (1,0)],
                     2:[(3,1), (2,1), (1,1), (0,1), (3,0), (2,0), (1,0), (0,0)],
                     3:[(1,0), (1,1), (1,2), (1,3), (0,0), (0,1), (0,2), (0,3)]}



class FeatureBlockData:
    def __init__(self):
        self.GraphicsPage = "features"
        self.GraphicsBlock = 1
        self.EntryRestrictions = {'n':0, 'e':0, 's':0, 'w':0}  # Allowed from N, E, S, and W
        self.EntryEffect = ''

    def IsBlocked(self,direction,blockRotation):
        dir = self.RotateDirection(direction,blockRotation)
        if (self.EntryRestrictions.has_key(dir)):
            return self.EntryRestrictions[dir]
        return 1

    def RotateDirection(self,direction,blockRotation):
        directionIndex = RotationLookup[direction]
        directionIndex = (directionIndex + 4 - blockRotation)%4
        return RotationLookup[directionIndex]

    def GetGraphic(self,graphicsData,blockRotation):
        if (blockRotation == 0):
            return (graphicsData.textures[self.GraphicsPage][0],graphicsData.spriteRects[self.GraphicsPage][self.GraphicsBlock])
        else:
            textPageName = self.GraphicsPage+str(blockRotation)
            return (graphicsData.textures[textPageName][0],graphicsData.spriteRects[textPageName][self.GraphicsBlock])  
        


class FeatureBlock:
    def __init__(self):
        self.BlockData = None
        self.Position = Position.Position()
        self.Rotation = 0
        self.EffectData = ()
        

    def SetData(self,data):
        self.BlockData = data


    def SetRotation(self,rot):
        self.Rotation = rot%4

    def SetPosition(self, x,y):
        self.Position.SetPosition(x,y)      

    def Display(self,offsetX, offsetY, displayInfo, GraphicsData):
        if (self.BlockData == None):
            return
        blockSize = 32 * displayInfo.GetSizeMod()        
        sprite = self.BlockData.GetGraphic(GraphicsData, self.Rotation)
        displayInfo.GetScreen().blit(sprite[0],
                                     (offsetX+self.Position.X*blockSize,offsetY + self.Position.Y * blockSize),
                                     sprite[1])
        

class Feature:
    def __init__(self):
        self.FeatureBlocks = []
        self.Rotation = 0
        self.Position = Position.Position()

    def Display(self, offsetX, offsetY, displayInfo, graphicsData):
        blockSize = 32 * displayInfo.GetSizeMod()
        for block in self.FeatureBlocks:
            block.Display(offsetX+self.Position.X*blockSize,
                          offsetY+self.Position.Y*blockSize,
                          displayInfo, graphicsData)

    def EntryAllowed(self, startPos,endPos):
        # Get the feature at the player's position...
        posX = endPos[0] - self.Position.X
        posY = endPos[1] - self.Position.Y

        startPosX = startPos[0] - self.Position.X
        startPosY = startPos[1] - self.Position.Y
        
        entryEffect = 1
        enteredFeatureList = []

        direction1 = endPos[0] - startPos[0]
        direction2 = endPos[1] - startPos[1]
        exitdirection1 = ''
        exitdirection2 = ''
        # Remember, the forbidden 'zone' is where the travelling comes FROM, not the real
        # direction of travel (why did I do it that way? Oh, well)
        if (direction1 > 0):            
            direction1 = 'w'
            exitdirection1 = 'e'
        elif (direction1 < 0):
            direction1 = 'e'
            exitdirection1 = 'w'
        else:
            direction1 = ''

        if (direction2 > 0):
            direction2 = 'n'
            exitdirection2 = 's'
        elif (direction2 < 0):
            direction2 = 's'
            exitdirection2 = 'n'
        else:
            direction2 = ''
            
        

        
        for block in self.FeatureBlocks:
            if (block.Position.X == posX) and (block.Position.Y == posY):
                enteredFeatureList.append(block)
                if not (direction1 == ''):
                    if (block.BlockData.IsBlocked(direction1,self.Rotation)):
                        entryEffect = 0
                if not (direction2 == ''):
                    if (block.BlockData.IsBlocked(direction2,self.Rotation)):
                        entryEffect = 0
            #check if we're allowed to LEAVE the block
            if (block.Position.X == startPosX) and (block.Position.Y == startPosY):
                if not (exitdirection1 == ''):
                    if (block.BlockData.IsBlocked(exitdirection1,self.Rotation)):
                        entryEffect = 0
                if not (exitdirection2 == ''):
                    if (block.BlockData.IsBlocked(exitdirection2,self.Rotation)):
                        entryEffect = 0                        
                
        return (entryEffect, enteredFeatureList)                       
                        
                    

    def GetAllFeatures(self, initialPosX, initialPosY):
        posX = initialPosX - self.Position.X
        posY = initialPosY - self.Position.Y
        blockList = []
        for block in self.FeatureBlocks:
            if (block.Position.X == posX) and (block.Position.Y == posY):
                blockList.append((block.BlockData.EntryEffect, block.EffectData))
        return blockList
        
     
        

    def SetPosition(self, posX, posY):
        self.Position.SetPosition(posX,posY)

    def CreateStaircase(self, rot):
        self.Rotation = rot%4
        if (len(FeatureBlockMasterList)<1):
            LoadFeatureBlockData()
        for i in range(0,6):
            newblock = FeatureBlock()
            newblock.SetData(FeatureBlockMasterList[i])
            newblock.SetRotation(rot)
            newblock.SetPosition(Block3x2Locations[rot][i][0],Block3x2Locations[rot][i][1])
            self.FeatureBlocks.append(newblock)
        # Need to set blocks 2 and 5 with their teleport location
                    
            
    def CreateRug(self, rot):
        self.Rotation = rot%4
        if (len(FeatureBlockMasterList)<1):
            LoadFeatureBlockData()
        for i in range(0,8):
            newblock = FeatureBlock()
            newblock.SetData(FeatureBlockMasterList[i+6])
            newblock.SetRotation(rot)
            newblock.SetPosition(Block4x2Locations[rot][i][0],Block4x2Locations[rot][i][1])
            self.FeatureBlocks.append(newblock)   

        
            
           
def LoadStaircaseData():
    FeatureBlockMasterList[0] = FeatureBlockData()
    FeatureBlockMasterList[0].GraphicsBlock = 1
    FeatureBlockMasterList[0].EntryRestrictions['n'] = 1 

    FeatureBlockMasterList[1] = FeatureBlockData()
    FeatureBlockMasterList[1].GraphicsBlock = 2
    FeatureBlockMasterList[1].EntryRestrictions['n'] = 1

    FeatureBlockMasterList[2] = FeatureBlockData()
    FeatureBlockMasterList[2].GraphicsBlock = 3
    FeatureBlockMasterList[2].EntryRestrictions['n'] = 1     
    FeatureBlockMasterList[2].EntryRestrictions['e'] = 1
    FeatureBlockMasterList[2].EntryEffect='tport'

    FeatureBlockMasterList[3] = FeatureBlockData()
    FeatureBlockMasterList[3].GraphicsBlock = 9
    FeatureBlockMasterList[3].EntryRestrictions['s'] = 1 

    FeatureBlockMasterList[4] = FeatureBlockData()
    FeatureBlockMasterList[4].GraphicsBlock = 10
    FeatureBlockMasterList[4].EntryRestrictions['s'] = 1

    FeatureBlockMasterList[5] = FeatureBlockData()
    FeatureBlockMasterList[5].GraphicsBlock = 11
    FeatureBlockMasterList[5].EntryRestrictions['s'] = 1     
    FeatureBlockMasterList[5].EntryRestrictions['e'] = 1
    FeatureBlockMasterList[5].EntryRestrictions['e'] = 1
    FeatureBlockMasterList[5].EntryEffect='tport'

def LoadRugData():
    FeatureBlockMasterList[6] = FeatureBlockData()
    FeatureBlockMasterList[6].GraphicsBlock = 5
    FeatureBlockMasterList[7] = FeatureBlockData()
    FeatureBlockMasterList[7].GraphicsBlock = 6
    FeatureBlockMasterList[8] = FeatureBlockData()
    FeatureBlockMasterList[8].GraphicsBlock = 7
    FeatureBlockMasterList[9] = FeatureBlockData()
    FeatureBlockMasterList[9].GraphicsBlock = 8
    
    FeatureBlockMasterList[10] = FeatureBlockData()
    FeatureBlockMasterList[10].GraphicsBlock = 13
    FeatureBlockMasterList[11] = FeatureBlockData()
    FeatureBlockMasterList[11].GraphicsBlock = 14
    FeatureBlockMasterList[12] = FeatureBlockData()
    FeatureBlockMasterList[12].GraphicsBlock = 15
    FeatureBlockMasterList[13] = FeatureBlockData()
    FeatureBlockMasterList[13].GraphicsBlock = 16       
    

def LoadColumnData():
    FeatureBlockMasterList[14] = FeatureBlockData()
    FeatureBlockMasterList[14].GraphicsBlock = 11
    FeatureBlockMasterList[14].EntryRestrictions =  {'n':1, 'e':1, 's':1, 'w':1}    
  


def LoadFeatureBlockData():
    LoadStaircaseData()
    LoadRugData()
    LoadColumnData()
    





            

