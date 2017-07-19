import gameData
import _pickle as cpickle
import sys
sys.path.insert(0, '../helper/')
from BFS import bfs
import multiprocessing as mp

npcPath = "../data/gameData/npcs/"

class Portal:
    
    trigger = "step"
    
    def __init__(self, reg, x, y, toReg, toX, toY):
        self.x = x
        self.y = y
        self.reg = reg
        self.toX = toX
        self.toY = toY
        self.toReg = toReg
        
    def trig(self, game=None):
        if game is not None:
            game.x = self.toX
            game.y = self.toY
            game.region = gameData.Region.load(self.toReg)
        
    """
       ^
    x-----
    
    ^ = direction
    x = coordinates
    - = wall
    """
    def portalWall(source, length, ori, reg, dim):
        for i in range(length):
            if ori == "l":
                source.append(Portal(reg, 0, dim-i, reg-1, 20, dim-i))
            elif ori == "u":
                source.append(Portal(reg, dim+i, 0, reg-10, dim+i, 11))
            elif ori == "r":
                source.append(Portal(reg, 20, dim+i, reg+1, 0, dim+i))
            elif ori == "d":
                source.append(Portal(reg, dim-i, 11, reg+10, dim-i, 0))
        
        
class Wall:
    
    trigger = "none"
    
    def __init__(self, reg, x, y):
        self.reg = reg
        self.x = x
        self.y = y
        
class NPC:
    
    trigger = "z"
    
    def __init__(self, region, x, y, direc, name, todo):
        self.x = x
        self.y = y
        self.direc = direc
        self.region = region
        self.name = name
        self.todo = todo
        
    def trig():
        pass
        
    def generatePath(self, region, x, y):
        with open(gameData.regionPath + "regional.p", "rb") as file:
            regional = cpickle.load(file)
            
        self.pathR = bfs(regional, self.region, region)

    def findPortals(self, pathR, c):
        portals = []

        for i in self.region.area:
            for j in i:
                if type(j) is Portal and j.toReg == pathR[c]:
                    portals.append(j)
                    
        return portals
            
    def queueSubpath(self, portals):
        subpath = None

        for i in portals:
            temp = bfs(self.region.lg, "e" + str(self.x) + "/" + str(self.y), "p" + str(i.x) + "/" + str(i.y))
            if subpath is None or len(temp) < len(subpath):
                subpath = temp
            
            
        self.pathQueue = Queue()
        
        for i in subpath:
            pathQueue.put(i)
            
        self.inTransit = True
            
        #create regions with waypoints, load regions, contrust lg, BFS again
        
        
        
    def save(self):
        with open(npcPath + self.name + ".p", "wb") as file:
            cpickle.dump(self, file)
        
    def load(name):
        with open(npcPath + name + ".p", "rb") as file:
            return cpickle.load(file)
    
class Todo:
    
    def __init__(self, name, region, x, y, direc, dwell, action):
        self.region = region
        self.x = x
        self.y = y
        self.direc = direc
        self.dwell = dwell
        self.name = name
        self.action = action