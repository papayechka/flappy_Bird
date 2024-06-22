from pygame import *
from random import randint
from time import time as timer #імпортуємо функцію для засікання часу, щоб інтерпретатор не шукав цю функцію в pygame модулі time, даємо їй іншу назву самі


mixer.init()
mixer.music.load('song.mp3')
mixer.music.play()
fire_sound = mixer.Sound('dag.ogg')

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))


img_back = "Phon.jpg"
img_hero = "yellow_bird.png"
img_Wall1 = "wall.png"
img_non_killable_Wall1 = "Wall2.png"
img_health = "healthPoint.png"

score = 0
lost = 0
goal = 100
max_lost = 500
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, sixe_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed,speed_y_down):
        super().__init__( sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed)
        self.speed_y_down=speed_y_down
        
    def update(self):
         
        if self.rect.y <=win_height-150:
            self.rect.y += self.speed_y_down
        
        keys = key.get_pressed()
        if keys[K_SPACE] and self.rect.y >= 0:
            self.rect.y -= self.speed
        # if self.rect.y>win_height: 
            

class Wall1(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed,isBot=True,):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        self.isBot=isBot
        self.isPassed=False
        if self.isBot==True:
            self.image = transform.rotate(self.image, 180)

    def update(self):
        self.rect.x -= self.speed
        global lost, score
        if player.rect.x>self.rect.x:
            if self.isPassed == False:
                score = score+0.5
                self.isPassed=True
        if self.rect.x < 0 and self.isBot==False:
            self.kill()

            wall2 = Wall1(img_Wall1, 700, randint(250,500 ), 80, 300,5,False)
            walls.add(wall2)
           
            wall = Wall1(img_Wall1, 700, 0, 80, wall2.rect.y-150,5)
            walls.add(wall)
            
        
             
        if self.rect.x < 0 and self.isBot==True:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

player = Player(img_hero, 150, win_height - 100, 80, 55, 26 ,15)


health_packs = sprite.Group()

walls = sprite.Group()



wall2 = Wall1(img_Wall1, 600, randint(250,500 ), 80, 300,5,False)
walls.add(wall2)
wall = Wall1(img_Wall1, 600, 0, 80, wall2.rect.y-150,5)
walls.add(wall)

wall3 = Wall1(img_Wall1, 350, randint(250,500 ), 80, 300,5,False)
walls.add(wall3)
wall4 = Wall1(img_Wall1, 350, 0, 80, wall3.rect.y-150,5)
walls.add(wall4)




run = True
finish = False
clock = time.Clock()
FPS = 30
rel_time = False  # прапор, що відповідає за перезаряджання
num_fire = 0  # змінна для підрахунку пострілів    


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
      

    if not finish:
        window.blit(background, (0, 0))
        player.update()
        walls.update()
        
        health_packs.update()
        
        health_packs.draw(window)
        player.reset()
        walls.draw(window)
       
        if sprite.spritecollide(player, walls, False):
            life = life - 1
            
        #програш
        if life == 0 or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))


        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font1.render("Рахунок: " + str(score)[0],1, (255,255,255))
        window.blit(text,(10, 20))

        text_lose = font1.render("Пропущенно: " + str(lost),1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        
        
        display.update()

    clock.tick(FPS)
