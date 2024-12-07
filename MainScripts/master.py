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
main_ui_manager.add_button("Select", (750, 270), (50,20), picks(0))
main_ui_manager.add_button("Select", (750, 320), (50,20), picks(1))
main_ui_manager.add_button("Select", (750, 370), (50,20), picks(2))
pygame.display.set_caption("FINE")

# Clock
clock = pygame.time.Clock()

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
    [Tile((j * cell_size) + 300, (i * cell_size) + 200, cell_size, cell_size, dullrgb[map[i][j]]) for j in range(cols)]
    for i in range(rows) #DECLAN IS NOT ENTIRELY SURE HOW THIS WORKS
]

# State variables
runner = True
dispin = False
seltily, seltilx = 0, 0
current_inner_grid = []

# Set up font
font = pygame.font.Font(None, 25)  # None uses the default font, 36 is the font size
medfont = pygame.font.Font(None, 18)

# Render text
hov = "helo"
hovtext = font.render(hov, True, white) # middle is antialias
title = font.render("Carrier Info", True, white)
slot1 = medfont.render(active[0][0], True, white)
slot2 = medfont.render(active[1][0], True, white)
slot3 = medfont.render(active[2][0], True, white)


def update_inner_grid(y, x):
    """Generate the inner grid for the selected outer cell based on its value."""
    global current_inner_grid
    inner_data = mapin[y][x]  # Retrieve the inner grid data for the selected cell
    current_inner_grid = [
        [
            Tile(
                (j * insize) + 300,
                (i * insize) + 200,
                insize,
                insize,
                woy[inner_data[i][j]]  # Use the specific value for the tile color
            )
            for j in range(len(inner_data[0]))
        ]
        for i in range(len(inner_data))
    ]

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
                    tile.color = rgb[map[i][j]]
                    tile.hovanim(screen)
                else:
                    tile.color = dullrgb[map[i][j]]


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

    Carrier(screen, title, slot1, slot2, slot3)

    main_ui_manager.update(time_delta)
    main_ui_manager.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()