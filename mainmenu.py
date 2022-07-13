"""ursina imports"""
from ursina import * # pylint: disable=unused-wildcard-import,wildcard-import,redefined-builtin

SCORE_FILE_PATH = "scores.txt"
ENCODING = "utf-8"

class MainMenu(Entity):
    """ main menu class """
    def __init__(self, player, is_game_started):
        super().__init__(
            parent = camera.ui)
        self.player = player
        self.main_menu = Entity(parent = self, enabled = False)
        self.is_game_started = is_game_started
        self.leaderboard_texts = []
        self.scores = {}


        def close_name_window():
            """ closing name window """
            enter_name.enabled = False
            self.main_menu.enabled = True
            mouse.locked = False

        def save_name():
            """ saving name to file """
            entered_name = enter_name.content[1].text
            if bool(re.match(r'[^a-zA-Z0-9]', entered_name)) is False:
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

        def close_leaderboard():
            """ closing leaderboard """
            leader_board.enabled = False
            self.main_menu.enabled = True
            mouse.locked = False

        leader_board = WindowPanel(
            title = 'Leaderboard',
            position = (0, 0.35), # position of the window
            content = (
              Text(name = 'place', text = "", color = color.white,
                font_size = 20, origin = 0, y = 0.25),
              Space(),
              Text(name = 'place', text = "", color = color.white,
                font_size = 20, origin = 0, y = 0.20),
              Space(),
              Text(name = 'place', text = "", color = color.white,
                font_size = 20, origin = 0, y = 0.15),
              Space(),
              Text(name = 'place', text = "", color = color.white,
                font_size = 20, origin = 0, y = 0.10),
              Space(),
              Text(name = 'place', text = "", color = color.white,
                font_size = 20, origin = 0, y = 0.5),
              Space(),
              Button(text = 'Exit', color = color.azure, on_click = close_leaderboard),
         ),
            popup = True,
            enabled = False
        )

        def fill_leaderboads_texts():
            """ filling leaderboard texts """
            for element in leader_board.content:
                if isinstance(element, Text):
                    self.leaderboard_texts.append(element)

        def load_scores():
            """ loading score from file """
            try:
                with open(SCORE_FILE_PATH, "r", encoding=ENCODING) as file:
                    for line in file:
                        name, score = line.split()
                        self.scores[name] = int(score)
            except OSError:
                print("Could not load scores:", SCORE_FILE_PATH, str(OSError))

        def start():
            """ starting game """
            self.player.enabled = True
            mouse.locked = True
            self.main_menu.enabled = False
            self.player.position = (0, 0, 0)
            self.is_game_started = True
            enter_name.enabled = False
            self.player.start_engine()

        def fill_leaderboard():
            """ filling leaderboard with scores from dict """
            sorted_dict = sorted(self.scores.items(), key=lambda item: item[1], reverse = True)
            if len(sorted_dict) >= 5:
                top_5 = sorted_dict[:5]
            else:
                top_5 = sorted_dict
            for index, (name, score) in enumerate(top_5):
                self.leaderboard_texts[index].text = "Name: " + name + " Score: " + str(score)

        def display_leaderboard():
            """display leaderboard"""
            fill_leaderboard()
            leader_board.enabled = True
            self.main_menu.enabled = False

        def restart():
            """ restarting game """
            self.main_menu.enabled = False
            application.start()

        def resume():
            """ resuming game"""
            self.main_menu.enabled = False
            application.paused = not application.paused
            self.is_game_started = True
            mouse.locked = True
            self.player.start_engine()

        load_scores()
        fill_leaderboads_texts()

        if self.is_game_started is False:
            start_button = Button(text = "Start the race", color = color.azure,
                scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
            start_button.on_click = Func(start)
            enter_name.enabled = True
        else:
            resume_button = Button(text = "Resume game", color = color.azure, 
                scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
            resume_button.on_click = Func(resume)
            restart_button = Button(text = "Restart game", color = color.azure,
                scale_y = 0.1, scale_x = 0.3, y = 0.15, parent = self.main_menu)
            restart_button.on_click = Func(restart)

        leader_button = Button(text = "Leaderboard", color = color.azure,
            scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)
        quit_button = Button(text = "Quit", color = color.azure,
            scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)
        quit_button.on_click = application.quit
        leader_button.on_click = Func(display_leaderboard)
