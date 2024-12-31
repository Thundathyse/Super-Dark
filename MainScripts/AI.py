import math

ss = .5
sfa = 1 - ss
sfb = ((sfa/2) - (sfa/4))
sfa -= sfb
print("Sensor Accuracy: ", ss, "| Sensor Fail (rate) Alpha: ", sfa, "| Sensor Fail (rate) Beta: ", sfb, "\n----")
belief = []

def initial(map):
    belief = [[0 for i in range(len(map))] for j in range(len(map[0]))] # INITIAL BELIEF
    
    for i in range(len(map)):
        for j in range(len(map[i])):
            belief[i][j] = 1/(len(map)*len(map[0]))

    print(belief)
    return belief

def detect(map,reading, belly):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j][0] == reading:
                belly[i][j] *= ss
            else:
                if abs(reading - map[i][j][0]) > 1:
                    belly[i][j] *= sfb
                else:
                    belly[i][j] *= sfa
    nlzr = 0
    for i in range(len(belly)):
        nlzr += sum(belly[i])

    for i in range(len(belly)):
        for j in range(len(belly[i])):
            belly[i][j] /= nlzr

    return belly

def thermdetect(map,reading, belly):
    sfe, sfk, sfg = (sfb/3 + sfb/6), sfb/6, ss/3
    print("new sensor fails", sfe, sfk, sfg)
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j][0] == reading:
                belly[i][j] *= ss
            else:
                if abs(reading - map[i][j][0]) > 1:
                    belly[i][j] *= sfe
                elif abs(reading - map[i][j][0]) > 3:
                    belly[i][j] *= sfk
                else:
                    belly[i][j] *= sfg
    nlzr = 0
    for i in range(len(belly)):
        nlzr += sum(belly[i])

    for i in range(len(belly)):
        for j in range(len(belly[i])):
            belly[i][j] /= nlzr

    return belly

def topdetect(map,reading, belly):
    sfc, sfd = (sfb/2 + sfb/ 4), sfb/4
    print("new sensor fails", sfc, sfd)
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j][0] == reading:
                belly[i][j] *= ss
            else:
                if abs(reading - map[i][j][0]) > 1:
                    belly[i][j] *= sfc
                elif abs(reading - map[i][j][0]) > 3:
                    belly[i][j] *= sfd
                else:
                    belly[i][j] *= sfa
    nlzr = 0
    for i in range(len(belly)):
        nlzr += sum(belly[i])

    for i in range(len(belly)):
        for j in range(len(belly[i])):
            belly[i][j] /= nlzr

    return belly

def combo(red, yel, blu):
    result = [[0 for _ in range(len(red[0]))] for _ in range(len(red))]

    for i in range(len(red)):
        for j in range(len(red[i])):
            result[i][j] = red[i][j] + yel[i][j] + blu[i][j]

    return result
