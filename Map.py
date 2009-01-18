# MAP
# Handles a list of rooms. All maps are registered with a MAPMASTER, and all rooms are registered
# with their respective maps. This will hopefully help us find stuff.
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
import Room

class cMapMaster:
    def __init__(self):
        self.mapCollection = dict()

    def RegisterMap(self,mapData):
        self.mapCollection[mapData.GetID()] = Map

    def UnregisterMap(self,mapData):
        try:
            self.mapCollection.pop[mapData.GetID()]
        finally:
            pass

    def FindMap(self,ID):
        try:
            return self.mapCollection[ID]
        except:
            return None

# GLOBAL ALERT!!!!
MapMaster = cMapMaster()


class Map(gameobject.GameObject):
    def __init__(self):
        gameobject.GameObject.__init__(self)
        self.rooms = dict()
        self.doors = dict()
        MapMaster.RegisterMap(self)
        

    def RegisterRoom(self,roomData):
        self.rooms[roomData.GetRoomID()] = roomData

    def RegisterDoor(self,doorData):
        self.doors[doorData.GetDoorID()] = doorData

    def UnregisterRoom(self,roomData):
        try:
            self.rooms.pop[roomData.GetRoomID()]
        finally:
            pass


    def UnregisterDoor(self, doorData):
        try:
            self.doors.pop[doorData.getDoorID()]
        finally:
            pass
        

    def FindRoom(self,roomID):
        try:
            return self.rooms[roomID]
        except:
            return None


    def FindDoor(self,doorID):
        try:
            return self.doors[doorID]
        except:
            return None

        

    def GetMapMaster(self):
        return MapMaster


        

        
        