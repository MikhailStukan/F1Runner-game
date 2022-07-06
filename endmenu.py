from ursina import *

from player import Player



class Endmenu(Entity):

    
    def __init__(self, player):
        super().__init__(
            parent = camera.ui)
    
        self.player = player
        self.end_menu = Entity(parent = self, enabled = True)

    
        Text("Your results : " + str(player.score), color = color.black, scale_y = 5, scale_x = 5, x = -0.35, y = 0.3, parent = self.end_menu),
        quit_button = Button(text = "Quit", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.end_menu)
        


        
        def save_score_tofile(self):
            with open('scores.txt', 'a') as f:
             f.write(str(self.player.name) + " " + str(self.player.score) + '\n')
            

        quit_button.on_click = save_score_tofile(self)
     
        