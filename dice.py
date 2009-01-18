# DICE
#
# Dice-Handling code
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
from random import randint


def StandardRoll(attackerScore,defenderScore):
    if (attackerScore<1): # If the attack rating is 0, the attack always fails
        return 0
    if (defenderScore<1): # Otherwise, automatic success on defense rating of 0
        return 1

    roll = randint(1,attackerScore+defenderScore)
    if (roll>defenderScore):
        return 1
    return 0

def DamageRoll(attackAmount, defenseAmount):
    if (attackAmount<1): # 0 attack rating? No damage will be done
        return 0
    if (defenseAmount < 1): # Man, don’t screw with us with negative numbersrs
        defenseAmount= 0


    total = randint(1,attackAmount + defenseAmount)
    total -= defenseAmount
    if (total<1):
        return 0
    return total


    