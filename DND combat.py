# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 21:17:36 2023

@author: bendc
"""
import random


class character(object):
    def __init__(self, name, health, weapons, AC, attack_mod, isplayer):
        self.name = name
        self.health = int(health)
        self.weapons = weapons 
        self.AC = int(AC)
        self.attack_mod = int(attack_mod) #Just str or dex mod plus proficiency bonus
        self.isplayer = bool(isplayer)

Ur = character('Ur', 50, {"Mace" : '1d6', "Maul" : '2d6'}, 14, 7, True)
Test = character("Test", 50, {"Mace" : '1d6', "Maul" : '2d6'}, 14, 7, False)
Test2 = character("Test2", 50, {"Mace" : '1d6', "Maul" : '2d6'}, 14, 7, False)

def roll(dice, crit):
    total = 0
    values = dice.partition("d")
    rolls = int(values[0])
    dice_type = int(values[2])
    
    if crit == True:
        total = rolls * dice_type
    
    else:
        for i in range(rolls):
            total += random.randint(1, dice_type)
    
    return total

def combat(attacker, defender):
    crit = False
    available_weapons = list(attacker.weapons.keys())
    print("Weapons available are", available_weapons) #Later: find some way that this displays as string, not list
    print("What weapon does", attacker.name, "attack with?")
    current_weapon = input()
    to_hit = random.randint(1,20) + attacker.attack_mod 
    print("Roll to hit:", to_hit)
    if to_hit <= defender.AC:
        print("The attack misses!")
    else:
        if to_hit - attacker.attack_mod == 20:
            print("Critical hit!")
            crit = True
        damage = roll(attacker.weapons[current_weapon], crit) + attacker.attack_mod - 3 #Just subtracting the proficiency bonus to get str mod
        defender.health -= damage
        print("The attack hits!")
        print("The attack does", damage, "damage")
        print(defender.name, "has", defender.health, "health remaining")
        
    return defender.health

def initiative(combatants):
    initiatives = {}
    order = []
    for i in combatants:
        initiatives.update({i : random.randint(1,20)})
    
    initiatives = dict(sorted(initiatives.items(), key = lambda x:x[1]))
    order = list(initiatives.keys())
    
    return order #Returns ordered list of character objects, but not necessarily their names


combatants = [Ur, Test, Test2]

def encounter(combatants):
    enemies = []
    party = []
    for i in combatants:
        if i.isplayer:
            party.append(i)
        else:
            enemies.append(i)
    
    enemy_names = [enemy.name for enemy in enemies]
    party_names = [party.name for party in party]
    
    print("Members of your party:", (party_names))
    print("Enemies you are facing:", (enemy_names))
    
    initiative_order = initiative(combatants)
    ordered_names = [character.name for character in initiative_order]

    print("Turns will progress in this order:", ordered_names)
    
    enemy_health = sum(enemy.health for enemy in enemies)
    party_health = sum(party.health for party in party)

    counter = 0
    while party_health > 0 and enemy_health > 0:
        
        if counter >= len(combatants):
            counter = counter % len(combatants)
            
        current_player = initiative_order[counter]
        print("Current player is", ordered_names[counter])
        
        if current_player in party:
            options = enemy_names
        else:
            options = party_names
        
        print("Current options for attack are", options)
        target = input("Who will you attack? ")
        if target in options:
            for i in initiative_order:
                if i.name == target:
                    defender = i
        else:
            print("Please choose a valid target") #Need to figure out how to return to target input
        combat(current_player, defender)
        counter += 1
        enemy_health = 0
        party_health = 0
        
        enemy_health = sum(enemy.health for enemy in enemies)
        party_health = sum(party.health for party in party)

encounter(combatants)



