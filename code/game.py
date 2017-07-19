import gameData
import helper2
import cevent
import pygame
from pygame.transform import scale2x as x2
from pygame.locals import *

regionPath = "../art.png/regions/"
npcPath = "../art.png/npcs/"
charPath = "../art.png/you/"
newGamePath = "../art.png/newGame/"
block = 64

class Game(cevent.CEvent):
    
    def __init__(self, app):
        self.app = app
        self.char = app.temp.char
        self.prog = app.temp.prog
        
        self.region = self.prog.region
        self.x = self.prog.x
        self.y = self.prog.y
        self.direc = self.prog.direc
        self.time = self.prog.time
        self.inTransit = False
        
        self.loadImages()
        
        self.debug = True
        
    def save(self):
        prog = gameData.Progress()
        prog.update(self)
        gameData.save(self.char, prog)
        
    def loadImages(self):
        self.pop = {}
        #self.regionDisp = pygame.image.load(regionPath + self.region.numb + ".png")
        self.regionDisp = x2(x2(pygame.image.load(regionPath + "testBackground2.png")))
        
        """
        self.charUp = pygame.image.load(charPath + "charUp.png")
        self.charDown = pygame.image.load(charPath + "charDown.png")
        self.charLeft = pygame.image.load(charPath + "charLeft.png")
        self.charRight = pygame.image.load(charPath + "charRight.png")
        """
        
        self.charUp = x2(pygame.image.load(newGamePath + "up.png"))
        self.charDown = x2(pygame.image.load(newGamePath + "down.png"))
        self.charLeft = x2(pygame.image.load(newGamePath + "left.png"))
        self.charRight = x2(pygame.image.load(newGamePath + "right.png"))
        self.male = x2(pygame.image.load(newGamePath + "male.png"))
        self.female = x2(pygame.image.load(newGamePath + "female.png"))
        
        for i in self.region.pop:
            self.pop.update({i.name : pygame.image.load(npcPath + i.name + ".png")})
            
    def getChar(self):
        if self.direc == (0,-1):
            return self.charUp
        elif self.direc == (1,0):
            return self.charRight
        elif self.direc == (0,1):
            return self.charDown
        elif self.direc == (-1,0):
            return self.charLeft
            
    
    def getDraw(self):
        return [self]
    
    def move(self, name=None):
        if name is None and self.inTransit and type(self.region.area[self.y + self.direc[1]][self.x + self.direc[0]]) is not helper2.Wall:
            self.x += self.direc[0]
            self.y += self.direc[1]
            self.charChecks()
        else: #NPC move
            pass
    
    def changeDirec(self, direc):
        if direc == self.direc:
            return False
        else:
            self.direc = direc
            return True
        
    def do(self):
        pass
    
    def charChecks(self):
        check = [[self.region.area[y][x] if x < len(self.region.area[0]) and x >= 0 and y < len(self.region.area) and y >= 0 else None for x in range(self.x-1,self.x+2)] for y in range(self.y-1, self.y+2)]
        
        for i in check:
            for j in i:
                if j is not None:
                    if j.y == self.y and j.x == self.x and j.trigger == "step":
                        j.trig(self)
                    elif j.trigger == "adj":
                        j.trig(self)        
        
    def checks(self):
        pass
    
    def draw(self):
        m = 11
        x = self.x
        y = self.y
        b = block

        self.app.display.blit(self.regionDisp, (m,0))
        
        self.app.display.blit(self.getChar(), (x*b + m, y*b))
        
        for i in self.region.pop:
            self.app.display.blit(self.female, (i.x*b + m, i.y*b))
                    
    def on_key_down(self, event):
        if event.key == K_UP or event.key == K_RIGHT or event.key == K_DOWN or event.key == K_LEFT:
            self.inTransit = True
            self.app.frameCount = 0            
        if event.key == K_UP:
            self.changeDirec((0,-1))
        elif event.key == K_RIGHT:
            self.changeDirec((1,0))
        elif event.key == K_DOWN:
            self.changeDirec((0,1))
        elif event.key == K_LEFT:
            self.changeDirec((-1,0))
        elif event.key == K_z:
            self.region.area[self.y + self.direc[1]][self.x + self.direc[0]].trig()
        elif event.key == K_s:
            self.save()
            
    def on_key_up(self, event):
        keys = pygame.key.get_pressed()
        
        if keys[K_UP]:
            self.changeDirec((0,-1))
        elif keys[K_RIGHT]:
            self.changeDirec((1,0))
        elif keys[K_DOWN]:
            self.changeDirec((0,1))
        elif keys[K_LEFT]:
            self.changeDirec((-1,0))
        else:
            self.inTransit = False