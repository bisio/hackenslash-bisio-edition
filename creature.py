# Creature Information
# Generic stats for any kind of creature
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
import Attributes
import TextBox





class Creature(gameobject.GameObject):
    def __init__(self):
        gameobject.GameObject.__init__(self)
        self.Attributes = Attributes.Attributes()
        self.hitpoints = self.Attributes.MaxHitPoints()
        self.baseArmor = 0
        self.magicpoints = self.Attributes.MaxMagicPoints()
        self.statChange = 1
        self.potionCount = dict()
        self.attackDamage = 4
        self.silver = 0
        self.spellEffects = []


    def GetLevel(self):
        return self.Attributes.GetLevel()

    def GetArmor(self):
        return self.baseArmor

    def GetPotionCount(self, potionName):
        if self.potionCount.has_key(potionName):
            return self.potionCount[potionName]
        else:
            return 0

    def GetAllPotions(self):
        return self.potionCount

    def GetMaxHitPoints(self):
        return self.Attributes.MaxHitPoints()

    def GetMaxMagicPoints(self):
        return self.Attributes.MaxMagicPoints()

    def GetCurrentHitPoints(self):
        return self.hitpoints

    def Heal(self,amount):
        self.oldHP = self.hitpoints
        self.hitpoints += amount
        if (self.hitpoints > self.GetMaxHitPoints()):
            self.hitpoints = self.GetMaxHitPoints()
        if not (self.oldHP == self.hitpoints):
            self.FlagStatChange(1)


                

    def AddPotion(self,potionName,quantity):
        potionName = potionName.capitalize()
        if (self.potionCount.has_key(potionName)):
            self.potionCount[potionName]+=quantity
        else:
            self.potionCount[potionName] = quantity
            

    def GetCurrentMagicPoints(self):
        return self.magicpoints


    def RegainMagic(self,amount):
        self.oldMagic = self.magicpoints
        self.magicpoints += amount
        if (self.magicpoints > self.GetMaxMagicPoints()):
            self.magicpoints = self.GetMaxMagicPoints()
        if not (self.oldMagic == self.magicpoints):
            self.FlagStatChange(1)

    def GetAttributes(self):
        return self.Attributes

    def FlagStatChange(self, flag):
        "This is for updating displays and so forth."
        self.statChange = flag

    def GetDefense(self):
        return self.Attributes.GetAttribute("Agility")+self.Attributes.GetSkill("combat")

    def GetOffense(self):
        return self.Attributes.GetAttribute("Strength")+self.Attributes.GetSkill("combat")

    def GetDamage(self):
        return self.attackDamage

    def GetStealSkill(self):
        return self.Attributes.GetAttribute("Agility")+self.Attributes.GetSkill("thievery")

    def GetPerception(self):
        return self.Attributes.GetAttribute("Wits")+self.Attributes.GetSkill("search")

     
  
    

    def GetMoney(self):
        return self.silver

    def SetMoney(self,amount):
        self.silver = amount
        self.FlagStatChange(1)

    def TakeMoney(self,amount):
        if (amount > self.silver) or (amount < 0):
            return 0
        self.silver -= amount
        self.FlagStatChange(1)
        return 1

    def GiveMoney(self,amount):
        if (amount < 0):
            return 0
        self.silver += amount
        self.FlagStatChange(1)        
        return 1

    def UpdateTurn(self):
        removedEffects = []
        for x in self.spellEffects:
            x[2] = x[2] - 1
            if (x[2]<=0):
                removedEffects.append(x)

        for x in removedEffects:
            TextBox.MainText.AddText("%s's %s:%d wears off."%(self.name,x[0],x[1]))
            self.spellEffects.remove(x)



    

    
        
        
    
    

