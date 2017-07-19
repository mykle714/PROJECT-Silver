import helper
import helper2
import gameData
import menu
import _pickle as cpickle
import sys
sys.path.insert(0, '../helper/')
import BFS


npc = helper2.NPC(45, 1, 1, (0,1), "memes", None)
npc.goto(46, 19, 1)