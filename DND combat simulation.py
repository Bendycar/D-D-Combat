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
        self.maxhealth = health
        self.weapons = weapons 
        self.AC = int(AC)
        self.attack_mod = int(attack_mod) #Just str or dex mod plus proficiency bonus
        self.isplayer = bool(isplayer)
        
    def reset_health(self):
        self.health = self.maxhealth

def roll(dice, crit):
    total = 0
    values = dice.partition("d")
    rolls = int(values[0])
    dice_type = int(values[2])
    
    if crit:
        total = rolls * dice_type
    
    else:
        for i in range(rolls):
            total += random.randint(1, dice_type)
    
    return total

def combat(attacker, defender):
    to_hit = random.randint(1,20) + attacker.attack_mod 
    if to_hit > defender.AC:
        crit = False
        current_weapon = list(attacker.weapons.keys())[0]
        if to_hit - attacker.attack_mod == 20:
            crit = True
        damage = roll(attacker.weapons[current_weapon], crit) + attacker.attack_mod - 3 #Just subtracting the proficiency bonus to get str/dex mod
        defender.health -= damage

    return defender.health

def initiative(combatants):
    initiatives = {}
    order = []
    for i in combatants:
        initiatives.update({i : random.randint(1,20)})
    
    initiatives = dict(sorted(initiatives.items(), key = lambda x:x[1]))
    order = list(initiatives.keys())
    
    return order #Returns ordered list of character objects, but not necessarily their names

def encounter(combatants):
    enemies = []
    party = []
    for i in combatants:
        if i.isplayer:
            party.append(i)
        else:
            enemies.append(i)
    
    enemy_names = [enemy.name for enemy in enemies]
    party_names = [member.name for member in party]

    initiative_order = initiative(combatants)
    
    enemy_health = sum(enemy.health for enemy in enemies)
    party_health = sum(member.health for member in party)

    counter = 0
    while party_health > 0 and enemy_health > 0:
        
        if counter >= len(combatants):
            counter = counter % len(combatants)
            
        current_player = initiative_order[counter]
        
        if current_player in party:
            options = enemy_names
        else:
            options = party_names
        
        target = random.choice(options)
        for i in initiative_order:
            if i.name == target:
                defender = i

        combat(current_player, defender)
        counter += 1
        
        enemy_health = sum(enemy.health for enemy in enemies)
        party_health = sum(party.health for party in party)

    return party_health

def encounter_sim(combatants, trials):
    party_wins = 0
    enemy_wins = 0  
    for i in range(trials):
        party_health = encounter(combatants)
        #print(party_health)
        if party_health <= 0:
            enemy_wins += 1 
        else:
            party_wins += 1
        
        for i in combatants:
            i.reset_health()
    
    win_percent =(party_wins / trials) * 100
    print("The party will win this encounter", int(win_percent), "percent of the time")
  

Ur = character('Ur', 50, {"Maul" : '2d6'}, 14, 7, True) #All characters in v1 of sim will only have 1 weapon
Test = character("Test", 5, {"Maul" : '2d6'}, 14, 7, False)
Test2 = character("Test2", 5, {"Maul" : '2d6'}, 14, 7, False)
combatants = [Ur, Test, Test2]
    
encounter_sim(combatants, 100)