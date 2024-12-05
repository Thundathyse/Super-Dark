import pygame
import pygame_gui
from constants import *
from tile import Tile
from utils import generate_map, locate, inner
from AI import initial
from UI import UIManager

def on_button_pressed():
    print("Button was pressed!")

# Initialize Pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((width, height))
ui_manager = UIManager((width, height), button_callback=on_button_pressed)
pygame.display.set_caption("FINE")
shared_state = {'button_pressed': False}

# Clock
clock = pygame.time.Clock()

# Generate map and tiles
map = generate_map()
belief = initial(map)
ranco = locate(map)


tile = [[Tile((j * cell_size) + 300, (i * cell_size) + 200, cell_size, cell_size, rgb[map[i][j]]) for j in range(cols)] for i in range(rows)]

# Main loop
runner = True
while runner:
    time_delta = clock.tick(60) / 1000.0  # Seconds passed since the last frame
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
            
        ui_manager.process_events(event)

    # Clear screen
    screen.fill(white)

    # Draw tiles
    pygame.draw.rect(screen,black,(290,190,420,420))
    pygame.draw.rect(screen,(200,0,0),(180,190,110,420))
    
    for row in tile:
        for t in row:
            t.show(screen)

    # Highlight cell under mouse
    mox, moy = pygame.mouse.get_pos()
    for i in range(len(tile)):
        for j in range(len(tile[i])):
            if (tile[i][j].x <= mox <= tile[i][j].x + tile[i][j].wi and 
                tile[i][j].y <= moy <= tile[i][j].y + tile[i][j].hi):
                pygame.draw.rect(screen, black, (tile[i][j].x, tile[i][j].y, tile[i][j].wi, tile[i][j].hi), 3)
        ui_manager.process_events(event)

    # Update and Draw
    ui_manager.update(time_delta)
    ui_manager.draw(screen)
    
    pygame.draw.rect(screen,black,(tile[ranco[0]][ranco[1]].x + 25,tile[ranco[0]][ranco[1]].y + 25, 50, 50))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()