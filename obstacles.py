""" ursina engine imports. """
from ursina import Sprite, random

COLL_SOUND_PATH = "/resources/sounds/car_collision.wav"
H_ORB_SOUND_PATH = "resources/sounds/health_orb.wav"
S_ORB_SOUND_PATH = None
C_ORB_SOUND_PATH = None


class Cars(Sprite):  # pylint: disable=too-many-instance-attributes
    """car class inherited from Sprite class"""
    def __init__(self, x, y):
        super().__init__(
            collider='box',
            name='car',
        )
        self.model = 'quad'
        self.x = x
        self.y = y
        self.scale = 3.5
        self.enabled = True
        self.speed = None
        self.always_on_top = True
        self.min_speed = 0.1
        self.max_speed = 0.7
        # self.collision_sound = Audio(COLL_SOUND_PATH,
        # loop = False, autoplay = False)

    def destroy(self):
        """playing collision sound and destroying sprite"""
        # self.collision_sound.play()
        self.enabled = False

    def update(self):
        """updating car position"""
        self.y -= self.random_speed()

    def random_speed(self):
        """random speed generator"""
        self.speed = random.uniform(self.min_speed, self.max_speed)
        return self.speed


class Pickup(Cars):
    """Pickup car"""
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.texture = 'resources/sprites/pickup_green.png'
        self.health = 2
        self.max_speed = 0.5

        for key, value in kwargs.items():
            setattr(self, key, value)


class Sedan(Cars):
    """Sedan car"""
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        self.texture = 'resources/sprites/sedan_yellow.png'
        self.health = 1
        self.max_speed = 0.7

        for key, value in kwargs.items():
            setattr(self, key, value)


class Truck(Cars):
    """Truck car"""
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        self.texture = 'resources/sprites/garbage_truck.png'
        self.health = 3
        self.max_speed = 0.3

        for key, value in kwargs.items():
            setattr(self, key, value)


class Obstacle(Sprite):
    """Obstacle class"""
    def __init__(self, x, y):
        super().__init__(
            collider='box',
            name='obstacle',
        )
        self.model = 'quad'
        self.x = x
        self.y = y
        self.scale = 3
        self.enabled = True
        self.always_on_top = True
        # self.collision_sound = Audio('resources/sounds/default.wav',
        #  loop = False, autoplay = False)

    def destroy(self):
        """playing collision sound and destroying sprite"""
        self.enabled = False
        # self.collision_sound.play()


class HealthOrb(Obstacle):
    """Health orb"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = 'resources/sprites/health_orb.png'
        self.health = 1
        self.name = 'health_orb'
        # self.collision_sound = Audio(H_ORB_SOUND_PATH,
        # loop = False, autoplay = False)


class SpeedOrb(Obstacle):
    """Speed orb"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = 'resources/sprites/speed_orb.png'
        self.speed_increase = 2
        self.name = 'speed_orb'
        # self_collision_sound = Audio(None, loop = False, autoplay = False)


class CoinOrb(Obstacle):
    """Coin orb"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = 'resources/sprites/coin_orb.png'
        self.score_increase = 1
        self.name = 'coin_orb'
        # self.collision_sound = Audio(None, loop = False, autoplay = False)
