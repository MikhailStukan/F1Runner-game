from os import remove
from ursina import *
from cars import Pickup

# Importing components

from player import Player
from mainmenu import MainMenu
from cars import *
from endmenu import Endmenu

app = Ursina()

# Window settings

window.title = "F1Runner"
camera.orthographic = True
mouse.locked = False
camera.fov = 50
window.fullscreen = False
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = False
window.vsync = True
window.color = color.rgb(0,94,184)
window.icon = load_texture('resources/sprites/player.png')


y = -20
roads_length = 28.7

# Sounds

engine_sound = Audio('/resources/sounds/car_starting_idle.wav', loop = False, autoplay= False)
race_sound = Audio('resources/sounds/car_acceleration.wav', loop = True, autoplay = False)

# heart texture

hearth_texture = load_texture('resources/sprites/heart.png')

#spawning cars

cars = []

def new_cars(x, ys):

    #spawn three variation of cars Pickup or Sedan or Truck

    if random.randint(0, 1) == 0:
        new = Pickup(x, ys, speed = random.uniform(0.1, 0.2))
    elif random.randint(0, 1) == 0:
        new = Sedan(x, ys, speed = random.uniform(0.1, 0.3))
    else:
        new = Truck(x, ys, speed = random.uniform(0.05, 0.1))

    cars.append(new)


# creating new road at coordinates y

roads = []

def newRoad(y):
    new = Sprite(model = 'quad', texture = 'resources/sprites/road_0.png', scale = 1.5, x = 0, y = y, z = 0)
    roads.append(new)

# remove road at coordinates y

def removeRoad(yx):
    for road in roads:
        if road.y <= yx:
            roads.remove(road)
            break

# remove car at coordinates y

def removeCars(yx):
    for car in cars:
        if car.y <= yx:
            cars.remove(car)
            break

# create initial 4 road sprites forward of the player

for x in range(0, 4):
    newRoad(y)
    y += roads_length # legth of one road sprite

#creating player

player = Player()

#deleting not visible roads and cars after player

def clean():
    if player.y >= roads[0].y + roads_length:
        removeRoad(roads[0].y + roads_length)
        removeCars(roads[0].y + roads_length)

#adding new roads and cars before player reaches the end of the screen and increasing player score by 1 for each road (WIP?) 

def add():
        if player.y >= roads[-1].y - roads_length - player.speed:
            newRoad(roads[-1].y + roads_length)
            new_cars(random.uniform(-6, 6), roads[-1].y + roads_length)
            player.score += 1

# Main Menu
mainmenu = MainMenu(player, False)

#displaying lifes in hearts
hearts = []
for i in range(player.life):
    heart = Sprite(texture = hearth_texture, scale = 0.3, x = -0.80 + (i/10), y = 0.40, parent = camera.ui)
    hearts.append(heart)
    heart.always_on_top = True


# Displaying current speed and score

speed_text = Text(text = "Speed: " + str(int(player.speed * 200)) + "km/h", size = 0.05, x = -0.85, y = 0.30)
score_text = Text(text= "Score: " + str(player.score), size = 0.05, x = -0.85, y = 0.20)


# if game isn't started, start sound is played

if (player.enabled == False):
    engine_sound.play()


#updating game

def update():
    if(player.enabled == True):
        engine_sound.pause()

    #health_text.text = "Lifes: " + str(player.life)

    #displaying hearts according to amount of lifes (player)

    if len(hearts) > player.life:
        hearts[player.life].enabled = False
        

    # updating speed and score

    score_text.text = "Score: " + str(player.score)
    speed_text.text = "Speed: " + str(int(player.speed * 200)) + "km/h"

    # moving camera with player

    camera.y = player.y + 20

    # cleaning memory (deleting roads and cars)

    clean()

    # spawn roads and cars

    add()
    

    # isAlive check for calling endmenu if lifes = 0

    if(player.isAlive == False):
        application.pause()
        end_menu = Endmenu(player)
        mouse.locked = False

    

           


# Pause manager

pause_handler = Entity(ignore_paused = True)


# Pause/unpause the game.

def pause_handler_input(key):
    if key == "escape" and not application.paused and player.enabled == True:
        resumemenu = MainMenu(player, True)
        mouse.locked = False
        engine_sound.pause()
        application.pause()
    



# Assign the input function to the pause handler.

pause_handler.input = pause_handler_input


# Running the app

app.run()




        
