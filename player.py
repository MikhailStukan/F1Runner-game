from ursina import *

# Player class

class Player(Sprite):
    def __init__(self, **kwargs):
        super().__init__(
            collider = 'box',
        )
        self.max_speed = .5
        self.min_speed = .1
        self.acceleration = .01
        self.min_turnspeed = .1
        self.max_turnspeed = .5
        self.speed = self.min_speed
        self.turnspeed = self.min_turnspeed
        self.texture = 'resources/sprites/player.png'
        self.model = 'quad'
        self.name = "player"
        self.score = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.scale = 3
        self.life = 3
        self.maxlife = 3
        self.isAlive = True
        self.always_on_top = True
        self.enabled = False

        for key, value in kwargs.items():
            setattr(self, key, value)



    # updating player position

    def update(self):
        if(self.isAlive):
            self.move()
            self.change_speed()
        if(self.life <= 0):
            self.disable()
            self.isAlive = False
        
        hit_info = self.intersects()
        if hit_info.hit:
            if(self.life > 0):
                self.take_damage(1)
                hit_info.entity.destroy()

    # deriving coordinates from the speed and changing x-axis from the turnspeed

    def move(self):
        self.y += self.speed
        self.x += held_keys['d'] * self.turnspeed
        self.x += held_keys['right arrow'] * self.turnspeed
        self.x -= held_keys['a'] * self.turnspeed
        self.x -= held_keys['left arrow'] * self.turnspeed
        self.rotation

    # changing speed and turnspeed when the keys are pressed (acceleration) and deceleration

    def change_speed(self):
        if self.speed < self.max_speed and self.turnspeed < self.max_turnspeed:
            if held_keys['w'] or held_keys['up arrow']:
                self.speed += self.acceleration
                self.turnspeed += self.acceleration
        else:
            self.speed = self.max_speed
            self.turnspeed = self.max_turnspeed
        
        if self.speed > self.min_speed and self.turnspeed > self.min_turnspeed:
            if held_keys['s'] or held_keys['down arrow']:
                self.speed -= self.acceleration
                self.turnspeed -= self.acceleration
            if held_keys['space']:
                self.speed -= self.acceleration * 2
                self.turnspeed -= self.acceleration * 2
        if self.speed < self.min_speed:
            self.speed = self.min_speed
        if self.turnspeed < self.min_turnspeed:
            self.turnspeed = self.min_turnspeed

    # adding score

    def add_score(self, score):
        self.score += score

    # damage player for X of damage

    def take_damage(self, damage):
        self.life -= damage

    # adding x life

    def add_life(self, life):
        if(self.life < self.maxlife):
            self.life += life
        else:
            self.life = self.maxlife
    

    
