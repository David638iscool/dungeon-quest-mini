import pygame
import sys
import random

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 600, 400
TILE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Quest - Mini Crawler")

clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 64)
font_small = pygame.font.SysFont(None, 32)

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (50, 150, 255)
WALL_COLOR = (0, 0, 0)
GOAL_COLOR = (255, 0, 0)
COIN_COLOR = (255, 215, 0)
ENEMY_COLOR = (255, 50, 50)
SCORE_COLOR = (0, 255, 0)  # Green score color

# --- Maze setup ---
ROWS = 11  # must be odd
COLS = 15  # must be odd
player_start = (1, 1)
move_speed = 5

# --- Maze generation ---
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    def carve(x, y):
        maze[y][x] = 0
        dirs = [(2,0),(-2,0),(0,2),(0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 1 <= nx < cols-1 and 1 <= ny < rows-1 and maze[ny][nx] == 1:
                maze[y+dy//2][x+dx//2] = 0
                carve(nx, ny)
    carve(1, 1)
    maze[rows-2][cols-2] = 'G'  # Mark the goal
    return maze

# --- Place collectibles ---
def place_coins(maze, count=5):
    coins = []
    while len(coins) < count:
        x = random.randint(1, COLS-2)
        y = random.randint(1, ROWS-2)
        if maze[y][x] == 0 and (x, y) != player_start and (x, y) != (COLS-2, ROWS-2):
            coins.append((x, y))
    return coins

# --- Enemy setup ---
class Enemy:
    def __init__(self, maze):
        while True:
            x = random.randint(1, COLS-2)
            y = random.randint(1, ROWS-2)
            if maze[y][x] == 0 and (x, y) != player_start:
                self.x, self.y = x, y
                self.px, self.py = x * TILE, y * TILE
                self.target = (x, y)
                self.dx, self.dy = 0, 0
                break
    def move(self, maze):
        if self.px == self.target[0] * TILE and self.py == self.target[1] * TILE:
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0:
                    self.target = (nx, ny)
                    self.dx = (nx - self.x) * 2
                    self.dy = (ny - self.y) * 2
                    self.x, self.y = nx, ny
                    break
        self.px += self.dx
        self.py += self.dy

# --- Game state ---
level_counter = 1
score = 0

def reset_level(is_goal_reached=False):
    global score  # Access the global score variable
    global player_x, player_y, player_px, player_py, target_tile, moving, maze, coins, enemies, level_counter
    player_x, player_y = player_start
    player_px = player_x * TILE
    player_py = player_y * TILE
    target_tile = (player_x, player_y)
    moving = False
    maze[:] = generate_maze(ROWS, COLS)
    coins[:] = place_coins(maze, count=7)
    enemies[:] = [Enemy(maze) for _ in range(3)]
    level_counter += 1  # Increment level
    if is_goal_reached:
        score += 10  # Increase score only when reaching the goal

# --- Intro screen ---
def show_intro():
    intro = True
    while intro:
        screen.fill(WHITE)
        title = font_large.render("Dungeon Quest", True, BLACK)
        start = font_small.render("Press ENTER to Start", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//3)))
        screen.blit(start, start.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                intro = False

# --- Movement check ---
def can_move(nx, ny):
    return 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] != 1

# --- Initialize level ---
maze = generate_maze(ROWS, COLS)
player_x, player_y = player_start
player_px, player_py = player_x * TILE, player_y * TILE
target_tile = (player_x, player_y)
moving = False
coins = place_coins(maze, 7)
enemies = [Enemy(maze) for _ in range(3)]

# --- Start intro ---
show_intro()

# --- Main loop ---
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Player input ---
    keys = pygame.key.get_pressed()
    if not moving:
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and can_move(player_x - 1, player_y):
            target_tile = (player_x - 1, player_y)
            move_dx, move_dy = -move_speed, 0
            moving = True
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and can_move(player_x + 1, player_y):
            target_tile = (player_x + 1, player_y)
            move_dx, move_dy = move_speed, 0
            moving = True
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and can_move(player_x, player_y - 1):
            target_tile = (player_x, player_y - 1)
            move_dx, move_dy = 0, -move_speed
            moving = True
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and can_move(player_x, player_y + 1):
            target_tile = (player_x, player_y + 1)
            move_dx, move_dy = 0, move_speed
            moving = True

    # --- Smooth movement ---
    if moving:
        player_px += move_dx
        player_py += move_dy
        tx, ty = target_tile[0] * TILE, target_tile[1] * TILE
        if ((move_dx > 0 and player_px >= tx) or (move_dx < 0 and player_px <= tx)):
            player_px = tx
        if ((move_dy > 0 and player_py >= ty) or (move_dy < 0 and player_py <= ty)):
            player_py = ty
        if player_px == tx and player_py == ty:
            player_x, player_y = target_tile
            moving = False
            # Check if the player reached the goal
            if maze[player_y][player_x] == 'G':
                reset_level(is_goal_reached=True)

    # --- Move enemies ---
    for e in enemies:
        e.move(maze)
        # Collision with player
        if abs(player_px - e.px) < TILE // 2 and abs(player_py - e.py) < TILE // 2:
            reset_level(is_goal_reached=False)  # Don't increase score if hit by enemy

    # --- Draw maze ---
    for r in range(ROWS):
        for c in range(COLS):
            cell = maze[r][c]
            rect = pygame.Rect(c * TILE, r * TILE, TILE, TILE)
            if cell == 1:
                pygame.draw.rect(screen, WALL_COLOR, rect)
            elif cell == 'G':
                pygame.draw.rect(screen, GOAL_COLOR, rect)

    # --- Draw coins ---
    for coin in coins:
        rect = pygame.Rect(coin[0] * TILE + TILE // 4, coin[1] * TILE + TILE // 4, TILE // 2, TILE // 2)
        pygame.draw.rect(screen, COIN_COLOR, rect)

    # --- Draw enemies ---
    for e in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, pygame.Rect(e.px, e.py, TILE, TILE))

    # --- Draw player ---
    pygame.draw.rect(screen, PLAYER_COLOR, pygame.Rect(player_px, player_py, TILE, TILE))

    # --- Display score ---
    score_text = font_small.render(f"Score: {score}", True, SCORE_COLOR)
    screen.blit(score_text, (10, 10))

    # --- Display level ---
    level_text = font_small.render(f"Level {level_counter}", True, BLACK)
    screen.blit(level_text, (WIDTH - 100, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()