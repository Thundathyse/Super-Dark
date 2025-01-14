import pygame
from pygame import RESIZABLE
import random
from constants import *
from MoveLogic import *
from Graphics import Tile, inTile
from utils import *
from AI import *
from UI import UIManager
from Key import *
from Units import *


# Toggles between displaying the inner and outer grid
def returnover():
    global displaying_inner_grid  # Use the global variable for inner grid display state
    if displaying_inner_grid:  # If currently displaying the inner grid
        displaying_inner_grid = False  # Switch to outer grid
    else:
        print("Outer grid already displayed")


# Cycles through the three different views
def switchview():
    global view_states
    if view_states[0]:
        view_states[0] = False
        view_states[1] = True
    elif view_states[1]:
        view_states[1] = False
        view_states[2] = True
    elif view_states[2]:
        view_states[2] = False
        view_states[0] = True


# Creates a 2D grid initialized with zeros
def empty(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]


# Updates the belief maps based on the grid's motion, thermal, and topographical data
def provide(grid_y, grid_x):
    troop_locations = get_troop_positions(grid_y, grid_x)
    motion_map, thermal_map, topo_map = motion_grids[grid_y][grid_x], thermal_grids[grid_y][grid_x], topo_grids[grid_y][
        grid_x]
    for i in range(len(troop_locations)):
        initial_belief = calculate_initial_belief(motion_map)
        print("Initial belief map", initial_belief, ".\n----")
        motion_belief = update_motion_belief(motion_map, motion_map[troop_locations[i][0]][troop_locations[i][1]][0],
                                             initial_belief)
        print("Post motion belief map", motion_belief, ".\n----")

        if available_moves > 1:
            thermal_belief = update_thermal_belief(thermal_map,
                                                   thermal_map[troop_locations[i][0]][troop_locations[i][1]][0],
                                                   initial_belief)
            print("Post thermal belief map", thermal_belief, ".\n----")

            if available_moves > 2:
                topo_belief = update_topo_belief(topo_map, topo_map[troop_locations[i][0]][troop_locations[i][1]][0],
                                                 initial_belief)
                print("Post topo belief map", topo_belief, ".\n----")

        thermal_belief, topo_belief = empty(4, 4), empty(4, 4)
        combined_belief = combine_beliefs(motion_belief, thermal_belief, topo_belief)
        print("Final combined belief map", combined_belief, ".\n----")

        all_units[grid_y][grid_x][troop_locations[i][0]][troop_locations[i][1]].update_belief_grid(combined_belief)

    process_turn(available_moves)


# Checks if a position contains a unit and returns its state
def possibleread(outer_y, outer_x, inner_y, inner_x):
    if all_units[outer_y][outer_x][inner_y][inner_x] != [0]:
        unit = all_units[outer_y][outer_x][inner_y][inner_x]
        if not unit.is_hidden:
            return "Position is uncertain"
        else:
            return f"({unit.x}, {abs(unit.y - 2)})"
    return ""


# Retrieves all troop positions from a given grid cell
def get_troop_positions(grid_y, grid_x):
    current_grid = motion_grids[grid_y][grid_x]
    troop_positions = []
    for i in range(len(current_grid)):
        for j in range(len(current_grid[i])):
            if current_grid[i][j][2] != 0:
                troop_positions.append([i, j])
    print("Troop positions in grid", grid_y, grid_x, ":", troop_positions)
    return troop_positions


# Troop selection state
selected_troops = [False, False, False]

# Dictionary of bug images with their paths
bug_image_paths = {
    0: "Resources/NONE.png",
    1: "Resources/Bugs/LBl.png",
    2: "Resources/Bugs/LBg.png",
    3: "Resources/Bugs/LBp.png",
    4: "Resources/Bugs/LBb.png",
    5: "Resources/Bugs/QB.png"
}

# Load and scale bug images
bug_sprites = [pygame.transform.scale(pygame.image.load(bug_image_paths[i]), (50, 50)) for i in bug_image_paths]

# Dictionary of friendly unit images with their paths
friendly_image_paths = {
    0: "Resources/NONE.png",
    1: "Resources/Friendlies/Infantry.png",
    2: "Resources/Friendlies/Mech.png",
    3: "Resources/Friendlies/Rover.png"
}

# Load and scale friendly unit images
friendly_sprites = [pygame.transform.scale(pygame.image.load(friendly_image_paths[i]), (50, 50)) for i in
                    friendly_image_paths]


# Handles end-of-turn logic
def process_turn(value):
    global available_moves, current_faction
    if available_moves > 0:
        available_moves -= value
    if available_moves <= 0:
        current_faction = toggle_faction(current_faction)


# Toggles between factions
def toggle_faction(current_faction):
    return 1 if current_faction == 0 else 0


# Directs troop movement based on user input
def direct_movement(direction):
    troop_positions = get_troop_positions(selected_tile_y, selected_tile_x)
    if troop_positions:
        for unit_index in range(len(troop_positions)):
            unit = all_units[selected_tile_y][selected_tile_x][troop_positions[unit_index][0]][
                troop_positions[unit_index][1]]
            unit.belief_map = calculate_movement(motion_grids[selected_tile_y][selected_tile_x], unit.speed, direction)
            new_location = determine_new_location(unit.speed, direction,
                                                  [troop_positions[unit_index][0], troop_positions[unit_index][1]])

            motion_grids[selected_tile_y][selected_tile_x][new_location[0]][new_location[1]][2] = unit.index
            motion_grids[selected_tile_y][selected_tile_x][troop_positions[unit_index][0]][
                troop_positions[unit_index][1]][2] = 0

            all_units[selected_tile_y][selected_tile_x][new_location[0]][new_location[1]] = unit
            all_units[selected_tile_y][selected_tile_x][troop_positions[unit_index][0]][
                troop_positions[unit_index][1]] = [0]

            update_inner_grid(selected_tile_y, selected_tile_x)
            print(get_troop_positions(selected_tile_y, selected_tile_x))
            process_turn(2)
    else:
        print("No troops available for movement")


# Initialize the grid for all units
all_units = create_empty_grid(4)
for i in range(len(all_units)):
    for j in range(len(all_units[i])):
        all_units[i][j] = create_empty_grid(4)


# Drops a troop onto the grid at the specified position
def drop_troop(unit_type, outer_y, outer_x, inner_y, inner_x):
    if (selected_troops[unit_type]) and active_units[unit_type][2] > 0 and \
            motion_grids[outer_y][outer_x][inner_y][inner_x][2] == 0:
        active_units[unit_type][2] -= 1
        selected_troops[unit_type] = False
        motion_grids[outer_y][outer_x][inner_y][inner_x][2] = active_units[unit_type][4]  # Assign speed
        process_turn(1)
        all_units[outer_y][outer_x][inner_y][inner_x] = create_unit_brain(outer_x, outer_y, -1, -1, False, [0],
                                                                          unit_type + 1)
        update_inner_grid(outer_y, outer_x)
    else:
        print("Cannot drop troop at this location")


# Sets a single troop selection as active
def set_single_selection(selection_array, index):
    for i in range(len(selection_array)):
        selection_array[i] = False
    selection_array[index] = True


# Selects a troop slot
def select_troop(slot_index):
    set_single_selection(selected_troops, slot_index)


# Generates label for a bug at a given position
def generate_bug_label(unit_grid, y, x):
    return default_font.render(unit_grid[y][x][1], True, black)


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((window_width, window_height), RESIZABLE)

# Set up screen UI
inner_ui_manager = UIManager((window_width, window_height))
main_ui_manager = UIManager((window_width, window_height))
inner_ui_manager.add_button("Back", (185, 200), (100, 50), returnover)
inner_ui_manager.add_button("View", (185, 260), (100, 50), switchview)
inner_ui_manager.add_button("North", (210, 320), (45, 30), lambda: direct_movement([1, 0]))
inner_ui_manager.add_button("West", (185, 350), (40, 30), lambda: direct_movement([0, 1]))
inner_ui_manager.add_button("South", (210, 380), (45, 30), lambda: direct_movement([-1, 0]))
inner_ui_manager.add_button("East", (240, 350), (40, 30), lambda: direct_movement([0, -1]))
main_ui_manager.add_button("Select", (750, 270), (50, 20), lambda: select_troop(0))
main_ui_manager.add_button("Select", (750, 320), (50, 20), lambda: select_troop(1))
main_ui_manager.add_button("Select", (750, 370), (50, 20), lambda: select_troop(2))
main_ui_manager.add_button("Transmit Readings (End turn)", (297, 125), (405, 60),
                           lambda: provide(selected_tile_y, selected_tile_x))
pygame.display.set_caption("FINE")

# Clock for game loop
clock = pygame.time.Clock()

# Set up fonts
default_font = pygame.font.Font(None, 25)
medium_font = pygame.font.Font(None, 18)
scanner_label = medium_font.render("Scanner Detecting:", True, white)
dropped_unit_label = medium_font.render("Dropped Unit:", True, white)


# Generates a label for a specific unit
def generate_label(unit_grid, y, x, is_highlighted):
    color = white if is_highlighted else black
    return default_font.render(unit_grid[y][x][1], True, color)


# Generate map and tiles
outer_map = generate_map()
motion_beliefs = calculate_initial_belief(outer_map)

# Generate inner grids for each cell in the outer map
motion_grids, thermal_grids, topo_grids = [], [], []
for i in range(len(outer_map)):
    motion_row, thermal_row, topo_row = [], [], []
    for j in range(len(outer_map[0])):
        motion_row.append(generate_inner_grid(outer_map[i][j]))
        thermal_row.append(generate_thermal_grid())
        topo_row.append(generate_topo_grid())
    motion_grids.append(motion_row)
    thermal_grids.append(thermal_row)
    topo_grids.append(topo_row)

outer_tile_grid = [
    [Tile((j * cell_size) + 300, (i * cell_size) + 200, cell_size, cell_size, outer_tile_colors[outer_map[i][j][0]],
          generate_label(outer_map, i, j, False)) for j in range(columns)]
    for i in range(rows)
]

# State variables
available_moves = 4
current_faction = 1
game_running = True
displaying_inner_grid = False
view_states = [True, False, False]
selected_tile_y, selected_tile_x = -1, -1
current_inner_grid = []
current_thermal_grid = []
current_topo_grid = []

# Render text labels
hover_text = ""
hover_display = default_font.render(hover_text, True, white)
title_label = default_font.render("Carrier Info", True, white)
belief_position_label = medium_font.render("Belief Position:", True, white)


# Updates the inner grid visuals based on the selected cell
def update_inner_grid(y, x):
    global current_inner_grid, current_thermal_grid, current_topo_grid
    motion_data = motion_grids[y][x]  # Motion grid for the selected cell
    thermal_data = thermal_grids[y][x]
    topo_data = topo_grids[y][x]
    print("Updating inner grid visuals", motion_data)

    current_inner_grid = [[inTile((j * inner_cell_size) + 300, (i * inner_cell_size) + 200, inner_cell_size,
                                  inner_cell_size, motion_tile_colors[motion_data[i][j][0]],
                                  generate_label(motion_data, i, j, False), bug_sprites[motion_data[i][j][3]],
                                  friendly_sprites[motion_data[i][j][2]]) for j in range(len(motion_data[0]))] for i in
                          range(len(motion_data))]
    current_thermal_grid = [[inTile((j * inner_cell_size) + 300, (i * inner_cell_size) + 200, inner_cell_size,
                                    inner_cell_size, thermal_tile_colors[thermal_data[i][j][0]],
                                    generate_label(thermal_data, i, j, False), bug_sprites[motion_data[i][j][3]],
                                    friendly_sprites[motion_data[i][j][2]]) for j in range(len(motion_data[0]))] for i
                            in range(len(motion_data))]
    current_topo_grid = [[inTile((j * inner_cell_size) + 300, (i * inner_cell_size) + 200, inner_cell_size,
                                 inner_cell_size, topo_tile_colors[topo_data[i][j][0]],
                                 generate_label(topo_data, i, j, True), bug_sprites[motion_data[i][j][3]],
                                 friendly_sprites[motion_data[i][j][2]]) for j in range(len(motion_data[0]))] for i in
                         range(len(motion_data))]


# Game loop
while game_running:
    time_delta = clock.tick(60) / 1000.0  # Time in seconds since last frame
    mouse_x, mouse_y = pygame.mouse.get_pos()

    hover_text = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if not displaying_inner_grid:
                # Check for outer grid cell clicks
                for i in range(len(outer_tile_grid)):
                    for j in range(len(outer_tile_grid[i])):
                        tile = outer_tile_grid[i][j]
                        if tile.x <= mouse_x <= tile.x + tile.width and tile.y <= mouse_y <= tile.y + tile.height:
                            selected_tile_y, selected_tile_x = i, j
                            displaying_inner_grid = True
                            update_inner_grid(selected_tile_y, selected_tile_x)
                            break
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Handle clicks within the inner grid
                    for i in range(len(current_inner_grid)):
                        for j in range(len(current_inner_grid[i])):
                            tile = current_inner_grid[i][j]
                            if tile.x <= event.pos[0] <= tile.x + tile.width and tile.y <= event.pos[
                                1] <= tile.y + tile.height:
                                print(f"Clicked inner cell at ({i}, {j})")
                                current_slot = -1
                                for h in range(len(selected_troops)):
                                    if selected_troops[h]:
                                        current_slot = h
                                    if current_slot != -1 and active_units[current_slot][1] > 0:
                                        drop_troop(current_slot, selected_tile_y, selected_tile_x, i, j)
                                        update_inner_grid(selected_tile_y, selected_tile_x)
                                break
        inner_ui_manager.process_events(event)
        main_ui_manager.process_events(event)

    # Clear screen
    screen.fill(background_color)

    # Draw UI elements
    pygame.draw.rect(screen, black, (290, 190, 420, 420))
    pygame.draw.rect(screen, red, (180, 190, 110, 420))

    # Draw key
    current_label = default_font.render(hover_text, True, white)
    Key(screen, scanner_label, dropped_unit_label, belief_position_label, current_label)

    if not displaying_inner_grid:
        # Highlight cell under mouse
        for outer_row_index in range(len(outer_tile_grid)):
            for outer_col_index in range(len(outer_tile_grid[outer_row_index])):
                outer_tile = outer_tile_grid[outer_row_index][outer_col_index]
                if outer_tile.x <= mouse_x <= outer_tile.x + outer_tile.width and outer_tile.y <= mouse_y <= outer_tile.y + outer_tile.height:
                    hover_text = f"({outer_col_index}, {abs(outer_row_index - 3)})"
                    outer_tile.color = active_tile_colors[outer_map[outer_row_index][outer_col_index][0]]
                    outer_tile.highlight(screen)
                else:
                    outer_tile.color = inactive_tile_colors[outer_map[outer_row_index][outer_col_index][0]]
        current_selection = ""

    else:
        inner_ui_manager.update(time_delta)
        inner_ui_manager.draw(screen)

        if view_states[0]:
            # Display motion grid
            pygame.draw.rect(screen, black, (180, 495, 110, 30))
            for motion_row in current_inner_grid:
                for motion_tile in motion_row:
                    motion_tile.show(screen)
            # Highlight cell under mouse
            for inner_row_index in range(len(current_inner_grid)):
                for inner_col_index in range(len(current_inner_grid[inner_row_index])):
                    motion_tile = current_inner_grid[inner_row_index][inner_col_index]
                    if motion_tile.x <= mouse_x <= motion_tile.x + motion_tile.width and motion_tile.y <= mouse_y <= motion_tile.y + motion_tile.height:
                        hover_text = f"IN ({selected_tile_x},{abs(selected_tile_y - 3)}),({inner_col_index}, {abs(inner_row_index - 2)})"
                        current_selection = str(
                            possibleread(selected_tile_y, selected_tile_x, inner_row_index, inner_col_index))
                        motion_tile.highlight(screen)
        elif view_states[2]:
            # Display thermal grid
            pygame.draw.rect(screen, black, (180, 495, 110, 30))
            for thermal_row in current_thermal_grid:
                for thermal_tile in thermal_row:
                    thermal_tile.show(screen)
            # Highlight cell under mouse
            for inner_row_index in range(len(current_thermal_grid)):
                for inner_col_index in range(len(current_thermal_grid[inner_row_index])):
                    thermal_tile = current_thermal_grid[inner_row_index][inner_col_index]
                    if thermal_tile.x <= mouse_x <= thermal_tile.x + thermal_tile.width and thermal_tile.y <= mouse_y <= thermal_tile.y + thermal_tile.height:
                        hover_text = f"IN ({selected_tile_x},{abs(selected_tile_y - 3)}),({inner_col_index}, {abs(inner_row_index - 1)})"
                        current_selection = str(
                            possibleread(selected_tile_y, selected_tile_x, inner_row_index, inner_col_index))
                        thermal_tile.highlight(screen)
        elif view_states[1]:
            # Display topographical grid
            pygame.draw.rect(screen, black, (180, 495, 110, 30))
            for topo_row in current_topo_grid:
                for topo_tile in topo_row:
                    topo_tile.show(screen)
            # Highlight cell under mouse
            for inner_row_index in range(len(current_topo_grid)):
                for inner_col_index in range(len(current_topo_grid[inner_row_index])):
                    topo_tile = current_topo_grid[inner_row_index][inner_col_index]
                    if topo_tile.x <= mouse_x <= topo_tile.x + topo_tile.width and topo_tile.y <= mouse_y <= topo_tile.y + topo_tile.height:
                        hover_text = f"IN ({selected_tile_x},{abs(selected_tile_y - 3)}),({inner_col_index}, {abs(inner_row_index - 2)})"
                        current_selection = str(
                            possibleread(selected_tile_y, selected_tile_x, inner_row_index, inner_col_index))
                        topo_tile.highlight(screen)

    # Display hover text if available
    if hover_text:
        hover_display = default_font.render(hover_text, True, white)
        if not displaying_inner_grid:
            screen.blit(hover_display, (210, 500))
        else:
            screen.blit(hover_display, (185, 500))

    # Render troop slots
    slot1 = medium_font.render((active_units[0][0] + " (" + str(active_units[0][2]) + ")"), True, white)
    slot2 = medium_font.render((active_units[1][0] + " (" + str(active_units[1][2]) + ")"), True, white)
    slot3 = medium_font.render((active_units[2][0] + " (" + str(active_units[2][2]) + ")"), True, white)

    # Display turn information
    turn_types = ["Enemies'", "Friendlies'"]
    turn_label = default_font.render((turn_types[current_faction] + " turn:"), True, white)
    moves_label = default_font.render(("Moves " + str(available_moves)), True, white)

    turnBanner(screen, turn_label, moves_label)
    Carrier(screen, title_label, slot1, slot2, slot3)

    main_ui_manager.update(time_delta)
    main_ui_manager.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

    pygame.quit()

