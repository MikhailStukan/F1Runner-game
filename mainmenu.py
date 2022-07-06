from re import X
from cv2 import fastNlMeansDenoising
from ursina import *



class MainMenu(Entity):
    def __init__(self, player, isGameStarted):
        super().__init__(
            parent = camera.ui)
        
        self.player = player
        self.main_menu = Entity(parent = self, enabled = True)
        self.isGameStarted = isGameStarted



# closing leaderboard window

        def close_leaderboard():
            leaderBoard.enabled = False
            self.main_menu.enabled = True
            mouse.locked = False

# leaderboard mockup panel

        leaderBoard = WindowPanel(
            title = 'Leaderboard',
            content = (
                Text("%Name results : #Score", color = color.white, font_size = 20),
                Text("%Name results : #Score", color = color.white, font_size = 20),
                Text("%Name results : #Score", color = color.white, font_size = 20),
              Button(text = 'Exit', color = color.azure, on_click = close_leaderboard),
         ),
            popup = True,
            enabled = False
        ) 

# game start
        def start():
            self.player.enabled = True
            mouse.locked = True
            self.main_menu.enabled = False
            self.player.position = (0, 0, 0)
            self.isGameStarted = True

# displaying leaderboard

        def display_leaderboard():
           leaderBoard.enabled = True
           self.main_menu.enabled = False

# restarting game (WIP)

        def restart():
            self.main_menu.enabled = False
            application.start()

#resume game

        def resume():
            self.main_menu.enabled = False
            application.paused = not application.paused
            self.isGameStarted = True
            mouse.locked = True

        # if game is not started

        if(self.isGameStarted == False):
            start_button = Button(text = "Start the race", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
            start_button.on_click = Func(start)

        # if
        else:
            resume_button = Button(text = "Resume game", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
            resume_button.on_click = Func(resume)
            restart_button = Button(text = "Restart game", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.15, parent = self.main_menu)
            restart_button.on_click = Func(restart)


       # drawing buttons for leaderboard and exit
        
        leader_button = Button(text = "Leaderboard", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)
        quit_button = Button(text = "Quit", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)
        quit_button.on_click = application.quit
        leader_button.on_click = Func(display_leaderboard)
