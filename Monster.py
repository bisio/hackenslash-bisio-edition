## MONSTER
## For... umm... monsters.
##
##
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
import dice
import Menu
import Barks
import Item
import random
import TextBox


class Monster(creature.Creature):
    def __init__(self):
        creature.Creature.__init__(self)
        self.name = "A Monster"
        self.GraphicsPage = ""
        self.GraphicsRect = 0
        self.screenPosX = 0
        self.screenPosY = 0
        self.facing = 0
        self.moveOffset = 0
        self.movement = (0,0)
        self.description = ["A generic monster."]
        self.isVisible = 0
        self.attitude = 0
        self.inactive = 0
        self.originalPosition = (0,0,0)

    def SetGraphics(self,pageName,rectNumber):
        self.GraphicsPage = pageName
        self.GraphicsRect = rectNumber

    def GetRoom(self):
        return self.position.roomID

    def SetStartingLocation(self, room, posX, posY):
        self.originalPosition = (room,posX,posY)
        self.position.MoveToRoom(room)
        self.position.X = posX
        self.position.Y = posY


    def GenerateScreenPosition(self, display, roomOffsetX, roomOffsetY):
        blockSize = 32 * display.GetSizeMod()
        halfBlockSize = blockSize / 2
        self.screenPosX = roomOffsetX + self.position.X * blockSize + halfBlockSize
        self.screenPosY = roomOffsetY + self.position.Y * blockSize + halfBlockSize



    def Display(self,displayInfo, graphicsData):        
        animData = graphicsData.textures[self.GraphicsPage]
        imageSurface = animData[0]
        imageRect = graphicsData.spriteRects[self.GraphicsPage][self.GraphicsRect]
        halfsizeX = 16
        halfsizeY = 16
        displayInfo.GetScreen().blit(imageSurface,(self.screenPosX - halfsizeX,self.screenPosY - halfsizeY),imageRect)

    
        
        
        
    def MouseOnMe(self,display, mPosX, mPosY):
        size = 16.0 * display.GetSizeMod()
        if ((mPosX > self.screenPosX - size) and (mPosX < self.screenPosX + size) and
            (mPosY > self.screenPosY - size) and (mPosY < self.screenPosY + size)):
            return 1
        return 0

    def IsSettled(self):
        "returns 1 if we're ready to move again, 0 if we're still in transit between squares."
        if (self.movement[0]==0) and (self.movement[1]==0) and (self.moveOffset ==0):
            return 1
        return 0

    def ContinueMovement(self, speed, map):
        if self.IsSettled():
            return
        self.moveOffset += speed
        
        if (self.moveOffset >= 1):
            if not (self.HandlePortalledMovement(map)):            
                self.position.X += self.movement[0]
                self.position.Y += self.movement[1]
                self.HandleSpecialEffectOnMove(map)
            self.movement = (0,0)
            self.moveOffset = 0

    def StartMove(self, moveX, moveY):
        if not self.IsSettled():
            return 0
        self.movement = (moveX,moveY)
        self.SetFacingFromMovement((moveX,moveY))


    def HandleSpecialEffectOnMove(self, map):
        "If the being walked into a feature that has a special effect, activate it now."
        room = map.FindRoom(self.position.roomID)

        featureList = room.GetFeatureBlockAtPosition(self.position.X, self.position.Y)
        if (len(featureList)<1):
            return 0
        if (featureList[0][0]=='tport'):
            tportRoom = featureList[0][1][0]
            tportXOff = featureList[0][1][1]
            tportYOff = featureList[0][1][2]
            self.position.X += tportXOff
            self.position.Y += tportYOff
            self.position.MoveToRoom(tportRoom)
        return 1


    def HandlePortalledMovement(self, map):
        "Handle any movement that transitions via portal."
        # Pre-calculate the player's new position
        adjustedPositionX = self.position.X + self.movement[0]
        adjustedPositionY = self.position.Y + self.movement[1]

        # is the new position outside the bounds of the room? If not, return 0 - no portalling necessary
        room = map.FindRoom(self.position.roomID)
        if ((adjustedPositionX >= 0) and (adjustedPositionY >= 0) and
            (adjustedPositionX < room.width) and (adjustedPositionY < room.height)):
                return 0

        # Get the creature's portal
        portal = room.GetPortal(self.position.X, self.position.Y)
        if (portal==None):
            return 0  # This will "bounce" the creature back to his previous position. Oh, well. He shouldn't be moving here anyway!

        # Transport the creature to a new offset based on the portal
        self.position.X += self.movement[0] - portal.destination[2]
        self.position.Y += self.movement[1] - portal.destination[3]
        self.position.MoveToRoom(portal.destination[1])
        self.position.PutInContainer(portal.destination[0],0)

        # Now tell the caller that we've already handled the movement        
        return 1


    def MakeMenu(self, menuType=0):
        menu = Menu.Menu()
        menu.Title = self.name
        menu.type = "monster"
        menu.menuID = menuType
        menu.object = self
        for x in self.description:
            menu.AddMessage(x)
        menu.AddMessage("Armor Class: %d"%(self.GetArmor()))
        menu.AddMessage("Hit Points: %d"%(self.GetCurrentHitPoints()))
        menu.MenuOptions = ["Attack","Cast Spell"]
        if (self.attitude==0):
            menu.MenuOptions.append("Negotiate")

        menu.SetPosition(self.screenPosX + 16, self.screenPosY - 16)                 
        menu.ResizeForBestFit()
        return menu

    def TakeDamage(self,damage):
        self.hitpoints -= damage


    def TakeBoltAttack(self, boltLevel, attacker):
        if (boltLevel<1):
            boltLevel = 1
        if (boltLevel>4):
            boltLevel = 4

        attackerLevel = attacker.PC.Attributes.GetAttribute("Wil")+attacker.PC.Attributes.GetSkill("magic")+attacker.GetBonusForAction("magic")
        defenderLevel = self.Attributes.GetAttribute("Wil")+self.Attributes.GetSkill("magic defense")+self.GetBonusForAction("magic defense")

        damageBase = 10 + attacker.PC.Attributes.GetSkill("magic") + attacker.GetBonusForAction("magic")

        totalDamage = 0
        for x in range(0,boltLevel):
            totalDamage += dice.DamageRoll(damageBase,0)


        save = dice.StandardRoll(defenderLevel, attackerLevel)
        
        if (save):
            totalDamage = (1+totalDamage)/2
            Barks.CreateFloatingBark("Saved! Reduced Damage (%d)!"%totalDamage,self.screenPosX, self.screenPosY)               
            TextBox.MainText.AddText("%s saves against magic "%self.name)
            TextBox.MainText.AddText("(%d to %d) for %d damage."%(attackerLevel,defenderLevel,totalDamage))
        else:
            Barks.CreateFloatingBark("Smack-down by bolt for %d damage!"%totalDamage,self.screenPosX, self.screenPosY)                           
            TextBox.MainText.AddText("%s fails saves against magic "%self.name)
            TextBox.MainText.AddText("(%d to %d) for %d damage."%(attackerLevel,defenderLevel,totalDamage))

        self.TakeDamage(totalDamage)



    def AddSpellEffect(self,effectName, effectLevel, effectDuration):
        # Find existing effects of the same name / value
        bExisting = 0
        for x in self.spellEffects:
            if x[0]==effectName:
                bExisting = 1
                if (x[1]>0) and (x[1]<=effectLevel):
                    x[2] = effectDuration
                    x[1] = effectLevel
                elif (x[1]<0) and (x[1]>=effectLevel):
                    x[2] = effectDuration
                    x[1] = effectLevel                    
                    
        if not bExisting:
            self.spellEffects.append([effectName,effectLevel,effectDuration])
            
            
    def TakeCurseAttack(self, curseLevel, attacker):
        if (curseLevel<1):
            curseLevel = 1
        if (curseLevel>4):
            curseLevel = 4

        duration = 10 + (attacker.PC.Attributes.GetSkill("magic")+attacker.GetBonusForAction("magic"))*2
            
        attackerLevel = attacker.PC.Attributes.GetAttribute("Will")+attacker.PC.Attributes.GetSkill("magic")+attacker.GetBonusForAction("magic")
        defenderLevel = self.Attributes.GetAttribute("Will")+self.Attributes.GetSkill("magic defense")+self.GetBonusForAction("magic defense")
        save = dice.StandardRoll(defenderLevel, attackerLevel)
        
        if (save):
            Barks.CreateFloatingBark("Saved! No effect!",self.screenPosX, self.screenPosY)               
            TextBox.MainText.AddText("%s saves against magic "%self.name)
            TextBox.MainText.AddText("(%d to %d) and isn't cursed."%(attackerLevel,defenderLevel))
        else:            
            Barks.CreateFloatingBark("CURSED",self.screenPosX, self.screenPosY)               
            TextBox.MainText.AddText("%s fails saves against magic"%self.name)
            TextBox.MainText.AddText("(%d to %d) and is cursed for %d rounds."%(attackerLevel,defenderLevel,duration))
            self.AddSpellEffect('curse',-curseLevel,duration)
            


    

    def GetSpellCastAtMe(self, pcPlayer, interactionString):
        spellData = interactionString.split(' ')
        spellLevel = int(spellData[1])
        spellCost = (spellLevel*2)-1
        if (spellCost>pcPlayer.PC.GetCurrentMagicPoints()):
            TextBox.MainText.AddText("Not enough magic points to cast %s"%interactionString)
            Barks.CreateFloatingBark("Not enough magic points!",pcPlayer.screenPosX, pcPlayer.screenPosY)               
            return 1
        pcPlayer.PC.magicpoints -= spellCost
        pcPlayer.PC.FlagStatChange(1)
        if (spellData[0].lower()=='curse'):
            self.TakeCurseAttack(spellLevel,pcPlayer)
        else:
            self.TakeBoltAttack(spellLevel, pcPlayer)
            
            
        
        
        



        

    def NegotiateBribe(self, pcPlayer):
        levelDiff = self.Attributes.GetLevel() - pcPlayer.PC.Attributes.GetLevel()
        baseAmount = self.Attributes.GetLevel() * 50
        if (baseAmount < 50):
            baseAmount = 50
        if (levelDiff < 0):
            baseAmount /= (1-levelDiff)
        elif (levelDiff > 0):
            baseAmount = baseAmount + (baseAmount * levelDiff / 2)

        self.NegotiationBase = baseAmount

        # Now do the bribe levels...
        menu = Menu.Menu()
        menu.Title = "Negotiate Bribe For "+self.name
        menu.type = "monster"
        menu.menuID = 1
        menu.object = self
        if (self.attitude<0):
            menu.AddMessage("The "+self.name+" looks pretty angry right now.")
            menu.AddMessage("I don't think it's in the mood to negotiate.")
            menu.AddMessage("How did you get this menu, anyway?")
        else:
            if (pcPlayer.PC.GetMoney()>=self.NegotiationBase/2):
                menu.MenuOptions = ["Bribe %d"%(self.NegotiationBase/2)]
            else:
                menu.AddMessage("You don't have enough money to BEGIN to offer a bribe.")
                menu.AddMessage("Better think of something else, quick!")

            if (pcPlayer.PC.GetMoney()>=self.NegotiationBase):
                menu.MenuOptions.append("Bribe %d"%self.NegotiationBase)
            
            if (pcPlayer.PC.GetMoney()>=self.NegotiationBase*2):
                menu.MenuOptions.append("Bribe %d"%(self.NegotiationBase*2))

        menu.SetPosition(self.screenPosX + 16, self.screenPosY - 16)                 
        menu.ResizeForBestFit()
        Menu.MasterMenu.AddMenu(menu)
        

    def GetBonusForAction(self,action):
        bonus = 0
        for x in self.spellEffects:
            if (x[0]=="buff") or (x[0]=="curse") or (x[0]==action):
                bonus += x[1]
        return bonus
        
    def GetBribed(self,pcPlayer,bribeString):
        if not (bribeString[:5]=="Bribe"):
            Barks.CreateFloatingBark("Huh? That's no bribe!",self.screenPosX - 128,self.screenPosY - 16)
            return

        # Pull out the amount from the string
        amount = int(bribeString[6:])
        success = 0
        PlayerSkill = pcPlayer.PC.Attributes.GetAttribute("Wits")+pcPlayer.PC.Attributes.GetSkill("Negotiation")
        MonsterSkill = self.Attributes.GetAttribute("Wits")+self.Attributes.GetSkill("Negotiate")
        try:
            if (amount>self.NegotiationBase):
                success = dice.StandardRoll(PlayerSkill+5,MonsterSkill)
            elif (amount < self.NegotiationBase):
                success = dice.StandardRoll(PlayerSkill,MonsterSkill+5)
            else:
                success = dice.StandardRoll(PlayerSkill,MonsterSkill)
        except:
            success = 0
            print "Error! Monster had no NegotiationBase from negotiation calculation"

        if (success):
            Barks.CreateFloatingBark("%s is appeased."%self.name,self.screenPosX - 128,self.screenPosY - 16)
            TextBox.MainText.AddText("%s accepts a bribe of %d"%(self.name,amount))
            pcPlayer.PC.TakeMoney(amount)
            self.attitude = 1
            return
        else:
            # Better do another check to make sure it's not offended.
            success = dice.StandardRoll(PlayerSkill,MonsterSkill)
            if (success):
                Barks.CreateFloatingBark("%s is not impressed by your puny offer."%self.name,self.screenPosX - 128,self.screenPosY - 16)
                TextBox.MainText.AddText("%s doesn't accept bribe of %d"%(self.name,amount))
                return
            else:
                Barks.CreateFloatingBark("%s is offended by your pathetic offer!"%self.name,self.screenPosX - 128,self.screenPosY - 16)
                TextBox.MainText.AddText("%s is offended by an attempted bribe of %d"%(self.name,amount))
                self.attitude =-1
                return
            
                

            

    def BeAttacked(self,attacker):
        armor = self.GetArmor() + self.GetBonusForAction("armor")
        defense = self.GetDefense() + self.GetBonusForAction("defense")
        offense = attacker.GetOffense()+attacker.GetBonusForAction("attack")
        damage = attacker.GetDamage() + attacker.GetBonusForAction("damage")
        # This will torque them off
        self.attitude = -1

        TextBox.MainText.AddText("Player (atk %d) attacks %s (def %d)"%(offense, self.name,defense))

        if (dice.StandardRoll(offense,defense)==0):
            Barks.CreateFloatingBark("Player misses!",self.screenPosX - 128,self.screenPosY - 16)
            TextBox.MainText.AddText("Player misses %s."%(self.name))
            return

        realDamage = dice.DamageRoll(damage,armor)
        TextBox.MainText.AddText("Damage %d vs. armor %d"%(damage, armor))            
        
        if (realDamage<1):
            Barks.CreateFloatingBark("Armor Resists Damage!",self.screenPosX - 128,self.screenPosY - 16)
            TextBox.MainText.AddText("Player does no damage.")
            return

        Barks.CreateFloatingBark("Player hits for %d!"%realDamage,self.screenPosX - 128,self.screenPosY - 16)
        TextBox.MainText.AddText("%s takes %d damage."%(self.name, realDamage))
        self.TakeDamage(realDamage)

        return        
            

    def DropItems(self,room):
        for item in self.contents:
            item.SetPosition(self.position.X, self.position.Y)
            item.position.PutInContainer(0)            
            room.contents.append(item)            


    def SetMovement(self, moveX, moveY):
        self.position.X += moveX
        self.position.Y += moveY

    def Deactivate(self):
        if not (self.position.roomID == self.originalPosition[0]):
            self.position.MoveToRoom(self.originalPosition[0])
            self.position.X = self.originalPosition[1]
            self.position.Y = self.originalPosition[2]
        self.inactive = 1

            

    def ChasePlayer(self,map,PCPlayer, offsetX, offsetY):
        moveX = 0
        moveY = 0
        room = map.FindRoom(self.position.roomID)
        if (offsetX < 0):
            moveX = -1
        elif (offsetX > 0):
            moveX = 1
        if (offsetY < 0):
            moveY = -1
        elif (offsetY > 0):
            moveY = 1

        if (moveX == 0) and (moveY == 0):  # WTH?!?!?!? We're on TOP of the player?
            return

        # Check if it's a legal move
        goodMove = 0
        if (not(room.AllowedMove((self.position.X, self.position.Y),
                                 (self.position.X + moveX, self.position.Y + moveY),
                                 0,[]))):
            if not (moveX==0):
                if (room.AllowedMove((self.position.X, self.position.Y),
                                 (self.position.X, self.position.Y + moveY),
                                 0,[])):
                    moveX = 0
                    goodMove = 1
                elif (room.AllowedMove((self.position.X, self.position.Y),
                                 (self.position.X + moveX, self.position.Y ),
                                 0,[])):
                    moveY = 0
                    goodMove = 1
        else:
            goodMove = 1

        if (not goodMove):
            return

        self.SetMovement(moveX,moveY)
        

                        
                                 
    def CastSpell(self,pcPlayer):
        print "Zot! Casting spell!"
        self.magicPoints -= 3
        return


        


    def HuntPlayer(self,map,PCPlayer):
        # If player is in a different room, only pursue
        # Fake it...

        if (random.randint(1,6)>1):
            return            
        
        room = map.FindRoom(self.position.roomID)
        # Go through list of portals. Is one connected to this room?
        portalTuple = room.FindPortalToRoom(PCPlayer.PC.position.roomID)

        # If there's no way to get there from here, give up.        
        if (portalTuple == None):
            self.Deactivate()
            self.attitude = 0            
            return

        # Poof this guy over here.
        tempPosX = portalTuple[0].startPosition[0]
        tempPosY = portalTuple[0].startPosition[1]
        try:
            if (portalTuple[0].orientation==0):
                tempPosX += portalTuple[1].startPosition + random.randint(0,portalTuple[1].size-1)
            else:
                tempPosY += portalTuple[1].startPosition + random.randint(0,portalTuple[1].size-1)
        except:
            if (portalTuple[0].orientation==0):
                tempPosX += portalTuple[1].startPosition
            else:
                tempPosY += portalTuple[1].startPosition
            

        tempPosX = tempPosX - portalTuple[1].destination[2]
        tempPosY = tempPosY - portalTuple[1].destination[3]

        self.position.MoveToRoom( PCPlayer.PC.position.roomID )
        self.position.X = tempPosX
        self.position.Y = tempPosY
        
        
        

            
                
    def Wander(self,map):
        if (random.randint(1,4)>1):
            return            
        
        room = map.FindRoom(self.position.roomID)
        moveX = random.randint(0,2)-1
        moveY = random.randint(0,2)-1

        if (self.position.X == 1) and (moveX<0):
            moveX = 1
        if (self.position.X == room.width-2) and (moveX > 0):
            moveX = -1
        if (self.position.Y == 1) and (moveY < 0):
            moveY = 1
        if (self.position.Y == room.height-2) and (moveY > 0):
            moveY = -1

        if (moveX == 0) and (moveY == 0):
            return
        if (not(room.AllowedMove((self.position.X, self.position.Y),
                                 (self.position.X + moveX, self.position.Y + moveY),
                                 0,[]))):
            return
        self.position.X += moveX
        self.position.Y += moveY
        
                
                


    def AIRunAI(self,map,PCPlayer):
        # Return 0 if we can't do anything
        if (self.inactive):
            return 0
        
        # Ignore the player if we're friendly...  Pass our turn
        if (self.attitude>0):
            self.Wander(map)
            return 1


        
        # In different rooms? Ignore IF we're not in angry mode
        bSameRoom = 1
        if (not (PCPlayer.PC.position.roomID==self.position.roomID)):
            bSameRoom = 0
        if (self.attitude>=0) and (not(bSameRoom)):
            self.Wander(map)
            return 0


        # Are we close enough to attack ?
        bCanAttack = 0
        bCanCastSpell = 0
        magicSkill = self.Attributes.GetSkill("Magic")
        combatSkill = self.Attributes.GetSkill("Combat")
                
        offsetX = PCPlayer.PC.position.X - self.position.X 
        offsetY = PCPlayer.PC.position.Y - self.position.Y
        if (bSameRoom) and (abs(offsetX)<=1) and (abs(offsetY)<=1):            
            bCanAttack = 1
 
        if (bSameRoom) and (magicSkill>0) and (self.magicPoints>0):
            bCanCastSpell = 1

        # If We CAN cast spells and PREFER it, do it.
        if (magicSkill>combatSkill) and (bCanCastSpell):
            self.CastSpell(PCPlayer)

        if (combatSkill>magicSkill) and (bCanAttack):
            PCPlayer.BeAttacked(self)
            return 1

        # Okay, we can't get what we want...
        if (bCanAttack):
            PCPlayer.BeAttacked(self)
            return 1

        if (bCanCastSpell):
            self.CastSpell(PCPlayer)
            return 1

        # Okay, we can't cast or attack, so we take action...

        # If we aren't angry, and the player is too far away, just hang out.        
        if (self.attitude==0) and ((not bSameRoom) or (abs(offsetX)>6) or abs(offsetY)>6):
            self.Wander(map)
            return 0

        if (not bSameRoom) and (self.attitude<0):
            self.HuntPlayer(map, PCPlayer)
            return 1

        if (bSameRoom):
            self.ChasePlayer(map,PCPlayer,offsetX,offsetY)
            return 1

        # Okay - I guess we're doing nothing
        self.Wander()
        
        # If the player is in another room, we're probably gonna go inactive soon.
        if not (bSameRoom):
            if random.randint(0,2)==0:
                self.Deactivate()
        return 0
                

        
        

    def RespondToMenu(self, menuID, PCObject, interactionString):
        if (interactionString == "Attack"):
            self.BeAttacked(PCObject)
            return 1
        if (interactionString == "Negotiate"):
            self.NegotiateBribe(PCObject)
            return 0
        if (interactionString == "Cast Spell"):
            PCObject.CastSpellAtMenu(self)
            return 0
        if (menuID==1):
            self.GetBribed(PCObject,interactionString)
            return 1
        if (menuID==2):
            # Cast Spell At Me
            self.GetSpellCastAtMe(PCObject,interactionString)
            return 1
    
        return 0    
        


def GenerateMonster(monsterType, monsterLevel, roomNumber):
    critter = Monster()
   
    critter.position.SetPosition(2,2)
    critter.position.MoveToRoom(roomNumber)

    # Ignore monsterType and level for now
    
    critter.SetGraphics("monsters1",1)
    critter.name = "Red-Eyed Goblin"
    critter.description = ["Red-Eyed Goblins are known for their red eyes,",
                           "their attention to detail, and their almost",
                           "infinite capacity for alcohol."]


    #item = Item.Item()
    #item.Assign("+1 Sword")
    item = Item.CreateRandomEquipmentItem(2)
    item.SetPosition(5,4)
    critter.contents.append(item)
    
    return critter

MonsterAdjectives = ["Hairy","Red-Eye","Bat-Winged","Giant","Bow-Legged","Tusked","Slack-Jawed",
                     "Purple-Crested","Silver-Maned","Double-Jointed","Snaggle-Toothed",
                     "Odiferous","Horn-Tailed","Pot-Bellied","Ham-Fisted","Long-Tailed",
                     "Extra-Crunchy","Southpaw","Rancid","Spotted","Horned"]

def GenerateRandomMonster(monsterLevel):
    critter = Monster()
    critter.SetGraphics("monsters1",1)
    critter.name = MonsterAdjectives[random.randint(0,len(MonsterAdjectives)-1)]+" Goblin"
    critter.description= ["The goblins will gitcha if you don't watch out!"]

    critter.Attributes.Skills["Combat"] = monsterLevel

    for x in range(0,monsterLevel):
        critter.Attributes.Stats[random.randint(0,4)] += 1
        skill = random.randint(0,2)
        if (skill==0):
            critter.Attributes.IncreaseSkill("Search",1)
        elif (skill==1):
            critter.Attributes.IncreaseSkill("Negotiate",1)
        else:
            critter.Attributes.IncreaseSkill("Magic defense",1)
                             
    #adjust monsterlevel
    if (monsterLevel<1):
        monsterLevel = 1

    # Does the monster get gear?
    if (random.randint(0,2)>0):
        # 3 in 4 it just has treasure
        if (random.randint(0,3)<3):
            item = Item.Item()
            item.Assign("Treasure")
            item.quantity = random.randint(1,monsterLevel*25) + random.randint(1,monsterLevel*25)
            item.SetPosition(5,4)
            critter.contents.append(item)
        elif (random.randint(0,2)<2):  #66% of the rest are POTIONS
            item = Item.Item()
            if (random.randint(0,1)==1):
                item.Assign("Potion of Healing")
            else:
                item.Assign("Potion of Essence")
                item.quantity = random.randint(1,3)
            item.SetPosition(5,4)
            critter.contents.append(item)            
        else:            
            item = Item.CreateRandomEquipmentItem(monsterLevel)
            item.quantity = 1
            item.SetPosition(2,2)
            critter.contents.append(item)
            
    return critter            
    
    
    

        