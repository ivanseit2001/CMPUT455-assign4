# UCB Algorithm
#The code is based on CMPUT 455 sample codes

import sys
from math import sqrt, log
from gtp_connection import point_to_coord,format_point
#from simulation_util import writeMoves

INFINITY = float('inf')


def mean(stats, i):
    return stats[i][0] / stats[i][1]
    
def ucb(stats, C, i, n):
    if stats[i][1] == 0:
        return INFINITY
    return mean(stats, i)  + C * sqrt(log(n) / stats[i][1])

def findBest(stats, C, n):
    best = -1
    bestScore = -INFINITY
    for i in range(len(stats)):
        score = ucb(stats, C, i, n) 
        if score > bestScore:
            bestScore = score
            best = i
    assert best != -1
    return best

def bestArm(stats): # Most-pulled arm
    best = -1
    bestScore = -INFINITY
    for i in range(len(stats)):
        if stats[i][1] > bestScore:
            bestScore = stats[i][1]
            best = i
    assert best != -1
    return best

def PercentageBased(tuple):
    return tuple[1]

def PullBased(tuple):
    return tuple[3]
def writeMoves(board, moves, stats):
    """
    Modified from simulation_util
    Write simulation results for each move.
    """
    gtp_moves = []
    for i in range(len(moves)):
       # move_string = "Pass"
        if moves[i] != None:
            x, y = point_to_coord(moves[i], board.size)
            move_string = format_point((x, y))
        else:
            move_string="Pass"
        if stats[i][1]!=0:       
            gtp_moves.append((move_string, 
                          stats[i][0]/stats[i][1],stats[i][0],stats[i][1]))
        else:
            gtp_moves.append((move_string,0,stats[i][0],stats[i][1]))
    sys.stderr.write("win rates: {}\n".format(sorted(gtp_moves,
                     key = PercentageBased, reverse = True)))
    sys.stderr.flush()

def runUcb(player,board,moves,toplay):
    stats = [[0,0] for _ in moves]
    for n in range(len(moves)*10):
        move = findBest(stats, 0.4, n)
        result=player.simulation(board,moves[move],toplay)
        if result==toplay:
            stats[move][0] += 1 # win
        stats[move][1] += 1
    bestMove=bestArm(stats)
    best=moves[bestMove]
    writeMoves(board,moves,stats)
    return best
    print("C = {} Statistics: {} Best arm {}".format(C, stats, bestArm(stats)))


# for C in [100, 10, sqrt(2), 1, 0.1, 0.01]:
#     runUcb(C, 10, defaultInit, simulateEasy, 1000)
    #runUcb(C, 4, defaultInit, simulateHard, 1000)
    #runUcb(C, 4, defaultInit, simulateHard, 100000)
    