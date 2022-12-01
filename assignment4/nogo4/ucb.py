# Cmput 455 sample code
# UCB algorithm
# Written by Martin Mueller

from math import log, sqrt
import sys
from gtp_connection import point_to_coord, format_point

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


def byPercentage(tuple):
    pass

def byPulls(tuple):
    pass

def writeMoves(board, stats, moves):
    pass

def runUcb(C, arms, init, simulate, maxSimulations):
    stats = [[0,0] for _ in range(arms)]
    for n in range(maxSimulations):
        move = findBest(stats, C, n)
        if simulate(move):
            stats[move][0] += 1 # win
        stats[move][1] += 1
    
    best_index = bestArm(stats)


    