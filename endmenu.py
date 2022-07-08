from ursina import *

from player import Player



class Endmenu(Entity):

    
    def __init__(self, player):
        super().__init__(
            parent = camera.ui)
    
        self.player = player
        self.end_menu = Entity(parent = self, enabled = True)

        # saving score to .txt file

        def save_score_tofile(self):
            try :
                with open("scores.txt", "a") as file:
                    file.write(str(self.player.name) + " " + str(self.player.score) + '\n')
            except:
                print("Error saving score to file")

        save_score_tofile(self)

        # displaying end results
        
        Text("Your results : " + str(player.score), color = color.white, scale_y = 5, scale_x = 5, x = -0.35, y = 0.3, parent = self.end_menu),
        quit_button = Button(text = "Quit", color = color.azure, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.end_menu)
          
        quit_button.on_click = application.quit
     
        