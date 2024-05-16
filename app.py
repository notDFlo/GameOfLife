import pygame
import numpy as np

# This is a simple, self-directed implementation of the Game of Life
# by John Conway. This is in no way a complete implementation, but 
# rather a simple demonstration of the game.
# I've added a feature to allo the player to spawn a random cell 
# on the grid *** note! this spawns a cell, not a clump of cells ***
#   - this is useful for manipulating clumps or ridding the grid of 
#     unwanted or infinitely-repeating clumps of cells (see TODO)

# Summary
# this is a self-contained, single file pygame application meant to 
# demonstrate the "Game of Life" by John Conway. 
# Its initial design was intended to be a "No-Player" type of game.
# However, this implementation does allow you to manipulate clumps
#   by clicking on the grid. Doing so will spawn a cell at the 
#   location of the click. This is useful for breaking up clumps,
#   and also merging clumps together, causing a cascading randomness
#   that can be interesting to watch.

#  Code/Game Notes:
# - This code simulates a grid of cells that are either alive or dead
# - each tick determines how the cells will change over time
# - the rules are simple:
#   - if a cell has 2 or 3 neighbors, it stays alive
#   - if a cell has less than 2 or more than 3 neighbors, it dies
#   - if a dead cell has exactly 3 neighbors, it becomes alive
# - the game is over when all cells are dead or in a state of recursive

# TODO
# 1. add logic to manage space between "blobs" of alive cells
# 2. eliminate the randomness which causes circular shapes

# Static/Global Variables
SCREEN_SIZE = WIDTH, HEIGHT = 1200, 500

# set alive cell properties
CELL_SIZE = 5
OUTLINE_COLOR = (25, 255, 64) # Green
ALIVE_COLOR = (128, 255, 64)  # Dark purple
DEAD_COLOR = (0, 0, 0) # Black

# GRID_COLOR = (25, 25, 25, 255) # White
GRID_COLOR = (0, 0, 0, 255) # Black
INITIAL_ALIVE_CELLS = 15

# Initialize pygame and the screen
pygame.init()
# set font and timer settings
FONT = pygame.font.Font(None, 36)
TEXT_COLOR = (255, 255, 255)  # White
start_ticks = pygame.time.get_ticks()
clock = pygame.time.Clock()

#set screen settings
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Game of Life")  # Set the window title
zeroed_x = WIDTH//CELL_SIZE
zeroed_y = HEIGHT//CELL_SIZE

# Define the grid
grid = np.zeros((zeroed_y, zeroed_x))

def initialize_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            cell = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (255, 0, 255), cell, 1)

# spawn live cells
def spawn_alive_blocks(min_size_of_clumps = 3, max_size_of_clumps = 8, number_of_clumps = 20):
    global grid
    for _ in range(number_of_clumps):
        x, y = np.random.randint(0, grid.shape[0]-max_size_of_clumps), np.random.randint(0, grid.shape[1]-max_size_of_clumps)
        shape_x, shape_y = np.random.randint(min_size_of_clumps, max_size_of_clumps+1), np.random.randint(min_size_of_clumps, max_size_of_clumps+1) # Randomize the shape
        grid[y:y+shape_y, x:x+shape_x] = 1

def update_grid():
  for x in range(0, WIDTH, CELL_SIZE):
    for y in range(0, HEIGHT, CELL_SIZE):
      cell = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
      cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE
      if grid[cell_y, cell_x] == 1:
        pygame.draw.rect(screen, OUTLINE_COLOR, cell, 1)  # Draw the outline
        # pygame.draw.rect(screen, ALIVE_COLOR, cell.inflate(-1, -1))  # Draw the inner cell
      else:
        pygame.draw.rect(screen, GRID_COLOR, cell, 1)

def update_game_state():
    global grid
    new_grid = grid.copy()
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            # Count the number of neighboring cells
            n_neigh = grid[(y-1)%grid.shape[0]:((y+2)%grid.shape[0]), (x-1)%grid.shape[1]:((x+2)%grid.shape[1])].sum() - grid[y, x]
            # Apply the rules of the game
            if grid[y, x] and not 2 <= n_neigh <= 3:
                new_grid[y, x] = 0
            elif n_neigh == 3:
                new_grid[y, x] = 1
    grid = new_grid

def handle_mouse_click(event):
   # Get the cell coordinates of the click
    cell_x, cell_y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
    # Toggle the cell state
    grid[cell_y, cell_x] = 1 if grid[cell_y, cell_x] == 0 else 0

def display_game_time():
    # Calculate the elapsed time
    elapsed_ticks = pygame.time.get_ticks() - start_ticks
    elapsed_seconds = elapsed_ticks // 1000
    elapsed_minutes = elapsed_seconds // 60
    elapsed_seconds %= 60

    # Create the text surface
    text = FONT.render(f"Time: {elapsed_minutes}:{elapsed_seconds:02}", True, TEXT_COLOR)

    # Draw the text on the screen
    screen.blit(text, (WIDTH - text.get_width(), 0))

def handle_mouse_input():
    # Get the cell coordinates of the click
    cell_x, cell_y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
    # Toggle the cell state
    grid[cell_y, cell_x] = 1 if grid[cell_y, cell_x] == 0 else 0

# # # # # # # # # # #
# initialize game
# Generate the initial state
spawn_alive_blocks()
# # # # # # # # # # #

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_input()
            
    screen.fill((0, 0, 0))
    initialize_grid()
    update_grid()
    update_game_state()
    display_game_time()
    pygame.display.flip()

    # time.sleep(0.2)
    clock.tick(200) # 60 fps