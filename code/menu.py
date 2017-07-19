import sys
sys.path.insert(0, '../../Pygame Text')
import os
import pygame_textinput as pgti
import helper
import pygame
import cevent
import pickle
import gameData
from pygame.locals import *

iconPath = "../art.png/newGame/"

class MainMenu(cevent.CEvent):
    
    path = "../images/"
    file = "main_menu.png"
    
    def __init__(self, app):
        self.app = app
        
        self.current = 0
        self.buttonShow = ["New Game", "Load Game", "Exit"]
        self.buttonAction = ["newGame", "loadGame", "exitGame"]
        
        pygame.font.init()
        
        self.font = pygame.font.SysFont(helper.calibri, 22)
        
        #self.image = pygame.image.load(self.path + self.file)
        
    def draw(self):
        
        color = helper.white
        block = 20
        x = 1000
        y = 500
        
        for i in range(3):            
            if(self.current == i):
                color = helper.color200_0_0
            else:
                color = helper.white
            
            self.app.display.blit(helper.textObject(self.buttonShow[i], self.font, color), (x, i*block + y))
            
    def getDraw(self):
        return [self]
    
    def on_key_down(self, event):
        if(event.key == K_DOWN and self.current < 2):
            self.current += 1
        if(event.key == K_UP and self.current > 0):
            self.current -= 1
        if(event.key == K_z):
            action = getattr(self, self.buttonAction[self.current])
            action()
            
    def newGame(self):
        self.app.changeState("newGame")
    
    def loadGame(self):
        self.app.changeState("loadGame")
    
    def exitGame(self):
        event = pygame.event.Event(QUIT)
        pygame.event.post(event)
        
class NewGame(cevent.CEvent):
    
    def __init__(self, app):
        self.app = app
        self.textInput = app.textInput
        self.font = pygame.font.SysFont(helper.calibri, 30)
        self.male = True
        self.clothes = 0
        self.species = 0
        self.focus = [0,0,0,0,0]
        self.points = 10
        self.talent = [0,0,0,0,0]
        self.total = 9.0
        self.message = "z: click/add points"
        self.message2 = "x: subtract points"
        
        self.makeGrid()
        self.loadImages()
        
    def loadImages(self):
        self.back = pygame.image.load(iconPath + "left.png")
        self.cont = pygame.image.load(iconPath + "right.png")
        self.maleIcon = pygame.image.load(iconPath + "male.png")
        self.femaleIcon = pygame.image.load(iconPath + "female.png")
        self.select = pygame.image.load(iconPath + "select.png")
        self.genderFrame = pygame.image.load(iconPath + "genderFrame.png")
        self.circle = pygame.image.load(iconPath + "circle.png")
        
    def makeGrid(self):
        self.lg = helper.LinkedGrid()
        self.lg.addUnit("Name")
        self.lg.addUnit("Male")
        self.lg.addUnit("Female")
        self.lg.addUnit("Focus1")
        self.lg.addUnit("Focus2")
        self.lg.addUnit("Focus3")
        self.lg.addUnit("Focus4")
        self.lg.addUnit("Focus5")
        self.lg.addUnit("ClothesLeft")
        self.lg.addUnit("ClothesRight")
        self.lg.addUnit("SpeciesLeft")
        self.lg.addUnit("SpeciesRight")
        self.lg.addUnit("Back")
        self.lg.addUnit("Continue")
        
        self.lg.setAllAdj("Name", right="ClothesLeft", down="Male")
        self.lg.setAllAdj("Male", right="Female", up="Name", down="Focus1")
        self.lg.setAllAdj("Female", left="Male", right="SpeciesLeft", up="Name", down="Focus1")
        self.lg.setAllAdj("ClothesLeft", left="Name", right="ClothesRight", down="SpeciesLeft")
        self.lg.setAllAdj("ClothesRight", left="ClothesLeft", right="Back", up="Back", down="SpeciesRight")
        self.lg.setAllAdj("SpeciesLeft", left="Female", right="SpeciesRight", up="ClothesLeft", down="Focus1")
        self.lg.setAllAdj("SpeciesRight", left="SpeciesLeft", up="ClothesRight", down="Continue")
        self.lg.setAllAdj("Focus1", left="Focus5", right="Focus2", up="Female", down="Focus2")
        self.lg.setAllAdj("Focus2", left="Focus1", right="Continue", up="Focus1", down="Focus3")
        self.lg.setAllAdj("Focus3", left="Focus4", right="Continue", up="Focus2")
        self.lg.setAllAdj("Focus4", right="Focus3", up="Focus5")
        self.lg.setAllAdj("Focus5", right="Focus1", up="Focus1", down="Focus4")
        self.lg.setAllAdj("Back", left="ClothesRight", down="ClothesRight")
        self.lg.setAllAdj("Continue", left="Focus3", up="SpeciesRight")
        
    def getDraw(self):
        return [self]
        
    def draw(self):
        m = 100  #margin
        a = 16  #adjustment
        w = self.app.w
        h = self.app.h
        c = (w - m*2)/3     #character display box width
        select = 2
        selectColor = helper.color0_0_200
        mult = 2
        color = helper.black
        
        malex = m*1.75 + c
        maley = m*2.5
        femalex = m*2.75 + c
        femaley = m*2.5
        clothesLeftx = m*5 + c + a
        clothesLefty = m*1.5 + a
        clothesRightx = m*7 + c
        clothesRighty = m*1.5 + a
        speciesLeftx = m*5 + c + a
        speciesLefty = m*2.5 + a
        speciesRightx = m*7 + c
        speciesRighty = m*2.5 + a
        backx = w-m-a
        backy = m-a
        continuex = w-m-a
        continuey = h-m-a
        
        
        pygame.draw.rect(self.app.display, helper.newGameMenu, pygame.Rect(m,m, w - m*2,h - m*2))       #frame
        
        pygame.draw.circle(self.app.display, helper.menuFrame, (m,m), a)
        pygame.draw.circle(self.app.display, helper.menuFrame, (m,h-m), a)        
        
        pygame.draw.rect(self.app.display, helper.charDisplay, pygame.Rect(m,m, c, h - m*2))     #char display
        
        pygame.draw.lines(self.app.display, helper.menuFrame, True, [(m,m), (m,h - m), (w-m, h-m), (w-m, m)], 10) #border    
        
        self.app.display.blit(self.app.textInput.get_surface(), (m*2.5 + c, m*1.5))       #name
        
        if(self.lg.current.name == "Name"):
            pygame.draw.lines(self.app.display, helper.black, True, [(m*1.375 + c, m*1.5), (m*1.375 + c, m*1.875), (m*2.25 + c, m*1.875), (m*2.25 + c, m*1.5)], 3)
            
        self.app.display.blit(helper.textObject("Name: ", self.font, color), (m*1.5 + c, m*1.75 - a))        #name text
        
        self.app.display.blit(pygame.transform.scale2x(self.maleIcon), (malex, maley))            #male
        self.app.display.blit(pygame.transform.scale2x(self.femaleIcon), (femalex, femaley))          #female
        
        if(self.male):
            self.app.display.blit(pygame.transform.scale2x(self.genderFrame), (malex, maley))
            
        else:
            self.app.display.blit(pygame.transform.scale2x(self.genderFrame), (femalex, femaley))
        
        self.app.display.blit(pygame.transform.scale2x(self.back), (clothesLeftx, clothesLefty))   #clothes left
        self.app.display.blit(pygame.transform.scale2x(self.cont), (clothesRightx, clothesRighty))   #clothes right
        
        text = "Clothes: " + str(self.clothes + 1)
        self.app.display.blit(helper.textObject(text, self.font, color), (m*5.875 + c, m + a*5.5))        #clothes text
        
        self.app.display.blit(pygame.transform.scale2x(self.back), (speciesLeftx, speciesLefty))   #species left
        self.app.display.blit(pygame.transform.scale2x(self.cont), (speciesRightx, speciesRighty))   #spcies right      
        
        text = "Species: " + str(self.species + 1)
        self.app.display.blit(helper.textObject(text, self.font, color), (m*5.875 + c, m*2 + a*5.5))        #species text
        
        sin72 = 0.951
        cos72 = 0.309
        sin54 = 0.809
        cos54 = 0.588
        o = (m*2.5 + c, m*5)
        f1 = self.focus[0]
        f2 = self.focus[1]
        f3 = self.focus[2]
        f4 = self.focus[3]
        f5 = self.focus[4]
        t = self.total
        
        pentagonf = [(o[0], o[1] - m), (o[0] + m*sin72, o[1] - m*cos72), (o[0] + m*cos54, o[1] + m*sin54), (o[0] - m*cos54, o[1] + m*sin54), (o[0] - m*sin72, o[1] - m*cos72)]
        
        for i in range(5):
            pygame.draw.line(self.app.display, helper.black, (o[0], o[1]), pentagonf[i])     
        
        pygame.draw.lines(self.app.display, helper.black, True, pentagonf, 2)     #focus
        
        pentagonfv = [(o[0], o[1] - m*(f1/t)),(o[0] + m*sin72*(f2/t), o[1] - m*cos72*(f2/t)), (o[0] + m*cos54*(f3/t), o[1] + m*sin54*(f3/t)), (o[0] - m*cos54*(f4/t), o[1] + m*sin54*(f4/t)), (o[0] - m*sin72*(f5/t), o[1] - m*cos72*(f5/t))]
        
        pygame.draw.lines(self.app.display, helper.color200_0_0, True, pentagonfv, select)     #focus values
        
        o = (m*6.5 + c, m*5)
        t1 = self.talent[0]
        t2 = self.talent[1]
        t3 = self.talent[2]
        t4 = self.talent[3]
        t5 = self.talent[4]
    
        pentagont = [(o[0], o[1] - m), (o[0] + m*sin72, o[1] - m*cos72), (o[0] + m*cos54, o[1] + m*sin54), (o[0] - m*cos54, o[1] + m*sin54), (o[0] - m*sin72, o[1] - m*cos72)]
        
        for i in range(5):
            pygame.draw.line(self.app.display, helper.black, (o[0], o[1]), pentagont[i])
       
        pygame.draw.lines(self.app.display, helper.black, True, pentagont, 2)     #talent
    
        pentagontv = [(o[0], o[1] - m*(t1/t)),(o[0] + m*sin72*(t2/t), o[1] - m*cos72*(t2/t)), (o[0] + m*cos54*(t3/t), o[1] + m*sin54*(t3/t)), (o[0] - m*cos54*(t4/t), o[1] + m*sin54*(t4/t)), (o[0] - m*sin72*(t5/t), o[1] - m*cos72*(t5/t))]
        pygame.draw.lines(self.app.display, helper.color0_200_0, True, pentagontv, 2)     #talent values
        
        
        #circles
        self.app.display.blit(self.back, (backx, backy))   #back
        self.app.display.blit(self.cont, (continuex, continuey))  #continue
            
        #points
        pygame.draw.circle(self.app.display, helper.male, (int(pentagonf[0][0] + m), int(pentagonf[0][1])), a)
        pygame.draw.circle(self.app.display, helper.black, (int(pentagonf[0][0] + m), int(pentagonf[0][1])), a, 1)
        
        if(self.points < 10):
            self.app.display.blit(helper.textObject(str(self.points), self.font, color), (pentagonf[0][0] + m -6, pentagonf[0][1] - 8))
        else:
            self.app.display.blit(helper.textObject(str(self.points), self.font, color), (pentagonf[0][0] + m -12, pentagonf[0][1] - 8))
            
        self.app.display.blit(helper.textObject(self.message, self.font, helper.white), (m*5, m-a*4))
        self.app.display.blit(helper.textObject(self.message2, self.font, helper.white), (m*5, m-a*2))        #
             
        
        if(self.lg.current.name == "Male"):
            self.app.display.blit(pygame.transform.scale2x(self.select), (malex, maley))
        elif(self.lg.current.name == "Female"):
            self.app.display.blit(pygame.transform.scale2x(self.select), (femalex, femaley))
        elif(self.lg.current.name == "ClothesLeft"):
            self.app.display.blit(pygame.transform.scale2x(self.select), (clothesLeftx, clothesLefty))
        elif(self.lg.current.name == "ClothesRight"):
            self.app.display.blit(pygame.transform.scale2x(self.select), (clothesRightx, clothesRighty))
        elif(self.lg.current.name == "SpeciesLeft"):
            self.app.display.blit(pygame.transform.scale2x(self.select), (speciesLeftx, speciesLefty))
        elif(self.lg.current.name == "SpeciesRight"):
            self.app.display.blit(pygame.transform.scale2x(self.select), (speciesRightx, speciesRighty))
        elif(self.lg.current.name == "Back"):
            self.app.display.blit(self.select, (backx, backy))
        elif(self.lg.current.name == "Continue"):
            self.app.display.blit(self.select, (continuex, continuey))
        for i in range(5):      #focus
            
            self.app.display.blit(self.circle, (pentagonf[i][0] - a, pentagonf[i][1] - a))
            self.app.display.blit(self.circle, (pentagont[i][0] - a, pentagont[i][1] - a))         
            
            if(self.lg.current.name == ("Focus" + str(i+1))):
                self.app.display.blit(self.select, (pentagonf[i][0] - a, pentagonf[i][1] - a))
                
            text = str(self.focus[i])
            self.app.display.blit(helper.textObject(text, self.font, color), (pentagonf[i][0] - 6, pentagonf[i][1] -9))        #focus numbers
            text = str(self.talent[i])
            self.app.display.blit(helper.textObject(text, self.font, color), (pentagont[i][0] - 6, pentagont[i][1] -9))        #talent numbers            
    
    
    
    def on_key_down(self, event):
        if(event.key == K_DOWN and self.lg.current.down != None):
            self.lg.current = self.lg.findUnit(self.lg.current.down)
        if(event.key == K_UP and self.lg.current.up != None):
            self.lg.current = self.lg.findUnit(self.lg.current.up)
        if(event.key == K_LEFT and self.lg.current.left != None):
            self.lg.current = self.lg.findUnit(self.lg.current.left)   
        if(event.key == K_RIGHT and self.lg.current.right != None):
            self.lg.current = self.lg.findUnit(self.lg.current.right)
        if(event.key == K_z):
            if(self.lg.current.name == "Male"):
                self.male = True
            elif(self.lg.current.name == "Female"):
                self.male = False
            elif(self.lg.current.name == "ClothesLeft"):
                self.clothes -= 1
                if(self.clothes < 0):
                    self.clothes = gameData.Player.clothes_quantity - 1
            elif(self.lg.current.name == "ClothesRight"):
                self.clothes += 1
                self.clothes %= gameData.Player.clothes_quantity              
            elif(self.lg.current.name == "SpeciesLeft"):
                self.species -= 1
                if(self.species < 0):
                    self.species = gameData.Player.species_quantity - 1
                    
                for i in range(5):
                    self.talent[i] = gameData.talent_matrix[self.species][i]
            elif(self.lg.current.name == "SpeciesRight"):
                self.species += 1
                self.species %= gameData.Player.species_quantity
                for i in range(5):
                    self.talent[i] = gameData.talent_matrix[self.species][i]
            elif(self.lg.current.name[:5] == "Focus"):
                f = int(self.lg.current.name[5:]) - 1
                if(self.focus[f] < self.total and self.points > 0):
                    self.focus[f] += 1
                    self.points -= 1
            elif(self.lg.current.name == "Back"):
                self.app.changeState("mainMenu")
            elif(self.lg.current.name == "Continue"):
                if((self.app.textInput.get_text() + ".p") in os.listdir(gameData.savePath)):
                    self.message2 = "That name is already taken!"
                    self.message = ""
                else:
                    char = gameData.Character(self.app.textInput.get_text(), self.male, self.clothes, self.species, self.focus)
                    
                    prog = gameData.Progress()
                    prog.newGame()
                    
                    gameData.save(char, prog)
                    gameData.load(char.name, self.app)
                    self.app.changeState("game")
        if(event.key == K_x):
            if(self.lg.current.name[:5] == "Focus"):
                f = int(self.lg.current.name[5:]) - 1
                if(self.focus[f] > 0):
                    self.focus[f] -= 1
                    self.points += 1
                    
class LoadGame(cevent.CEvent):
    def __init__(self, app):
        self.app = app
        self.font = pygame.font.SysFont(helper.calibri, 30)
        self.current = 0
        self.color = helper.color0_0_200
        self.updateList()
        self.message = "z: select file"
        self.message2 = "x: toggle delete mode"
        self.loadImages()
        
    def loadImages(self):
        self.back = pygame.image.load(iconPath + "left.png")     
        
    def updateList(self):
        os.chdir("../data/saves")
        files = [f for f in os.listdir(".") if os.path.isfile(os.path.join(".", f))]
        self.loads = [[None for x in range(4)] for y in range(4)]
        
        r = -1
        for i in range(len(files)):
            j = i % 4
            if j == 0:
                r += 1
            self.loads[r][j] = files[i][:-2]
        os.chdir("../../code")        
    
    def getDraw(self):
        return [self]
    
    def draw(self):
        m = 100  #margin
        a = 16  #adjustment
        w = self.app.w
        h = self.app.h
        bW = (w-m*2)/4      #boxW
        bH =(h-m*2)/4       #boxH
        th = 10             #thickness
        select = 3
        
        pygame.draw.rect(self.app.display, helper.newGameMenu, pygame.Rect(m,m, w - m*2,h - m*2))       #frame
        
        pygame.draw.lines(self.app.display, helper.menuFrame, True, [(m,m), (m,h - m), (w-m, h-m), (w-m, m)], th)
        
        pygame.draw.circle(self.app.display, helper.menuFrame, (m,m), a)
        pygame.draw.circle(self.app.display, helper.menuFrame, (m,h-m), a)
        pygame.draw.circle(self.app.display, helper.menuFrame, (w-m,h-m), a)
        
        self.app.display.blit(self.back, (w-m-a, m-a))   #back
        
        for i in range(3):
            pygame.draw.line(self.app.display, helper.menuFrame, (m + (i+1)*bW, m), (m + (i+1)*bW, h-m), th)
            
        for i in range(4):
            pygame.draw.line(self.app.display, helper.menuFrame, (m, m + (i+1)*bH), (w-m,m + (i+1)*bH), th)
        
        for i in range(4):
            for j in range(4):
                text = self.loads[i][j]
                self.app.display.blit(helper.textObject(text, self.font, helper.black), (m + j*bW + a, m + i*bH + a))
                
        self.app.display.blit(helper.textObject(self.message, self.font, helper.white), (m*5, m-a*4))
        self.app.display.blit(helper.textObject(self.message2, self.font, helper.white), (m*5, m-a*2))        #message
        
        if self.current != -1:        
            y = int(self.current / 4)
            x = self.current % 4
            box = [(m + x*bW, m + y*bH), (m + (x+1)*bW, m + y*bH), (m + (x+1)*bW, m + (y+1)*bH), (m + x*bW, m + (y+1)*bH)]
            pygame.draw.lines(self.app.display, self.color, True, box, 3)
        else:
            pygame.draw.circle(self.app.display, helper.color0_0_200, (int(w-m), int(m)), a, select)
        
    def on_key_down(self, event):
        if((event.key == K_UP or event.key == K_RIGHT) and self.current == 3):
            self.current = -1 #back
        elif(event.key == K_DOWN and self.current < 12):
            self.current += 4
        elif(event.key == K_UP and self.current > 3 and self.current != -1):
            self.current -= 4
        elif(event.key == K_RIGHT and not (self.current in [(i*4-1) for i in range(1,5)]) and self.current != -1):
            self.current += 1
        elif(event.key == K_LEFT and not(self.current in [(i*4) for i in range(4)])):
            if(self.current == -1):
                self.current = 3
            else:
                self.current -= 1
        elif(event.key == K_z and self.color == helper.color0_0_200):
            y = int(self.current / 4)
            x = self.current % 4                
            if(self.current == -1):
                self.app.changeState("mainMenu")
            elif self.loads[y][x] != None:
                gameData.load(self.loads[y][x], self.app)
                self.app.changeState("game")
        elif(event.key == K_z and self.color == helper.color200_0_0):
            y = int(self.current / 4)
            x = self.current % 4
            if(self.current == -1):
                self.app.changeState("mainMenu")            
            elif self.loads[y][x] != None:
                path = gameData.savePath + self.loads[y][x] + ".p"
                os.remove(path)
                self.updateList()
                self.color = helper.color0_0_200
        elif(event.key == K_x):
            if(self.color == helper.color0_0_200):
                self.color = helper.color200_0_0
            else:
                self.color = helper.color0_0_200