import random
from constants import rows, cols

def generate_map():
    return [[random.randint(0, 2) for i in range(cols)] for i in range(rows)]

def locate(map):
    genco = [random.randint(0,3),random.randint(0,3)]
    print(genco)
    return genco

def inner():
    inmap = []
    twos_count = 0
    max_twos = 3

    for i in range(3):
        row = []
        for j in range(3):
            if twos_count < max_twos:
                value = random.randint(0, 2)
                if value == 2:
                    twos_count += 1
            else:
                # Ensure no more 2s are added once the limit is reached
                value = random.randint(0, 1)
            row.append(value)
        inmap.append(row)

    return inmap