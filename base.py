from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w = 65, h = 65, speed = 5):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def reset(self, window: Surface):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, img, x, y, w=65, h=65, speed=5):
        super().__init__(img, x, y, w, h, speed)
        self.bullets = sprite.Group()
        self.score = 0 # for killing the ene

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
        # if keys[K_SPACE]:
        #     mixer.Sound("fire.ogg").play()
        #     self.fire()
    
    def fire(self):
        bullet = Bullet(
            "bullet.png",
            self.rect.centerx,
            self.rect.top,
            10,
            15,
            10
        )
        self.bullets.add(bullet)



class Enemy(GameSprite):
    pass_scr = 0 # for passing the player
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500 - self.image.get_width():
            Enemy.pass_scr += 1 # increase the missing
            self.rect.y = 0
            self.rect.x = randint(
                self.image.get_width(),
                700 - self.image.get_width()
            )

# bullet class
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()