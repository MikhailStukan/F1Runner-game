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
        self.road_width = 5.0
        self.speed = self.min_speed
        self.turnspeed = self.min_turnspeed
        self.texture = 'resources/sprites/player.png'
        self.model = 'quad'
        self.name = "player"
        self.score = 0
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
        
        # collider check

        hit_info = self.intersects()

        if hit_info.hit and hit_info.entity.name == "car":
            # handle collision with car and taking damage
            self.take_damage(int(hit_info.entity.health))
            # destroying car which was hit
            hit_info.entity.destroy()
            # reduction amount of score for hitting car, that is based on the health of the car
            self.add_score(int(hit_info.entity.health * -1))
            


    # deriving coordinates from the speed and changing x-axis from the turnspeed
    # border on the right and left of the road 


    def move(self):

        # increasing y coordinate based on speed

        self.y += self.speed

        # checking for road width so player doen't go out of the screen

        if (self.x > self.road_width):
            self.x = self.road_width
        if (self.x < -self.road_width):
            self.x = -self.road_width

        else:
            # handling turning of the player based on the turnspeed
            
            self.x += held_keys['d'] * self.turnspeed
            self.x += held_keys['right arrow'] * self.turnspeed
            self.x -= held_keys['a'] * self.turnspeed
            self.x -= held_keys['left arrow'] * self.turnspeed


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

    # damage player for X of damage, checking for enough lifes

    def take_damage(self, damage):
        if self.life - damage > 0:
            self.life -= damage
        else:
            self.life = 0
            self.disable()
            self.isAlive = False
        

    # adding x life

    def add_life(self, life):
        if(self.life < self.maxlife):
            self.life += life
        else:
            self.life = self.maxlife
    

    
