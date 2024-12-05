import math

ss = .9
sf = 1 - ss

def initial(map):
    belief = [[0 for i in range(len(map))] for j in range(len(map[0]))] # INITIAL BELIEF
    
    for i in range(len(map)):
        for j in range(len(map[i])):
            belief[i][j] = 1/(len(map)*len(map[0]))

    print(belief)
    return belief

def detect(map,reading):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == reading:
                belief[i][j] *= ss
            else:
                belief[i][j] * sf
    print(belief)