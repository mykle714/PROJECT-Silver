import pygame
import cevent
import time
import sys
sys.path.insert(0, '../../Pygame Text')
import pygame_textinput as pgti
import game
import gameData
import menu
import helper
from pygame.locals import *

#speed up ideas
#dont rerender entire screen every frame
#increase BFS intervals

class App(cevent.CEvent):
    def __init__(self, FPS=60, dim=(1366,768)):     #11 pixel vertical margin, no vertical margin 21x12 grid
        super().__init__()
        self.running = False
        self.display = None
        self.FPS = FPS
        self.w = dim[0]
        self.h = dim[1]
        self.textInput = None
        self.temp = None
        
        self.temptime = 0
        
    def init(self):
        pygame.init()
        
        #self.display = pygame.display.set_mode((self.w, self.h), pygame.FULLSCREEN)
        self.display = pygame.display.set_mode((self.w, self.h), pygame.HWSURFACE)
        
        pygame.display.set_caption("insert title here")
        
        self.running = True
        
        self.clock = pygame.time.Clock()
        
        self.changeState("mainMenu")
        
    def loop(self):
        self.clock.tick(self.FPS)
        
    def cleanup(self):
        pygame.quit()
        
    def on_exit(self):
        self.running = False
        self.cleanup()
        
    def render(self):            
        self.display.fill((50,50,50))      #background
        self.draw = self.stateObj.getDraw()
        
        for i in self.draw:
            i.draw()
            
        pygame.display.flip()
        
    def execute(self):
        self.frameCount = 0
        
        if(self.init() == False):
            self.running = False
            
        while(self.running):
            self.debugTime("Loop")
            self.render()
            self.loop()
            
            if(self.gameState == "newGame" and self.textInput != None and self.stateObj.lg.current.name == "Name"):
                self.textInput.update(events)
            elif(self.gameState == "game" and self.stateObj.inTransit):
                if self.frameCount % 8 == 0:
                    self.frameCount = 0
                    self.stateObj.move()
                    self.stateObj.checks()
                self.frameCount += 1
            
            events = pygame.event.get()
            for event in events:                
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.on_exit()
                    break
                    
                if event.type == KEYDOWN:
                    self.stateObj.on_key_down(event)
                elif event.type == KEYUP:
                    self.stateObj.on_key_up(event)
                    
    #input
    def on_key_down(self, event):
        pass
            
    #game states
    def changeState(self, name):
        self.gameState = name
        
        stateName = getattr(self,self.gameState)
        self.state = stateName()
        
        #print("Game state changed to ", name)
        
    def mainMenu(self):
        self.stateObj = menu.MainMenu(self)
    
    def newGame(self):
        self.textInput = pgti.TextInput(font_family="arial", font_size = 36)
        self.stateObj = menu.NewGame(self)
        
    def loadGame(self):
        self.stateObj = menu.LoadGame(self)
    
    def game(self):
        self.stateObj = game.Game(self)
        
    def debugTime(self, message):
        temp2 = time.time()
        print(message + ":\t" + str(temp2 - self.temptime))
        
        self.temptime = temp2
        
            
app = App()
app.execute()