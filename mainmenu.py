from re import X
from turtle import position
from cv2 import fastNlMeansDenoising
from ursina import *



class MainMenu(Entity):
    def __init__(self, player, isGameStarted):
        super().__init__(
            parent = camera.ui)
        
        self.player = player
        self.main_menu = Entity(parent = self, enabled = False)
        self.isGameStarted = isGameStarted

        

# saving player name

        def save_name():
            
            #getting entered name
            
        
            entered_name = enter_name.content[1].text

            # checking name for prohibited characters and maximum length

            if(bool(re.match(r'[^a-zA-Z0-9]', entered_name)) == False):
                if len(entered_name) > 10:
                    enter_name.content[4].text = "Name is too long"
                    entered_name = ""
                elif len(entered_name) < 3:
                    enter_name.content[4].text = "Name is too short"
                    entered_name = ""
                else:
                    self.player.name = entered_name
                    close_name_window()
            else:
                enter_name.content[4].text = "Name can only contain letters and numbers"


        def close_name_window():
            enter_name.enabled = False
            self.main_menu.enabled = True
            mouse.locked = False



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
              Text(name = 'place', text = "", color = color.white, font_size = 20, origin = 0, y = 0.25),
              Space(),
              Text(name = 'place', text = "", color = color.white, font_size = 20, origin = 0, y = 0.20),
              Space(),
              Text(name = 'place', text = "", color = color.white, font_size = 20, origin = 0, y = 0.15),
              Space(),
              Text(name = 'place', text = "", color = color.white, font_size = 20, origin = 0, y = 0.10),
              Space(),
              Text(name = 'place', text = "", color = color.white, font_size = 20, origin = 0, y = 0.5),
              Space(),
              Button(text = 'Exit', color = color.azure, on_click = close_leaderboard),
         ),
            popup = True,
            enabled = False
        ) 

# enter player name panel

        enter_name = WindowPanel(
            title = 'Enter your name',
            position = (0, 0.1), # position of the window
            content = (
                Space(),
                InputField(name = 'InputName', text = '', placeholder = 'Enter your name'),
                Space(),
                Text(name = 'error_text', text = "", color = color.white, font_size = 20),
                Button(text = 'Submit', color = color.azure, on_click = save_name),
        ),
            popup = True,
            enabled = False
        )
        
        # list of leaderboard texts

        self.leaderboard_texts = []
        for element in leaderBoard.content:
            if isinstance(element, Text):
                self.leaderboard_texts.append(element)



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
            enter_name.enabled = False
            self.player.start_engine()

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
           fill_leaderboard(self)  
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
            self.player.start_engine()

        load_scores(self)
        # if game is not started
        if(self.isGameStarted == False):
            start_button = Button(text = "Start the race", color = color.azure, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
            start_button.on_click = Func(start)
            enter_name.enabled = True
        else:
            resume_button = Button(text = "Resume game", color = color.azure, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
            resume_button.on_click = Func(resume)
            restart_button = Button(text = "Restart game", color = color.azure, scale_y = 0.1, scale_x = 0.3, y = 0.15, parent = self.main_menu)
            restart_button.on_click = Func(restart)


       # drawing buttons for leaderboard and exit
        
        leader_button = Button(text = "Leaderboard", color = color.azure, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)
        quit_button = Button(text = "Quit", color = color.azure, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)
        quit_button.on_click = application.quit
        leader_button.on_click = Func(display_leaderboard)
       
