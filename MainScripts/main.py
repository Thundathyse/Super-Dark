import pygame
from constants import *
from tile import Tile
from utils import generate_map, locate, inner
from AI import initial
from UI import UIManager

def on_button_pressed():
    global dispin  # Use the global dispin variable
    if dispin:  # If currently displaying the inner grid
        print("Returning to the outer grid...")
        dispin = False  # Return to the outer grid
    else:
        print("Button pressed but dispin is False.")

# Initialize Pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((width, height))
ui_manager = UIManager((width, height), button_callback=on_button_pressed)
pygame.display.set_caption("FINE")

# Clock
clock = pygame.time.Clock()

# Generate map and tiles
map = generate_map()
belief = initial(map)
ranco = locate(map)

# Generate mapin (inner grids for each outer grid cell)
mapin = [[inner() for _ in range(len(map[0]))] for _ in range(len(map))]
outer_tile_grid = [
    [Tile((j * cell_size) + 300, (i * cell_size) + 200, cell_size, cell_size, rgb[map[i][j]]) for j in range(cols)]
    for i in range(rows)
]

# State variables
runner = True
dispin = False
seltily, seltilx = 0, 0
current_inner_grid = []

def update_inner_grid(y, x):
    global current_inner_grid
    current_inner_grid = [
        [Tile((j * insize) + 300, (i * insize) + 200, insize, insize, yob[mapin[y][x][i][j]]) for j in range(intc)]
        for i in range(intr)
    ]

# Main loop
while runner:
    time_delta = clock.tick(60) / 1000.0  # Seconds passed since the last frame
    mox, moy = pygame.mouse.get_pos()

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
        ui_manager.process_events(event)

    # Clear screen
    screen.fill(white)

    # Draw UI
    pygame.draw.rect(screen, black, (290, 190, 420, 420))
    pygame.draw.rect(screen, (200, 0, 0), (180, 190, 110, 420))

    if not dispin:
        # Display outer grid
        for row in outer_tile_grid:
            for tile in row:
                tile.show(screen)
        # Highlight cell under mouse
        for i in range(len(outer_tile_grid)):
            for j in range(len(outer_tile_grid[i])):
                tile = outer_tile_grid[i][j]
                if tile.x <= mox <= tile.x + tile.wi and tile.y <= moy <= tile.y + tile.hi:
                    pygame.draw.rect(screen, black, (tile.x, tile.y, tile.wi, tile.hi), 3)
    else:
        # Display current inner grid
        for row in current_inner_grid:
            for tile in row:
                tile.show(screen)
        # Highlight cell under mouse
        for i in range(len(current_inner_grid)):
            for j in range(len(current_inner_grid[i])):
                tile = current_inner_grid[i][j]
                if tile.x <= mox <= tile.x + tile.wi and tile.y <= moy <= tile.y + tile.hi:
                    pygame.draw.rect(screen, black, (tile.x, tile.y, tile.wi, tile.hi), 3)

    # Update and Draw UI
    ui_manager.update(time_delta)
    ui_manager.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()