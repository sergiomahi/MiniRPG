import random
import math
from .magic import Spell

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items, is_enemy):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkh = atk + 10
        self.atkl = atk - 10
        self.df = df
        self.magic = magic
        self.actions = ["Attack", "Magic", "Items"]
        self.items = items
        self.is_enemy = is_enemy
    
    
    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)
    

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp
    
    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost
        if self.mp < 0:
            self.mp = 0

    def heal(self, points):
        if self.hp + points > self.maxhp:
            self.hp = self.maxhp
        else:
            self.hp += points 

    def choose_action(self):
        i = 1
        print("\nActions")
        for item in self.actions:
            print("    {} {}".format(i,item))
            i += 1
    
    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "Magic" + bcolors.ENDC)
        for spell in self.magic:
            print("    {} {} (cost: {})".format(i, spell.name, spell.cost))
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "Items" + bcolors.ENDC)
        for it in self.items:
            print("    {} {} : {} x({})".format(i, it["item"].name, it["item"].description, it["quantity"]))
            i += 1


    def create_dynamic_spaced_bar(self, value, maxvalue, lenth):
        bar_ticks = math.ceil((value / maxvalue) * lenth)
        bar = ""

        while (bar_ticks > 0):
            bar += "█"
            bar_ticks -= 1
        
        while (len(bar) < lenth):
            bar += " "
        return bar

    def get_enemy_stats(self):
        num_bars = 50
        hp_bar = self.create_dynamic_spaced_bar(self.hp, self.maxhp, num_bars)
        white_spaces = " "*21 
        under_scores =  "_"*num_bars

        print(" {}".format(white_spaces + under_scores))
        print("{:6} {:5}/{:5}   |{}{}{}|".format(self.name, self.hp, self.maxhp, bcolors.FAIL, hp_bar, bcolors.ENDC))


    def get_hp_bar(self):
        num_bars = 10
        hp_bar = self.create_dynamic_spaced_bar(self.hp, self.maxhp, num_bars)
        return (" HP: {:5}/{:5}  |{}|".format(self.hp, self.maxhp, hp_bar))

    def get_mp_bar(self):
        num_bars = 5
        mp_bar = self.create_dynamic_spaced_bar(self.mp, self.maxmp, num_bars)
        return (" MP: {:5}/{:5}      |{}|".format(self.mp, self.maxmp, mp_bar))



    def get_stats(self):

        hp_bar = self.create_dynamic_spaced_bar(self.hp, self.maxhp, 25)
        mp_bar = self.create_dynamic_spaced_bar(self.mp, self.maxmp, 10)

        print("                       _________________________                __________")
        print("{} {:6}  {:4}/{} {}   |{}{}{}|     {}/{}    |{}{}{}|".format(bcolors.BOLD, self.name, self.hp, self.maxhp, bcolors.ENDC, bcolors.OKGREEN, hp_bar, bcolors.ENDC, self.mp, self.maxmp, bcolors.OKBLUE, mp_bar, bcolors.ENDC))

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "Enemies" + bcolors.ENDC)
        for enemy in enemies:
            print("    {} {} ".format(i, enemy.name))
            i += 1
        
        enemy_choice = int(input("Choose enemy:")) - 1
        
        return enemies[enemy_choice]

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        enemy_dmg = spell.generate_damage()
        
        HEAL_SPELL_NAME = "white"
        LOW_HP = 0.5
        enemy_hp_percentage = self.get_hp() / self.get_max_hp()

        if self.mp <= spell.cost or spell.type == HEAL_SPELL_NAME and enemy_hp_percentage < LOW_HP:
            self.choose_enemy_spell()
        
        return spell, enemy_dmg

    def get_is_enemy(self):
        return self.is_enemy

    def is_dead(self):
        if self.hp == 0:
            return True
        return False

    def check_mp(self, spell):
        if self.mp >= spell.cost:
            return True
        return False
