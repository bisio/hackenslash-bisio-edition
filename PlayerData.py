# Player Information

import PlayerCharacter
import pygame
import jtext
import Attributes
import Menu
import dice
import Barks
import TextBox
import random



def LoadPlayerGraphics(graphicsData):
    graphicsData.LoadTexture("player0","art\\player.png")
    for i in range(1,8):
        graphicsData.AssignTexture("player"+str(i),pygame.transform.rotate(graphicsData.textures["player0"][0],45*i))

    


class PlayerData:
    def __init__(self):
        self.PC = PlayerCharacter.PlayerCharacter()
        self.screenPosX = 0
        self.screenPosY = 0
        self.facing = 0
        self.movement = (0,0)
        self.moveOffset = 0
        self.StatWindow = None
        self.map = None
        self.TookItem = 0
        self.PC.LevelupFlag = 0
        self.WanderingMonsterFlag = 0
        self.RestFlag = 1

    def SetInitialGamePosition(self):
        self.PC.SetPosition(6,6)
        self.PC.position.roomID = 1


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
        self.map = map
        if self.IsSettled():
            return
        self.moveOffset += speed
        
        if (self.moveOffset >= 1):
            if not (self.HandlePortalledMovement(map)):            
                self.PC.position.X += self.movement[0]
                self.PC.position.Y += self.movement[1]
                self.HandleSpecialEffectOnMove(map)
            self.movement = (0,0)
            self.moveOffset = 0
            

    def StartMove(self, moveX, moveY):
        if not self.IsSettled():
            return 0
        self.movement = (moveX,moveY)
        self.SetFacingFromMovement((moveX,moveY))

        
        
    def HandleSpecialEffectOnMove(self, map):
        "If the player walked into a feature that has a special effect, activate it now."
        room = map.FindRoom(self.PC.position.roomID)

        featureList = room.GetFeatureBlockAtPosition(self.PC.position.X, self.PC.position.Y)
        if (len(featureList)<1):
            return 0
        if (featureList[0][0]=='tport'):
            tportRoom = featureList[0][1][0]
            tportXOff = featureList[0][1][1]
            tportYOff = featureList[0][1][2]
            self.PC.position.X += tportXOff
            self.PC.position.Y += tportYOff
            self.PC.position.MoveToRoom(tportRoom)
        return 1


    def Rest(self):
        self.RestFlag = 1
        self.PC.Heal(500)
        self.PC.RegainMagic(500)
        self.PC.spellEffects = []
        
    

    def GetRoomOffset(self, wallSize):
        halfWallSize = (wallSize * 0.5) + 0.5
        partialPosX = 0
        partialPosY = 0
        if (self.moveOffset > 0):
            partialPosX = self.moveOffset * self.movement[0]
            partialPosY = self.moveOffset * self.movement[1]

        roomPosX = int((self.PC.position.X + partialPosX) * wallSize + halfWallSize )
        roomPosY = int((self.PC.position.Y + partialPosY) * wallSize + halfWallSize )

        offsetX = self.screenPosX - roomPosX
        offsetY = self.screenPosY - roomPosY

        return (offsetX, offsetY)     


    def HandlePortalledMovement(self, map):
        "Handle any movement that transitions via portal."
        # Pre-calculate the player's new position
        adjustedPositionX = self.PC.position.X + self.movement[0]
        adjustedPositionY = self.PC.position.Y + self.movement[1]

        # is the new position outside the bounds of the room? If not, return 0 - no portalling necessary
        room = map.FindRoom(self.PC.position.roomID)
        if ((adjustedPositionX >= 0) and (adjustedPositionY >= 0) and
            (adjustedPositionX < room.width) and (adjustedPositionY < room.height)):
                return 0

        # Get the player's portal
        portal = room.GetPortal(self.PC.position.X, self.PC.position.Y)
        if (portal==None):
            return 0  # This will "bounce" the player back to his previous position. Oh, well. He shouldn't be moving here anyway!

        # Transport the player to a new offset based on the portal
        self.PC.position.X += self.movement[0] - portal.destination[2]
        self.PC.position.Y += self.movement[1] - portal.destination[3]
        self.PC.position.MoveToRoom(portal.destination[1])
        self.PC.position.PutInContainer(portal.destination[0],0)

        # Now tell the caller that we've already handled the movement        
        return 1
        
        

    def GetPlayerRoom(self):
        return self.PC.position.roomID
    

    def SetScreenPosition(self, posX, posY):
        self.screenPosX = posX
        self.screenPosY = posY

    def SetFacingDirect(self,dir):
        self.facing = dir%8

    def SetFacingFromMovement(self,tDir):
        if (tDir[0] == 1):
            self.facing = 6 - tDir[1]  # Somewhere East-y
        elif (tDir[0] == -1):
            self.facing = 2 + tDir[1]  # Somewhere West-y
        else:
            if (tDir[1]==-1):
                self.facing = 0 # North
            elif (tDir[1]==1):
                self.facing = 4 # South
            # If none of the above: No change in direction




    def GetOffense(self):
        baseOffense = self.PC.GetOffense()
        return baseOffense

    def GetDefense(self):
        baseDefense = self.PC.GetDefense()
        return baseDefense

    def GetArmor(self):
        return self.PC.GetArmor()
    
    def GetDamage(self):
        return 8

    def TakeDamage(self,damage):
        self.PC.hitpoints -= damage
        self.PC.statChange =1

    def IsDead(self):
        if (self.PC.hitpoints<1):
            return 1
        return 0


    def GetBonusForAction(self,action):
        bonus = 0
        for x in self.PC.Equipment.keys():
            item = self.PC.Equipment[x]
            if not (item==None):
                if item.itemType.effects.has_key(action):
                    bonus += item.itemType.effects[action]

        for x in self.PC.spellEffects:
            if (x[0]=="buff") or (x[0]=="curse") or (x[0]==action):
                bonus += x[1]
        return bonus
                    

    def GiveXP(self, XPAmount):
        self.PC.GainExperience(XPAmount)



    def BeAttacked(self,attacker):
        armor = self.GetArmor() + self.GetBonusForAction("armor")
        defense = self.GetDefense() + self.GetBonusForAction("defend")
        offense = attacker.GetOffense() + attacker.GetBonusForAction("attack")
        damage = attacker.GetDamage() + attacker.GetBonusForAction("damage")
        attackerVert = attacker.position.Y

        if (attackerVert == self.PC.position.Y):
            offsetY = 32
        else:
            offsetY = -16

        TextBox.MainText.AddText("%s (atk %d) attacks player (def %d)"%(attacker.name,offense,defense))

        if (dice.StandardRoll(offense,defense)==0):
            Barks.CreateFloatingBark("%s misses player!"%attacker.name,self.screenPosX - 128,self.screenPosY + offsetY)
            TextBox.MainText.AddText("%s misses!"%attacker.name)            
            return


        realDamage = dice.DamageRoll(damage,armor)
        TextBox.MainText.AddText("Damage %d vs. armor %d"%(damage, armor))            
        if (realDamage<1):
            Barks.CreateFloatingBark("Player's Armor Resists Damage!",self.screenPosX - 128,self.screenPosY + offsetY)
            TextBox.MainText.AddText("Attack does no damage!")            
            return

        Barks.CreateFloatingBark("%s hits Player for %d!"%(attacker.name,realDamage),self.screenPosX - 128,self.screenPosY + offsetY)
        TextBox.MainText.AddText("Player takes %d damage"%(realDamage))            
        self.TakeDamage(realDamage)
 
        return  



    def Display(self,displayInfo, graphicsData):        
        playerAnimData = graphicsData.textures["player"+str(self.facing)]
        tempPlayerSurface = playerAnimData[0]
        halfsizeX = tempPlayerSurface.get_rect().right / 2
        halfsizeY = tempPlayerSurface.get_rect().bottom / 2
        displayInfo.GetScreen().blit(tempPlayerSurface,(self.screenPosX - halfsizeX,self.screenPosY - halfsizeY))

        # Attribute window
        window = pygame.rect.Rect((displayInfo.GetScreenWidth()*3/4)-1,0,
                                  displayInfo.GetScreenWidth()/4 - 1,displayInfo.GetScreenHeight()/3-1)
        tempwindow = pygame.rect.Rect(0,0,window.width-1,window.height)
        window.width +=1
        window.height +=1
        
        if (self.StatWindow==None):
            self.StatWindow = pygame.Surface((window.width,window.height))          
        
       
        self.DisplayStats(self.StatWindow,tempwindow)
        displayInfo.GetScreen().blit(self.StatWindow,(window.left,window.top)) 
           



    def DisplayStats(self,surface,rect):
        if not (self.PC.statChange):
            return
            
        self.PC.FlagStatChange(0)

        # Draw Background
        pygame.draw.polygon(surface,(16,16,48),
                            [(rect.left,rect.top),(rect.right, rect.top),
                            (rect.right,rect.bottom), (rect.left, rect.bottom)])

        # Draw Rectangle behind the attributes      
        pygame.draw.polygon(surface,(64,64,96),
                            [(rect.left+1,rect.top+17),(rect.right-1, rect.top+17),
                            (rect.right-1,rect.top+54), (rect.left+1, rect.top+54)])

        # Frame it all        
        pygame.draw.polygon(surface,(199,176,0),
                            [(rect.left,rect.top),(rect.right, rect.top),
                            (rect.right,rect.bottom), (rect.left, rect.bottom)],
                            1)

        # Draw Stats        
        
        posX = 2
        posY = 1
        pcAttributes = self.PC.Attributes        
        jtext.PrintTextAt(self.PC.name,surface,
                          rect.left + posX, rect.top + posY,(255,255,255))
        posY = 17
        
        
        for attribute in Attributes.AttributeNames:            
            jtext.PrintSmallTextAt("%s: %d"%(attribute,pcAttributes.GetAttribute(attribute)),
                                   surface,
                                   rect.left+posX,rect.top + posY,(255,255,255))
            posY += 12
            if (posY >= 52):
                posY = 17
                posX += rect.width/2

        posY = 36 + 18
        posX = 2
        jtext.PrintTextAt("Hit Points: %d / %d"%( self.PC.GetCurrentHitPoints(), self.PC.GetMaxHitPoints()),
                          surface,
                          rect.left + posX, rect.top + posY,(255,255,255))
        posY += 16
        jtext.PrintTextAt("Magic Points: %d / %d"%(self.PC.GetCurrentMagicPoints(), self.PC.GetMaxMagicPoints()),
                          surface,
                          rect.left + posX, rect.top + posY,(255,255,255))

        posY += 16
        jtext.PrintTextAt("Attack: %d"%(pcAttributes.GetAttribute("Strength")+pcAttributes.GetSkill("combat")),
                          surface,
                          rect.left + posX, rect.top + posY,(255,255,255))
        posY += 16
        jtext.PrintTextAt("Defense: %d"%(pcAttributes.GetAttribute("Agility")+pcAttributes.GetSkill("combat")),
                          surface,
                          rect.left + posX, rect.top + posY,(255,255,255))
        posY += 16
        jtext.PrintTextAt("Armor: %d"%(self.PC.GetArmor()),
                          surface,
                          rect.left + posX, rect.top + posY,(255,255,255))

        posY += 16
        jtext.PrintTextAt("Experience: %d"%(self.PC.GetExperience()),
                          surface,
                          rect.left + posX, rect.top + posY,(255,255,255))           
        
        posY += 16
        jtext.PrintTextAt("Silver: %d"%(self.PC.GetMoney()),
                          surface,
                          rect.left + posX, rect.top + posY,(255,255,255))                            
                          

    def SetMainInventoryOptions(self,menu):
        for x in self.PC.Equipment.keys():
            if not (self.PC.Equipment[x]==None):
                menu.MenuOptions.append("%s: %s"%(x,self.PC.Equipment[x].itemType.name))
        

    def GetSkillsList(self,menu):
        skillStr = ""
        for x in Attributes.SkillNames:
            bFlush = 0
            if (len(skillStr)>1):
                skillStr += "   "
                bFlush = 1
            skillStr += x+": "+str(self.PC.Attributes.GetSkill(x))
            if (bFlush):
                menu.AddMessage(skillStr)
                skillStr = ""
        if len(skillStr)>1:
            menu.AddMessage(skillStr)
            
            
            


    def InsertItemMenuDescription(self,menu,itemString):
        try:
            slotname = itemString.split(':')[0]
            item = self.PC.Equipment[slotname]
            menu.Title = item.itemType.name
            desc = item.GetItemDetails()
            for x in desc:
                menu.AddMessage(x)
            
            
        except:
            menu.Title = "Unknown Item"
            menu.AddMessage("No item found for slot matching the string:")
            menu.AddMessage(itemString)
            


    def CastSpellAtMenu(self, monster):
        # Keep track of who our target was
        self.monsterTarget = monster
        menu = Menu.Menu()
        menu.Title = "Cast Spell At %s"%monster.name
        menu.type = "monster"
        menu.menuID = 2
        menu.object = monster
        casterLevel = self.PC.Attributes.GetSkill("Magic")
        spellLevelsAvailable = 1 + casterLevel/3
        if (spellLevelsAvailable>4):
            spellLevelsAvailable = 4
        menu.menuOptions = []
        for x in range(1,spellLevelsAvailable+1):
            menu.MenuOptions.append("Bolt %d"%x)
        for x in range(1,spellLevelsAvailable+1):
            menu.MenuOptions.append("Curse %d"%x)
        menu.SetPosition(self.screenPosX + 16, self.screenPosY - 16)                 
        menu.ResizeForBestFit()            
        Menu.MasterMenu.AddMenu(menu)


        
    def GetPlayerSpellMenuOptions(self):
        casterLevel = self.PC.Attributes.GetSkill("Magic")
        spellLevelsAvailable = 1 + casterLevel/3
        if (spellLevelsAvailable>4):
            spellLevelsAvailable = 4
        menuOptions = []
        for x in range(1,spellLevelsAvailable+1):
            menuOptions.append("Cure %d"%x)
        for x in range(1,spellLevelsAvailable+1):
            menuOptions.append("Buff %d"%x)        
        for x in range(1,spellLevelsAvailable+1):
            menuOptions.append("Armor %d"%x)
        return menuOptions
        

        

    def MakeMenu(self, menuType=0):
        menu = Menu.Menu()
        menu.Title = "Player"
        menu.type = "player"
        menu.menuID = menuType
        menu.object = self
        if (menuType==0):
            menu.MenuOptions = ["Inventory","Use Potion","Cast Spell","See Skills","Pass"]
            if (self.PC.LevelupFlag):
                menu.MenuOptions.append("Level Up!")
            try:
                room = self.map.FindRoom(self.PC.position.roomID)
                if (room.safeRoom):
                    menu.MenuOptions.insert(0,"Rest")
            except:
                pass
            menu.MenuOptions.append("Main Menu")
        elif (menuType==1):
            # Potion menu
            potionList = self.PC.GetAllPotions()
            menu.MenuOptions = []
            for x in potionList.keys():
                if potionList[x]>0:
                    menu.MenuOptions.append(x)            
        elif (menuType==2):
            # Spell menu
            menu.MenuOptions = self.GetPlayerSpellMenuOptions()
        elif (menuType==3):
            # Inventory Menu # 1
            menu.MenuOptions = []
            self.SetMainInventoryOptions(menu)
            #menu.AddMessage("Weapon: Sword")
            menu.MenuOptions.append("View Potions")
        elif (menuType==4):
            potionList = self.PC.GetAllPotions()
            menu.MenuOptions = []
            for x in potionList.keys():
                if potionList[x]>0:
                    menu.AddMessage("Potion of %s: %d"%(x,potionList[x]))
            if len(menu.msgText)<1:
                menu.AddMessage("No potions.")
            menu.MenuOptions = ["View Equipment"]
        elif (menuType==5):
            menu.MenuOptions=["View Equipment","View Potions"]
        elif (menuType==6):
            self.GetSkillsList(menu)
            self.MenuOptions = []
        elif (menuType==7) or (menuType==8) or (menuType==9):
            self.WriteLevelUpMenu(menuType,menu)
        menu.SetPosition(self.screenPosX + 16, self.screenPosY - 16)                 
        menu.ResizeForBestFit()            
        return menu        
                
    def AddSpellEffect(self,effectName, effectLevel, effectDuration):
        # Find existing effects of the same name / value
        bExisting = 0
        for x in self.PC.spellEffects:
            if x[0]==effectName:
                bExisting = 1
                if (x[1]>0) and (x[1]<=effectLevel):
                    x[2] = effectDuration
                    x[1] = effectLevel
                elif (x[1]<0) and (x[1]>=effectLevel):
                    x[2] = effectDuration
                    x[1] = effectLevel                    
                    
        if not bExisting:
            self.PC.spellEffects.append([effectName,effectLevel,effectDuration])


    def BlessMe(self, spellLevel):
        if (spellLevel<1):
            spellLevel = 1
        if (spellLevel>4):
            spellLevel = 4
        Barks.CreateFloatingBark("BUFFED +%d!"%spellLevel,self.screenPosX, self.screenPosY)               
        TextBox.MainText.AddText("Player is blessed with good fortune.")            
        duration = 10 + (self.PC.Attributes.GetSkill("magic")+self.GetBonusForAction("magic"))*2
        self.AddSpellEffect('buff',spellLevel,duration)
        

    def MagicArmorMe(self, spellLevel):
        if (spellLevel<1):
            spellLevel = 1
        if (spellLevel>4):
            spellLevel = 4
        Barks.CreateFloatingBark("ARMORED!",self.screenPosX, self.screenPosY)               
        TextBox.MainText.AddText("Player glows with magical armor.")               
        duration = 10 + (self.PC.Attributes.GetSkill("magic")+self.GetBonusForAction("magic"))*2
        self.AddSpellEffect('armor',spellLevel,duration)

    def HealSelf(self,spellLevel):
        if (spellLevel<1):
            spellLevel = 1
        if (spellLevel>4):
            spellLevel = 4
        healBase = 6+(self.PC.Attributes.GetSkill("magic")+self.GetBonusForAction("magic"))*2
        healTotal = 0
        for x in range(0,spellLevel):
            healTotal += dice.DamageRoll(healBase,0)
            
        Barks.CreateFloatingBark("Healed for %d"%healTotal,self.screenPosX, self.screenPosY)               
        TextBox.MainText.AddText("Player heals self for %d."%healTotal)               
        
        self.PC.Heal(healTotal)


    def CastSpellsOnSelf(self, interactionString):
        spellData = interactionString.split(' ')
        spellLevel = int(spellData[1])
        spellCost = (spellLevel*2)-1
        if (spellCost>self.PC.GetCurrentMagicPoints()):
            TextBox.MainText.AddText("Not enough magic points to cast %s"%interactionString)
            Barks.CreateFloatingBark("Not enough magic points!",self.screenPosX, self.screenPosY)               
            return 1
        self.PC.magicpoints -= spellCost
        self.PC.FlagStatChange(1)
        if (spellData[0].lower()=='buff'):
            self.BlessMe(spellLevel)
        elif (spellData[0].lower()=='armor'):
            self.MagicArmorMe(spellLevel)
        else:
            self.HealSelf(spellLevel)        
        return 1


    def HandleLevelUpMenu(self,menuID,interactionString):
        print "Levelup Menu %d"%menuID
        if (menuID==7):
            # Classes
            print "Got Levelupclass = %s"%interactionString
            self.LevelupClass = interactionString
            return
        elif (menuID==8):
            # Skills
            print "Got LevelupSkill = %s"%interactionString
            self.LevelupSkill = interactionString
            return
        else:
            # Ability score...
            self.LevelupAbility = interactionString
            
            # Now cram it all down!
            self.PC.Attributes.IncreaseAttribute(self.LevelupAbility,1)
            self.PC.Attributes.IncreaseSkill(self.LevelupClass,1)
            self.PC.Attributes.IncreaseSkill(self.LevelupSkill,1)
            self.PC.LevelupFlag = 0
            self.PC.Attributes.AdjustLevel()
            self.PC.FlagStatChange(1)

        return            

    def WriteLevelUpMenu(self,menuID, menu):
        if (menuID==7):
            menu.AddMessage("Congratulations! Thou hast Kicked Some Tail")
            menu.AddMessage("and now gaineth a level for Greater Tail Kicking")
            menu.AddMessage("Potential. Pick a class skill to improve:")
            menu.MenuOptions = ["Combat","Magic","Thievery"]
            return
        elif (menuID==8):
            menu.AddMessage("Choose a secondary skill to improve:")
            menu.MenuOptions = []
            for x in Attributes.SkillNames:
                if (not x=="Combat") and (not x=="Magic") and (not x=="Thievery"):
                    menu.MenuOptions.append(x)
            return
        else:
            menu.AddMessage("Almost Done, Thou Heroic Somethingoranother.")
            menu.AddMessage("Chooseth thou some ability to... uh, boosteth.")
            menu.MenuOptions = []
            for x in Attributes.AttributeNames:
                menu.MenuOptions.append(x)
            return
        
    
        
    def RespondToMenu(self, menuID, PCObject, interactionString):
   
        if (interactionString=="Inventory") or (interactionString=="View Equipment"):
            menu = self.MakeMenu(3)
            Menu.MasterMenu.AddMenu(menu)
            return 0
        if (menuID==0) or (menuID == 4):              
            if (interactionString=="Use Potion"):
                menu = self.MakeMenu(1)
                Menu.MasterMenu.AddMenu(menu)
                return 0
            elif (interactionString=="Cast Spell"):
                menu = self.MakeMenu(2)
                Menu.MasterMenu.AddMenu(menu)
                return 0
            elif (interactionString=="See Skills"):
                menu = self.MakeMenu(6)
                Menu.MasterMenu.AddMenu(menu)
                return 0
            elif (interactionString=="Pass"):
                # Skip my turn
                return 1
            elif (interactionString=="Level Up!"):
                menu = self.MakeMenu(7)
                Menu.MasterMenu.AddMenu(menu)
                return 0
            elif (interactionString=="Rest"):
                self.Rest()
                return 1
            return 0
        elif (menuID==3):
            if (interactionString=="View Potions"):
                menu = self.MakeMenu(4)
                Menu.MasterMenu.AddMenu(menu)
                return 0
            # Display specific equipment
            menu = self.MakeMenu(5)
            self.InsertItemMenuDescription(menu,interactionString)
            # It's been modified, so we need to resize it again
            menu.ResizeForBestFit()                        
            Menu.MasterMenu.AddMenu(menu)
            return 0
        elif (menuID==1):
            self.DrinkPotion(interactionString)
            return 1
        elif (menuID==2):
            self.CastSpellsOnSelf(interactionString)
            return 1
        elif (menuID==7) or (menuID==8) or (menuID==9):
            self.HandleLevelUpMenu(menuID,interactionString)
            if (menuID<9):
                menu=self.MakeMenu(menuID+1)
                Menu.MasterMenu.AddMenu(menu)
            return 0


        return 0       


    def TakeItemAsTreasure(self, item):
        if (item.quantity < 1):
            item.quantity = 1
        self.PC.GiveMoney(item.itemType.TreasureValue) * item.quantity
        TextBox.MainText.AddText('Player cashes in %s'%item.itemType.name)
        item.position.PutInContainer(-1)  # Make it clear out of room.
        self.TookItem = 1                                                      
        
          

    def ReplaceItem(self,item, replacementString):
        slotname = replacementString.split(':')[0]
        if (self.PC.ReplaceItem(slotname,item)==0):
            print "Error! Unable to take item %s into slot %s"%(item.itemType.name,slotname)
        else:
            TextBox.MainText.AddText("Player replaces %s with %s"%(replacementString.split(':')[1].strip(),item.itemType.name))
            self.TookItem = 1                                                      
            
            
            
        
        

    def PickUpItem(self,item):
        # Pure Treasure?
        if (item.quantity < 1):
            item.quantity = 1
        if (item.itemType.equipmentType==0):
            TextBox.MainText.AddText("Grabbed %s for %d silver."%(item.itemType.name,
                                                                  item.itemType.TreasureValue * item.quantity))
            self.TookItem = 1                                                      
            self.PC.GiveMoney(item.itemType.TreasureValue * item.quantity)
            return 1
        if (item.itemType.equipmentType==1):
            self.PC.AddPotion(item.itemType.name[10:].capitalize(),item.quantity)
            TextBox.MainText.AddText("Picked up %d %s"%(item.quantity,item.itemType.name))
            self.TookItem = 1                                                                  
            return 1

        # Okay - it's specific equipment. Uh-oh.
        # Step 1 - see if we can replace it in the player's inventory
        val = self.PC.FindEmptyItemSlot(item)
        if (val==1):
            TextBox.MainText.AddText("Player equipped %s"%item.itemType.name)
            self.TookItem = 1                                                                  
            return 1

        # Okay, we SHOULDN'T have gotten the pick-up option! Argh!
        print "Error! Tried to pick up an item without a free slot. Should have gotten a replace option instead."
        
            
        
        
        
                
                
    def DrinkPotion(self,potionName):
        if (not self.PC.potionCount.has_key(potionName)) or (self.PC.potionCount[potionName]<1):
            Barks.CreateFloatingBark("Potion Not Available",self.screenPosX,self.screenPosY)
            return

        self.PC.potionCount[potionName] -=1

        if (potionName=="Healing"):
            TextBox.MainText.AddText("Player drinks a healing potion.")
            self.PC.Heal(self.PC.Attributes.GetAttribute("Health"))
            return
        if (potionName=="Essence"):
            TextBox.MainText.AddText("Player drinks an essence potion.")
            self.PC.RegainMagic(self.PC.Attributes.GetAttribute("Will"))
            return        

            
        
        
        
                



        
        