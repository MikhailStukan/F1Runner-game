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

    # disable rendering 

    def destroy(self):
        self.enabled = False

    def update(self):
        self.y -= self.speed

# pickup 

class Pickup(Cars):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.texture = 'resources/sprites/pickup_green.png'
        self.health = 2
        self.speed = 0.05

        for key, value in kwargs.items():
            setattr(self, key, value)

        
# sedan

class Sedan(Cars):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        self.texture = 'resources/sprites/sedan_yellow.png'
        self.health = 1
        self.speed = 0.1

        for key, value in kwargs.items():
            setattr(self, key, value)



# truck

class Truck(Cars):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        self.texture = 'resources/sprites/Truck.png',
        self.health = 3
        self.speed = 0.02

        for key, value in kwargs.items():
            setattr(self, key, value)
