# ITEM
#
# Handles moveable items
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
import gameobject
import Menu
import dice
import TextBox
import Barks
import random

MasterItemList = dict()

#EquipmentType:
# 0: None (treasure / Container Only)
# 1: Potion
# 2: Wand
# 3: Weapon
# 4: Shield
# 5: Armor
# 6: Ring
# 7: Headgear
# 8: Amulet
# 9: Cloak
# 10: Boots (footgear)
# 11: Quest Item


class ItemData:
    def __init__(self):
        self.name = ""
        self.baseName = ""
        self.GraphicsPage = "items1"
        self.GraphicsBlock = 1
        # Size: 1: Portable, insignificant.
        # 2: Portable, weighty
        # 3: Not portable
        self.size = 0
        self.maxQuantity = 0   # No Max
        self.TreasureValue = 0
        self.equipmentSlot = 0
        self.usableFromInventory = 0
        self.effects = dict()
        self.isContainer = 0
        self.interactionList = ["pick up"]
        self.equipmentType = 0
        
        

    def AssignName(self,name,baseName=""):
        self.name = name
        if (baseName==""):
            self.baseName = name
        else:
            self.baseName = baseName

        MasterItemList[name] = self
        
                    
        
        

class Item(gameobject.GameObject):
    def __init__(self):
        gameobject.GameObject.__init__(self)
        self.itemType = None
        self.quantity = 1
        self.identified = 1
        self.trap = 0
        self.lockLevel = 0
        self.hiddenLevel = 0
        

    def IsTreasure(self):
        if (self.itemType == None):
            return 0
        if (self.itemType.TreasureValue>0):
            return 1
        return 0

    def ConvertToTreasure(self):
        if not self.IsTreasure():
            return
        return self.itemType.TreasureValue * self.quantity

    
    def SellPrice(self, quantity):
        if (self.itemType == None):
            return 0
        if (quantity > self.quantity):
            return 0        
        return self.itemType.sellValue * quantity

    def Assign(self,name):
        if (MasterItemList.has_key(name)):
            self.itemType = MasterItemList[name]
        else:
            self.itemType = None
            print "Unable for find graphics object for item named '%s'!"%name

    def AssignDirect(self,itemType):
        self.itemType = itemType

    def SetQuantity(self,qty):
        if (self.itemType == None):
            return 0
        if (qty > self.itemType.maxQuantity):
            self.quantity = self.itemType.maxQuantity
            return self.quantity
        self.quantity = qty
        return qty

    def SetPosition(self, posX, posY):
        self.position.SetPosition(posX, posY)
        
    
    def Display(self, offsetX, offsetY, displayInfo, graphicsData):
        if (self.itemType == None):
            return
        surface = graphicsData.textures[self.itemType.GraphicsPage][0]
        spriteRect = graphicsData.spriteRects[self.itemType.GraphicsPage][self.itemType.GraphicsBlock]

        itemSize = 32 * displayInfo.GetSizeMod()
        
        displayInfo.GetScreen().blit(surface,
                                     (offsetX + self.position.X * itemSize, offsetY + self.position.Y * itemSize ),
                                     spriteRect)


    def GetItemDetails(self): # Returns a list of details about this item
        detailList = ["Name: %s"%self.itemType.name]
        for x in self.itemType.effects.keys():
            detailList.append("+ %d to %s"%(self.itemType.effects[x],x))
        return detailList



    def CheckForUnlock(self, oPC):
        if (self.lockLevel < 1):
            return 1
        lockpicking = oPC.PC.Attributes.GetAttribute('Agility') + oPC.PC.Attributes.GetSkill("Thievery")+oPC.GetBonusForAction("Thievery")
        rslt = dice.StandardRoll(lockpicking,
                                 self.lockLevel)
        if (rslt>0):
            TextBox.MainText.AddText("Player (%d) picks lock (%d)"%(lockpicking,self.lockLevel))
            self.lockLevel = 0
            return 1
        else:
            TextBox.MainText.AddText("Player (%d) fails to pick lock(%d)"%(lockpicking,self.lockLevel))
            return 0
            

    def CheckForTraps(self, oPC):
        if (self.trap < 1):
            return 1
        lockpicking = oPC.PC.Attributes.GetAttribute('Wits') + oPC.PC.Attributes.GetSkill("Search")+oPC.GetBonusForAction("Search")
        rslt = dice.StandardRoll(lockpicking,
                                 self.trap)
        if (rslt>0):
            TextBox.MainText.AddText("Player (%d) avoids trap (%d)"%(lockpicking,self.trap))
            Barks.CreateFloatingBark("Player avoids trap!",oPC.screenPosX - 128,oPC.screenPosY -16)
        else:
            TextBox.MainText.AddText("Player (%d) accidentally sets off trap (%d)"%(lockpicking,self.trap))
            damageLevel = self.trap / 2
            realDamage = dice.DamageRoll(damageLevel,oPC.PC.GetArmor())
            Barks.CreateFloatingBark("Boom! Player sets off trap for %d damage!"%realDamage,oPC.screenPosX - 128,oPC.screenPosY -16)
            TextBox.MainText.AddText("Player takes %d damage through armor."%realDamage)
            oPC.TakeDamage(realDamage)
                                                                        
        

    def GetOpened(self,oPC):
        print "attempting to open item."
        oPC.TookItem = 1                                                              
        if (self.lockLevel>0):
            rslt = self.CheckForUnlock(oPC)
            if (rslt < 0): #Nothing happens
                Barks.CreateFloatingBark("Lockpicking Attempt Failed",oPC.PC.position.X,oPC.PC.position.Y)
                TextBox.MainText.AddMessage("Player failed to unlock %s"%self.name)
                oPC.WanderingMonsterFlag = 1
                return
        if (self.trap>0):
            self.CheckForTraps(oPC)

        if (oPC.map==None):
            print "ERROR! No map available."
            return  #Can't do anything yet

        # Now dump our contents on the ground, and make ourselves dissapear
        room = oPC.map.FindRoom(oPC.PC.position.roomID)
        for item in self.contents:
            item.SetPosition(self.position.X, self.position.Y)
            item.position.PutInContainer(0)
            room.contents.append(item)
        self.contents = []
        # Make ourselves scarce
        self.position.PutInContainer(-1)
        

    def RespondToMenu(self, menuID, PCObject, interactionString):
        action = interactionString.lower()
        if (action=="pick up"):
            val = PCObject.PickUpItem(self)
            if (val==0):  #Ummm... nothing happened
                return 0
            if (val==1):  # Remove item from room
                self.position.PutInContainer(-1)
                return 1
        if (action=="take as treasure"):
            PCObject.TakeItemAsTreasure(self)
            return 1
        if (action[:7])=="replace":
            PCObject.ReplaceItem(self,interactionString[8:])
            return 1
        if (action=="open"):
            self.GetOpened(PCObject)
            return 1
        return 0 
    

    def CheckIfEquipmentReplacementNeeded(self, oPC, menu):
        # If equipmentType < 2, no replacement EVER needed
        if (self.itemType.equipmentType<2):
            return 
        if oPC.PC.DoesFreeSlotExist(self.itemType.equipmentType):
            return

        # Clear out the old menu list
        oldList = menu.MenuOptions
        oldList.remove("Pick up")        
        if (oldList==None):
            oldList = []
            
        menu.MenuOptions = []
        
        replacementList = oPC.PC.GetReplacedEquipment(self.itemType.equipmentType)
        for x in replacementList:
            menu.MenuOptions.append("Replace %s: %s"%(x[0],x[1].itemType.name))

        menu.MenuOptions = menu.MenuOptions + oldList
        
        

    def MakeMenu(self, pcPlayer):
        menu = Menu.Menu()
        menu.Title = self.itemType.baseName
        menu.type = "item"
        menu.object = self
        # Copy menu options
        for x in self.itemType.interactionList:
            menu.MenuOptions.append("%s"%x)

        # Check to see if we have to replace an item.
        if (menu.MenuOptions[0]=="Pick up"):
            self.CheckIfEquipmentReplacementNeeded(pcPlayer, menu)

        bigDesc = self.GetItemDetails()
        for x in bigDesc:
            menu.AddMessage(x)
    
        menu.ResizeForBestFit()
        return menu
        

RandomProperty = ("defense","attack","damage","armor","Thievery","Magic","Magic Defense",
                  "Search","Haggle","Negotiate")
                  


def CreateRandomEquipmentItem(level):
    item = ItemData()
    item.isContainer = 0
    item.GraphicsBlock=2
    item.size = 1
    item.equipmentType = random.randint(3,10)
    item.effects = dict()

    if (level<0):
        level = 1
    mainProp = random.randint(1,(1+level)/2)
    
    # Skip Wands
    if (item.equipmentType==3): #Sword
        item.GraphicsBlock = 2
        fx = random.randint(1,3)
        if (fx==1):
            item.effects = {'attack':mainProp, 'damage':mainProp}
        elif (fx==2):
            item.effects = {'attack':mainProp}
        else:
            item.effects = {'damage':mainProp}
        item.baseName = "Sword"
        item.name = "+%d Sword"%mainProp
    elif (item.equipmentType==4): #shield
        item.GraphicsBlock = 6        
        item.effects = {'defense':mainProp}
        item.baseName = "Shield"
        item.name = "+%d Shield"%mainProp        
    elif (item.equipmentType==5): # Armor
        item.GraphicsBlock = 4
        item.effects = {'armor':mainProp}
        item.baseName = "Armor"
        item.name = "+%d Armor"%mainProp                  
    elif (item.equipmentType==6): #ring
        item.GraphicsBlock = 7
        item.baseName = "Ring"
        item.name = "Ring"
    elif (item.equipmentType==7): # headgear
        item.GraphicsBlock = 8
        item.baseName = "Helmet"
        item.name = "Helmet"        
    elif (item.equipmentType==8): #amulet
        item.GraphicsBlock = 9
        item.baseName = "Amulet"
        item.name = "Amulet"        
    elif (item.equipmentType==9): # cloak
        item.GraphicsBlock = 10
        item.baseName = "Cloak"
        item.name = "Cloak"        
    elif (item.equipmentType==10): # boots
        item.GraphicsBlock = 11
        item.baseName = "Boots"
        item.name = "Boots"          

    if (len(item.effects.keys())<1) or (random.randint(1,4)==1):
        # Add a new property
        prop = random.randint(0,len(RandomProperty)-1)
        item.name += " of %s"%RandomProperty[prop]
        item.effects[RandomProperty[prop]]=random.randint(1,(1+level)/2)

    item.TreasureValue = 0
    for x in item.effects.keys():
        item.TreasureValue += pow(2,item.effects[x])

    item.TreasureValue *= 50        
    item.interactionList = ["Pick up", "Take as treasure"]

    itemInstance = Item()
    itemInstance.AssignDirect(item)
    return itemInstance
     


def CreateItemTypes():
    if (len(MasterItemList)>1):
        return
    item = ItemData()
    item.isContainer = 1
    item.size = 3
    item.equipmentType = 0
    item.interactionList = ["Open"]
    item.AssignName("Chest","Chest")

    item = ItemData()
    item.isContainer = 0
    item.GraphicsBlock=2
    item.size = 1
    item.equipmentType = 3
    item.TreasureValue = 200
    item.interactionList = ["Pick up", "Take as treasure"]
    item.effects = {'attack':1, 'damage':1}
    item.AssignName("+1 Sword","Sword")

    item = ItemData()
    item.isContainer = 0
    item.equipmentType = 1    
    item.GraphicsBlock=5
    item.size = 1
    item.interactionList = ["Pick up"]
    item.AssignName("Potion of Healing","Potion")

    item = ItemData()
    item.isContainer = 0
    item.equipmentType = 1    
    item.GraphicsBlock=5
    item.size = 1
    item.interactionList = ["Pick up"]
    item.AssignName("Potion of Essence","Potion")    

    item = ItemData()
    item.isContainer = 0
    item.equipmentType = 0    
    item.GraphicsBlock=3
    item.size = 1
    item.TreasureValue = 1
    item.interactionList = ["Pick up"]
    item.AssignName("Treasure","Treasure")     
    


# Fill all items        
CreateItemTypes()        
        