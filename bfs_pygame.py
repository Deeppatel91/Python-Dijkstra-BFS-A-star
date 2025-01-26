import pygame as pg
from random import random
from collections import deque

# Constants
COLS, ROWS = 25, 15
TILE = 60
SCREEN_WIDTH, SCREEN_HEIGHT = COLS * TILE, ROWS * TILE

# Colors
COLORS = {
    'background': (0, 0, 0),
    'wall': (139, 69, 19),  # Brown
    'visited': (34, 139, 34),  # Forest Green
    'queue': (47, 79, 79),  # Dark Slate Gray
    'path': (255, 255, 255),  # White
    'start': (0, 0, 255),  # Blue
    'end': (255, 0, 255),  # Magenta
    'grid_line': (50, 50, 50)  # Dark Gray
}

def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < COLS and 0 <= y < ROWS and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

# Initialize Pygame
pg.init()
sc = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption("BFS Pathfinding")
clock = pg.time.Clock()

# Grid initialization
grid = [[1 if random() < 0.2 else 0 for col in range(COLS)] for row in range(ROWS)]

# Graph initialization
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# BFS settings
start = (0, 0)
queue = deque([start])
visited = {start: None}
cur_node = start

# Main loop
while True:
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    # Fill screen with background color
    sc.fill(COLORS['background'])

    # Draw grid lines
    for x in range(COLS):
        for y in range(ROWS):
            pg.draw.rect(sc, COLORS['grid_line'], (x * TILE, y * TILE, TILE, TILE), 1)

    # Draw walls
    [[pg.draw.rect(sc, COLORS['wall'], get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]

    # Draw visited nodes
    [pg.draw.rect(sc, COLORS['visited'], get_rect(x, y)) for x, y in visited]

    # Draw queue nodes
    [pg.draw.rect(sc, COLORS['queue'], get_rect(x, y)) for x, y in queue]

    # BFS logic
    if queue:
        cur_node = queue.popleft()
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node

    # Draw path
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.rect(sc, COLORS['path'], get_rect(*path_segment), TILE, border_radius=TILE // 3)
        path_segment = visited[path_segment]

    # Draw start and end points
    pg.draw.rect(sc, COLORS['start'], get_rect(*start), border_radius=TILE // 3)
    pg.draw.rect(sc, COLORS['end'], get_rect(*path_head), border_radius=TILE // 3)

    # Update display
    pg.display.flip()
    clock.tick(7)