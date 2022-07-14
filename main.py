""" imports """
from ursina import (Audio,
                    Entity,
                    Sprite,
                    Text,
                    Ursina,
                    application,
                    camera,
                    color,
                    load_texture,
                    mouse,
                    window,
                    random)
from player import Player  # pylint: disable=import-error
from mainmenu import MainMenu  # pylint: disable=import-error
from obstacles import (Pickup, Sedan, Truck, HealthOrb, SpeedOrb)  # pylint: disable=import-error
from endmenu import Endmenu  # pylint: disable=import-error

app = Ursina()

window.title = "F1Runner"
camera.orthographic = True
mouse.locked = False
camera.fov = 50
window.fullscreen = False
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True
window.vsync = 60
window.color = color.black

ROADS_LENGTH = 28.7
LEFT_BOUND = -5.5
RIGHT_BOUND = 5.5
MAX_CARS = 20
MAX_ORBS = 2
INITIAL_AMOUNT_ROADS = 4
INITIAL_Y = -20
CAMERA_OFFSET = 15
HEART_TEXTURE = load_texture('resources/sprites/heart.png')
ROAD_TEXTURE = load_texture('resources/sprites/road_1.png')
START_SOUND = Audio('/resources/sounds/car_starting_idle.wav', loop=False, autoplay=False)

cars = []


def new_cars(x_coord, y_coord):
    """spawn new cars"""
    if random.randint(0, 1) == 0:
        new = Pickup(x_coord, y_coord)
    elif random.randint(0, 1) == 0:
        new = Sedan(x_coord, y_coord)
    else:
        new = Truck(x_coord, y_coord)
    cars.append(new)


roads = []


def new_road(y):
    """spawn new road"""
    new = Sprite(name="road", model='quad',
                 texture=ROAD_TEXTURE, scale=1.5, x=0, y=y, z=0)
    roads.append(new)


def remove_road(y_coord):
    """remove road"""
    iter_road = roads
    for road in iter_road:
        if road.y <= y_coord:
            roads.remove(road)
            break


def remove_car(y_coord):
    """remove car"""
    iter_car = cars
    for car in iter_car:
        if car.y <= y_coord:
            cars.remove(car)
            break


def remove_orb(y_coord):
    """remove orb"""
    iter_orb = orbs
    for orb in iter_orb:
        if orb.y <= y_coord:
            orbs.remove(orb)
            break


orbs = []


def spawn_orbs(x_coord, y_coord):
    """spawn orbs"""
    if random.randint(0, 1) == 0:
        new = HealthOrb(x_coord, y_coord)
        orbs.append(new)
    else:
        new = SpeedOrb(x_coord, y_coord)
        orbs.append(new)


def initial_spawn(roads_amount):
    """create initial road sprites"""
    for _ in range(0, roads_amount):
        spawn_y = INITIAL_Y
        new_road(spawn_y)
        spawn_y += ROADS_LENGTH


initial_spawn(INITIAL_AMOUNT_ROADS)

player = Player()
mainmenu = MainMenu(player, False)


def clean():
    """cleaning memory"""
    if player.y >= roads[0].y + ROADS_LENGTH:
        remove_road(roads[0].y + ROADS_LENGTH)
        remove_car(roads[0].y + ROADS_LENGTH)
        remove_orb(roads[0].y + ROADS_LENGTH)


def general_spawn():
    """spawning objects before player reach end of screen + score"""
    if player.y >= roads[-1].y - ROADS_LENGTH - (player.max_speed + player.speed):
        new_road(roads[-1].y + ROADS_LENGTH)
        if len(cars) < MAX_CARS:
            new_cars(random.uniform(LEFT_BOUND, RIGHT_BOUND), roads[-1].y + ROADS_LENGTH)
            player.score += 1


def orbs_spawn():
    """spawn orbs"""
    if player.y >= roads[-1].y - ROADS_LENGTH - random_distance_to_orb() and len(orbs) < MAX_ORBS:
        spawn_orbs(random.uniform(LEFT_BOUND, RIGHT_BOUND),
                   roads[-1].y + ROADS_LENGTH + random_distance_to_orb())


def random_distance_to_orb():
    """random distance to orb"""
    distance_to_orb = random.uniform(ROADS_LENGTH * 2, 30 * ROADS_LENGTH)
    return distance_to_orb


hearts = []


def spawn_hearts():
    """spawn hearts"""
    for i in range(player.maxlife):
        heart = Sprite(texture=HEART_TEXTURE, scale=0.3, x=(-0.80 + (i/10)), y=0.40,
                       parent=camera.ui, always_on_top=True)
        hearts.append(heart)


if player.enabled is False:
    START_SOUND.play()


def updating_hearts():
    """updating hearts"""
    if player.life != player.maxlife:
        for i in range(player.life):
            hearts[i].visible = True
        for i in range(player.life, player.maxlife):
            hearts[i].visible = False


def create_texts():
    """creating speed and score texts"""
    speed = Text(text="Speed: " + str(int(player.speed * 200)) + "km/h",
                 size=0.05, x=(-0.85), y=0.30)
    score = Text(text="Score: " + str(player.score), size=0.05, x=(-0.85),
                 y=0.20)
    return speed, score


spawn_hearts()

speed_text, score_text = create_texts()


def move_camera(offset_y):
    """move camera"""
    camera.y = player.y + offset_y


def updating_texts():
    """updating texts"""
    speed_text.text = "Speed: " + str(int(player.speed * 200)) + "km/h"
    score_text.text = "Score: " + str(player.score)


def game_cycle():
    """game cycle"""
    move_camera(CAMERA_OFFSET)
    general_spawn()
    orbs_spawn()
    updating_hearts()
    updating_texts()
    clean()


def game_over():
    """game over"""
    application.pause()
    Endmenu(player)
    player.engine_sound.stop()
    mouse.locked = False


def update():
    """updating game state"""
    if player.is_alive and player.enabled is True and mainmenu.is_game_started is True:
        START_SOUND.pause()
        game_cycle()
    elif player.is_alive is False:
        game_over()


def pause_handler_input(key):
    """pause/unpause the game"""
    if key == "escape" and not application.paused and player.enabled and player.is_alive:
        resumemenu = MainMenu(player, True)
        resumemenu.main_menu.enabled = True
        player.stop_engine()
        mouse.locked = False
        START_SOUND.pause()
        application.pause()


pause_handler = Entity(ignore_paused=True)
pause_handler.input = pause_handler_input

app.run()
