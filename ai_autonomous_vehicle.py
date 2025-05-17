import pygame
import heapq
import sys
import csv

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
WHITE, BLACK, GREY, GREEN, RED, BLUE = (255,255,255), (0,0,0), (160,160,160), (0,255,0), (255,0,0), (0,0,255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Autonomous Vehicle & Robotics Simulation")
clock = pygame.time.Clock()

# Global variables
grid = []
start = goal = None
ROWS = COLS = 0

# Load map from CSV
def load_map_csv(filename):
    global grid, start, goal, ROWS, COLS
    grid = []
    start = goal = None
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for y, row in enumerate(reader):
            grid_row = []
            for x, val in enumerate(row):
                if val == '1':
                    grid_row.append(1)
                else:
                    grid_row.append(0)
                if val == 'S':
                    start = (x, y)
                elif val == 'G':
                    goal = (x, y)
            grid.append(grid_row)
    ROWS = len(grid)
    COLS = len(grid[0])

# Heuristic for A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* pathfinding
def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        neighbors = [(0,1),(1,0),(-1,0),(0,-1)]
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < COLS and 0 <= neighbor[1] < ROWS:
                if grid[neighbor[1]][neighbor[0]] == 1:
                    continue
                temp_g = g_score[current] + 1
                if neighbor not in g_score or temp_g < g_score[neighbor]:
                    g_score[neighbor] = temp_g
                    f = temp_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))
                    came_from[neighbor] = current
    return []

# Main loop
def main():
    load_map_csv("map.csv")
    path = a_star(start, goal)
    robot_pos = list(start)
    running = True

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw grid
        for y in range(ROWS):
            for x in range(COLS):
                rect = pygame.Rect(x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, GREY, rect, 1)
                if grid[y][x] == 1:
                    pygame.draw.rect(screen, BLACK, rect)

        # Draw path
        for x, y in path:
            pygame.draw.rect(screen, BLUE, (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Move robot along path
        if path:
            target = path.pop(0)
            robot_pos[0], robot_pos[1] = target

        # Draw start, goal, robot
        pygame.draw.rect(screen, GREEN, (start[0]*GRID_SIZE, start[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, RED, (goal[0]*GRID_SIZE, goal[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.circle(screen, BLUE, (robot_pos[0]*GRID_SIZE + GRID_SIZE//2, robot_pos[1]*GRID_SIZE + GRID_SIZE//2), GRID_SIZE//3)

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
