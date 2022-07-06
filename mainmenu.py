from re import X
from turtle import position
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
            self.leaderboard_1.enabled = False
            self.leaderboard_2.enabled = False
            self.leaderboard_3.enabled = False
            self.leaderboard_4.enabled = False
            self.leaderboard_5.enabled = False
            self.main_menu.enabled = True
            mouse.locked = False

# leaderboard mockup panel

        leaderBoard = WindowPanel(
            title = 'Leaderboard',
            position = (0, 0.35), # position of the window
            content = (
              Text(text = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n"), # empty text to make space for leaderboard texts
              Button(text = 'Exit', color = color.azure, on_click = close_leaderboard),
         ),
            popup = True,
            enabled = False
        ) 
        
        # leaderboard texts - 5 places for first 5 players

        self.leaderboard_1 = Text(text = "", color = color.white, font_size = 20, parent = leaderBoard.content, origin = 0, y = 0.2)
        self.leaderboard_2 = Text(text = "", color = color.white, font_size = 20, parent = leaderBoard.content, origin = 0, y = 0.1)
        self.leaderboard_3 = Text(text = "", color = color.white, font_size = 20, parent = leaderBoard.content, origin = 0, y = 0)
        self.leaderboard_4 = Text(text = "", color = color.white, font_size = 20, parent = leaderBoard.content, origin = 0, y = -0.1)
        self.leaderboard_5 = Text(text = "", color = color.white, font_size = 20, parent = leaderBoard.content, origin = 0, y = -0.2)
        
        # list of texts

        self.leaderboard_texts = [self.leaderboard_1, self.leaderboard_2, self.leaderboard_3, self.leaderboard_4, self.leaderboard_5]


# load scores from file into dictionary 

        def load_scores(self):
            try:
                with open("scores.txt", "r") as file:
                    self.scores = {}
                    for line in file:
                        name, score = line.split()
                        self.scores[name] = int(score)
            except:
                print("Error loading scores from file")


# game start

        def start():
            self.player.enabled = True
            mouse.locked = True
            self.main_menu.enabled = False
            self.player.position = (0, 0, 0)
            self.isGameStarted = True

# fill leaderboard_texts with names and scores from dictionary

        def fill_leaderboard(self):
            # sort dictionary by value
            sorted_dict = sorted(self.scores.items(), key=lambda item: item[1], reverse = True)
            # get top 5 scores
            if(len(sorted_dict) >= 5):
                top_5 = sorted_dict[:5]
            else:
                top_5 = sorted_dict
            # fill leaderboard_texts with names and scores from dictionary
            for index, (name, score) in enumerate(top_5):
                self.leaderboard_texts[index].text = "Name: " + name + " Score: " + str(score)
                
                

# displaying leaderboard

        def display_leaderboard():
           load_scores(self)
           fill_leaderboard(self)
           self.leaderboard_1.enabled = True
           self.leaderboard_2.enabled = True
           self.leaderboard_3.enabled = True
           self.leaderboard_4.enabled = True      
           self.leaderboard_5.enabled = True  
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
