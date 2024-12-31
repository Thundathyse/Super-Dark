import random
from constants import rows, cols

inthreatlevel = {
    0:"No Threat",
    1:"Low Threat",
    2:"Med Threat",
    3:"High Threat"
}

outthreatlevel = {
    0:"High Threat",
    1:"Med Threat",
    2:"Low Threat"
}

thermlevel = {
    0:"10-20",
    1:"20-30",
    2:"30-40",
    3:"40-50",
    4:"50+"
}

def generate_map():
    mapper = []
    rc = 0
    mr = 1

    for i in range(rows):
        row = []
        for j in range(cols):
            value = []
            if rc < mr:
                value.append(random.randint(0, 2))
                if value[0] == 0:
                    rc += 1
            else:
                # Ensure no more 2s are added once the limit is reached
                value.append(random.randint(1, 2))
            value.append(outthreatlevel.get(value[0]))
            row.append(value)
        mapper.append(row)
    return mapper

def emp(size):
    mapper = []

    for i in range(size):
        row = []
        for j in range(size):
            value = []
            value.append(0)
            row.append(value)
        mapper.append(row)
    return mapper

def locate(map):
    genco = [random.randint(0,3),random.randint(0,3)]
    return genco

def lowtrun():
    count = 0
    inmap = []

    for i in range(3):
        row = []
        for j in range(3):
            value = []
            if count < 5:
                value.append(random.randint(0, 2))
                if value[0] == 1:
                    count += 1
            else:
                value.append(random.randint(0, 0))
            value.append(inthreatlevel.get(value[0]))
            value.append(0)
            value.append(0)
            row.append(value)
        inmap.append(row)
    return inmap

def medtrun():
    count = 0
    inmap = []

    for i in range(3):
        row = []
        for j in range(3):
            value = []
            if count < 8:
                value.append(random.randint(0, 3))
                if value[0] == 3:
                    count += 1
            else:
                value.append(random.randint(0, 2))
            value.append(inthreatlevel.get(value[0]))
            value.append(0)
            value.append(0)
            row.append(value)
        inmap.append(row)
    return inmap

def hightrun():
    count = 0
    inmap = []

    for i in range(3):
        row = []
        for j in range(3):
            value = []
            if count < 8:
                value.append(random.randint(1, 3))
                if value[0] == 3:
                    count += 1
            else:
                value.append(random.randint(1, 2))
            value.append(inthreatlevel.get(value[0]))
            value.append(0)
            value.append(0)
            row.append(value)
        inmap.append(row)
    return inmap

def thermrun():
    count = 0
    thermap = []

    for i in range(3):
        row = []
        for j in range(3):
            value = []
            if count < 4:
                value.append(random.randint(0, 4))
                if value == 4:
                    count += 1
            else:
                value.append(random.randint(0, 2))
            value.append(thermlevel.get(value[0]))
            row.append(value)
        thermap.append(row)
    return thermap

def inner(cvaloc):
    if cvaloc[0] == 2:
        inmap = lowtrun()
    elif cvaloc[0] == 1:
        inmap = medtrun()
    else:
        inmap = hightrun()
    return inmap

def thermapper():
    return thermrun()