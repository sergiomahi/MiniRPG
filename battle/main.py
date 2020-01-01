from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random
import sys 

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

class EnemyButton():
    def __init__(self, p):
        self.button = QPushButton(p.name) 
        self.enemy = p
        self.hp_label = QLabel(p.get_hp_bar())
        self.mp_label = QLabel(p.get_mp_bar())

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.button)       
        self.vbox.addWidget(self.hp_label)
        self.vbox.addWidget(self.mp_label)



        #menu = QMenu()
        #menu.addAction(p.get_hp_bar(), self.show_hp)
        #menu.addAction(p.get_mp_bar(), self.show_mp)
        
        #self.button.setMenu(menu)


    def show_hp(self):
        print("HP")
    
    def show_mp(self):
        print("MP")

    def take_damage_if_ready(self):
        self.enemy.take_damage(500)
        self.hp_label.setText(self.enemy.get_hp_bar())
        
        #self.button.setMenu(menu)
    

class Application(QWidget):
    def __init__(self, enemies, players):
        super().__init__()
        self.current_player = players[0]
        self.attack_ready = False

        self.setWindowTitle("RPG")
        self.createApp(enemies, players)

    def createApp(self, enemies, players):
        grid = QGridLayout()
        turn_of = QLabel("Turn of {}".format(self.current_player.name))
        grid.addWidget(turn_of, 0, 0, 1, 3)
        
        
        row = 2
        col = 0
        enemy_buttons = []
        for button in enemies:
            b_object = EnemyButton(button)
            b_object.button.clicked.connect(lambda state, x=b_object: x.take_damage_if_ready())        

            grid.addLayout(b_object.vbox, row, col, 1, 1)

            enemy_buttons.append(b_object)
            row += 1

        row = 2
        col = 3
        for button in players:
            b_object = EnemyButton(button)
            grid.addWidget(b_object.button, row, col, 1, 1)
            row += 1



        self.attack_button = QPushButton("Attackt")
        row += 1
        grid.addWidget(self.attack_button, row, 0, 1, 4 )

        self.attack_button.clicked.connect(self.is_attack_ready)


        self.setLayout(grid)
        self.show()

    

    def is_attack_ready(self):
        if self.attack_ready:
            self.attack_button.setText("Attack")
            self.attack_ready = False
        else:
            self.attack_button.setText("Attack ready!")
            self.attack_ready = True
        

if __name__ == "__main__":

    

    # Create Black Magic

    DMG_SPELL_NAME = "black"
    HEAL_SPELL_NAME = "white"
    fire = Spell("Fire", 10, 100, DMG_SPELL_NAME) 
    thunder = Spell("Thunder", 10, 100, DMG_SPELL_NAME) 
    blizzard = Spell("Blizzard", 10, 100, DMG_SPELL_NAME) 
    meteor = Spell("Meteor", 20, 200, DMG_SPELL_NAME) 
    quake = Spell("Quake", 14, 140, DMG_SPELL_NAME) 

    # Create WHite Magic
    cure = Spell("Cure", 12, 120, HEAL_SPELL_NAME) 
    cura = Spell("Cura", 18, 180, HEAL_SPELL_NAME) 


    # Create some items.
    ITEM_TYPES=["Potion", "Elixir", "Attack", "MegaElixir"]

    potion = Item("Potion", ITEM_TYPES[0], "Heals 50 HP", 50)
    hipotion = Item("Hiper Potion", ITEM_TYPES[0], "Heals 100 HP", 100)
    superpotion = Item("Super Potion", ITEM_TYPES[0], "Heals 500 HP", 500)
    elixir = Item("Elixir", ITEM_TYPES[1], "Fully restores HP/MP of one party member",9999)
    megaelixir = Item("Mega Elixir", ITEM_TYPES[3], "Fully restores party's HP/MP.", 9999)

    grenade = Item("Grenade", ITEM_TYPES[2], "Deals 500 damage", 500)


    PLAYER_SPELLS = [fire, thunder, blizzard, meteor, quake, cure, cura]
    PLAYER_ITEMS = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5}, {"item": superpotion, "quantity": 5}, 
                    {"item": elixir, "quantity": 5}, {"item": megaelixir, "quantity": 5}, {"item": grenade, "quantity": 5}]

    # Instantiate people
    player1 = Person("Valos", 3260, 65, 180, 34, PLAYER_SPELLS, PLAYER_ITEMS)
    player2 = Person("Lyss", 4160, 65, 200, 34, PLAYER_SPELLS, PLAYER_ITEMS)
    player3 = Person("Kay", 3089, 65, 300, 34, PLAYER_SPELLS, PLAYER_ITEMS)
    players = [player1, player2, player3]

    enemy2 = Person("Culo", 1200, 65, 80, 100, PLAYER_SPELLS, PLAYER_ITEMS)
    enemy1 = Person("Javio", 12000, 65, 350, 25, PLAYER_SPELLS, PLAYER_ITEMS)
    enemy3 = Person("Culo", 1200, 65, 80, 100, PLAYER_SPELLS, PLAYER_ITEMS)
    enemies = [enemy2, enemy1, enemy3]

    ######################
    ##
    ##   App initialization
    ##
    ######################
    app = QApplication(sys.argv)

    window = Application(enemies, players)

    sys.exit(app.exec_())


    running = True
    i = 0

    print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

    def print_hp(p, name, color):
        print("{} HP: {} {}/{} {}".format(name, color, p.get_hp(), p.get_max_hp(), bcolors.ENDC))
        
    def print_mp(p, name, color):
        print("{} MP: {} {}/{} {}".format(name, color, p.get_mp(), p.get_max_mp(), bcolors.ENDC))
        

    while (running):
        print("=========================================")
        print("\n\n")
        print("NAME                 HP                                       MP")

        for player in players:
            player.get_stats()
        
        print("\n{}ENEMIES{}\n".format(bcolors.FAIL, bcolors.ENDC))
        print("NAME                 HP                                       MP")
        for enemy in enemies:
            enemy.get_enemy_stats()

        for player in players:
            if player.get_hp() == 0:
                continue

            print("\n\n{}Turn of {}{}{}{}".format(bcolors.BOLD, bcolors.OKBLUE, bcolors.UNDERLINE, player.name, bcolors.ENDC))
            player.choose_action()
            choice = input("Choose action: ")

            real_choice = int(choice) - 1

            if real_choice == 0:
                dmg = player.generate_damage()
                enemy = player.choose_target(enemies)
                enemy.take_damage(dmg)
                print("You attacked {} for {} points of damage.".format(enemy.name, dmg))
                if enemy.get_hp() == 0:  ## Add this as a function.
                    enemies.remove(enemy)
                    print("Enemy {} defeated!".format(enemy.name))


            elif real_choice == 1:
                player.choose_magic()
                magic_choice = int(input("Choose magic:")) - 1

                if magic_choice == -1:
                    continue


                spell = player.magic[magic_choice]
                magic_dmg = spell.generate_damage()

                if spell.cost > player.get_mp():
                    print(bcolors.FAIL + 'Not enough MP!' + bcolors.ENDC)
                    continue

                player.reduce_mp(spell.cost)

                if spell.type == HEAL_SPELL_NAME:
                    allied = player.choose_target(players)
                    allied.heal(magic_dmg)
                    print("{}{} heals for {} {}".format(bcolors.OKBLUE, spell.name, magic_dmg, bcolors.ENDC))
                elif spell.type == DMG_SPELL_NAME:            
                    enemy = player.choose_target(enemies)
                    enemy.take_damage(magic_dmg)
                    print("{}{} {} hits {} points of damage to {}.".format(bcolors.OKBLUE, spell.name, bcolors.ENDC, magic_dmg, enemy.name))
                    if enemy.get_hp() == 0:
                        enemies.remove(enemy)
                        print("Enemy {} defeated!".format(enemy.name))

            elif real_choice == 2:
                player.choose_item()
                item_choice = int(input("Choose item:")) - 1

                if item_choice == -1:
                    continue

                item = player.items[item_choice]["item"]

                if player.items[item_choice]["quantity"] == 0:
                    print('{} \nYou have no more {}!  {}'.format(bcolors.FAIL, item.name, bcolors.ENDC))
                    continue
                player.items[item_choice]["quantity"] -= 1

                if item.type == ITEM_TYPES[0]:
                    player.heal(item.prop)
                    print('{} \n{} heals for {} {}'.format(bcolors.OKGREEN, item.name, item.prop, bcolors.ENDC))
                elif item.type == ITEM_TYPES[1]:
                    player.hp = player.maxhp
                    player.mp = player.maxmp #### ACCESING HERE?? I WOULD LIKE TO KNOW HOW PRIVATE METHODS WORKS.
                    print('{} \n{} fully restores hp and mp {}'.format(bcolors.OKGREEN, item.name, bcolors.ENDC))
                elif item.type == ITEM_TYPES[2]:
                    enemy = player.choose_target(enemies)
                    enemy.take_damage(item.prop)
                    print('{} \n{} deals {} points of damage to {}{}'.format(bcolors.FAIL, item.name, item.prop, enemy.name, bcolors.ENDC))
                    if enemy.get_hp() == 0:
                        enemies.remove(enemy)
                        print("Enemy {} defeated!".format(enemy.name))
                elif item.type == ITEM_TYPES[3]:
                    for p in players:
                        p.hp = p.maxhp
                        p.mp = p.maxmp
                


        for enemy in enemies:
            #if enemy_hp_percentage <= LOW_HP:
            enemy_choice = random.randrange(0,2)

            if enemy_choice == 0:
                enemy_dmg = enemy.generate_damage()

                targeted_player = players[random.randrange(0,len(players))]
                targeted_player.take_damage(enemy_dmg)
                print("Enemy {} attacked for {} points of damage to {} ".format(enemy.name, enemy_dmg, targeted_player.name))
            elif enemy_choice == 1:
                spell, magic_dmg = enemy.choose_enemy_spell()
                print(spell.name, magic_dmg)
                if spell.type == HEAL_SPELL_NAME:
                    enemy.heal(magic_dmg)
                    print("{}{} used {} and heals for {} {}".format(bcolors.OKBLUE, enemy.name, spell.name, magic_dmg, bcolors.ENDC))
                elif spell.type == DMG_SPELL_NAME:            
                    targeted_player = players[random.randrange(0,len(players))]
                    targeted_player.take_damage(magic_dmg)
                    print("{}{}{} hits {} points of damage to {}.".format(bcolors.OKBLUE, spell.name, bcolors.ENDC, magic_dmg, targeted_player.name))
                    if targeted_player.get_hp() == 0:
                        print("Player {} died!".format(enemy.name))

        print("--------------------------------")

        if len(enemies)==0:
            print( bcolors.OKGREEN + "You win!" + bcolors.ENDC)
            running = False
        else:
            num_deaths = 0
            for p in players:
                if p.get_hp() == 0:
                    num_deaths += 1
            if num_deaths == len(players):
                print( bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
                running = False 
        

        #running = False