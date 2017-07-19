import sys
sys.path.insert(0, '../code/')
from helper import LinkedGrid
from helper import Unit
import os.path as path
import queue
import random

def convert(f):
    file = open(path.expanduser("~") + "\\Desktop\\" + f + ".csv", "r")
    
    string = file.read()
    array = []
    subarray = []
    buf = ""
    for i in string:
        if i == '\n':
            subarray.append(buf)
            buf = ""
            array.append(subarray)
            subarray = []
        elif i == ',':
            subarray.append(buf)
            buf = ""
        else:
            buf += i
            
    lg = LinkedGrid()

    for i in range(len(array)):
        for j in range(len(array[i])):
            if(array[i][j] != 'w'):
                if(len(array[i][j]) > 0):
                    name = array[i][j][0]
                else:
                    name = "e"
                lg.addUnit(name + str(j) + "/" + str(i))
                temp = lg.findUnit(name + str(j) + "/" + str(i))
                temp.x = j
                temp.y = i
            
    for i in range(len(array)):
        for j in range(len(array[i])):
            left = None
            up = None
            right = None
            down = None
            if(j-1 >= 0 and array[i][j-1] != 'w'):
                left = str(i) + "," + str(j-1)
            if(i-1 >= 0 and array[i-1][j] != 'w'):
                up = str(i-1) + "," + str(j)
            if(j+1 < len(array[i]) and array[i][j+1] != 'w'):
                right = str(i) + "," + str(j+1)
            if(i+1 < len(array) and array[i+1][j] != 'w'):
                down = str(i+1) + "," + str(j)
                
            lg.setAllAdj(str(i) + "," + str(j), left=left, right=right, up=up, down=down)
        
    file.close()
    return lg, array

def bfs(lg, s, g):
    start = str(s)
    goal = str(g)
    q = queue.Queue()
    
    visited = {}
    distances = {}
    
    for i in lg.units:
        visited.update({i.name : False})
        distances.update({i.name : []})
        
    distances[start] = [lg.findUnit(start)]
    visited[start] = True
    current = lg.findUnit(start)
    noEnd = False
    
    while(distances[goal] == []):
        direcs = current.attr.copy()
        random.shuffle(direcs)
        for i in direcs:
            check = lg.findUnit(getattr(current, i))
            if check != None and not visited[check.name]:
                q.put(check)
                distances[check.name] = distances[current.name].copy()
                distances[check.name].append(check)
        if(q.empty()):
            noEnd = True
            break
        else:
            current = q.get(False)

        visited[current.name] = True
        
    if noEnd:
        return None
    else:    
        return distances[goal]
    
def printMap(maap):
    if type(maap) is str:
        print(maap)
    else:
        print(convertBack(maap))
        
def convertBack(array):
    ret = ""
    
    for i in array:
        for j in i:
            if j == '0':
                ret += " "
            elif j == '1':
                ret += "1"
            elif j == ' ':
                ret += "x"
            ret += " "
        ret += "\n"
        
    return ret