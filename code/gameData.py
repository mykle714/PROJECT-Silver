import _pickle as cpickle
import os
import helper
import helper2
import game
import sys
sys.path.insert(0, '../helper/')
from BFS import convert

ext = "../data/"
savePath = "../data/saves/"
artPath = "../art.png/"
gameDataPath = "../data/gameData/"
regionPath = gameDataPath + "regions/"

talent_matrix = [(0,0,0,0,0),   #human
                 (5,4,1,2,3)]   #harpie?

class Character:
    
    attr = ["name", "isMale", "clothes", "species", "focus"]
        
    def __init__(self, name, isMale, clothes, species, focus):
        self.name = name
        self.isMale = isMale
        self.clothes = clothes
        self.species = species
        self.focus = focus

class Region:
    
    attr = ["numb", "pop", "area"]
    regional = None
    
    numb = None
    pop = []      #movable objects + people
    area = None     #array where walls and portals live

    def __init__(self, number, stuff=None, lg=None):
        if stuff == None:
            self.load(number)
        else:
            self.numb = number
            self.area = [[None for x in range(21)] for y in range(12)]
            self.populate(stuff)
            self.lg = lg
            
            with open("../data/gameData/regions/region" + str(number) + ".p", "wb") as file:
                cpickle.dump(self, file)
            
    def getRegionalMap(self):
        if Region.regional == None:
            Region.regional = helper.LinkedGrid.load("regional")
        else:
            return Region.regional
        
    def create(number, file):
        stuff = []
        
        lg, array = convert(file)
        
        for i in range(len(array)):
            for j in range(len(array[i])):
                if len(array[i][j]) >= 1 and array[i][j] == "w":
                    stuff.append(helper2.Wall(number, j,i))
                elif len(array[i][j]) >= 2 and array[i][j][:2] == "pw":
                    #pw09-l-11    9 long, going left, at position 11
                    helper2.Portal.portalWall(stuff, int(array[i][j][2:4]), array[i][j][5], number, int(array[i][j][7:9]))
                elif len(array[i][j]) >= 1 and array[i][j][0] == "p":
                    #p01-02-03   goes to region 1, (2,3)
                    stuff.append(helper2.Portal(number, j,i, int(array[i][j][1:3]), int(array[i][j][4:6]), int(array[i][j][7:9])))
                    
        region = Region(number, stuff, lg)
        
        with open(regionPath + "region" + str(number) + ".p", "wb") as f:
            cpickle.dump(region, f)
        
    def printRegion(numb):
        with open(regionPath + "region" + str(numb) + ".p", "rb") as f:
            region = cpickle.load(f)
        
        for i in region.area:
            temp = ""
            for j in i:
                if type(j) is helper2.Wall:
                    temp += "w"
                elif type(j) is helper2.Portal:
                    temp += "p"
                else:
                    temp += " "
            print(":" + temp)

    def save(self):
        with open(regionPath + "region" + self.numb + ".p", "wb") as file:
            cpickle.dump(self, file)
    
    def load(number):
        with open(regionPath + "region" + str(number) + ".p", "rb") as file:
            ret = cpickle.load(file)
        return ret
            
    def populate(self, stuff=None):
        if stuff == None:
            stuff = self.pop
            
        for i in stuff:
            self.area[i.y][i.x] = i
        
    def updatePop(self):
        remove =  []
            
        for i in self.pop:
            if(hasattr(i, "region") and i.region != self.numb):
                self.area[i.y][i.x] = None
                remove.append(i)
        self.pop = [x for x in self.pop if x not in remove]
        
class Player:
    clothes_quantity = 4
    species_quantity = 2
    
    attr = ["clothes_quantity", "species_quantity"]
    
    def __init__(self):
        for i in Player.attr:
            setattr(self, i, getattr(Player, i))
    
    def setPlayer(player):
        for i in Player.attr:
            setattr(Player, i, getattr(player, i))
        
    def save():
        ps = Player()
        with open(ext + "playerData.p", "wb") as file:
            cpickle.dump(ps, file) 
        
    def load():
        with open(ext + "playerData.p", "rb") as file:
            ps = cpickle.load(file)
        
        Player.setPlayer(ps)
        
class Progress:

    attr = ["region", "x", "y", "direc", "time"]

    def __init__(self):
        self.region = None
        self.x = None
        self.y = None
        self.time = None
        self.direc = None
    
    def setProgress(self, progress):
        for i in Progress.attr:
            setattr(self, i, getattr(progress, i))
        
    def newGame(self):
        self.region = Region(45) #starting region
        self.x = 1       #starting coords
        self.y = 1
        self.direc = (0,1)   #facing down
        self.time = 0
        
    def update(self, game):
        for i in Progress.attr:
            setattr(self, i, getattr(game, i))
        
class Save:
    def __init__(self, char=None, prog=None):
        self.char = char
        self.prog = prog
        
    def set(self):
        Character.setChar(self.char)
        Progress.setProgress(self.prog)

def save(char, prog):
    Player.save()
    
    save = Save(char, prog)
    
    with open(savePath + char.name + ".p", "wb") as file:
        cpickle.dump(save, file)
    
def load(char, app):
    with open(savePath + char + ".p", "rb") as file:
        save = cpickle.load(file)
    app.temp = save
    
def loadPlayer():
    Player.load()