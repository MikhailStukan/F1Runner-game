from tkinter import RIGHT
from ursina import *

# Importing components

from player import Player
from mainmenu import MainMenu
from obstacles import Pickup, Sedan, Truck, HealthOrb, SpeedOrb
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
window.vsync = 60
window.color = color.rgb(0,94,184)
window.icon = load_texture('resources/sprites/player.png')

# CONSTANTS

Y = -20
ROADS_LENGTH = 28.7
LEFT_BOUND = -5.5
RIGHT_BOUND = 5.5
MAX_CARS = 20
MAX_ORBS = 2

# Sounds

engine_sound = Audio('/resources/sounds/car_starting_idle.wav', loop = False, autoplay= False)
race_sound = Audio('resources/sounds/car_acceleration.wav', loop = True, autoplay = False)

# heart texture

hearth_texture = load_texture('resources/sprites/heart.png')

#spawning cars

cars = []

def new_cars(x, ys):
        #spawn three variation of cars Pickup or Sedan or Truck on coordinates x and y
        if random.randint(0, 1) == 0:
            new = Pickup(x, ys)
        elif random.randint(0, 1) == 0:
            new = Sedan(x, ys)
        else:
            new = Truck(x, ys)

        cars.append(new)

# creating new road at coordinates y

roads = []

def newRoad(y):
    new = Sprite(name = "road", model = 'quad', texture = 'resources/sprites/road_0.png', scale = 1.5, x = 0, y = y, z = 0)
    roads.append(new)

# remove road after coordinates y

def removeRoad(yx):
    for road in roads:
        if road.y <= yx:
            roads.remove(road)
            break

# remove car after coordinates y

def removeCars(yx):
    for car in cars:
        if car.y <= yx:
            cars.remove(car)
            break

# remove orbs after coordinates y

def removeOrbs(yx):
    for orb in orbs:
        if orb.y <= yx:
            orbs.remove(orb)
            break

orbs = []

# spawning orbs

def spawn_orbs(x, y):
        if random.randint(0, 1) == 0:
            new = HealthOrb(x, y)
            orbs.append(new)
        else:
            new = SpeedOrb(x, y)
            orbs.append(new)

# create initial 4 road sprites forward of the player

for x in range(0, 4):
    newRoad(Y)
    Y += ROADS_LENGTH # legth of one road sprite

#creating player

player = Player()

#deleting not visible roads, cars, orbs after player

def clean():
    if player.y >= roads[0].y + ROADS_LENGTH:
        removeRoad(roads[0].y + ROADS_LENGTH)
        removeCars(roads[0].y + ROADS_LENGTH)
        removeOrbs(roads[0].y + ROADS_LENGTH)

#adding new roads, cars before player reaches the end of the screen and increasing player score by 1 for each road (WIP?) 

def general_spawn():
        if player.y >= roads[-1].y - ROADS_LENGTH - (player.max_speed + player.speed):
            newRoad(roads[-1].y + ROADS_LENGTH)
            if(len(cars) < MAX_CARS):
                new_cars(random.uniform(LEFT_BOUND, RIGHT_BOUND), roads[-1].y + ROADS_LENGTH)
            player.score += 1

# spawning orbs

def orbs_spawn():
    distance_to_orb = random.uniform(0,ROADS_LENGTH)
    if player.y >= roads[-1].y - ROADS_LENGTH - (player.max_speed + player.speed) and len(orbs) < MAX_ORBS:
        spawn_orbs(random.uniform(LEFT_BOUND, RIGHT_BOUND), roads[-1].y + ROADS_LENGTH + distance_to_orb)



# Main Menu

mainmenu = MainMenu(player, False)

#displaying lifes in hearts

hearts = []

for i in range(player.maxlife):
    heart = Sprite(texture = hearth_texture, scale = 0.3, x = -0.80 + (i/10), y = 0.40, parent = camera.ui, always_on_top = True)
    hearts.append(heart)

# Displaying current speed and score

speed_text = Text(text = "Speed: " + str(int(player.speed * 200)) + "km/h", size = 0.05, x = -0.85, y = 0.30)
score_text = Text(text= "Score: " + str(player.score), size = 0.05, x = -0.85, y = 0.20)

# if game isn't started, start sound is played

if (player.enabled == False):
    engine_sound.play()

# function for displaying hearts according to amount of lifes (player)

def updating_hearts():
    if player.life != player.maxlife:
        for i in range(player.life):
            hearts[i].visible = True
        for i in range(player.life, player.maxlife):
            hearts[i].visible = False

#updating game state

def update():
    if(player.enabled == True):
        engine_sound.pause()

    #updating hearts

    updating_hearts()

    # updating speed and score

    score_text.text = "Score: " + str(player.score)
    speed_text.text = "Speed: " + str(int(player.speed * 350)) + "km/h"

    # moving camera with player

    camera.y = player.y + 15

    # cleaning memory (deleting roads and cars)

    clean()

    # spawn roads and cars

    general_spawn()

    # orb spawn

    orbs_spawn()
    
    # isAlive check for calling endmenu if lifes = 0

    if(player.isAlive == False):
        application.pause()
        end_menu = Endmenu(player)
        mouse.locked = False

# Pause manager

pause_handler = Entity(ignore_paused = True)

# Pause/unpause the game.

def pause_handler_input(key):
    if key == "escape" and not application.paused and player.enabled and player.isAlive:
        resumemenu = MainMenu(player, True)
        resumemenu.main_menu.enabled = True
        mouse.locked = False
        engine_sound.pause()
        application.pause()
    
# Assign the input function to the pause handler.

pause_handler.input = pause_handler_input

# Running the app

app.run()




        
