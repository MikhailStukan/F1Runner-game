from ursina import * # pylint: disable=unused-wildcard-import,wildcard-import,redefined-builtin

SCORE_FILE_PATH = "scores.txt"
ENCODING = "utf-8"

class Endmenu(Entity):
    """end menu class"""
    def __init__(self, player):
        super().__init__(parent = camera.ui)
        self.player = player
        self.end_menu = Entity(parent = self, enabled = True)

        def save_score_tofile():
            """saving score to file"""
            try :
                with open(SCORE_FILE_PATH, "a", encoding=ENCODING) as file:
                    file.write(str(self.player.name) + " " + str(self.player.score) + '\n')
            except OSError:
                print("Could not write scores:", SCORE_FILE_PATH, str(OSError))

        def restart_game():
            """restarting game"""
            return

        save_score_tofile()

        results = Text("Your results : ", color = color.white,
            scale_y = 5, scale_x = 5, x = -0.35, y = 0.3, parent = self.end_menu)
        restart_button = Button(text = "Restart", color = color.azure,
            scale_y = 0.1, scale_x = 0.3, y = 0, parent = self.end_menu)
        quit_button = Button(text = "Quit", color = color.azure,
            scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.end_menu)

        results.text = "Your results : " + str(self.player.score)
        restart_button.on_click = Func(restart_game)
        quit_button.on_click = application.quit
