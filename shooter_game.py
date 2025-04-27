from pygame import *
from random import randint
from time import time as tm

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

lost = 0
score = 0
ammo = 10
ammo_reload = False

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
explosion_sound = mixer.Sound('vzriv.ogg')
win_sound = mixer.Sound('pobeda.ogg')
lose_sound = mixer.Sound('proigrish.ogg')

run = True
finish = False
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_size_x, player_size_y, player_speed):
        super().__init__()
        self.size_x = player_size_x
        self.size_y = player_size_y
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 600)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(Enemy):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 600)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('rocket.png', 250, 420, 65, 65, 5)

bullets = sprite.Group()
enemies = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(80, 600), 0, 65, 65, randint(1, 2))
    enemies.add(enemy)
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(80, 600), 0, 65, 65, randint(2, 3))
    asteroids.add(asteroid)
bullets = sprite.Group()


font.init()
text_font = font.SysFont('Arial', 32)
text_font2 = font.SysFont('Arial', 64)
text_font3 = font.SysFont('Arial', 40)

win_text = text_font2.render('ВЫ ПОБЕДИЛИ!', 1, (50, 255, 50))
lose_text = text_font2.render('ВЫ ПРОИГРАЛИ!', 1, (255, 50, 50))
restart_text = text_font3.render('Нажмите R чтобы начать заново', 1, (255, 255, 255))

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if ammo <= 0:
                    ammo_reload = True
                    current_time = tm()
                    ammo = 10
                if ammo_reload:
                    if tm() - current_time >= 2:
                        ammo_reload = False
                else:
                    fire_sound.play()
                    player.fire()
                    ammo -= 1
            elif finish == True:
                if e.key == K_r:
                    finish = False
                    score = 0
                    lost = 0
                    ammo = 10
                    ammo_reload = False
                    for b in bullets:
                        b.kill()
                    for e in enemies:
                        e.kill()
                    for a in asteroids:
                        a.kill()

                    time.delay(100)
                    for i in range(5):
                        enemy = Enemy('ufo.png', randint(80, 600), 0, 65, 65, randint(1, 2))
                        enemies.add(enemy)
                    for i in range(3):
                        asteroid = Asteroid('asteroid.png', randint(80, 600), 0, 65, 65, randint(2, 3))
                        asteroids.add(asteroid)
    if finish != True:
        window.blit(background, (0, 0))
        score_text = text_font.render('Счёт: ' + str(score), 1, (50,255,50))
        window.blit(score_text, (10, 20))
        lost_text = text_font.render('Пропущено: ' + str(lost), 1, (255,50,50))
        window.blit(lost_text, (10, 50))
        bullet_text = text_font.render('Патроны: ' + str(ammo), 1, (255, 255, 255))
        window.blit(bullet_text, (10, 80))
        if ammo_reload:
            reload_text = text_font.render('Перезарядка...', 1, (200, 30, 30))
            window.blit(reload_text, (250, 450))
        player.update()
        bullets.update()
        player.reset()
        enemies.update()
        asteroids.update()
        enemies.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        sprite_collide2 = sprite.groupcollide(asteroids, bullets, False, False)
        sprite_collide = sprite.groupcollide(enemies, bullets, True, True)
        for s in sprite_collide:
            score = score + 1
            enemy = Enemy('ufo.png', randint(80, 600), 0, 65, 65, randint(1, 2))
            enemies.add(enemy)
            explosion_sound.play()

        if lost >= 6 or sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            window.blit(lose_text, (100, 200))
            window.blit(restart_text, (65, 260))
            finish = True
            lose_sound.play()

        if score >= 10:
            window.blit(win_text, (100, 200))
            window.blit(restart_text, (65, 260))
            finish = True
            win_sound.play()

        display.update()
    clock.tick(60)