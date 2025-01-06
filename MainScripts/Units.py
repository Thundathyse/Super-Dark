unitdict = {
    1:["Infantry", 1, 10, 10, 1],
    2:["Mech", 1, 10, 20, 2],
    3:["Tank", 1, 10, 30, 3]
}

own = []

active = [unitdict.get(1),
          unitdict.get(2),
          unitdict.get(3)]

class brain:
    def __init__(self, ox, oy,  bx, by, h, belmap, ind):
        self.bx = bx
        self.by = by
        self.h = h
        self.ox = ox
        self.oy = oy
        self.belmap = belmap
        self.health = (unitdict.get(ind))[2]
        self.sp = (unitdict.get(ind))[4]
        self.ind = ind

    def upgrid(self, nmap):
        self.belmap = nmap
        self.h = False

        can = [[0 for _ in range(3)] for _ in range(9)]

        init = 0

        for i in range(9):
            for j in range(3):
                can[init][0] = self.belmap[i%3][j]
                can[init][1] = i
                can[init][2] = j

                init += 1

        n = len(can)
        for i in range(n - 1):
            swap = False
            for j in range(n - i - 1):
                if can[j][0] < can[j + 1][0]:
                    can[j], can[j + 1] = can[j + 1], can[j]
                    swap = True
            if not swap:
                break

        if can[0][0] != can[1][0]:
            self.by = can[0][1]
            self.bx = can[0][2]
            self.h = True

        print(can, "can")
        return self.bx, self.by