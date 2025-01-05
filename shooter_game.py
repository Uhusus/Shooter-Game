# main.py
#Create your own shooter
from pygame import *
from base import *
from random import randint

font.init()
font_tem = font.Font(None, 20)


width = 700
height = 500
window = display.set_mode((width, height))

display.set_caption("Shooter Game")

background = transform.scale(
    image.load('galaxy.jpg'),
    (width, height)
)

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

fire_sound = mixer.Sound("fire.ogg")
shoot = mixer.Sound('fire.ogg')


player = Player('rocket.png', 300, 420, 60,60)
enemies = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    enemy = Enemy('ufo.png', 
                  x=randint(15, 610), 
                  y=0, 
                  w=60,h=60,
                  speed=randint(1, 3))
    enemies.add(enemy)

for i in range(3):
    aster = Enemy('asteroid.png',
                  x=randint(15,619),
                  y=0,
                  w=60,h=60,
                  speed=randint(1,2))
    asteroids.add(aster)

game = True
finish = False
while game:
    if not finish:
        window.blit(background, (0, 0))
        player.reset(window)
        player.update()
        player.bullets.draw(window)
        player.bullets.update() 


        enemies.draw(window)
        enemies.update()

        asteroids.draw(window)
        asteroids.update()

        sprite.groupcollide(player.bullets, asteroids, True, False)

        player_asteriod = sprite.spritecollide(
            player,
            asteroids,
            False
        )
        player_collided = sprite.spritecollide(
            player,
            enemies,
            False
        )
        # lose condition
        if player_collided or Enemy.pass_scr >= 3 or player_asteriod:
            finish = True
            lose = font.Font(None, 70).render(
                "YOU LOSE!",
                True,
                (255, 0, 0)
            )
            window.blit(lose, (200, 200))
        
        # winning condition
        if player.score > 10:
            finish = True
            win = font.Font(None, 70).render(
                "YOU WIN!",
                True,
                (0, 255, 0)
            )
            window.blit(win, (200, 200))

        
        killing_list = sprite.groupcollide(player.bullets, enemies, True, True)
        for killed in killing_list:
            player.score += 1
            new_enemy = Enemy('ufo.png', 
                  x=randint(15, 610), 
                  y=0, 
                  w=60,h=60,
                  speed=randint(1, 3))
            enemies.add(new_enemy)
        
        # statistics
        score = font_tem.render(
            f"Score: {player.score}",
            True,
            (255,255,255)
        )
        missing = font_tem.render(
            f"Missing: {Enemy.pass_scr}",
            True,
            (255,255,255)
        )
        window.blit(score, (15, 30))
        window.blit(missing, (15, 45))

    else:
        for e in enemies:
            e.kill()

        for a in asteroids:
            a.kill()
        
        for b in player.bullets:
            b.kill()
        player.score = 0
        Enemy.pass_scr = 0

        time.delay(3000)

        finish = False

        for i in range(5):
            enemy = Enemy('ufo.png', 
                        x=randint(15, 610), 
                        y=0, 
                        w=60,h=60,
                        speed=randint(1, 3))
            enemies.add(enemy)

        for i in range(3):
            aster = Enemy('asteroid.png',
                        x=randint(15,619),
                        y=0,
                        w=60,h=60,
                        speed=randint(1,2))
            asteroids.add(aster)


    for e in event.get():
        if e.type == QUIT:
            game = False
        
        if not finish and e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                # fire_sound.play()

    
    clock.tick(FPS)
    display.update()