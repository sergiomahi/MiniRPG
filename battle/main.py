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



class Application(QWidget):
    def __init__(self, enemies, players):
        super().__init__()
        self.current_player = players[0]
        self.num_turns = 1
        self.attack_ready = False

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
        

    def attack(self, button):
        if button.take_damage_if_ready(self.attack_ready, self.current_player.generate_damage()):
            print(self.current_player.name)

            num_players_alive = len(self.players_alive(self.players))
            
            if self.num_turns < num_players_alive:
                self.current_player = self.players[self.num_turns] # Take next player
                self.num_turns += 1
            else:
                self.current_player = enemies[0] # First enemy
                self.num_turns += 1
    
            if self.current_player.get_is_enemy():
                for enemy in self.enemies:
                    if not enemy.is_dead():
                        self.current_player = enemy
                        self.enemyAttack()
                    
                self.current_player = self.players[self.players_alive(self.players)[0]] ## Next player alive
                self.num_turns = 1
            
            # Check if the current player is dead in other to select next alive player
            if self.current_player.is_dead():
                next_alive_player_index = self.next_player_alive()
                self.current_player = self.players[next_alive_player_index]
                self.num_turns += next_alive_player_index

            self.is_attack_ready()
            self.updateTurnLabel()


    def updateTurnLabel(self):
        self.turn_of.setText("Turn of {}".format(self.current_player.name))


    def players_alive(self, players, init=0):
        indexes = []
        for p in players:
            if not p.is_dead():
                indexes.append(init)
            init+=1
        return indexes

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
            
            
    def check_game_over(self):
        players = [p.is_dead() for p in self.players]
        enemies = [e.is_dead() for e in self.enemies]

        if (all(players)):
            print("Enemies won!")
            
            buttonReply = QMessageBox.question(self, 'PyQt5 message', "Enemies won!", QMessageBox.Yes, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                exit(1)

            self.show()
        print(all(enemies))


        
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
    player1 = Person("Valos", 100, 65, 180, 34, PLAYER_SPELLS, PLAYER_ITEMS, False)
    player2 = Person("Lyss", 10, 65, 200, 34, PLAYER_SPELLS, PLAYER_ITEMS, False)
    player3 = Person("Kay", 10, 65, 300, 34, PLAYER_SPELLS, PLAYER_ITEMS, False)
    players = [player1, player2, player3]

    enemy2 = Person("Culo", 1200, 65, 80, 100, PLAYER_SPELLS, PLAYER_ITEMS, True)
    enemy1 = Person("Javio", 12000, 65, 350, 25, PLAYER_SPELLS, PLAYER_ITEMS, True)
    enemy3 = Person("Culo", 1200, 65, 80, 100, PLAYER_SPELLS, PLAYER_ITEMS, True)
    enemies = [enemy2, enemy1, enemy3]

    ######################
    ##
    ##   App initialization
    ##
    ######################
    app = QApplication(sys.argv)

    window = Application(enemies, players)

    sys.exit(app.exec_())
