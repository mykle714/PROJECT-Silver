import helper
import helper2
import gameData
import menu
import _pickle as cpickle
import sys
sys.path.insert(0, '../helper/')
import BFS

lg = helper.LinkedGrid()

lg.addUnit("45")
lg.addUnit("46")

lg.setAllAdj("45", right="46")
lg.setAllAdj("46", left="45")

with open(gameData.regionPath + "regional.p", "wb") as f:
    cpickle.dump(lg, f)