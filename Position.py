# Position.py
# Position within a place
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

class Position:

    def __init__(self):
        self.containerType = 0    
        self.containerID = 0     # ContainerID = 0 means nowhere
        self.roomID = 0          # Room 0 is always the default - the "non-room"
        self.X = 0
        self.Y = 0
        
        
    def SetPosition(self,x,y):
        self.X = x
        self.Y = y
        return

    def PutInContainer(self,id, type=0):
        self.containerID = id
        self.containerType = type

    def MoveToRoom(self,roomNumber):
        self.roomID = roomNumber

    def GetContainer():
        return self.containerID

    def GetContainerType():
        return self.containerType

    def GetRoomID():
        return self.roomID

    def GetLocation():
        return (x,y)

    

        

    

        
    