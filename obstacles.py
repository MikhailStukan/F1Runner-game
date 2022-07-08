from ursina import *

# car class inhterited from Sprite class

class Cars(Sprite):
    def __init__(self, x , y):
        super().__init__(
            collider = 'box',
            name = 'car',
        )
        self.model = 'quad',
        self.x = x
        self.y = y
        self.scale = 3.5
        self.enabled = True
        self.always_on_top = True
        self.min_speed = 0.1
        self.max_speed = 0.7
        self.collision_sound = Audio('resources/sounds/car_collision.wav', loop = False, autoplay = False)
    # disable rendering 

    def destroy(self):
        self.collision_sound.play()
        self.enabled = False

    def update(self):
        self.y -= self.random_speed()

    def random_speed(self):
        self.speed = random.uniform(self.min_speed, self.max_speed)
        return self.speed

# pickup 

class Pickup(Cars):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.texture = 'resources/sprites/pickup_green.png'
        self.health = 2
        self.max_speed = 0.5

        for key, value in kwargs.items():
            setattr(self, key, value)

        
# sedan

class Sedan(Cars):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        self.texture = 'resources/sprites/sedan_yellow.png'
        self.health = 1
        self.max_speed = 0.7

        for key, value in kwargs.items():
            setattr(self, key, value)



# truck

class Truck(Cars):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        self.texture = 'resources/sprites/garbage_truck.png'
        self.health = 3
        self.max_speed = 0.3

        for key, value in kwargs.items():
            setattr(self, key, value)

# obstacle class inhterited from Sprite class

class Obstascle(Sprite):
    def __init__(self, x, y):
        super().__init__(
            collider = 'box',
            name = 'obstacle',
        )
        self.model = 'quad',
        self.x = x
        self.y = y
        self.scale = 3
        self.enabled = True
        self.always_on_top = True
        self.collision_sound = Audio('resources/sounds/default.wav', loop = False, autoplay = False)

    def destroy(self):  
        self.enabled = False
        self.collision_sound.play()

# health orb - adding health

class HealthOrb(Obstascle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = 'resources/sprites/health_orb.png'
        self.health = 1
        self.name = 'health_orb'
        self.collision_sound = Audio('resources/sounds/health_orb.wav', loop = False, autoplay = False)
    
# speed orb - adding speed 

class SpeedOrb(Obstascle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = 'resources/sprites/speed_orb.png'
        self.speed_increase = 2 
        self.name = 'speed_orb'
        self_collision_sound = Audio('resources/sounds/speed_orb.wav', loop = False, autoplay = False)
    
# coin - adding score

class CoinOrb(Obstascle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = 'resources/sprites/coin_orb.png'
        self.score_increase = 1
        self.name = 'coin_orb'
        self.collision_sound = Audio('resources/sounds/coin_orb.wav', loop = False, autoplay = False)