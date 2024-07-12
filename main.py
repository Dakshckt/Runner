import pygame
import os
import random
from os.path import join

WIDTH , HEIGHT = 900 , 600
WIN = pygame.display.set_mode((WIDTH , HEIGHT))

pygame.init()

class player:
    def __init__(self , x , y, width , height):
        self.x = x 
        self.y = y
        self.originalY = y
        self.originalHeight = height
        self.width , self.height = width , height
        self.count = 0
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.isDown = False
        self.downCount = 10
        self.slideSound = pygame.mixer.Sound("./AllPhotos/slideSound.mp3")
        self.jumpSound = pygame.mixer.Sound("./AllPhotos/jmupSound.mp3")
        self.image()
        self.imageLoad()
    
    def image(self):
        self.boyRun = [pygame.image.load(f"./AllPhotos/R{i + 1}.png") for i in range(12)]
        self.boyRun = [pygame.transform.scale(img , (self.width , self.height)) for img in self.boyRun]

    def imageLoad(self):
        self.rollImage = pygame.image.load(os.path.join("AllPhotos","fall.png"))
        self.rollImage = pygame.transform.scale(self.rollImage , (self.width , self.height))
        self.rollImage = pygame.transform.rotate(self.rollImage , 45)
        self.jumpImage = pygame.image.load(os.path.join("AllPhotos","jump.png"))
        self.fallImage = pygame.image.load(os.path.join("AllPhotos","fall.png"))
        self.jumpImage = pygame.transform.scale(self.jumpImage , (self.width , self.height))
        self.fallImage = pygame.transform.scale(self.fallImage , (self.width , self.height))

    def draw(self , WIN):
        self.hitbox = (self.x + 12, self.y + 15 , self.width - 22 , self.height - 18)
        self.move()
        if self.count+1 >= 36:
            self.count = 0
        if self.x > 300:
            self.x = 300
        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.isJump = True
            # self.jumpSound.play()
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.isDown = True
            # self.slideSound.play()

        if self.isDown == True:
            self.isJump = False
        if self.isJump == True:
            self.isDown = False


        if self.isJump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y = self.y - ((self.jumpCount ** 2) / 5) * neg
                self.jumpCount -= 0.5
                if neg == 1:
                    WIN.blit(self.jumpImage , (self.x , self.y))
                    # pygame.draw.rect(WIN , (0 , 0 , 255) , self.hitbox , 1)
                elif neg == -1:
                    WIN.blit(self.fallImage , (self.x , self.y))
                    # pygame.draw.rect(WIN , (0 , 0 , 255) , self.hitbox , 1)
            else:
                self.jumpCount = 10
                self.isJump = False
        else:
            self.jumpCount = 10
            self.isJump = False
            if not(self.isDown):
                WIN.blit(self.boyRun[self.count // 3] , (self.x , self.y))
                # pygame.draw.rect(WIN , (0 , 0 , 255) , self.hitbox , 1)
            

        if self.isDown:
            self.isJump = False
            
            if self.downCount <= 35:
                self.downCount += 1
                # self.height = 70
                self.y = self.originalY + 30
                WIN.blit(self.rollImage , (self.x , self.y))
                # pygame.draw.rect(WIN , (0 , 0 , 255) , self.hitbox , 1)
            else:
                self.isDown = False
                self.downCount = 10
                self.height = self.originalHeight
                self.y = self.originalY
        
       

    def move(self):
        self.count += 1
        self.x += self.vel  


class Enemy:
    def __init__(self , x , y , width , height , image , vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel 
        self.enemy = []
        self.displayImage = image
        self.image = pygame.image.load(os.path.join("AllPhotos",self.displayImage))
        self.image = pygame.transform.scale(self.image , (self.width , self.height))
        
    def draw(self , WIN , hitbox1 , hitbox2):
        self.hitbox1 = hitbox1
        self.hitbox2 = hitbox2
        self.move()
        
        WIN.blit(self.image , (self.x , self.y))
        # pygame.draw.rect(WIN , (255,0,0) , self.hitbox1 , 1)
        # pygame.draw.rect(WIN , (0,0,255) , self.hitbox2 , 1)
    
    def move(self):
        self.x -= self.vel
    


def get_floor(name , width , height , x , y):
    backgroundFloor = pygame.image.load(join('AllPhotos',name))
    backgroundFloor = pygame.transform.scale(backgroundFloor , (width , height))

    floorBoxs = []

    for i in range(WIDTH // width + 2):
        box = (i * width - x , y)
        floorBoxs.append(box)

    return floorBoxs , backgroundFloor        


def get_background(name):
    backgroundTile = pygame.image.load(join('AllPhotos',name))

    width = backgroundTile.get_width()
    height = backgroundTile.get_height()
    
    tiles = []
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            box = (i*width , j*height)
            tiles.append(box)

    return tiles , backgroundTile


def gameOver():
    pygame.init()

    gameOverImage = pygame.image.load("./AllPhotos/gameOver.webp")
    gameOverImage = pygame.transform.scale(gameOverImage , (400 , 400))
    WIN.blit(gameOverImage , (250 , -50))
    font = pygame.font.SysFont('comicsans' , 20 , True )
    ReplayText = font.render("Enter `p` to replay the game" , 1 , (0,0,0))
    QuitText = font.render("Enter `q` to replay the game" , 1 , (0,0,0))
    WIN.blit(ReplayText , (30 , 300))
    WIN.blit(QuitText , (580 , 300))

    pygame.display.update()

    isStart = False
    while not isStart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if pygame.key.get_pressed()[pygame.K_p]:
            print("P button Pressed")
            isStart = True
            main()
        elif pygame.key.get_pressed()[pygame.K_q]:
            print("Q button Pressed")
            pygame.quit()
        
         


def drawWindow(WIN  , score, tiles , imageTile , floorBoxs , imageFloor , boy , drawEnemy):
    for box in tiles:
        WIN.blit(imageTile , box)

    for box in floorBoxs:
        WIN.blit(imageFloor , box)
    
    for enemy in drawEnemy:
        if enemy.displayImage == 'GrayBat.png':
            hitbox1 = enemy.x + 18 , enemy.y + 20 , enemy.width - 45 , enemy.height - 60
            hitbox2 = enemy.x + 60 , enemy.y + 20 , enemy.width - 100 , enemy.height - 40
        elif enemy.displayImage == 'BlueParrat.png':
            hitbox1 = enemy.x + 20 , enemy.y + 35 , enemy.width - 60 , enemy.height - 70
            hitbox2 = enemy.x + 50 , enemy.y + 20 , enemy.width - 100 , enemy.height - 50
        elif enemy.displayImage == 'BlueSnail.png':
            hitbox1 = enemy.x + 30 , enemy.y + 20 , enemy.width - 70 , enemy.height - 40
            hitbox2 = enemy.x + 30 , enemy.y + 20 , enemy.width - 70 , enemy.height - 30
        elif enemy.displayImage == 'GreenMuk.png':
            hitbox1 = enemy.x + 30 , enemy.y + 20, enemy.width - 90 , enemy.height - 20
            hitbox2 = enemy.x + 30 , enemy.y + 20, enemy.width - 90 , enemy.height - 20
        elif enemy.displayImage == 'TreeLog.png':
            hitbox1 = enemy.x + 15 , enemy.y + 25 , enemy.width - 35 , enemy.height - 50 
            hitbox2 = enemy.x + 15 , enemy.y + 25 , enemy.width - 35 , enemy.height - 50 

        enemy.draw(WIN , hitbox1 , hitbox2)
    
    boy.draw(WIN)

    for enemy in drawEnemy:
        if boy.hitbox[0] + boy.hitbox[2] >= enemy.hitbox1[0] and boy.hitbox[0] <= enemy.hitbox1[0] + enemy.hitbox1[2] and boy.hitbox[1] + boy.hitbox[3] >= enemy.hitbox1[1] and boy.hitbox[1] <= enemy.hitbox1[1] + enemy.hitbox1[3] or boy.hitbox[0] + boy.hitbox[2] >= enemy.hitbox2[0] and boy.hitbox[0] <= enemy.hitbox2[0] + enemy.hitbox2[2] and boy.hitbox[1] + boy.hitbox[3] >= enemy.hitbox2[1] and boy.hitbox[1] <= enemy.hitbox2[1] + enemy.hitbox2[3]:
            gameOver()

    pygame.display.update()


def main():
    pygame.init()
    run = True 
    backgroundTile = 'Blue.png'
    floor = 'Idle.png'
    floorWidth , floorHeight = 100 , 100   
    boy = player(100 , 400 , 90 , 100)
    x , y = 0 , 500
    backgroundSpeed = 6
    speedInc = 0.004
    score = 0
    music = pygame.mixer.music.load('./AllPhotos/subwaySurfer.mp3')
    pygame.mixer.music.play(-1)

    FPS = 60

    clock = pygame.time.Clock()
    clockCount = 0
    CLOCKINCREMENT = 2000

    iteration = 0
    first = True
    go = False

    standCount = 0


    drawEnemy = []

    while run:
        dt = clock.tick(FPS)

        while first:
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    first = False
                    run = False

            standing = [pygame.image.load(f'./AllPhotos/I{i+1}.png') for i in range(11)]
            standing = [pygame.transform.scale(img , (boy.width , boy.height)) for img in standing]

            if standCount+1 >= 22:
                standCount = 0

            tile , imageTile = get_background(backgroundTile)
            floorBoxs , imageFloor = get_floor(floor , floorWidth , floorHeight , x , y)
            for box in tile:
                WIN.blit(imageTile , box)
            for box in floorBoxs:
                WIN.blit(imageFloor , box)

            WIN.blit(standing[standCount // 2] , (boy.x , boy.y))
            standCount += 1
            
            runnerTitle = pygame.image.load('AllPhotos/runnerTitle.png')
            runnerTitle = pygame.transform.scale(runnerTitle , (500 ,150))
            WIN.blit(runnerTitle , (200 , 50))

            font1 = pygame.font.SysFont('comicsans' , 20 , True)
            text1 = font1.render('Press `s` to start the game' , 1 , (0,0,0))
            WIN.blit(text1 , (300 , 200))


            pygame.display.update()

            if pygame.key.get_pressed()[pygame.K_s]:
                go = True
                first = False
        
        if go:
            clockCount += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False        
            
            x += backgroundSpeed
            if x >= floorWidth:
                x = 0
            
            backgroundSpeed += speedInc
            backgroundSpeed = min(backgroundSpeed , 15)
            
            iteration += 1

            if clockCount > CLOCKINCREMENT:
                if iteration > 1000:
                    CLOCKINCREMENT = 1000
                elif iteration > 2500:
                    CLOCKINCREMENT = 500
                elif iteration > 5000:
                    CLOCKINCREMENT = 300

                airEnemy = ['GrayBat.png','BlueParrat.png']
                groundEnemy = ['BlueSnail.png','GreenMuk.png','TreeLog.png']
                enemyX = WIDTH  
                enemyY = random.choice([400 , 340])
                if enemyY == 400:
                    enemyImage = random.choice(groundEnemy)
                elif enemyY == 340:
                    enemyImage = random.choice(airEnemy)
                if enemyImage == "BlueSnail.png" or enemyImage == 'GreenMuk.png':
                    enemyWidth , enemyHeight = 180 , 100
                elif enemyImage == 'GrayBat.png':
                    enemyWidth , enemyHeight = 150 , 100
                elif enemyImage == 'TreeLog.png':
                    enemyWidth , enemyHeight = 120 , 120
                else:
                    enemyWidth , enemyHeight = 150 , 120
                
                enemy = Enemy(enemyX , enemyY , enemyWidth , enemyHeight , enemyImage , backgroundSpeed )
                drawEnemy.append(enemy)
                clockCount = 0
            
            for enemy in drawEnemy:
                enemy.vel = backgroundSpeed

            tile , imageTile = get_background(backgroundTile)
            floorBoxs , imageFloor = get_floor(floor , floorWidth , floorHeight , x , y)

            drawWindow(WIN , score , tile , imageTile , floorBoxs , imageFloor , boy , drawEnemy)
    pygame.quit()


if __name__ == '__main__':
    main()