import random
from constants import rows, cols

def generate_map():
    mapper = []
    rc = 0
    mr = 1

    for i in range(rows):
        row = []
        for j in range(cols):
            if rc < mr:
                value = random.randint(0, 2)
                if value == 0:
                    rc += 1
            else:
                # Ensure no more 2s are added once the limit is reached
                value = random.randint(1, 2)
            row.append(value)
        mapper.append(row)
        #print("red count ", i," = ",rc)
    return mapper

def locate(map):
    genco = [random.randint(0,3),random.randint(0,3)]
    #print(genco)
    return genco

def inner(cvaloc):
    inmap = []
    twos_count = 0
    max_twos = cvaloc

    for i in range(3):
        row = []
        for j in range(3):
            if twos_count < max_twos:
                value = random.randint(0, 2)
                if value == 2:
                    twos_count += 1
            else:
                # Ensure no more 2s are added once the limit is reached
                value = random.randint(1, 2)
            row.append(value)
        inmap.append(row)
    return inmap