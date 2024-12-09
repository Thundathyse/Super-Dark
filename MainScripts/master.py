import pygame
from constants import *
from Graphics import Tile
from utils import generate_map, locate, inner
from AI import initial
from UI import UIManager
from Key import *
from Units import *

def returnover():
    global dispin  # Use the global dispin variable
    if dispin:  # If currently displaying the inner grid
        print("Returning to the outer grid...")
        dispin = False  # Return to the outer grid
    else:
        print("Button pressed but dispin is False.")

#TROOP DROP SYSTEM
pick = [False, False, False]

def droptroop(num, outy, outx, iny, inx):
    active[num][1] -= 1
    print(active[num][1])
    pick[num] = False
    mapin[outy][outx][iny][inx][0] = 3

def setonly(boolarray, index):
    for i in range(len(boolarray)):
        if boolarray[i]:
            boolarray[i] = False
    boolarray[index] = True

def picks(slot):
    setonly(pick, slot)


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))

# Set up screen
inner_ui_manager = UIManager((width, height))
main_ui_manager = UIManager((width, height))
inner_ui_manager.add_button("Back", (185, 200), (100, 50), returnover)
main_ui_manager.add_button("Select", (750, 270), (50,20), lambda: picks(0)) # lambda Function: This allows you to pass a function that will be called later (when the button is clicked) instead of immediately calling picks during the button's creation.
main_ui_manager.add_button("Select", (750, 320), (50,20), lambda: picks(1))
main_ui_manager.add_button("Select", (750, 370), (50,20), lambda: picks(2))
pygame.display.set_caption("FINE")

# Clock
clock = pygame.time.Clock()


# Set up font
font = pygame.font.Font(None, 25)  # None uses the default font, 36 is the font size
medfont = pygame.font.Font(None, 18)


def createlabel(cu, y, x):

    return font.render(cu[y][x][1], True, black)


# Generate map and tiles
map = generate_map()
belief = initial(map)
ranco = locate(map)

# Generate mapin (inner grids for each outer grid cell)
mapin = []
for i in range(len(map)):
    row = []
    for j in range(len(map[0])):
        row.append(inner(map[i][j]))
    mapin.append(row)

outer_tile_grid = [
    [Tile((j * cell_size) + 300, (i * cell_size) + 200, cell_size, cell_size, dullryg[map[i][j][0]], createlabel(map, i, j)) for j in range(cols)]
    for i in range(rows) #DECLAN IS NOT ENTIRELY SURE HOW THIS WORKS
]


# State variables
runner = True
dispin = False
seltily, seltilx = 0, 0
current_inner_grid = []

# Render text
hov = "helo"
hovtext = font.render(hov, True, white) # middle is antialias
title = font.render("Carrier Info", True, white)

def update_inner_grid(y, x):
    """Generate the inner grid for the selected outer cell based on its value."""
    global current_inner_grid
    inner_data = mapin[y][x]  # Retrieve the inner grid data for the selected cell
    current_inner_grid = [[Tile((j * insize) + 300,(i * insize) + 200,insize,insize,woyr[inner_data[i][j][0]], createlabel(inner_data, i, j)) for j in range(len(inner_data[0]))]for i in range(len(inner_data))]

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
                            dispin = True
                            update_inner_grid(seltily, seltilx)
                            break
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    if dispin:  # Only check inner cells if we're in the inner grid view
                        for i in range(len(current_inner_grid)):
                            for j in range(len(current_inner_grid[i])):
                                tile = current_inner_grid[i][j]
                                if tile.x <= event.pos[0] <= tile.x + tile.wi and tile.y <= event.pos[
                                    1] <= tile.y + tile.hi:
                                    print(f"Clicked inner cell at ({i}, {j})")
                                    curs = -1
                                    for h in range(len(pick)):
                                        if pick[h]:
                                            curs = h
                                            print("curs ", curs)
                                    if curs !=  -1 and active[curs][1] > 0:
                                        print(event.pos[0])
                                        droptroop(curs, seltily, seltilx, i, j)
                                        update_inner_grid(seltily, seltilx)
                                    else:
                                        print("stick,")
                                    break
        inner_ui_manager.process_events(event)
        main_ui_manager.process_events(event)

    # Clear screen
    screen.fill(gray)

    # Draw UI
    pygame.draw.rect(screen, black, (290, 190, 420, 420))
    pygame.draw.rect(screen, (200, 0, 0), (180, 190, 110, 420))

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


    else:
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
                    tile.hovanim(screen)
        # Update and Draw UI
        inner_ui_manager.update(time_delta)
        inner_ui_manager.draw(screen)

    # Hover Text
    if hov:  # Only render if hov is not empty
        hovtext = font.render(hov, True, white)
        if not dispin:
            screen.blit(hovtext, (210, 500))
        else:
            screen.blit(hovtext, (185, 500))

    slot1 = medfont.render((active[0][0] + " (" + str(active[0][1]) + ")"), True, white)
    slot2 = medfont.render((active[1][0] + " (" + str(active[1][1]) + ")"), True, white)
    slot3 = medfont.render((active[2][0] + " (" + str(active[2][1]) + ")"), True, white)

    Carrier(screen, title, slot1, slot2, slot3)

    main_ui_manager.update(time_delta)
    main_ui_manager.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
