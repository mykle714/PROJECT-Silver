import _pickle as cpickle

################################
#Universal Data
white = (255,255,255)
black = (0,0,0)
grey = (150,150,150)
blue = (0,0,255)
color0_0_200 = (0,0,200)            #blue
red = (255,0,0)
color200_0_0 = (200,0,0)            #red
green = (0,255,0)
color0_200_0 = (0,200,0)            #green
newGameMenu = (234,213,123)
charDisplay = (200,200,200)
male = (230,230,250)
female = (255,218,185)
yellowFrame = (255,215,0)
arrow = (255,165,0)
menuFrame = (255,165,0)
calibri = "calibri.ttf"

def textObject(text, font, color):
    surface = font.render(text, True, color)
    return surface

class LinkedGrid:               #2D menus
    def __init__(self):
        self.units = []
        self.head = None
    
    def addUnit(self, name):
        temp = self.findUnit(name)
        if temp != None:
            print("Unit with that name already exists")
            return None
        
        unit = Unit(self, name)
        self.units.append(unit)
        
        if self.head == None:
            self.head = unit
            self.current = unit
            
    def setUnitAdj(self, name, dir, inst):
        unit = self.findUnit(name)
        
        if unit == None:
            return None
        else:
            unit.setAdj(dir, inst)
    
    def setAllAdj(self, name, left=None, right=None, up=None, down=None):
        unit = self.findUnit(name)
        
        if unit == None:
            return None
        else:
            unit.setAllAdj(left, right, up, down)
        
    def findUnit(self, name):
        for i in self.units:
            if i.name == name:
                #print(name, " unit found")
                return i
        #print(name, " unit not found")
        return None
    
    def printGrid(self):
        for i in self.units:
            i.printUnit()
            
    def load(file):
        with open("../data/gameData/regions/" + file + ".p", "rb") as file:
            f = cpickle.load(file)
        return f
        
        
class Unit:
    
    attr = ["left", "right", "up", "down"]
    
    def __init__(self, source, name):
        self.source = source
        self.name = name
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0
        
    def setAdj(self, dir, name):
        unit = self.source.findUnit(name)
        
        if unit == None:
            return None
        else:
            setattr(self, dir, unit)
            
    def setAllAdj(self, left=None, right=None, up=None, down=None):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        
    def getAdj(self, dir):                  #prob not gunna use
        return getattr(self, "self." + dir)
    
    def printUnit(self):
        up = None
        down = None
        left = None
        right = None
        
        if self.up != None:
            up = self.up
            
        if self.down != None:
            down = self.down
            
        if self.left != None:
            left = self.left
            
        if self.right != None:
            right = self.right
            
        print("name: ", self.name, "\tup: ", up, "\tdown: ", down, "\tleft: ", left, "\tright: ", right)