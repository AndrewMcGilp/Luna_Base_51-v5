#Luna Base 51 -Pi- by Andrew McGilp March-2020
#A Python Pygame for the Raspberry Pi
# 'Luna Base 51-v5-11'

"""
Notice:

  Please note that this software is used entirely at your own RISK and comes with 
  absolutely no guarantee or warrantee what so ever and by using this software 
  you agree to these terms. It is free to be used by a private individual and
  copy and distribute verbatim copies for free but not free for any commercial
  use without permission. changing the code is not allowed.
  
"""

import pygame, math, sys, random
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480#for small screen
SCR_RES = 0
SCR_FULL = 0
SND_LEVEL = 3
IMG_NO = 0
MENU_SET = 1#First time run

#Color    R    G    B
WHITE  = (255, 255, 255)
GREEN  = (0  , 255,   0)
RED    = (255, 0  ,   0)
BLUE   = ( 80, 150, 255)
YELLOW = (255, 255,  80)
BR_COLOR = BLUE

LEFT = 1
MIDDLE = 2
RIGHT = 3
UP = 4
DOWN = 5
MENU_NO = 0

# All the bool stuff true/false
done = False
showMsg = False
pauseGame = False
endGame = False
editName = False
testMode = False
changeCol = 0

#Player Position
posX = 0
posY = 0
towerPosY = 0
#Mouse Pos
posx = 0
posy = 0
loopCount = 0
numIndex = 0
imgSelect = 0

char = '_'
strName0 = 'Pi_0.........'#Edit this Name to yours in Hall of Fame, use right mouse button to delete! 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, 16)# plays better in full screen mode
pygame.display.set_caption('Luna Base 51-v5')
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

#----------Load sprites images sound and fonts----------
#Load Font's
myHudFont = pygame.font.SysFont("Courier", 18)#Use a mono block font
mySelFont = pygame.font.SysFont("Courier", 24)
myMsgFont = pygame.font.SysFont("Courier", 92)

strMsg = myMsgFont.render('Update ME-0!', True, GREEN)
strMsg1 = myHudFont.render('Update ME-1!', True, WHITE)

settList = []
nameList = []
charList = ['','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','U','R','S','T','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','$','@','*','&','!','_']
sndTrxList = ['NONE','Sounds/SndTrx1.ogg']

#Load image's
bgImg = pygame.image.load('Stars_Earth1.png').convert()
startImg = pygame.image.load('GameStart1.png').convert_alpha()
underLayImg = pygame.image.load('UnderLay1.png').convert_alpha()
overLayImg = pygame.image.load('OverLay1.png').convert_alpha()
crossHairImg = pygame.image.load('CrossHair.png').convert_alpha()
baseImg = pygame.image.load('MoonBase6.png').convert_alpha()
tower0Img = pygame.image.load('Tower1.png').convert_alpha()
tower1Img = pygame.image.load('Tower3.png').convert_alpha()
coverImg = pygame.image.load('MtlPlate2.png').convert_alpha()
laserImg = pygame.image.load('Laser.png').convert_alpha()
alienImg1 = pygame.image.load('ufoBug1.png').convert_alpha()#
alienImg2 = pygame.image.load('bugTop2.png').convert_alpha()#
alienImg3 = pygame.image.load('ufoBug2.png').convert_alpha()#Alien ufoBug damaged
holeImg1= pygame.image.load('hole7.png').convert_alpha()#
asteroidImg3 = pygame.image.load('Asteroid3.png').convert_alpha()#
expoldImg = pygame.image.load('Explod5.png').convert_alpha()
damageImg = pygame.image.load('Damage3.png').convert_alpha()
playerImg = pygame.image.load('player4.png').convert_alpha()
ufoImg1 = pygame.image.load('UFO4.png').convert_alpha()
ufoImg2 = pygame.image.load('UFO6.png').convert_alpha()
missileImg = pygame.image.load('Bomb2.png').convert_alpha()
powerUpImg = pygame.image.load('PowerUp1.png').convert_alpha()
shieldUpImg = pygame.image.load('ShieldUp1.png').convert_alpha()
shieldGridImg = pygame.image.load('ShieldGrid.png').convert_alpha()

#Init and Load Sounds
if (pygame.mixer.get_init() != None):
    pygame.mixer.pre_init(44100,16, 2, 4096)#pygame.mixer.init()
    pygame.mixer.set_reserved(4)
    
    laserSnd = pygame.mixer.Sound('laser.ogg')
    explodSnd = pygame.mixer.Sound('explos.ogg')
    btnSnd = pygame.mixer.Sound('btnSound.ogg')
    buzzSnd = pygame.mixer.Sound('Buzzer4.ogg')
    pwrDnSnd = pygame.mixer.Sound('powerDown.ogg')
    pwrUpSnd = pygame.mixer.Sound('powerUp.ogg')
    drillSnd = pygame.mixer.Sound('DrillSound4.ogg')
    hitSnd = pygame.mixer.Sound('hitSound2.ogg')
    
else:
    print('ERROR_:_No sound mixer!')
    done = True

#Global variables
hiScore = 0
score = 0
ufosToShoot = 0
bonusPoints = 0
levelNo = 0
health = 0
oldHealth = 0
rank = 0
rndRangeY = -400
shieldLevel = 0
bombCount = 0
vibePosX  = 0
vibeTime = 0

# The player sprite
player_list = pygame.sprite.Group()
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.myTexture1 = playerImg
        self.position = (posX, posY)
        self.direction = 0
        self.rect = self.myTexture1.get_rect()
        self.radius = int(self.rect.width / 2)#* .90
        if (testMode):
            pygame.draw.rect(self.myTexture1, RED, self.rect, 1)
            pygame.draw.circle(self.myTexture1, YELLOW, self.rect.center, self.radius, 1)
            
    def update(self):

        self.position = (posX, posY)
        tan = math.atan2((posy - posY), (posx - posX))
        deg = round(math.degrees(tan), 0)
        self.dir = -(deg + 90)
        if (self.dir < 80 and self.dir > -80):
            self.direction = self.dir
        self.image = pygame.transform.rotate(self.myTexture1, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def fireLaser(self):#Fire the laser

        laser = Laser(self.direction)
        laser_list.add(laser)
        laser.rect.x = posX
        laser.rect.y = posY
        if SND_LEVEL > 0:
            
            PlaySound(0)       
       
#Add the player
player = Player()
player_list.add(player)

# The laser sprite
laser_list = pygame.sprite.Group()
class Laser(pygame.sprite.Sprite):

    def __init__(self, Direction):
        super().__init__()
        self.myTexture1 = laserImg
        self.position = (posX, posY)# player position
        self.speed = 40
        self.direction = Direction
        self.image = pygame.transform.rotate(self.myTexture1, self.direction)
        self.rect = self.image.get_rect()
        self.radius = 3
        self.x = int(self.rect.width / 2 - 3)
        self.y = int(self.rect.height / 2 - 3)
        if (testMode):
            pygame.draw.rect(self.image, YELLOW, (self.x, self.y, 6, 6), 1)
            pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 1)
            
    def update(self):
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += - self.speed * math.sin(rad)
        y += -self.speed * math.cos(rad)
        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.speed = 5
        
        if (self.rect.y < -20 or self.rect.y > SCREEN_HEIGHT + 20 or self.rect.x < -10 or self.rect.x > SCREEN_WIDTH + 10):
            self.kill()
            
    def takeHit(self):
        self.kill()
        
#The asteroid stuff
asteroid_list = pygame.sprite.Group()
class Asteroid(pygame.sprite.Sprite):
    
    def __init__(self, speedY, Type, image, size, rot, posX, posY):
        super().__init__()
        self.image = image
        self.image = pygame.transform.rotate(image, rot)
        self.image = pygame.transform.scale(self.image, (size , size))
        self.rect = pygame.Rect(self.image.get_rect())
        self.radius = int(self.rect.width / 2)
        if (testMode):
            pygame.draw.rect(self.image, RED, self.rect, 1)
            pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius, 1)
        self.rect.x = posX
        self.rect.y = posY
        self.type = Type
        self.speedY = speedY
        self.health = 10
        
    def update(self):

        if (self.rect.y > SCREEN_HEIGHT -50):
            self.giveHit()
        else:
            self.rect.y += self.speedY
        
    def takeHit(self):
        
        global score
        global health
        global oldHealth

        mag = 2
        num = 0
        
        if (self.type == 0):#Bomb
            score += 40 * rank
            self.health -= 10
            mag = 4         
        elif (self.type == 1):#Asteroid
            score += 10
            self.health -= 10
        elif (self.type == 2):#Health shield icon
            num = 1
            self.health -= 10
            PlaySound(5)
            CreateShields() 
        elif (self.type == 3):#Power up icon
            num = 2 
            score += 50
            if(health > 0):
                health += 50
            PlaySound(5)
            self.health -= 10
             
            if (health == oldHealth):
                oldHealth = health

        elif (self.type == 4):#small alien craft must shoot two times
            PlaySound(7)
            self.image = image = alienImg3
            self.health -= 5
            score += 20

        if (self.health <= 0):
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, mag, num)
            self.kill()
        
    def giveHit(self):#Hits player and leaves damage

        global health

        if (self.type == 0):#Bomb
            CreateDamage(self.rect.x + 20, self.rect.y, 50, 0)
            CreateDamage(self.rect.x - 25, self.rect.y + 10, 50, 0)
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, 8, 0)
            health -= 50
            
        elif (self.type == 1):#Asteroid
            health -= 10
            CreateDamage(self.rect.x - 5, self.rect.y - 5, 10, 0)
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, 2, 0)
            
        elif (self.type == 2):#Health shield icon
            #PlaySound(4)
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, -2, 1)
            
        elif (self.type == 3):#Power Up icon
            #PlaySound(4)
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, -2, 2)

        elif (self.type == 4):#Alien ship
            if (self.health <= 5):#Crash land and explod
                CreateDamage(self.rect.x - 5, self.rect.y - 5, 10, 0)
                CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, 2, 0)                
                health -= 10
            else:
                CreateDamage(self.rect.x - 5, self.rect.y -5, 10, 1)#Land and make a hole in the base
                CreateEffectsFX(self.rect.x, self.rect.y + 10, self.rect.width, -2, 3)
                health -= 20
            
        self.kill()
        
            
    def removeMe(self):#Make me shrink or explod if it hits the shield and leave no damage
        
        if (self.type == 0 or self.type == 1):
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, 2, 0)
            
        elif (self.type == 2):
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, -2, 1)
            
        elif (self.type == 3):
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, -2, 2)

        elif (self.type == 4):
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, 2, 0)
            
        self.kill()
        
#Create Ufo's aka Mothership or UFO's
ufo_list = pygame.sprite.Group()
class Ufo(pygame.sprite.Sprite):
    
    def __init__(self, speed, posX, posY):
        super().__init__()
        self.image = ufoImg1
        self.timer = 0
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = posX
        self.rect.y = posY
        self.health = 100
        self.speed = speed
        self.radius = int(self.rect.width * .35 / 2)
        self.x = int(0)
        self.y = int(self.rect.height * .25)
        self.w = int(self.rect.width)
        self.h = int(self.rect.height * .50)        
        if (testMode):
            pygame.draw.rect(self.image, RED, (self.x, self.y, self.w, self.h), 1)
            pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius, 1)
            
    def update(self):
        
        if (self.timer > 0):
            self.timer -= 1
            self.image = ufoImg2
        else:
            self.image = ufoImg1
        
        if (self.rect.x > SCREEN_WIDTH + 600 or self.rect.x < -600):
            self.kill()
        else:
            self.rect.x += self.speed
        
    def takeHit(self):
        
        global bombCount
        global score
        global bonusPoints
        global ufosToShoot
        
        PlaySound(7)
        self.timer = 5
        dropY = self.rect.bottom - 25
        
        if (self.rect.x > 80 and self.rect.x < 600 and self.speed > -5 and self.speed < 5):
            
            self.speed = self.speed * 2
            bombCount += 1
                
            if (self.speed > 0):
                dropX = self.rect.x + 40
            else:
                dropX = self.rect.x + 30               

            if (bombCount == 3):
                CreatePowerUpIcn()
            elif (bombCount == 6):
                CreateShieldIcn()
                bombCount = 0
                
            CreateMissile(dropX, dropY)
            score += 20

        else: #add bonus UFOs and points
                       
            if (self.speed == 5 or self.speed == -5):
                ufosToShoot -= 1
                bonusPoints += 50
                self.speed = self.speed * 4        
           
#Explosion or implosion effect     
effectsFX_list = pygame.sprite.Group()       
class EffectsFX(pygame.sprite.Sprite):
    
    def __init__(self, posx, posy, size, mag, num):
        super().__init__()
        if (num == 0):
            self.myTexture1 = expoldImg
        elif (num == 1):
            self.myTexture1 = shieldUpImg
        elif (num == 2):
            self.myTexture1 = powerUpImg
        else:
            self.myTexture1 = alienImg2

        self.image = self.myTexture1
        self.rect = pygame.Rect(self.myTexture1.get_rect())
        self.rect.x = posx
        self.rect.y = posy
        self.timer = 0
        self.size = size
        self.mag = mag
       
    def update(self):
        
        self.size += self.mag
        if (self.size < 0):
            self.size = 0
        self.rect.y -= int(self.mag * 0.5)
        self.rect.x -= int(self.mag * 0.5)
        self.image = pygame.transform.scale(self.myTexture1, (self.size , self.size)) 
        self.timer += 1
        if (self.timer > 26):
            self.kill()        
              
#Shield
shield_list = pygame.sprite.Group()
class Shield(pygame.sprite.Sprite):

    def __init__(self, posx, posy, health):
        super().__init__()
        self.image = shieldGridImg
        self.rect = pygame.Rect(self.image.get_rect())
        self.radius = int(self.rect.height / 2)
        self.w = self.rect.width
        self.h = self.rect.height
        if (testMode):
            pygame.draw.rect(self.image, RED, self.rect, 1)
            pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius, 1)
        self.rect.x = posx
        self.rect.y = posy
        self.health = health
        
    def takeHit(self, aType):#, dValue):
        
        PlaySound(4)
        if (aType == 1):
            self.health -= 50
        else:
            self.health -= 100
            
        if (self.health <= 0):
            self.kill()
        else:
            self.image = pygame.transform.scale(self.image, (int(self.w), int(self.health * .01 * self.h)))
                          
#Create Damage        
damage_list = pygame.sprite.Group()
class Damage(pygame.sprite.Sprite):
    
    def __init__(self, posx, posy, num):
        super().__init__()
        if (num == 1):
            self.image = holeImg1
        else:
            self.image = damageImg

        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = posx
        self.rect.y = posy
        
    def update(self):
        self.rect.x = self.rect.x - vibePosX
                
def CreateMissile(dropX, dropY):#Drop the Missile using the asteroid class
    
    asteroid = Asteroid(3.0, 0, missileImg, 50, 0, dropX, dropY)
    asteroid_list.add(asteroid)
    
def CreateShieldIcn():#Shield icon
    
    asteroid = Asteroid(2.0, 2, shieldUpImg, 50, 0, random.randrange(60, 740), -100)
    asteroid_list.add(asteroid)

def CreatePowerUpIcn():#Power Up icon
    
    asteroid = Asteroid(2.0, 3, powerUpImg, 50, 0, random.randrange(60, 740), -100)
    asteroid_list.add(asteroid)
    
def CreateAsteroids():
    
    qty = levelNo * 10 + 20

    if (imgSelect == 1):#Aliens and asteroids
        for i in range(int(qty * 0.8)):#Asteroids
            rndSize = random.randrange(30, 55)
            rndRot = random.randrange(0, 3)
            rndRot = rndRot * 90
            asteroid = Asteroid(1.0, 1, asteroidImg3, rndSize, rndRot, random.randrange(20, 740), random.randrange(rndRangeY, -200))
            asteroid_list.add(asteroid)
            
        for i in range(int(qty * 0.2)):#Aliens 
            asteroid = Asteroid(1.5, 4, alienImg1, 50, 0, random.randrange(50, 710), random.randrange(rndRangeY, -200))
            asteroid_list.add(asteroid)
            
    elif (imgSelect == 2):#Aliens only
        for i in range(int(qty * 0.5)):
            asteroid = Asteroid(1.0, 4, alienImg1, 50, 0, random.randrange(50, 710), random.randrange(rndRangeY, -200))
            asteroid_list.add(asteroid)

    else:#Atreroids only random sizes
        
        for i in range(qty):
            rndSize = random.randrange(30, 55)
            rndRot = random.randrange(0, 3)
            rndRot = rndRot * 90
            asteroid = Asteroid(1.0, 1, asteroidImg3, rndSize, rndRot, random.randrange(20, 740), random.randrange(rndRangeY, -200))
            asteroid_list.add(asteroid)
              
#Create UFO  
def CreateUfo(spd, x, y):
    
    ufo = Ufo(spd, x, y)
    ufo_list.add(ufo)    

def CreateUfos(type):
    
    global ufosToShoot
    ufosToShoot = 0      

    if (type == 0):
        CreateUfo(2, -350, 30)
    elif (type == 1):
        CreateUfo(-2, 1150, 30)
    elif (type == 2):
        CreateUfo(2, -350, 30)
        CreateUfo(-2, 1150, 30)
    elif (type == 5):
        ufosToShoot = 4  
        CreateUfo(5, -500, 50)
        CreateUfo(-5, 1300, 50)
        CreateUfo(5, -350, 150)
        CreateUfo(-5, 1150, 150) 
    elif (type == 10):
        ufosToShoot = 6
        CreateUfo(5, -500, 50)
        CreateUfo(-5, 1175, 100)
        CreateUfo(5, -350, 150)
        CreateUfo(-5, 1025, 200) 
        CreateUfo(5, -500, 250)
        CreateUfo(-5, 1175, 300)
    else:
        ufosToShoot = 6
        CreateUfo(5, -350, 50)
        CreateUfo(5, -500, 100)
        CreateUfo(5, -350, 150)
        CreateUfo(5, -500, 200) 
        CreateUfo(5, -350, 250)
        CreateUfo(5, -500, 300)

#Create Shields
def CreateShields():
    
    global shieldLevel
    
    posYadder = shieldLevel * 30
    shield = [
    Shield(25, SCREEN_HEIGHT - 100 - posYadder, 100),
    Shield(175, SCREEN_HEIGHT - 130 - posYadder, 100),
    Shield(325, SCREEN_HEIGHT - 160 - posYadder, 100),
    Shield(475, SCREEN_HEIGHT - 130 - posYadder, 100),
    Shield(625, SCREEN_HEIGHT - 100 - posYadder, 100)
    ]
    shield_list.add(*shield)
 
    if (shieldLevel < 2):
        shieldLevel += 1
    else:
        shieldLevel = 0
        
#Create damage
def CreateDamage(posx, posy, vTime, num):
    
    global vibeTime
    
    damage = Damage(posx, posy, num)
    damage_list.add(damage)
    vibeTime = vTime
    
#Create explotion effect   
def CreateEffectsFX(posx, posy, size, mag, num):
    
    if (SND_LEVEL > 0):
        if (num == 3):
            PlaySound(6)
        else:
            if (mag >= 0):
                PlaySound(1)
            else:
                PlaySound(4)
        
    effectsFX = EffectsFX(posx, posy, size, mag, num)  
    effectsFX_list.add(effectsFX)

        
#Write all the game settings        
def WriteFile(content):
    
    try:
        f = open('settings10.txt', "w")
        f.write(content)#\n
        f.close()
         
    except IOError:
        print('Could not create a file!')

#Read and load all the game settings        
def ReadFile():

    try:    
        f = open('settings10.txt', "r")
        if f.mode == 'r':
            objFile = f.read()                  
            f.close()
            ParseData(objFile)
    except:#If no file create it
        #print('Could not Find File!')
        SetDefaults()

def ParseData(strMain):#Pares data

    global IMG_NO
    global SND_LEVEL   
    global settList
    global nameList
    global strName0
    
    SND_LEVEL = 0
    
    try:
        listMain = strMain.split('~')
        
        settList.clear()
        for i in range(0, 5, 1):
            settList.append(int(listMain[i]))
        #Set the screen sound
        SetScreen(settList[0], settList[1])
        SetSound(settList[2])
        IMG_NO = settList[3]
        SetMenu(settList[4])

        nameList.clear()
        for i in range(5, 10, 1):
            subStr = listMain[i]
            subList = subStr.split('|')
            nameList.append([subList[0], int(subList[1])])
            
        strName0 = listMain[10]
        listMain.clear()

    except:
        print('Could not Parse Data!')

    UpdateRank(0)

def PlaySound(num):
    #Default 8 channels 0-7   
    if (num == 0):#Laser sound
        pygame.mixer.Channel(0).play(laserSnd)
    elif (num == 1):#Explod sound
        pygame.mixer.Channel(1).play(explodSnd) 
    elif (num == 2):#Button sound
        pygame.mixer.Channel(2).play(btnSnd)
    elif (num == 3):#Buzzer sound
        #pygame.mixer.Channel(3).queue(buzzSnd)
        pygame.mixer.Channel(3).play(buzzSnd)
    elif (num == 4):#Power Down sound
        pygame.mixer.Channel(4).play(pwrDnSnd)
    elif (num == 5):#Power Up Sound
        pygame.mixer.Channel(4).play(pwrUpSnd)
    elif (num == 6):#Bug drill sound
        pygame.mixer.Channel(2).play(drillSnd)
    elif (num == 7):#Bug UFO hit sound
        pygame.mixer.Channel(2).play(hitSnd)
    else:
        print('ERROR_:_Out_Of_Range_:_PlaySound!')        
 
 
def SetDefaults():
    
    #print('Default game settings!')#Load default settings
    WriteFile('0~0~3~0~0~Pi_5.........|100~Pi_4.........|200~Pi_3.........|300~Pi_2.........|400~Pi_1.........|500~' + strName0)
    ParseData('0~0~3~0~4~Pi_5.........|100~Pi_4.........|200~Pi_3.........|300~Pi_2.........|400~Pi_1.........|500~' + strName0)
    
def SetScreen(resValue, fullScr):

    global SCR_RES
    global SCR_FULL
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global posX
    global posY
    global towerPosY

    SCR_RES = resValue
    SCR_FULL = fullScr

    if (SCR_RES == 1):
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
    else:
        SCREEN_WIDTH = 800  
        SCREEN_HEIGHT = 480
        
    if (fullScr == 1):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN, 16)  
    else:      
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, 16)

    #Set the position of the player
    posX = SCREEN_WIDTH / 2 
    posY = SCREEN_HEIGHT - 20
    towerPosY = SCREEN_HEIGHT - 210
    SetMenu(0)
    pygame.mouse.set_pos(232, 400)

def SetSound(value):
    
    global SND_LEVEL
    global nameList
    
    SND_LEVEL += value
    
    if (SND_LEVEL < 0):
        SND_LEVEL = 0
    elif (SND_LEVEL > 9):
        SND_LEVEL = 9
    try:
        explodSnd.set_volume(SND_LEVEL * 0.035)# Set sound effect volume
        laserSnd.set_volume(SND_LEVEL * 0.05)# Set sound effect volume
        btnSnd.set_volume(SND_LEVEL * 0.09)#
        buzzSnd.set_volume(SND_LEVEL * 0.1)#
        pwrDnSnd.set_volume(SND_LEVEL * 0.04)#
        pwrUpSnd.set_volume(SND_LEVEL * 0.04)#
        drillSnd.set_volume(SND_LEVEL * 0.04)#
        hitSnd.set_volume(SND_LEVEL * 0.030)#
    except:
        print('ERROR_:_SetSound')

    SetMenu(0)

def SetMenu(value):

    global MENU_NO
    global strMsg1
    
    MENU_NO += value   
    
    if (MENU_NO < 0):
        MENU_NO = 6
    elif (MENU_NO > 6):
        MENU_NO = 0    
    
    if MENU_NO == 0:   
        strMsg1 = mySelFont.render('START GAME :', True, WHITE)#
    if MENU_NO == 1:
        if SCR_FULL == 1:
            strMsg1 = mySelFont.render('FULL SCREEN : OFF', True, GREEN)#
        else:
            strMsg1 = mySelFont.render('FULL SCREEN : ON', True, YELLOW)#
    if MENU_NO == 2:
        strMsg1 = mySelFont.render('SOUND FX LEVEL : %s' %SND_LEVEL, True, GREEN)#
    if MENU_NO == 3:
        if SCR_RES  == 1:
            strMsg1 = mySelFont.render('RESOLUTION : 800X480 ', True, GREEN)#
        else:
            strMsg1 = mySelFont.render('RESOLUTION : 800X600 ', True, YELLOW)#         
    if MENU_NO == 4:   
        strMsg1 = mySelFont.render('HELP SCREEN :', True, GREEN)#
        SetText(0)
    if MENU_NO == 5:
        strMsg1 = mySelFont.render('HALL OF FAME :', True, BLUE)#
        SetText(1)
            
    if MENU_NO == 6:     
        strMsg1 = mySelFont.render('QUIT:', True, RED)#

def EditName(num0, num1):
    
    global nameList
    global strName0
    global strMsg1
    global numIndex
    global editName
    
    char = charList[numIndex]
    listLen = len(charList) - 1
 
    if (num1 == 0):#Scroll up and down through the alphabet and numbers

        if (len(strName0) < 13):
            
            numIndex += num0
            
            if (numIndex < 0):
                numIndex = listLen
            elif (numIndex > listLen):
                numIndex = 0
            
            char = charList[numIndex]
        else:
            char = charList[0]

    elif (num1 == 1):#Add Selected char

        if (len(strName0) < 13):
            strName0 += char
        
        numIndex = 0
        char = charList[numIndex]
        
    elif (num1 == 2):
        
        if (len(strName0)>0):
            strName0 = strName0[:-1]
            
        numIndex = 0
        char = charList[numIndex]
        
    elif (num1 == 3):#Save and Exit

        i = 0
        s = 0
        search = '..***~~~***..'
        
        try:
            for sublist in nameList:
                if (sublist[0] == search):
                    s = sublist[1]
                    nameList.pop(i)
                    break
                i += 1
                
            for l in range(13 - len(strName0)):
                strName0 += '.'
                
            nameList.insert(i, [strName0, s])
                
        except:#print('COULD NOT EDIT NAME!')
            strMsg1 = myHudFont.render('COULD NOT EDIT NAME!', True, RED)
           
        numIndex = 0
        UpdateRank(0)
        SetText(1)
        editName = False

    else:
        print('Out Of Range!')
        
    #print(nameList)
    
    if (editName):  
        strMsg1 = myHudFont.render('EDIT NAME: ' + strName0 + '_[' + char + ']', True, RED)
    else:
        strMsg1 = myHudFont.render('HALL OF FAME :', True, BLUE)

def UpdateRank(score0):

    global strName1
    global strName2
    global strName3
    global strName4 
    global strName5
    
    global score1 
    global score2 
    global score3 
    global score4 
    global score5
    global hiScore
    global editName    
    global nameList

    search = '..***~~~***..'
    
    try:#Update Rankings
        nameList.append([search, score0])
        nameList.sort(key = lambda nameList: nameList[1])
        
        strName1 = nameList[1][0]
        strName2 = nameList[2][0]
        strName3 = nameList[3][0]
        strName4 = nameList[4][0]
        strName5 = nameList[5][0]

        score1 = nameList[1][1]
        score2 = nameList[2][1]
        score3 = nameList[3][1]
        score4 = nameList[4][1]
        score5 = nameList[5][1]
               
        hiScore = score5
        
    except:
        print('Could not Update Rank!')

    if (nameList[0][0] != search):
        SetMenu(5)       
        editName = True
        EditName(0, 0)
        SetText(2)

    nameList.remove(nameList[0])

            
def SetText(num):

    global strLine0
    global strLine1
    global strLine2
    global strLine3
    global strLine4   
    global strLine5
    global strLine6

    try:
        if (num == 0):
    
            strLine0 = '_________***HELP-SCREEN***_________'
            strLine1 = 'MOUSE - MOVE TO AIM'
            strLine2 = 'LEFT CLICK - ENTER OR FIRE OR DOWN'
            strLine3 = 'RIGHT CLICK - BACK OR PAUSE OR UP'
            strLine4 = 'MIDDLE CLICK - SELECT OR SCREENSHOT'
            strLine5 = 'WHEEL - SCROLL UP OR DOWN MENU'
            strLine6 = '__________________________HAVE FUN!'
        else:
        
            strLine0 = '_________***HALL-OF-FAME***________'
        
            if (num == 1):
                strLine1 = 'RANK_1 : ' + strName5 + ' : ' + str(score5)
                strLine2 = 'RANK_2 : ' + strName4 + ' : ' + str(score4)
                strLine3 = 'RANK_3 : ' + strName3 + ' : ' + str(score3)
                strLine4 = 'RANK_4 : ' + strName2 + ' : ' + str(score2)
                strLine5 = 'RANK_5 : ' + strName1 + ' : ' + str(score1)            
                strLine6 = '_______________________________END.'
            else:
                strLine1 = '1.TO_EDIT_THE_NAME'
                strLine2 = '2.USE_RMB_TO_DELETE_'
                strLine3 = '3.USE_MOUSE_WHEEL_TO_SCROLL'
                strLine4 = '4.USE_CMB_TO_SELECT_CHARACTER'
                strLine5 = '5.USE_LMB_SAVE_AND_EXIT'                
                strLine6 = 'LMB=SAVE_:_CMB=SELECT_:_RMB=DEL'
    except:
        print('Could not set text!')
        
    strLine0 = myHudFont.render(strLine0, True, BLUE)#
    strLine1 = myHudFont.render(strLine1, True, WHITE)
    strLine2 = myHudFont.render(strLine2, True, WHITE)
    strLine3 = myHudFont.render(strLine3, True, WHITE)
    strLine4 = myHudFont.render(strLine4, True, WHITE)
    strLine5 = myHudFont.render(strLine5, True, WHITE)
    strLine6 = myHudFont.render(strLine6, True, RED)
            
def ResetGame():# Reset all game values

    global health 
    global oldHealth 
    global bombCount
    global shieldLevel
    global score
    global rank
    global rndRangeY
    global pauseGame
    global levelNo
    global endGame
    global vibeTime
    global towerPosY
    global playBuzz 
    
    UpdateRank(score)
    score = 0
    pauseGame = False
    endGame = False
    playBuzz = True
    health = 0
    oldHealth = 0
    bombCount = 0
    shieldLevel = 0   
    rank = 0
    rndRangeY = -400
    RemoveSprites()
    levelNo = 0
    vibeTime = 0
    towerPosY = SCREEN_HEIGHT - 210
    pygame.mouse.set_pos(232, 400)
       
def RemoveSprites():

    for damage in damage_list:
        damage_list.remove(damage)
    for laser in laser_list:
        laser_list.remove(laser)
    for asteroid in asteroid_list:
        asteroid_list.remove(asteroid)
    for ufo in ufo_list:
        ufo_list.remove(ufo)
    for shield in shield_list:
        shield_list.remove(shield)
    for effectsFX in effectsFX_list:
        effectsFX_list.remove(EffectsFX)
        
def NewLevel():

    global levelNo 
    global rndRangeY 
    global loopCount
    global strMsg
    global health
    global oldHealth
    global rank
    global bonusPoints
    global score
    global bonusPoints
    global imgSelect

    levelNo += 1
    rndRangeY -= 50
    loopCount = -50
    
    if (levelNo % 5 == 0):
        bonusPoints = 50
        CreateUfos(levelNo)
        strMsg = myMsgFont.render('BONUS UFOs!', True, RED)
        
        if (levelNo == 5):
            imgSelect = 1#Aliens and asteroids
        else:
            imgSelect = 2#Aliens only
    else:
        #imgSelect = 2#Remove this code later Aliens only
        CreateAsteroids()
        imgSelect = 0#Reset for next level Asteroids only
    
        if (bonusPoints == 0):
            if (health == oldHealth):
                rank += 1
                strMsg = myMsgFont.render(' PERFECT!', True, BLUE)           
            else:
                strMsg = myMsgFont.render('GET READY!', True, YELLOW)
        else:
            if (ufosToShoot == 0):
                bonusPoints = bonusPoints * 2
                strMsg = myMsgFont.render('***' + str(bonusPoints) + '***', True, RED)
            else:
                strMsg = myMsgFont.render('***' + str(bonusPoints) + '***', True, YELLOW)

        if (levelNo % 2 == 0):
            rndUfo = random.randrange(0,2)
            CreateUfos(rndUfo)
    
    score += bonusPoints
    oldHealth = health
    bonusPoints = 0
        
def GameOver():
    
    global strMsg
    global endGame
    global loopCount

    endGame = True
    loopCount = -200
    strMsg = myMsgFont.render('GAME OVER!', True, RED)

    for i in range(30):
        x = random.randrange(0, 760)
        y = random.randrange(15, 50)
        CreateDamage(x, SCREEN_HEIGHT - y, 150, 0)
        
    effectsFX = [
    EffectsFX(0, SCREEN_HEIGHT - 50, 50, 4, 0),
    EffectsFX(125, SCREEN_HEIGHT - 50, 50, 5, 0),
    EffectsFX(250, SCREEN_HEIGHT - 50, 50, 6, 0),
    EffectsFX(375, SCREEN_HEIGHT - 50, 50, 6, 0),
    EffectsFX(500, SCREEN_HEIGHT - 50, 50, 5, 0),
    EffectsFX(625, SCREEN_HEIGHT - 50, 50, 6, 0)
    ]
    effectsFX_list.add(*effectsFX)

    if SND_LEVEL  > 0:
        PlaySound(1)

def ScreenShot():
    
    global IMG_NO
    
    #fileName = ('/home/pi/Desktop/scrShot-' + str(IMG_NO) + '-.png')
    fileName = ('scrShot-' + str(IMG_NO) + '-.png')
    pygame.image.save(screen, fileName)
    strMsg1 = myHudFont.render('SCREENSHOT TAKEN! :', True, YELLOW)
    IMG_NO += 1

def SaveGame():
    
    global nameList
    
    if (editName):
        EditName(0, 3)
        
    try:
        content = (str(SCR_RES) + '~' + str(SCR_FULL) + '~' + str(SND_LEVEL) + '~' + str(IMG_NO) + '~' + str(0))
    
        for sublist in nameList:
            sub0 = sublist[0]
            sub1 = str(sublist[1])
            content += '~' + sub0 + '|' + sub1
        
        content += '~' + strName0
        WriteFile(content)
    except:
        print('Could not save game settings!')
                
def BtnLeft():#Update Inter and or Fire btn

    global MENU_NO
    global levelNo
    global strMsg
    global pauseGame
    global health
    global SCR_FULL
    global SCR_RES
    global SND_LEVEL
    global done
    
    if (MENU_NO == 0 and endGame == False):
        if health > 0:
            if (loopCount == 0):
                player.fireLaser()
            pauseGame = False
        else:
            if (levelNo > 0):
                ResetGame()
            else:
                health = 100
                pygame.mouse.set_pos(400, 300)
                                
    elif (MENU_NO == 1):
        if (SCR_FULL == 1):
            SCR_FULL = 0
        else:
            SCR_FULL = 1
        SetScreen(SCR_RES, SCR_FULL)
    elif (MENU_NO == 2):
        SetSound(-1)
        PlaySound(0)

    elif (MENU_NO == 3):
        if (SCR_RES == 1):
            SCR_RES = 0
        else:
            SCR_RES = 1
            
        SetScreen(SCR_RES, SCR_FULL)
        
    elif (MENU_NO == 4):
        SetMenu(-4)
        
    elif (MENU_NO == 5):
        
        if (editName):
            EditName(0, 3)
        else:
            SetMenu(-5)        
            
    elif (MENU_NO == 6):
        done = True
        
def BtnCenter():
    
    if (editName):
        PlaySound(2)
        EditName(0, 1)
    else:
        ScreenShot()
        
def BtnRight():#Update return or back

    global levelNo
    global pauseGame
    global strMsg
    global health
    global done

    if (levelNo > 0):
        if (pauseGame == False and health > 0):
            pauseGame = True
            strMsg = myMsgFont.render('  PAUSED', True, GREEN)
        else:
            ResetGame()            
    else:
        
        if (MENU_NO == 1):
            SetMenu(-1)
            
        elif (MENU_NO == 2):
            SetSound(1)
            PlaySound(0)
            
        if (MENU_NO == 3):
            SetMenu(-3)
            
        elif (MENU_NO == 4):
            SetMenu(-4)
        
        elif (MENU_NO == 5):
            
            if (editName):
                EditName(0, 2)
            else:
                SetMenu(-5) 
        
        elif (MENU_NO == 6):
            done = True

def BtnUp():#Up btn
    
    if (testMode and levelNo != 0):
        CreateShields()

    if (editName):
        EditName(1, 0)
    else:
        if (levelNo == 0):
            PlaySound(2)
            SetMenu(1)
               
def BtnDown():#Down btn
    
    
    if (testMode and levelNo != 0):    
        CreateUfo(2, -350, 30)

    if (editName):
        EditName(-1, 0)
    else:
        if (levelNo == 0):
            PlaySound(2)
            SetMenu(-1)       

def UpdateMouse():    #Handel input **Mouse** or **RAT**

    global posx
    global posy
    global done
    
    for event in pygame.event.get():
        
        pos = pygame.mouse.get_pos()
        posx = pos[0]
        posy = pos[1]#
        
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:#Left click
                BtnLeft()
                    
            elif event.button == MIDDLE:# Middle click 
                BtnCenter()

            elif event.button == RIGHT:#Right click
                BtnRight()

            elif event.button == UP:# Wheel Up 
                BtnUp()
                
            elif event.button == DOWN:# Wheel Down
                BtnDown()

def UpdateGame():#check for collitions
    
    global BR_COLOR
    
    for laser in laser_list:
        
        laser_hit_list = pygame.sprite.spritecollide(laser, asteroid_list, False, pygame.sprite.collide_circle)  
            
        for asteroid in laser_hit_list:
            laser.takeHit()
            asteroid.takeHit()
            
        ufo_hit_list = pygame.sprite.spritecollide(laser, ufo_list, False)
        
        for ufo in ufo_hit_list:
            laser.takeHit()
            ufo.takeHit()

    for shield in shield_list:
        
        shield_hit_list = pygame.sprite.spritecollide(shield, asteroid_list, False) 
        
        for asteroid in shield_hit_list:
            shield.takeHit(asteroid.type)
            asteroid.removeMe()   

def DrawScreen():#___________________RENDERING________________

    global towerPosY
    global vibePosX
    
    screen.fill((0, 0, 0))
    screen.blit(bgImg, (0, 0))
    
    if(vibePosX == 0 and endGame != True):
        screen.blit(tower0Img, (610 + vibePosX , towerPosY))
    else:
        screen.blit(tower1Img, (610 + vibePosX , towerPosY))
        if (health <= 0):
            towerPosY += 1
    screen.blit(baseImg, (vibePosX, SCREEN_HEIGHT - 71))
    laser_list.draw(screen)
    player_list.draw(screen)
    shield_list.draw(screen)
    screen.blit(coverImg, (338 + vibePosX, SCREEN_HEIGHT - 28))
    damage_list.draw(screen)
    asteroid_list.draw(screen)
    ufo_list.draw(screen)
    effectsFX_list.draw(screen)
       
    if (levelNo > 0):        
        hudScore = myHudFont.render('SCORE: %s' % score, True, BLUE )#score
        hudHiScore = myHudFont.render('HI-SCORE: %s' % hiScore, True, BLUE)#hi score
        hudHealth = myHudFont.render('POWER: %s' % health, True, BR_COLOR)#health
        hudLevel = myHudFont.render('LEVEL: %s' % levelNo, True, BLUE)#Level
        hudRank = myHudFont.render('RANK: %s' % rank, True, BLUE)#strFPS
        #Draw the HUD
        screen.blit(hudScore, (20, 10))
        screen.blit(hudHiScore, (200, 10))
        screen.blit(hudHealth, (420, 10))
        screen.blit(hudLevel, (560, 10))
        screen.blit(hudRank, (690, 10))
        if (showMsg or pauseGame):
            screen.blit(strMsg, (140, 200))            
    else:
        screen.blit(underLayImg, (185, 30))
        
        if (MENU_NO == 4 or MENU_NO == 5):#Hall of Fame and Help Screen
            
            screen.blit(overLayImg, (185, 30))
            
            screen.blit(strLine0, (205, 55))
            screen.blit(strLine1, (205, 85))
            screen.blit(strLine2, (205, 115))
            screen.blit(strLine3, (205, 145))
            screen.blit(strLine4, (205, 175))
            screen.blit(strLine5, (205, 205))
            screen.blit(strLine6, (205, 235))
            
        screen.blit(strMsg1, (290, 386))
        screen.blit(startImg, (100, 10))
    
    if (testMode):
        # String Info text
        strFPS = str(round(clock.get_fps(),2))
        #List of stuff to test -rank ranking vibePosX vibeTime endGame loopCount bonusPoints str(len(asteroid_list)) imgSelect-
        strInfo = myHudFont.render('Info: %s' % strFPS, True, YELLOW )#score editName
        screen.blit(strInfo, (20, 30))
    
    screen.blit(crossHairImg, (posx - 15, posy - 15))

ReadFile()#Read and load the game settings


while not done:#____________________The Main game loop___________________

    UpdateMouse()
    UpdateGame()

    if (health > 0):#Game Logik
        
        if (len(asteroid_list) == 0  and len(ufo_list) == 0):#Move to next level
            NewLevel()
            
        if (hiScore < score):
            hiScore = score

        if (loopCount < 0):
            loopCount += 1
            showMsg = True
        else:
            showMsg = False    
    else:        
        
        if (levelNo != 0):
            
            if (endGame == False):
                GameOver()
                loopCount = -200

            if (loopCount < 0):
                loopCount += 1
                showMsg = True
            else:
                showMsg = False
                
                ResetGame()      

    if (pauseGame == False):#Update all the sprites if not paused
        asteroid_list.update()
        laser_list.update()    
        player_list.update()
        effectsFX_list.update()
        ufo_list.update()
        damage_list.update()
        
        if (vibeTime > 0):
            if (vibeTime % 2 == 0):
                vibePosX = 1
            else:
                vibePosX = -1
            vibeTime -= 1
        else:
            vibePosX = 0

        if (health <= 0):
            health = 0
            BR_COLOR = RED
        elif (health < 50):
            changeCol += 1
            if (changeCol < 30):
                BR_COLOR = RED
            elif (changeCol < 60):
                BR_COLOR = YELLOW
            else:
                PlaySound(3)
                changeCol = 0       
        else:
            BR_COLOR = BLUE
        
         
    DrawScreen()
    
    pygame.display.flip()
    clock.tick(30)#FPS
    
#__________________EXIT_THE_GAME____________
    
SaveGame()#Save the game settings
pygame.quit()
sys.exit()

#Last build 1298 lines
#Still_To_Do_List!
#Find and Fix Buggs
#Make UFO change color after been hit!!