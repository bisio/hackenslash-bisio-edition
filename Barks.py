# Barks.PY
#
# Little comments / words that appear and float up over a character
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

import jtext
import pygame


class Bark:
    def __init__(self):
        # Image: Our graphic
        self.baseImage = None
        self.rotatedImage = None
        

        # mountedObject: The object we're following around        
        self.mountedObject = None

        # Spin
        self.spin = 0
        self.angle = 0
        self.stopAngle = 0
        self.duration = 0  # Duration = 0 means it lasts until we tell you to stop
        self.curTime = 0

        # Scale change
        self.scaleStart = 1
        self.scaleDelta = 0
        self.scaleEnd = 1
        self.curScale = 0

        # Translate
        self.movement = [0,0]
        self.offsetPosition = [0,0]
        self.basePosition = [0,0]
        self.color = (255,255,255,255)

        self.centered = (0,0)
        self.drawPosition = (0,0)
        self.useRotated = 0

        # Don't do color changes for now (expensive!)
        

    def Create(self, strMessage, posX, posY, color = (255,255,255,255)):
        self.baseImage = jtext.GetMessageSprite(strMessage,color)
        self.basePosition = [posX,posY]

    def SetScaleFactor(self, startScale, endScale, timeToChange):
        self.scaleStart = startScale
        self.curScale = startScale
        self.scaleEnd = endScale
        self.scaleDelta = (endScale - startScale) / timeToChange


    def SetCentered(self,centerX, centerY):
        self.centered = (centerX,centerY)

    def Spin(self, angle, maxAngle=0):
        self.spin = angle
        self.stopAngle = maxAngle
        if not (angle == 0):
            self.centered = (1, 1)
        
    def Expired(self):
        if (self.duration <= 0):
            return 0
        if (self.curTime > self.duration):
            return 1
        return 0

    def Update(self, timeDelta):
        "Animates the bark."

        if (self.duration > 0):
            self.curTime += timeDelta
        
        # Don't update if we don't have a message yet
        if (self.baseImage == None):
            return
        
        if (not self.spin == 0) or (not self.scaleDelta == 0):
            self.angle += self.spin * timeDelta

            if not (self.stopAngle == 0):            
                if ((self.spin > 0) and (self.angle > self.stopAngle)):
                    self.angle = self.stopAngle
                elif ((self.spin < 0) and (self.angle < self.stopAngle)):
                    self.angle = self.stopAngle                           

            
            self.curScale += self.scaleDelta * timeDelta
            if (self.scaleDelta>0):
                if (self.curScale > self.scaleEnd):
                    self.curScale = self.scaleEnd
                elif (self.scaleDelta < 0):
                    self.curScale = self.scaleEnd
            self.rotatedImage = pygame.transform.rotozoom(self.baseImage,
                                                          self.angle, self.curScale)
            self.useRotated = 1
        else:
            self.useRotated = 0

        self.offsetPosition[0] += self.movement[0] * timeDelta
        self.offsetPosition[1] += self.movement[1] * timeDelta

        self.drawPosition = [self.offsetPosition[0] + self.basePosition[0],
                        self.offsetPosition[1] + self.basePosition[1]]        

        if not (self.mountedObject == None):
            self.drawPosition = [self.drawPosition[0]+mountedObject.Position().X,
                                 self.drawPosition[1]+mountedObject.Position().Y]

        if (self.centered[0]):
            if (self.useRotated):
                self.drawPosition[0] -= self.rotatedImage.get_width() * 0.5
            else:
                self.drawPosition[0] -= self.baseImage.get_width() * 0.5

        if (self.centered[1]):
            if (self.useRotated):
                self.drawPosition[1] -= self.rotatedImage.get_height() * 0.5
            else:
                self.drawPosition[1] -= self.baseImage.get_height() * 0.5


    def Draw(self,screen):
        if (self.useRotated):
            screen.blit(self.rotatedImage,(self.drawPosition[0],self.drawPosition[1]))
        else:
            if not (self.baseImage == None):
                screen.blit(self.baseImage,(self.drawPosition[0],self.drawPosition[1]))

                
        
        
BarkList = []

def AddBark(newBark):
    BarkList.append(newBark)
    

def RemoveBark(remBark):
    BarkList.remove(remBark)
    

def UpdateBarks(timeDelta):
    killList = []
    for x in BarkList:
        #try:
        x.Update(timeDelta)
        if (x.Expired()):
            killList.append(x)
        #except:
        #    print "Got an illegal bark entry %s / %s"%(str(x),str(ex))

    # Get rid of expired barks
    for x in killList:
        RemoveBark(x)
        

            

def DisplayBarks(screen):
    for x in BarkList:
        try:
            x.Draw(screen)
        except:
            print "Got an illegal bark entry %s"%(str(x))


def ResetBarks():
    BarkList = []



def CreateFloatingBark(strMessage, posX, posY):
    myBark = Bark()
    myBark.Create(strMessage, posX, posY)
    myBark.movement = [0,-30]
    myBark.duration = 2.0
    AddBark(myBark)
    
    
    

        
                
                
                

                
            
            
            
                        
        
        

                
        
                
        

