"""ursina imports"""
from ursina import *

CAR_ACCEL_SOUND_PATH = "resources/sounds/car_acceleration.wav"

class Player(Sprite): # pylint: disable=too-many-instance-attributes
    """player class"""
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
        self.x = None
        self.y = None
        self.life = 3
        self.maxlife = 3
        self.is_alive = True
        self.always_on_top = True
        self.enabled = False
        self.engine_sound = Audio(CAR_ACCEL_SOUND_PATH, loop = True, autoplay = False)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def start_engine(self):
        """start engine sound"""
        self.engine_sound.play()

    def stop_engine(self):
        """stop engine sound"""
        self.engine_sound.stop()

    def update(self):
        """update method"""
        if self.is_alive:
            self.move()
            self.change_speed()
        if self.life <= 0:
            self.disable()
            self.is_alive = False
        hit_info = self.intersects()
        if hit_info.hit: #colliders
            if hit_info.entity.name == "car":
                # handle collision with car and taking damage
                self.take_damage(int(hit_info.entity.health))
                # destroying car which was hit
                hit_info.entity.destroy()
                # reduction amount of score for hitting car, that is based on the health of the car
                self.add_score(int(hit_info.entity.health * -1))
            elif hit_info.entity.name == "health_orb":
                # adding life to player
                self.add_life(hit_info.entity.health)
                # destroying health orb
                hit_info.entity.destroy()
            elif hit_info.entity.name == "speed_orb":
                # increasing speed of player
                self.add_speed(hit_info.entity.speed_increase)
                # destroying speed orb
                hit_info.entity.destroy()
            elif hit_info.entity.name == "score_orb":
                # adding score to player
                self.add_score(hit_info.entity.score_increase)
                # destroying score orb
                hit_info.entity.destroy()

    def move(self):
        """changing player coordinates"""
        self.y += self.speed # increasing y coordinate based on speed
        # checking for road width so player doen't go out of the screen
        if self.x > self.road_width:
            self.x = self.road_width
        if self.x < -self.road_width:
            self.x = -self.road_width
        else:
            # handling turning of the player based on the turnspeed
            self.x += held_keys['d'] * self.turnspeed
            self.x += held_keys['right arrow'] * self.turnspeed
            self.x -= held_keys['a'] * self.turnspeed
            self.x -= held_keys['left arrow'] * self.turnspeed
    def change_speed(self):
        """changing speed and turnspeed when the keys are pressed (acceleration) and deceleration"""
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

    def add_score(self, score):
        """increasing score"""
        self.score += score

    def take_damage(self, damage):
        """taking damage"""
        if self.life - damage > 0:
            self.life -= damage
        else:
            self.life = 0
            self.disable()
            self.is_alive = False

    def add_speed(self, speed):
        """adding speed to player"""
        if self.speed < self.max_speed:
            self.speed += speed
        else:
            self.speed = self.max_speed

    def add_life(self, life):
        """adding life to player"""
        if self.life < self.maxlife:
            self.life += life
        else:
            self.life = self.maxlife
