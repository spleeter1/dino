import pygame
import random

pygame.init()
clock = pygame.time.Clock()

# Tiêu đề và icon
pygame.display.set_caption('Dino game')
icon = pygame.image.load(r'assets\dinosaur.jpg')
pygame.display.set_icon(icon)

# Cửa sổ game
screen = pygame.display.set_mode((600, 300))

# Load hình ảnh
background = pygame.image.load(r'assets\resizedBackground.png')
tree = pygame.image.load(r'assets\fire2.png')
dino = pygame.image.load(r'assets\resizedDP.png')
heart = pygame.image.load(r'assets\heart_resized.png')

# Khởi tạo
score, hscore = 0, 0
background_x, background_y = 0, 0
tree_x, tree_y = 550, 230
dino_x, dino_y = 0, 210
x_def = 5
y_def = 6  # tốc độ rơi của dino
jump = False
jump_count = 0
max_jumps = 2
lives = 3
gameplay = True

# Tạo heart
heart_x, heart_y = None, None
heart_visible = False

def appear_heart():
    global heart_x, heart_y, heart_visible
    if not heart_visible and random.randint(1, 100) == 1:
        heart_x = random.randint(600, 1200)
        heart_y = random.randint(80, 210)
        heart_visible = True

# Hàm kiểm tra va chạm
def checkvc():
    global lives
    if dino_hcn.colliderect(tree_hcn):  # Hàm kiểm tra va chạm
        lives -= 1
        return False
    return True

# Hàm kiểm tra va chạm với heart
def check_heart_collision():
    global lives, heart_x, heart_y, heart_visible
    if heart_visible:
        heart_rect = heart.get_rect(topleft=(heart_x, heart_y))
        if dino_hcn.colliderect(heart_rect):
            lives += 1
            heart_visible = False

# Đưa score vào game
game_font = pygame.font.Font('04B_19.TTF', 20)
def score_view():
    if gameplay:
        score_txt = game_font.render(f'Score: {int(score)}', True, (255, 0, 0))
        screen.blit(score_txt, (250, 50))
        hscore_txt = game_font.render(f'High Score: {int(hscore)}', True, (255, 0, 0))
        screen.blit(hscore_txt, (350, 50))
        lives_txt = game_font.render(f'Lives: {int(lives)}', True, (255, 0, 0))
        screen.blit(lives_txt, (150, 50))
    else:
        score_txt = game_font.render(f'Score: {int(score)}', True, (255, 0, 0))
        screen.blit(score_txt, (250, 50))
        hscore_txt = game_font.render(f'High Score: {int(hscore)}', True, (255, 0, 0))
        screen.blit(hscore_txt, (350, 50))
        over_txt = game_font.render(f'Game Over', True, (255, 0, 0))
        screen.blit(over_txt, (250, 210))
        lives_txt = game_font.render(f'Lives: {int(lives)}', True, (255, 0, 0))
        screen.blit(lives_txt, (150, 50))

def reset_tree():
    global tree_x
    tree_x = 550

def reset_game():
    global background_x, background_y, tree_x, tree_y, dino_x, dino_y, score, lives, gameplay, heart_x, heart_y, heart_visible
    background_x, background_y = 0, 0
    tree_x, tree_y = 550, 230
    dino_x, dino_y = 0, 210
    score = 0
    lives = 3
    heart_x, heart_y = None, None
    heart_visible = False
    gameplay = True

# Vòng lặp xử lý game
running = True
while running:
    # Chỉnh FPS
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameplay:
                if jump_count < max_jumps:
                    jump = True
                    jump_count += 1
            if event.key == pygame.K_SPACE and not gameplay:
                reset_game()

    if gameplay:
        # Background
        background_hcn = screen.blit(background, (background_x, background_y))
        background2_hcn = screen.blit(background, (background_x + 600, background_y))
        background_x -= x_def
        if background_x == -600:
            background_x = 0
        # Tree
        tree_hcn = screen.blit(tree, (tree_x, tree_y))
        tree_x -= x_def
        if tree_x == -20:
            tree_x = 550
        # Dino
        dino_hcn = screen.blit(dino, (dino_x, dino_y))
        if dino_y >= 80 and jump:
            dino_y -= y_def
        else:
            jump = False
        if dino_y < 210 and not jump:
            dino_y += y_def
        if dino_y == 210:
            jump_count = 0  # Reset jump count when dino touches the ground
        # Hearts
        appear_heart()
        check_heart_collision()
        if heart_visible:
            screen.blit(heart, (heart_x, heart_y))
            heart_x -= x_def
            if heart_x < -20:
                heart_visible = False
        score += 0.01
        if hscore < score:
            hscore = score
        if not checkvc():
            reset_tree()
        if lives == 0:
            gameplay = False
        score_view()
    else:
        # Reset game
        background_hcn = screen.blit(background, (background_x, background_y))
        tree_hcn = screen.blit(tree, (tree_x, tree_y))
        dino_hcn = screen.blit(dino, (dino_x, dino_y))
        score_view()
    pygame.display.update()
