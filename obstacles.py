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
    # disable rendering 

    def destroy(self):
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
        self.texture = 'resources/sprites/Truck.png',
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
        self.enabled = True
        self.always_on_top = True

    def destroy(self):  
        self.enabled = False

# health orb - adding health

class HealthOrb(Obstascle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = 'resources/sprites/health_orb.png'
        self.health = 1
        self.scale = 3.5
        self.name = 'health_orb'
    
# speed orb - adding speed 

class SpeedOrb(Obstascle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = 'resources/sprites/speed_orb.png'
        self.speed_increase = 2 
        self.scale = 3.5
        self.name = 'speed_orb'
    