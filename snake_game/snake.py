# Snake.py
# Simple snake game using pygame library in python
# By hutton edney and AI help

from pygame_library import *
import pygame, random, os
pygame.init()
pygame.mixer.init()
MUSIC = ["sakpase.mp3", "relentless.mp3", "at_the_party.mp3", "hooligan.mp3"]
EAT_SOUND = pygame.mixer.Sound("eat.mp3")
WIDTH, HEIGHT = 800, 600
FONT = pygame.font.SysFont("Arial", 48)
SMALL_FONT = pygame.font.SysFont("Arial", 28)
GREEN, BLACK, WHITE, RED = (0,255,0), (0,0,0), (255, 255, 255), (255, 0, 0)
CELL_SIZE = 20
SNAKE_DIR = os.path.expanduser("~/Desktop/snake_game/snake_body")
win = make_win(WIDTH, HEIGHT, "Snake")
fruits = ["big_grape.png", "banana.png", "tomato.png", "raspberry.png"]
MAX_SNAKE_LEN = (WIDTH//CELL_SIZE) * (HEIGHT //CELL_SIZE)
ICON_SIZE = 50
completed_levels = set()

def load_snake_sprite(name):
    path = os.path.join(SNAKE_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
def load_sprite(name):

    return pygame.image.load(name).convert_alpha()
fruit_sprites = {name: load_sprite(name) for name in fruits}
snake_head_up = load_snake_sprite("head_up.png")
snake_head_down = load_snake_sprite("head_down.png")
snake_head_right = load_snake_sprite("head_right.png")
snake_head_left = load_snake_sprite("head_left.png")
snake_body = load_snake_sprite("body_horizontal.png")
snake_tail_up = load_snake_sprite("tail_up.png")
snake_tail_down = load_snake_sprite("tail_down.png")
snake_tail_right = load_snake_sprite("tail_right.png")
snake_tail_left = load_snake_sprite("tail_left.png")
lock_icon = pygame.transform.scale(pygame.image.load("lock.png").convert_alpha(), (ICON_SIZE, ICON_SIZE))
check_icon = pygame.transform.scale(pygame.image.load("check.png").convert_alpha(), (ICON_SIZE, ICON_SIZE))
def level_select():
    levels = []
    button_size = 80
    padding = 20

    # Calculate width of the 5x2 grid
    total_w = 5 * button_size + 4 * padding
    start_x = (WIDTH - total_w) // 2
    start_y = HEIGHT // 3

    # Generate level button rectangles
    for i in range(10):
        row = i // 5
        col = i % 5
        x = start_x + col * (button_size + padding)
        y = start_y + row * (button_size + padding)
        rect = pygame.Rect(x, y, button_size, button_size)
        levels.append(rect)

    CHECK_PAD = 8  # how far the checkmark is from edge

    while True:
        win.fill((25, 25, 25))
        draw_txt(win, "SELECT LEVEL", FONT, GREEN, WIDTH // 2, HEIGHT // 5)

        for i, rect in enumerate(levels):
            lvl = i + 1

            # Draw the button box
            pygame.draw.rect(win, WHITE, rect, border_radius=10)

            # Draw the level number
            draw_txt(win, str(lvl), SMALL_FONT, BLACK, rect.centerx, rect.centery)

            # -------------------------
            #   ICON PLACEMENT FIXED
            # -------------------------

            # ✔ Completed level → checkmark in top-right
            if lvl in completed_levels:
                check_x = rect.right - ICON_SIZE - CHECK_PAD
                check_y = rect.top + CHECK_PAD
                win.blit(check_icon, (check_x, check_y))

            # 🔒 Locked level → centered lock icon
            elif lvl > 1 and (lvl - 1) not in completed_levels:
                lock_x = rect.centerx - ICON_SIZE // 2
                lock_y = rect.centery - ICON_SIZE // 2
                win.blit(lock_icon, (lock_x, lock_y))

        # Back button
        back_rect = draw_txt(win, "BACK", SMALL_FONT, WHITE, WIDTH // 2, HEIGHT - 80)

        pygame.display.update()

        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # BACK
                if back_rect.collidepoint(event.pos):
                    return None

                # LEVEL BUTTONS
                for i, rect in enumerate(levels):
                    if rect.collidepoint(event.pos):
                        lvl = i + 1

                        # Block locked levels
                        if lvl > 1 and (lvl - 1) not in completed_levels:
                            continue

                        # Configure gameplay:
                        speed = 8 + lvl
                        target_score = 5 + lvl * 5

                        return {
                            "level": lvl,
                            "speed": speed,
                            "target_score": target_score
                        }

def shuffle():
    return random.choice(MUSIC)
def play_music(file, volume=0.5, loop=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loop)
def stop_music():
    pygame.mixer.music.stop()
def transition(new_file, fade=500, volume=0.5, loop=-1):
    pygame.mixer.music.fadeout(fade)
    pygame.time.delay(fade)
    pygame.mixer.music.load(new_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loop, fade_ms=fade)
def draw_txt(surface, text, font, color, x, y):
    draw = font.render(text, True, color)
    rect = draw.get_rect(center=(x,y))
    surface.blit(draw, rect)
    return rect
def pause():
    paused = True
    while paused:
        win.fill((0,0,0))
        draw_txt(win, "PAUSED", FONT, (0, 255, 0), WIDTH//2, HEIGHT//3)
        res_rec = draw_txt(win, "RESUME", SMALL_FONT, (200, 200, 200), WIDTH//2, HEIGHT//2)
        quit_rec = draw_txt(win, "QUIT", SMALL_FONT, (200,200,200), WIDTH//2, HEIGHT//1.75)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if res_rec.collidepoint(event.pos):
                    return "resume"
                if quit_rec.collidepoint(event.pos):
                    return "quit"
def fruit():
    fx = random.randrange(0, WIDTH, CELL_SIZE)
    fy = random.randrange(0, HEIGHT, CELL_SIZE)
    return fx, fy
def grow(fruit_x, fruit_y):
    # add one green rect to the spot that the fruit was eaten
    snake_body = pygame.draw.rect(win, GREEN, (fruit_x, fruit_y, CELL_SIZE, CELL_SIZE))
def gamelines():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(win, (40,40,40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(win, (40,40,40), (0,y), (WIDTH, y))
def fail_screen(text):
    lines = text.split("\n")
    while True:
        win.fill((30,30,30))
        y = HEIGHT // 3
        for line in lines:
            draw_txt(win, line, SMALL_FONT if line != "GAME OVER" else FONT, RED if "GAME OVER" in line else WHITE, WIDTH//2, y)
            y += 50
        menu_rect = draw_txt(win, "BACK TO MENU", SMALL_FONT, (200,200,200), WIDTH//2, HEIGHT//2)
        pygame.display.update()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_rect.collidepoint(event.pos):
                        menu_song = shuffle()
                        transition(menu_song)
                        return "menu"                     
def win_screen(level):
    completed_levels.add(level)
    while True:
        win.fill((20, 50, 20))
        draw_txt(win, "YOU WIN!", FONT, GREEN, WIDTH//2, HEIGHT//3)
        menu_rect = draw_txt(win, "BACK TO MENU", SMALL_FONT, WHITE, WIDTH//2, HEIGHT//2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    menu_song = shuffle()
                    transition(menu_song)
                    return "menu"
def show_menu():
    menu_song = shuffle()
    play_music(menu_song)
    running = True
    while running:
        win.fill((30,30,30))
        draw_txt(win, "SNAKE", FONT, (0,255,0), WIDTH//2, HEIGHT//3)
        start_rect = draw_txt(win, "START", SMALL_FONT, (200,200,200), WIDTH//2, HEIGHT//2)
        quit_rect = draw_txt(win, "QUIT", SMALL_FONT, (200,200,200), WIDTH//2, HEIGHT//1.75)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    level_data = level_select()
                    if level_data is None:
                        continue
                    game_song = shuffle()
                    transition(game_song)
                    return level_data
                if quit_rect.collidepoint(event.pos):
                    running = False
                    return False
    return False
def keybinds(dx, dy, event):
    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_w, pygame.K_UP):
            dx, dy, = 0, -20
        elif event.key in (pygame.K_a, pygame.K_LEFT):
            dx, dy, = -20, 0
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            dx, dy, = 0, 20
        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            dx, dy, = 20, 0
        elif event.key == pygame.K_p:
            pygame.mixer.music.set_volume(0.2)
            result = pause()
            pygame.mixer.music.set_volume(0.5)
            if result == "quit":
                return "menu", dx, dy
    return None, dx, dy
def tail_sprite(snake):
    if len(snake) < 2:
        return snake_tail_down
    (x1,y1) = snake[-2]
    (x2,y2) = snake[-1]
    dx = x2 - x1
    dy = y2 - y1
    if dx > 0:
        return snake_tail_right
    elif dx < 0:
        return snake_tail_left
    elif dy > 0:
        return snake_tail_down
    elif dy < 0:
        return snake_tail_up
    return snake_tail_down
def play_game(level_data):
    running = True
    clock = pygame.time.Clock()
    snake = [(WIDTH//2, HEIGHT//2)]
    dx, dy = CELL_SIZE, 0
    fruit_x, fruit_y = fruit()
    fruit_sprite = random.choice(list(fruit_sprites.values()))
    score = 0
    level = level_data["level"]
    speed = level_data["speed"]
    target_score = level_data["target_score"]
    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            result, dx, dy = keybinds(dx, dy, event)
            if result == "menu":
                return "menu"
        hx, hy = snake[0]
        new_head = (hx + dx, hy + dy)
        snake.insert(0, new_head)
        if new_head == (fruit_x, fruit_y):
                    EAT_SOUND.play()
                    score += 1
                    if score >= target_score:
                        pygame.mixer.music.set_volume(0.3)
                        return win_screen(level)
                    fruit_x, fruit_y = fruit()
                    fruit_sprite = random.choice(list(fruit_sprites.values()))
        else:
            snake.pop()
        if len(snake) >= MAX_SNAKE_LEN:
            pygame.mixer.music.set_volume(0.3)
            return win_screen(level)
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            pygame.mixer.music.set_volume(0.2)
            return fail_screen("GAME OVER\nYou ran into the wall!")
        if new_head in snake[1:]:
            pygame.mixer.music.set_volume(0.2)
            return fail_screen("GAME OVER\nYou ran into yourself!")
        win.fill(BLACK)
        gamelines()
        scaled_fruit = pygame.transform.scale(fruit_sprite, (CELL_SIZE, CELL_SIZE))
        win.blit(scaled_fruit, (fruit_x, fruit_y))
        for i, (sx, sy) in enumerate(snake):
            if i == 0:
                if dx > 0:
                    head_img = snake_head_right
                elif dx < 0:
                    head_img = snake_head_left
                elif dy < 0:
                    head_img = snake_head_up
                elif dy > 0:
                    head_img = snake_head_down

                win.blit(head_img, (sx, sy))
            elif i == len(snake) - 1:
                tail_img = tail_sprite(snake)
                win.blit(tail_img, (sx, sy))
            else:
                win.blit(snake_body, (sx, sy))
        draw_txt(win, f"Score: {score}/{target_score}", SMALL_FONT, WHITE, 80, 20)
        draw_txt(win, f"Level: {level}", SMALL_FONT, WHITE, 70, 50)
        pygame.display.update()
    return False
def main():
    while True:
        play = show_menu()
        if not play:
            break
        result = play_game(play)
        if result == "menu":
            continue
    pygame.quit()
main()

