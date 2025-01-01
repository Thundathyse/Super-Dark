def find(map, y, x, dc, g):
    return ((map[y][x][0] - dc) % 3) * g

def movement(map, speed, dir):
    posmov = [.25, .5, .25]
    movmap = [[[0 for _ in range(3)] for _ in range(4)] for _ in range(4)]
    v = [dir[0] * speed, dir[1] * speed]
    for i in range(len(map)):
        for j in range(len(map[i])):
            addval = [0 for _ in range(3)]  # added values list
            if v[0] > v[1]:
                dc = v[0]
            else:
                dc = v[1]

            for g in range(len(posmov)):
                addval[g] = (find(map, i, j, dc, posmov[g]))

            movmap[i][j] = addval

    nl = 0

    for y in range(len(movmap)):
        for h in range(len(movmap[y])):
            nl += sum(movmap[y][h])

    for t in range(len(movmap)):
        for r in range(len(movmap[t])):
            for d in range(len(movmap[t][r])):
                movmap[t][r][d] /= nl

    for v in range(len(movmap)):
        for b in range(len(movmap[v])):
            movmap[v][b] = sum(movmap[v][b])

    return movmap

def truemove(speed, dir, loc):
    v = [dir[0] * speed, dir[1] * speed]
    print(loc, "og")
    print(v, "lnsa")
    print(((loc[0] - v[0]) % 4), "jog")
    loc[0] = ((loc[0] - v[0]) % 4)
    loc[1] = ((loc[1] - v[1]) % 4)
    print(loc, "loc")
    return loc
