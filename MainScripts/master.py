import pygame
from pygame import RESIZABLE

from constants import *
from MoveLogic import *
from Graphics import Tile, inTile
from utils import *
from AI import *
from UI import UIManager
from Key import *
from Units import *

def returnover():
    global dispin  # Use the global dispin variable
    if dispin:  # If currently displaying the inner grid
        dispin = False  # Return to the outer grid
    else:
        print("no need")

def switchview():
    global view
    if view[0]:
        view[0] = False
        view[1] = True
    elif view[1]:
        view[1] = False
        view[2] = True
    elif view[2]:
        view[2] = False
        view[0] = True

def empty(x,y):
    return [[0 for _ in range(x)] for _ in range(y)]

def provide(gridy, gridx):
    li = ow(gridy, gridx)
    loc, tloc, toploc = mapin[gridy][gridx], thermapin[gridy][gridx], toppin[gridy][gridx]
    for i in range(len(li)):
        blif = initial(loc)
        print("Initial belief map ", blif, ". \n----")
        nblif = (detect(loc,loc[li[i][0]][li[i][1]][0], blif))
        print("Post Baye's motion belief map ", nblif, ". \n----")
        if moves > 1:
            tnblif = (thermdetect(tloc,tloc[li[i][0]][li[i][1]][0], blif))
            print("Post Baye's thermal belief map ", nblif, ". \n----")
            if moves > 2:
                topnblif = (topdetect(toploc,toploc[li[i][0]][li[i][1]][0], blif))
                print("Post Baye's topographical belief map ", nblif, ". \n----")
        tnblif,topnblif = empty(4,4),empty(4,4)

        fina = (combo(nblif, tnblif, topnblif))
        print("Post combination belief map ", fina, ". \n----")
        allunits[gridy][gridx][li[i][0]][li[i][1]].upgrid(fina)
    Turn(moves)


def possibleread(outy, outx, iny, inx):
    if allunits[outy][outx][iny][inx] != [0]:
        if not allunits[outy][outx][iny][inx].h:
            return "pos. is uncertain"
        else:
            return "(" + str(allunits[outy][outx][iny][inx].bx) + "," + str(abs(allunits[outy][outx][iny][inx].by - 2)) + ")"
    else:
        return ""


def ow(x,y):#where troop
    grid = mapin[x][y]
    lotl = []#list of troop locations
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j][2] != 0:
                lotl.append([i,j])
    print("List of motion troop locations " , lotl, ". In the inner grid ", y, ", ",x)
    return lotl

#TROOP DROP SYSTEM
pick = [False, False, False]

bugdict = {
    0: "Resources/NONE.png",
    1: "Resources/Bugs/LBl.png",
    2: "Resources/Bugs/LBg.png",
    3: "Resources/Bugs/LBp.png",
    4: "Resources/Bugs/LBb.png",
    5: "Resources/Bugs/QB.png"
}

fdict = {
    0: "Resources/NONE.png",
    1: "Resources/Friendlies/Infantry.png",
    2: "Resources/Friendlies/Mech.png",
    3: "Resources/Friendlies/Rover.png",
}

bsprite = []

for i in range(len(bugdict)):
    bsprite.append(1)
    bsprite[i] = pygame.image.load(bugdict.get(i))
    bsprite[i] = pygame.transform.scale(bsprite[i], (50, 50))

fsprite = []

for i in range(len(fdict)):
    fsprite.append(1)
    fsprite[i] = pygame.image.load(fdict.get(i))
    fsprite[i] = pygame.transform.scale(fsprite[i], (50, 50))

def Turn(val):
    global moves, faction
    if moves > 0:
        moves -= val
    if moves <= 0:
        faction = toggle(faction)

def toggle(ooto):
    if ooto == 0:
        ooto = 1
    else:
        ooto = 0
    return ooto

def direct(val):
    lt = ow(seltily, seltilx)
    if lt:
        for u in range(len(lt)):
            allunits[seltily][seltilx][lt[u][0]][lt[u][1]].belmap = movement(mapin[seltily][seltilx], allunits[seltily][seltilx][lt[u][0]][lt[u][1]].sp, val)
            nloc = truemove(allunits[seltily][seltilx][lt[u][0]][lt[u][1]].sp, val, [lt[u][0], lt[u][1]])
            mapin[seltily][seltilx][nloc[0]][nloc[1]][2] = allunits[seltily][seltilx][lt[u][0]][lt[u][1]].ind
            mapin[seltily][seltilx][lt[u][0]][lt[u][1]][2] = 0
            allunits[seltily][seltilx][nloc[0]][nloc[1]] = allunits[seltily][seltilx][lt[u][0]][lt[u][1]]
            allunits[seltily][seltilx][lt[u][0]][lt[u][1]] = [0]
            update_inner_grid(seltily,seltilx)
            print(ow(seltily, seltilx))
            Turn(2)
    else:
        print("nah")

allunits = emp(4)
for i in range(len(allunits)):
    for j in range(len(allunits[i])):
        allunits[i][j] = emp(4)

def droptroop(num, outy, outx, iny, inx): #w means "whose turn?"
    if (pick[num]) and active[num][2] > 0 and mapin[outy][outx][iny][inx][2] == 0:
        active[num][2] -= 1
        pick[num] = False
        mapin[outy][outx][iny][inx][2] = active[num][4] # speed
        Turn(1)
        allunits[outy][outx][iny][inx] = (brain(outx, outy, -1, -1, False, [0], num + 1))
        update_inner_grid(outy, outx)
    else:
        print("No")

def setonly(boolarray, index):
    for i in range(len(boolarray)):
        if boolarray[i]:
            boolarray[i] = False
    boolarray[index] = True

def picks(slot):
    setonly(pick, slot)

def pickbug(cu, y, x):
    return font.render(cu[y][x][1], True, black)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height),RESIZABLE)

# Set up screen
inner_ui_manager = UIManager((width, height))
main_ui_manager = UIManager((width, height))
inner_ui_manager.add_button("Back", (185, 200), (100, 50), returnover)
inner_ui_manager.add_button("View", (185, 260), (100, 50), switchview)
inner_ui_manager.add_button("North", (210, 320), (45, 30), lambda: direct([1,0]))
inner_ui_manager.add_button("West", (185, 350), (40, 30), lambda: direct([0,1]))
inner_ui_manager.add_button("South", (210, 380), (45, 30), lambda: direct([-1,0]))
inner_ui_manager.add_button("East", (240, 350), (40, 30), lambda: direct([0,-1]))
main_ui_manager.add_button("Select", (750, 270), (50,20), lambda: picks(0)) # lambda Function: This allows you to pass a function that will be called later (when the button is clicked) instead of immediately calling picks during the button's creation.
main_ui_manager.add_button("Select", (750, 320), (50,20), lambda: picks(1))
main_ui_manager.add_button("Select", (750, 370), (50,20), lambda: picks(2))
main_ui_manager.add_button("Transmit Readings(End turn)", (297, 125), (405,60), lambda: provide(seltily,seltilx))
pygame.display.set_caption("FINE")

# Clock
clock = pygame.time.Clock()


# Set up font
font = pygame.font.Font(None, 25)  # None uses the default font, 36 is the font size
medfont = pygame.font.Font(None, 18)
keyt = medfont.render("Scanner Detecting:", True, white)
keytt = medfont.render("Dropped Unit:", True, white)

def label(cu, y, x, col):
    if not col:
        return font.render(cu[y][x][1], True, black)
    else:
        return font.render(cu[y][x][1], True, white)

# Generate map and tiles
map = generate_map()
belief = initial(map)

# Generate mapin (inner grids for each outer grid cell)
mapin = []
thermapin = []
toppin = []
for i in range(len(map)):
    row = []
    trow = []
    topw = []
    for j in range(len(map[0])):
        row.append(inner(map[i][j]))
        trow.append(thermapper())
        topw.append(thermapper())
    mapin.append(row)
    thermapin.append(trow)
    toppin.append(topw)

outer_tile_grid = [
    [Tile((j * cell_size) + 300, (i * cell_size) + 200, cell_size, cell_size, dullryg[map[i][j][0]], label(map, i, j, False)) for j in range(cols)]
    for i in range(rows) #DECLAN IS NOT ENTIRELY SURE HOW THIS WORKS
]


# State variables
moves = 4
faction = 1
runner = True
dispin = False
view = [True, False, False]
global seltily, seltilx
seltily, seltilx = -1, -1
current_inner_grid = []
current_intherm_grid = []
current_intop_grid = []

# Render text
hov = "helo"
hovtext = font.render(hov, True, white) # middle is antialias
title = font.render("Carrier Info", True, white)
cert = medfont.render("Belief Position:", True, white)

def update_inner_grid(y, x):
    global current_inner_grid, current_intherm_grid, current_intop_grid
    inner_data = mapin[y][x] # Retrieve the inner motion grid data for the selected cell
    intherm_data = thermapin[y][x]
    intop_data = toppin[y][x]
    print("vassoj", inner_data)
    current_inner_grid = [[inTile((j * insize) + 300,(i * insize) + 200,insize,insize,woyr[inner_data[i][j][0]], label(inner_data, i, j, False),bsprite[inner_data[i][j][3]],fsprite[inner_data[i][j][2]]) for j in range(len(inner_data[0]))]for i in range(len(inner_data))] # TEMPORARY, for show with the friendly
    current_intherm_grid = [[inTile((j * insize) + 300,(i * insize) + 200,insize,insize,bgyor[intherm_data[i][j][0]], label(intherm_data, i, j, False),bsprite[inner_data[i][j][3]],fsprite[inner_data[i][j][2]]) for j in range(len(inner_data[0]))]for i in range(len(inner_data))]
    current_intop_grid = [[inTile((j * insize) + 300,(i * insize) + 200,insize,insize,blues[intop_data[i][j][0]], label(intop_data, i, j, True),bsprite[inner_data[i][j][3]],fsprite[inner_data[i][j][2]]) for j in range(len(inner_data[0]))]for i in range(len(inner_data))]


#OVERWORLD STAGES
chosen = [0,0]
certain = ""

# Main loop
while runner:
    time_delta = clock.tick(60) / 1000.0  # Seconds passed since the last frame
    mox, moy = pygame.mouse.get_pos()

    hov = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if not dispin:
                # Check if a cell on the outer grid is clicked
                for i in range(len(outer_tile_grid)):
                    for j in range(len(outer_tile_grid[i])):
                        tile = outer_tile_grid[i][j]
                        if tile.x <= mox <= tile.x + tile.wi and tile.y <= moy <= tile.y + tile.hi:
                            seltily, seltilx = i, j
                            chosen[0],chosen[1] = i,j
                            dispin = True
                            update_inner_grid(seltily, seltilx)
                            break
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    if dispin:  # Only check inner cells if we're in the inner grid view
                        for i in range(len(current_inner_grid)):
                            for j in range(len(current_inner_grid[i])):
                                tile = current_inner_grid[i][j]
                                if tile.x <= event.pos[0] <= tile.x + tile.wi and tile.y <= event.pos[1] <= tile.y + tile.hi:
                                    print(f"Clicked inner cell at ({i}, {j})")
                                    curs = -1
                                    for h in range(len(pick)):
                                        if pick[h]:
                                            curs = h
                                        if curs !=  -1 and active[curs][1] > 0:
                                            droptroop(curs, seltily, seltilx, i, j)
                                            update_inner_grid(seltily, seltilx)
                                    break
        inner_ui_manager.process_events(event)
        main_ui_manager.process_events(event)

    # Clear screen
    screen.fill(gray)

    # Draw UI
    pygame.draw.rect(screen, black, (290, 190, 420, 420))
    pygame.draw.rect(screen, (200, 0, 0), (180, 190, 110, 420))

    # Draw key
    certaintext = font.render(str(certain), True, white)

    Key(screen, keyt, keytt, cert, certaintext)

    if not dispin:
        # Display outer grid
        pygame.draw.rect(screen, black, (180, 495, 110, 30))
        for row in outer_tile_grid:
            for tile in row:
                tile.show(screen)
        # Highlight cell under mouse
        for i in range(len(outer_tile_grid)):
            for j in range(len(outer_tile_grid[i])):
                tile = outer_tile_grid[i][j]
                if tile.x <= mox <= tile.x + tile.wi and tile.y <= moy <= tile.y + tile.hi:
                    hov = f"({j}, {abs(i - 3)})"
                    tile.color = ryg[map[i][j][0]]
                    tile.hovanim(screen)
                else:
                    tile.color = dullryg[map[i][j][0]]
        certain = ""


    else:
        inner_ui_manager.update(time_delta)
        inner_ui_manager.draw(screen)

        if view[0]:
            # Display current inner grid
            pygame.draw.rect(screen, black, (180, 495, 110, 30))
            for row in current_inner_grid:
                for tile in row:
                    tile.show(screen)
            # Highlight cell under mouse
            for i in range(len(current_inner_grid)):
                for j in range(len(current_inner_grid[i])):
                    tile = current_inner_grid[i][j]
                    if tile.x <= mox <= tile.x + tile.wi and tile.y <= moy <= tile.y + tile.hi:
                        hov = f"IN ({seltilx},{abs(seltily -3)}),({j}, {abs(i - 2)})"
                        certain = str(possibleread(seltily, seltilx, i, j))
                        tile.hovanim(screen)
        elif view[2]:
            # Display current inner grid
            pygame.draw.rect(screen, black, (180, 495, 110, 30))
            for r in current_intherm_grid:
                for th in r:
                    th.show(screen)
            # Highlight cell under mouse
            for i in range(len(current_intherm_grid)):
                for j in range(len(current_intherm_grid[i])):
                    th = current_intherm_grid[i][j]
                    if th.x <= mox <= th.x + th.wi and th.y <= moy <= th.y + th.hi:
                        hov = f"IN ({seltilx},{abs(seltily - 3)}),({j}, {abs(i - 2)})"
                        certain = str(possibleread(seltily, seltilx, i, j))
                        th.hovanim(screen)
        elif view[1]:
            # Display current inner grid
            pygame.draw.rect(screen, black, (180, 495, 110, 30))
            for f in current_intop_grid:
                for gh in f:
                    gh.show(screen)
            # Highlight cell under mouse
            for i in range(len(current_intop_grid)):
                for j in range(len(current_intop_grid[i])):
                    th = current_intop_grid[i][j]
                    if th.x <= mox <= th.x + th.wi and th.y <= moy <= th.y + th.hi:
                        hov = f"IN ({seltilx},{abs(seltily -3)}),({j}, {abs(i - 2)})"
                        certain = str(possibleread(seltily, seltilx, i, j))
                        th.hovanim(screen)

    # Hover Text
    if hov:  # Only render if hov is not empty
        hovtext = font.render(hov, True, white)
        if not dispin:
            screen.blit(hovtext, (210, 500))
        else:
            screen.blit(hovtext, (185, 500))

    slot1 = medfont.render((active[0][0] + " (" + str(active[0][2]) + ")"), True, white)
    slot2 = medfont.render((active[1][0] + " (" + str(active[1][2]) + ")"), True, white)
    slot3 = medfont.render((active[2][0] + " (" + str(active[2][2]) + ")"), True, white)

    # Turn display
    wt = ["Enemies'", "Friendlies'"]
    tur = font.render((wt[faction] + " turn:"), True, white)
    nomt = font.render(("Moves " + str(moves)), True, white)

    turnBanner(screen, tur, nomt)
    Carrier(screen, title, slot1, slot2, slot3)

    main_ui_manager.update(time_delta)
    main_ui_manager.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
