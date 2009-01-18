# GameObject
# This defines a very basic game Object. This object has a type,
# an ID, and contents (every object is a potential container).
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

import Position


class cObjectIDMaster:
    def __init__(self):
        self.Reset()

    def GetUniqueID(self):
        p = self.nextUniqueID
        self.nextUniqueID+=1
        return p

    def Reset(self):
        self.nextUniqueID = 1

    def DeclareObject(self, objectID):
        self.nextUniqueID = objectID +1
        


# Global Warning!
ObjectIDMaster = cObjectIDMaster()


class GameObject:
    def __init__(self):
        self.position = Position.Position()
        self.ID = ObjectIDMaster.GetUniqueID()  # -1 means no ID assigned
        self.type = 0  # Type 0 means ... ummm... nothing.
        self.contents = []  # Contents is what this object contains

    def GetType(self):
        return self.type

    def SetType(self,type):
        self.type = type

    def GetID(self):
        # If we don't have an ID yet, we had better assign ourselves one.
        if (self.ID < 0):
            self.ID = ObjectIDMaster.GetUniqueID()            
        return self.ID
    
    def Position(self):
        return self.position

    def SetPosition(self,posX,posY):
        self.position.X = posX
        self.position.Y = posY

    def GetContents(self):
        return self.contents

    def Display(self, offsetX, offsetY, displayInfo, graphicsData):
        pass
    
    

        

    
        