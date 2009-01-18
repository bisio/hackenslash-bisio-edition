# PlayerCharacter
# Game-Rule Information for the "player character" 
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

import creature


EquipmentSlotNames = ['Weapon','Shield','Armor','Amulet','Cloak','Boots','Headgear',
                      'Left Ring', 'Right Ring', 'Wand 1', 'Wand 2', 'Wand 3','Quest Item']


SlotTypeToName = {3:'Weapon',4:'Shield',5:'Armor', 7:'Headgear', 8:'Amulet',
                      9:'Cloak', 10:'Boots', 11:'Quest Item'}


class PlayerCharacter(creature.Creature):
    def __init__(self):
        creature.Creature.__init__(self)
        self.name = "Player"
        self.ExperiencePoints = 0
        self.Equipment = dict()
        self.LevelupFlag = 0
        for x in EquipmentSlotNames:
            self.Equipment[x] = None



    def GetExperience(self):
        return self.ExperiencePoints

    def GainExperience(self,amount):
        self.ExperiencePoints += amount
        level = self.Attributes.GetLevel()
        if (level<10):
            xpNeeded = (pow(2,level) * 100)-100
        else:
            xpNeeded = 75000+(25000 * (level-10))
        if (self.ExperiencePoints >= xpNeeded) and (level < 20):
            self.LevelupFlag = 1
        self.FlagStatChange(1)


    def DoesFreeSlotExist(self, equipmentType):
        if (equipmentType==2):
            if self.Equipment['Wand 1']==None:              
                return 1
            if self.Equipment['Wand 2']==None:        
                return 1
            if self.Equipment['Wand 3']==None:             
                return 1
            return 0
        if (equipmentType==6):
            if self.Equipment['Left Ring']==None:
                return 1
            if self.Equipment['Right Ring']==None:
                return 1
            return 0

        try:        
            slotname = SlotTypeToName[equipmentType]
        except:
            return 0
        if self.Equipment[slotname]==None:
            return 1       



    def FindEmptyItemSlot(self,item):  # Return 1 on success, 0 on failure
        equipmentType = item.itemType.equipmentType
        if (equipmentType==2):
            if self.Equipment['Wand 1']==None:
                self.Equipment['Wand 1'] = item
                item.position.PutInContainer(-1)                
                return 1
            if self.Equipment['Wand 2']==None:
                self.Equipment['Wand 2'] = item
                item.position.PutInContainer(-1)                
                return 1
            if self.Equipment['Wand 3']==None:
                self.Equipment['Wand 3'] = item
                item.position.PutInContainer(-1)                
                return 1
            return 0
        if (equipmentType==6):
            if self.Equipment['Left Ring']==None:
                self.Equipment['Left Ring'] = item
                item.position.PutInContainer(-1)
                return 1
            if self.Equipment['Right Ring']==None:
                self.Equipment['Right Ring'] = item
                item.position.PutInContainer(-1)
                return 1
            return 0

        try:        
            slotname = SlotTypeToName[equipmentType]
        except:
            return 0
        if self.Equipment[slotname]==None:
            self.Equipment[slotname] = item
            item.position.PutInContainer(-1)
            return 1
        return 0
            


    def ReplaceItem(self, slotname, item):
        if self.Equipment.has_key(slotname):
            try:
                oldItem = self.Equipment[slotname]
                self.GiveMoney(oldItem.itemType.TreasureValue)
                self.Equipment[slotname] = item
                item.position.PutInContainer(-1)
            except:
                return 0
        else:
            return 0
        

    def GetReplacedEquipment(self, equipmentType):
        if equipmentType<2:
            return []
        if (equipmentType==2):
            return [['Wand 1',self.Equipment['Wand 1']],
                    ['Wand 2',self.Equipment['Wand 2']],
                    ['Wand 3',self.Equipment['Wand 3']]]
        if (equipmentType==6):
            return [['Left Ring',self.Equipment['Left Ring']],
                    ['Right Ring',self.Equipment['Right Ring']]]

        try:
            slotname = SlotTypeToName[equipmentType] 
            return [[slotname,self.Equipment[slotname]]]
        except:
            return []
    

    
    
        
        

            

            

            

        