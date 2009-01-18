# Attributes.py
# For creature attributes

AttributeNames = ["Strength","Health","Willpower","Wits","Agility"]
AttributeAbbreviations = ["Str","Hea","Wil","Wit","Agi"]
SkillNames = ["Combat","Magic","Thievery","Search","Haggle","Negotiate","Magic defense"]



class Attributes:
    def __init__(self):
        self.Stats = [10,10,10,10,10]
        self.Skills = dict()
        self.Level = 0

    def IncreaseAttribute(self,attrName,amount):
        try:
            attrIndex = AttributeAbbreviations.index(attrName)
        except:
            try:
                attrIndex = AttributeNames.index(attrName)
            except:
                attrIndex = 0
        self.Stats[attrIndex]+= amount
        

    def IncreaseSkill(self,skillName2,amount):
        skillName=skillName2.capitalize()
        if (self.Skills.has_key(skillName)):
            self.Skills[skillName]+= amount
        else:
            self.Skills[skillName] = amount
        


    def MaxHitPoints(self):
        return self.Level + self.GetSkill("Combat") + self.Stats[1]

    def MaxMagicPoints(self):
        return self.GetSkill("Magic") + self.Stats[2]

    def GetLevel(self):
        if (self.Level<1):
            return self.AdjustLevel()
        else:
            return self.Level
            


    def GetAttribute(self,attrName):
        try:
            attrIndex = AttributeAbbreviations.index(attrName)
        except:
            try:
                attrIndex = AttributeNames.index(attrName)
            except:
                return 0
        return self.Stats[attrIndex]



    def GetSkill(self, skillName2):
        skillName=skillName2.capitalize()
        if (self.Skills.has_key(skillName)):
            return self.Skills[skillName]
        else:
            return 0

    def AdjustLevel(self):
        self.Level = self.GetSkill("Combat") + self.GetSkill("Magic") + self.GetSkill("Thievery")
        return self.Level

        
        
        

    
            
        
        
        
        
        