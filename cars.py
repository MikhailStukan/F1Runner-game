from ursina import *


class Cars(Sprite):
    def __init__(self):
        super().__init__(
            collider = 'box',
        )
        self.model = 'quad',
        self.x = 0,
        self.y = 0,
        self.z = 0,
        self.scale = 3.5
        self.enabled = True
        self.always_on_top = True

    def destroy(self):
        self.enabled = False

class Pickup(Cars):
    def __init__(self, x, y, **kwargs):
        super().__init__()
        self.texture = 'resources/sprites/pickup_green.png'
        self.x = x
        self.y = y
        self.speed = 0.05

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.y -= self.speed
        

class Sedan(Cars):
    def __init__(self, x, y, **kwargs):
        super().__init__()
        self.texture = 'resources/sprites/sedan_yellow.png'
        self.x = x
        self.y = y
        self.speed = 0.1

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.y -= self.speed

class Truck(Cars):
    def __init__(self, x, y, **kwargs):
        super().__init__()
        self.texture = 'resources/sprites/Truck.png',
        self.x = x
        self.y = y
        self.speed = 0.02

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.y -= self.speed