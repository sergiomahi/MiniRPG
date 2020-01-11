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


    def take_damage_if_ready(self, attack_ready, damage):
        if attack_ready:
            self.enemy.take_damage(damage)
            self.hp_label.setText(self.enemy.get_hp_bar())
            return True
        return False
    
    def take_magic_damage(self, spell):
        if spell:
            self.enemy.take_damage(spell.dmg)
            self.hp_label.setText(self.enemy.get_hp_bar())
            return True
        return False


class PlayerButton():
    def __init__(self, p):
        self.button = QPushButton(p.name) 
        self.player = p
        self.hp_label = QLabel(p.get_hp_bar())
        self.mp_label = QLabel(p.get_mp_bar())

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.button)       
        self.vbox.addWidget(self.hp_label)
        self.vbox.addWidget(self.mp_label)


    def take_damage_if_ready(self, attack_ready, damage):
        if attack_ready:
            self.player.take_damage(damage)
            self.hp_label.setText(self.player.get_hp_bar())
            return True
        return False


    def generate_magic_attack(self, spell):
        if spell:
            if (self.player.check_mp(spell)):
                self.player.reduce_mp(spell.cost)
                self.mp_label.setText(self.player.get_mp_bar())
                return True
            else:
                box = QMessageBox()
                box.setText("Not enough mana")
                box.setStandardButtons(QMessageBox.Yes)
                box.exec_()
        return False

    def heal(self, spell):
        if spell:
            self.player.heal(spell.dmg)
            self.hp_label.setText(self.player.get_hp_bar())
            return True
        return False



class Application(QWidget):
    def __init__(self, enemies, players):
        super().__init__()
        self.current_player = players[0]
        self.num_turns = 1
        self.attack_ready = False
        self.current_spell = False

        self.setWindowTitle("RPG")
        self.enemies = enemies
        self.players = players
        self.player_buttons = []
        self.enemy_buttons = []
        self.createApp(enemies, players)


    def createApp(self, enemies, players):
        grid = QGridLayout()
        self.turn_of = QLabel("Turn of {}".format(self.current_player.name))
        grid.addWidget(self.turn_of, 0, 0, 1, 3)
        
        row = 2
        col = 0
        for button in enemies:
            b_object = EnemyButton(button)
            b_object.button.clicked.connect(lambda state, x=b_object: self.attack(x))        

            grid.addLayout(b_object.vbox, row, col, 1, 1)

            self.enemy_buttons.append(b_object)
            row += 1

        row = 2
        col = 3        
        for button in players:
            b_object = PlayerButton(button)
            b_object.button.clicked.connect(lambda state, x=b_object: self.attack(x))        

            grid.addLayout(b_object.vbox, row, col, 1, 1)
            self.player_buttons.append(b_object)

            row += 1

        self.current_player_button = self.player_buttons[0]  # We take the first player as the current player button
        self.attack_button = QPushButton("Attackt")
        row += 1
        grid.addWidget(self.attack_button, row, 0, 1, 4 )


        self.magic_button = QPushButton("Magic")
        magic_menu = QMenu()
        for spell in self.current_player.magic:
            spell_action = magic_menu.addAction(spell.name)
            spell_action.triggered.connect(lambda state, x=spell: self.set_spell(x))

        self.magic_button.setMenu(magic_menu)
        row += 1
        grid.addWidget(self.magic_button, row, 0, 1, 4 )

        self.attack_button.clicked.connect(self.is_attack_ready)

        self.setLayout(grid)
        self.show()


    def set_spell(self, spell):
        if self.current_spell and not spell: # If there was a magic selected and now there isnt
            print("Spell deselected")

        self.current_spell = spell
        if self.current_spell:
            print("Selected spell: {}".format(self.current_spell.name))

            # We need to deactivate the basic attack if we select an spell.
            if self.attack_ready:   
                self.attack_button.setText("Attack")
                self.attack_ready = False


    def is_attack_ready(self):
        if self.attack_ready:
            self.attack_button.setText("Attack")
            self.attack_ready = False
        else:
            self.attack_button.setText("Attack ready!")
            self.attack_ready = True

        self.set_spell(False) # Everytime we click on attack the magic is reseted
        

    def manageTurns(self, button):

        num_players_alive = len(self.players_alive(self.players))
        
        if self.num_turns < num_players_alive:
            self.set_current_player(self.num_turns) # Take next player
            self.num_turns += 1
        else:
            self.set_current_player_enemy(0) # First enemy
            self.num_turns += 1

        if self.current_player.get_is_enemy():
            enemy_number = 0
            for enemy in self.enemies:
                if not enemy.is_dead():
                    self.set_current_player_enemy(enemy_number)
                    self.enemyAttack()
                enemy_number += 1
                
            self.set_current_player(self.players_alive(self.players)[0]) ## Next player alive
            self.num_turns = 1
        
        # Check if the current player is dead in other to select next alive player
        if self.current_player.is_dead():
            next_alive_player_index = self.next_player_alive()
            self.set_current_player(next_alive_player_index)
            self.num_turns += next_alive_player_index

        self.check_game_over()

        self.updateTurnLabel()


    def attack(self, button):
        if button.take_damage_if_ready(self.attack_ready, self.current_player.generate_damage()):
            self.manageTurns(button)
            self.is_attack_ready()


        if self.current_player_button.generate_magic_attack(self.current_spell): # Reduce the mp of the user
            if self.current_spell.type == DMG_SPELL_NAME:
                button.take_magic_damage(self.current_spell)
            elif self.current_spell.type == HEAL_SPELL_NAME:
                button.heal(self.current_spell)
                
            self.manageTurns(button)


    def updateTurnLabel(self):
        self.turn_of.setText("Turn of {}".format(self.current_player.name))


    def players_alive(self, players, init=0):
        indexes = []
        for p in players:
            if not p.is_dead():
                indexes.append(init)
            init+=1
        return indexes


    def set_current_player(self, index):
        self.current_player = self.players[index]
        self.current_player_button = self.player_buttons[index]


    def set_current_player_enemy(self, index):
        self.current_player = self.enemies[index]
        self.current_player_button = self.enemies[index]


    def next_player_alive(self):
        actual_position = self.players.index(self.current_player)
        next_players = self.players[actual_position:]
        players_alive = self.players_alive(next_players, actual_position)

        if not players_alive:
            return self.players_alive(self.players)[0]

        return players_alive[0]
         
    
    def enemyAttack(self):
        players_alive = self.players_alive(self.players)
        enemy_choice = random.randrange(0,1) # It can choose either option 0 attack or 1 magic. 

        if enemy_choice == 0:
            enemy_dmg = self.current_player.generate_damage()

            targeted_player_index = random.choice(players_alive)
            targeted_player = self.players[targeted_player_index]
            self.player_buttons[targeted_player_index].take_damage_if_ready(True, enemy_dmg)
            print("Enemy {} attacked for {} points of damage to {} ".format(self.current_player.name, enemy_dmg, targeted_player.name))

            self.check_game_over()

    
    def check_all_deads(self, players, name):
        message = "{} won!".format(name)

        if (all(players)):
            print(message)
            
            buttonReply = QMessageBox.question(self, 'PyQt5 message', message, QMessageBox.Yes, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                exit(1)
            
    def check_game_over(self):
        players = [p.is_dead() for p in self.players]
        enemies = [e.is_dead() for e in self.enemies]

        self.check_all_deads(players, "Enemies")    # If all players die enemies won
        self.check_all_deads(enemies, "Players")    # If all enemies die players won
    



        
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
    player1 = Person("Sergiyo", 400, 65, 180, 34, PLAYER_SPELLS, PLAYER_ITEMS, False)
    player2 = Person("Vandel", 300, 65, 200, 34, PLAYER_SPELLS, PLAYER_ITEMS, False)
    player3 = Person("Gudi", 350, 65, 300, 34, PLAYER_SPELLS, PLAYER_ITEMS, False)
    players = [player1, player2, player3]

    enemy2 = Person("dog", 300, 65, 80, 100, PLAYER_SPELLS, PLAYER_ITEMS, True)
    enemy1 = Person("Javio", 1200, 65, 350, 25, PLAYER_SPELLS, PLAYER_ITEMS, True)
    enemy3 = Person("dog", 300, 65, 80, 100, PLAYER_SPELLS, PLAYER_ITEMS, True)
    enemies = [enemy2, enemy1, enemy3]

    ######################
    ##
    ##   App initialization
    ##
    ######################
    app = QApplication(sys.argv)

    window = Application(enemies, players)

    sys.exit(app.exec_())
