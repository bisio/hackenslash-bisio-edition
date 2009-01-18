# MINIDUNGEON
# Create a mini-dungeon
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

import Room
import Map
import RoomFeature
import Item
import random
import Monster



def CreateRoom4(roomSimple, map):
    roomSimple.BuildRoom(12,12,1,6)

    # East Door    
    portal = Room.Portal()
    portal.startPosition = 5
    portal.size = 2
    portal.destination = (0,2,11,3)
    roomSimple.wall[1].portalList = [portal]
    roomSimple.wall[1].UpdatePortalRange()

    # North door
    portal = Room.Portal()
    portal.startPosition = 5
    portal.size = 2
    portal.destination = (0,3,0,-11)
    roomSimple.wall[0].portalList = [portal]
    roomSimple.wall[0].UpdatePortalRange()    

    roomSimple.SetRoomID(4,map)

    #Add a Rug
    rug = RoomFeature.Feature()
    rug.CreateRug(1)
    rug.SetPosition(2,3)
    roomSimple.AddFeature(rug)
    
    


def CreateRoom2(roomSimple, map):
    roomSimple.BuildRoom(10,7,4,16)
    portal = Room.Portal()
    portal.startPosition = 2
    portal.size = 2
    portal.destination = (0,4,-11,-3)
    roomSimple.wall[3].portalList = [portal]
    roomSimple.wall[3].UpdatePortalRange()
    roomSimple.SetRoomID(2,map)


    portal = Room.Portal()
    portal.startPosition = 2
    portal.size = 2
    portal.destination = (0,5,9,-3)
    roomSimple.wall[1].portalList = [portal]
    roomSimple.wall[1].UpdatePortalRange()

    #Add a staircase
    stairs = RoomFeature.Feature()
    stairs.CreateStaircase(0)
    stairs.SetPosition(2,3)
    stairs.FeatureBlocks[2].EffectData = (1,2,1) # Room, OffsetX, offsety    
    stairs.FeatureBlocks[5].EffectData = (1,2,1) # Room, OffsetX, offsety    
    roomSimple.AddFeature(stairs)


def CreateRoom1(roomSimple, map):
    roomSimple.BuildRoom(10,10,4,12)
    roomSimple.SetRoomID(1,map)
    roomSimple.safeRoom = 1
    roomSimple.name = "A Safe Place To Rest"

    #Add a staircase
    stairs = RoomFeature.Feature()
    stairs.CreateStaircase(2)
    stairs.SetPosition(4,4)
    stairs.FeatureBlocks[2].EffectData = (2,-3,-1) # Room, OffsetX, offsety
    stairs.FeatureBlocks[5].EffectData = (2,-3,-1) # Room, OffsetX, offsety    
    roomSimple.AddFeature(stairs)
    
    

def CreateRoom3(roomSimple, map):
    roomSimple.BuildRoom(12,12,1,3)
    portal = Room.Portal()
    portal.startPosition = 5
    portal.size = 2
    portal.destination = (0,4,0,11)
    roomSimple.wall[2].portalList = [portal]
    roomSimple.wall[2].UpdatePortalRange()
    roomSimple.SetRoomID(3,map)

    # Create vertical wall    
    wall = Room.Wall()
    wall.Generate(2,1,6,3,6)
    roomSimple.wall.append(wall)
    
    # Create horizontal wall
    wall = Room.Wall()
    wall.Generate(2,0,3,6,6)
    roomSimple.wall.append(wall)

def CreateRoom5 (roomSimple,map):
    roomSimple.BuildRoom(9,9,2,7)
    roomSimple.SetRoomID(5,map)
    
    portal = Room.Portal()
    portal.startPosition = 5
    portal.size = 2
    portal.destination = (0,2,-9,3)
    roomSimple.wall[3].portalList = [portal]
    roomSimple.wall[3].UpdatePortalRange()

    portal = Room.Portal()
    portal.startPosition = 4
    portal.size = 2
    portal.destination = (0,6,0,-10)
    roomSimple.wall[0].portalList = [portal]
    roomSimple.wall[0].UpdatePortalRange()    


def CreateRoom6 (roomSimple,map):
    roomSimple.BuildRoom(9,11,2,7)
    roomSimple.SetRoomID(6,map)
    

    portal = Room.Portal()
    portal.startPosition = 4
    portal.size = 2
    portal.destination = (0,5,0,10)
    roomSimple.wall[2].portalList = [portal]
    roomSimple.wall[2].UpdatePortalRange()    
  
    

    


def CreateDungeon():
    dungeonMap = Map.Map()
    roomList = []
    # create 8 blank rooms
    for i in range(0,8):
        roomList.append(Room.Room())
    CreateRoom1(roomList[0], dungeonMap)
    CreateRoom2(roomList[1], dungeonMap)
    CreateRoom3(roomList[2], dungeonMap)
    CreateRoom4(roomList[3], dungeonMap)
    CreateRoom5(roomList[4], dungeonMap)    
    CreateRoom6(roomList[5], dungeonMap)    

    return dungeonMap    


def ClearRoom(room):
    room.contents = []
    room.monsters = []

def FindSafeLocation(room):
    notFound = 1
    loc = (1,1)
    while (notFound):
        loc = (random.randint(1,room.width-2), random.randint(1,room.height-2))
        if room.AllowedMove((loc[0],loc[1]),(loc[0],loc[1]),0,room.monsters):
            return loc
        

def StockRoom(room, level):
    if (room.safeRoom):
        return
    monstersInRoom = 0
    if (random.randint(0,1)==1):
        monstersInRoom += 1
        monster = Monster.GenerateRandomMonster(random.randint(0,level))
        loc = FindSafeLocation(room)
        monster.position.PutInContainer(0)
        monster.position.MoveToRoom(room.roomID)
        monster.position.SetPosition(loc[0],loc[1])
        room.monsters.append(monster)

    if (level>0) and (random.randint(0,3)==1):
        monstersInRoom += 1
        monster = Monster.GenerateRandomMonster(random.randint(0,level-1))
        loc = FindSafeLocation(room)
        monster.position.PutInContainer(0)
        monster.position.MoveToRoom(room.roomID)
        monster.position.SetPosition(loc[0],loc[1])
        room.monsters.append(monster)
        

    if (level>1) and (random.randint(0,3)==1):
        monstersInRoom += 1
        monster = Monster.GenerateRandomMonster(random.randint(0,level-2))
        loc = FindSafeLocation(room)
        monster.position.PutInContainer(0)
        monster.position.MoveToRoom(room.roomID)
        monster.position.SetPosition(loc[0],loc[1])
        monster.SetStartingLocation(room.roomID,loc[0],loc[1])
        room.monsters.append(monster)
        
    if (random.randint(0,3+monstersInRoom)>2):
        item = Item.Item()
        loc = FindSafeLocation(room)
        item.position.PutInContainer(0)
        item.position.MoveToRoom(room.roomID)
        item.SetPosition(loc[0],loc[1])
        
        if (random.randint(0,3)>1):
            # It's treasure.
            item.Assign("Treasure")
            item.quantity = random.randint(10,(1+level)*25)
        elif (random.randint(0,1)==1):
            if (random.randint(0,1)==1):
                item.Assign("Potion of Healing")
            else:
                item.Assign("Potion of Essence")
            item.quantity = random.randint(1,3)
        else:
            item  = Item.CreateRandomEquipmentItem(level)
            item.position.PutInContainer(0)
            item.position.MoveToRoom(room.roomID)
            item.SetPosition(loc[0],loc[1])

        # 66% chance it's in a chest
        if (random.randint(0,2)>0):
            chest = Item.Item()
            chest.Assign("Chest")
            chest.position.PutInContainer(0)
            chest.position.MoveToRoom(room.roomID)
            chest.SetPosition(loc[0],loc[1])
            chest.contents = [item]
            if (random.randint(0,1)==1):
                chest.lockLevel = 10 + level
            if (random.randint(0,1)==1):
                chest.trap = 10+level
            room.contents = [chest]
        else:
            room.contents = [item]
            
            
            
    


def StockDungeon(dungeonMap, level):
    if (level<1):
        level = 1
    # Clear it out
    for x in dungeonMap.rooms.keys():
        room = dungeonMap.rooms[x]
        ClearRoom(room)
        StockRoom(room,level)

        
        
    
    
    