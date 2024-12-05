import random
from constants import rows, cols

def generate_map():
    return [[random.randint(0, 2) for i in range(cols)] for i in range(rows)]

def locate(map):
    genco = [random.randint(0,3),random.randint(0,3)]
    print(genco)
    return genco

def inner(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 0:
                inmap = [random.randint(0,1) for i in range(4)]
            elif map[i][j] == 1:
                inmap = [random.randint(0,1) for i in range(4)]
            else:
                inmap = [0 for i in range(4)]