import pygame
import sys
import random

# Function to create a new enemy
def create_enemy():
    size = 10
    x = random.randint(0, screen_width - size)
    y = 0
    return [x, y]

# Function to create a green mushroom
def create_mushroom():
    size = 10
    x = random.randint(0, screen_width - size)
    y = 0
    return [x, y]

# Function to display text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple 2D Game")

# Load images for player, enemy, and green mushroom and adjust their sizes
player_img = pygame.image.load('mario.png')
player_img = pygame.transform.scale(player_img, (50, 50))  # Adjust the size here
enemy_img = pygame.image.load('much.png')
enemy_img = pygame.transform.scale(enemy_img, (30, 30))  # Adjust the size here
mushroom_img = pygame.image.load('up.png')
mushroom_img = pygame.transform.scale(mushroom_img, (30, 30))  # Adjust the size here

# Load background image
background_img = pygame.image.load('back.jpg')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Load ground image
ground_img = pygame.image.load('ground.jpg')
ground_img = pygame.transform.scale(ground_img, (screen_width, 50))  # Adjust the size here

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the player
player_size = 10
player_img = pygame.transform.scale(player_img, (50, 50))  # Adjust the size here
player_width, player_height = player_img.get_rect().size
player_pos = [(screen_width - player_width) / 2, screen_height - 50 - player_height]  # Adjusted position
player_speed = 5
player_jump = False
jump_count = 10
player_lives = 3  # Mario's initial lives

# Initial enemy count and time interval for increasing enemies
initial_enemy_count = 5
enemy_increase_interval = 20000  # 20 seconds

# Initial green mushroom count and time interval for increasing mushrooms
initial_mushroom_count = 1
mushroom_increase_interval = 60000  # 60 seconds

# Green mushroom drop rate
initial_mushroom_drop_rate = 10  # Initial drop rate
max_mushroom_drop_rate = 10  # Maximum drop rate
mushroom_drop_rate_interval = 5000  # Increase drop rate every 5 seconds

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Timer variables
start_time = pygame.time.get_ticks()  # Get the initial time
enemy_speed = 5  # Initial speed
mushroom_speed = 2  # Mushroom speed
speed_increase_interval = 30000  # 30 seconds

# Timer variables for increasing enemies and mushrooms
enemy_increase_timer = pygame.time.get_ticks()
mushroom_increase_timer = pygame.time.get_ticks()
mushroom_drop_rate_timer = pygame.time.get_ticks()
current_enemy_count = initial_enemy_count
current_mushroom_count = initial_mushroom_count

# Score
mushroom_score = 0
score_font = pygame.font.SysFont(None, 30)

# Main game loop
while True:
    player_alive = True
    enemies = []  # Empty list of enemies at the start
    mushrooms = []  # Empty list of mushrooms at the start
    
    while player_alive:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player_jump:
                    player_jump = True

        # Move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_width:
            player_pos[0] += player_speed

        # Jump mechanic
        if player_jump:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_pos[1] -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                player_jump = False
                jump_count = 10

        # Apply gravity to bring Mario back down
        if not player_jump:
            if player_pos[1] < screen_height - 50 - player_height:
                player_pos[1] += 10

        # Move the enemies
        if pygame.time.get_ticks() - enemy_increase_timer >= enemy_increase_interval:
            current_enemy_count += 5  # Increase enemy count by 5 every 20 seconds
            enemy_increase_timer = pygame.time.get_ticks()

        if len(enemies) < current_enemy_count:  # Spawn enemies up to the current count
            enemies.append(create_enemy())

        for enemy in enemies:
            enemy[1] += enemy_speed  # Adjust enemy speed here
            if enemy[1] > screen_height:
                enemies.remove(enemy)
                # fruit_score += 1

            # Check collision with player
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_width, player_height)
            enemy_rect = pygame.Rect(enemy[0], enemy[1], 30, 30)  # Use fixed size for enemy
            if player_rect.colliderect(enemy_rect):
                player_lives -= 1  # Deduct one life if collision occurs
                if player_lives == 0:  # Game over if lives are exhausted
                    player_alive = False
                    # Reset player position
                    player_pos = [(screen_width - player_width) / 2, screen_height - 50 - player_height]
                else:
                    # Move player to a suitable position
                    player_pos[1] = min(player_pos[1] - 50, screen_height - 50 - player_height)  # Ensure player doesn't go below ground

                enemies.remove(enemy)  # Remove enemy after collision

        # Move the mushrooms
        if pygame.time.get_ticks() - mushroom_increase_timer >= mushroom_increase_interval:
            current_mushroom_count += 1  # Increase mushroom count by 1 every 60 seconds
            mushroom_increase_timer = pygame.time.get_ticks()

        if len(mushrooms) < current_mushroom_count:  # Spawn mushrooms up to the current count
            mushrooms.append(create_mushroom())

        for mushroom in mushrooms:
            mushroom[1] += mushroom_speed  # Adjust mushroom speed here
            if mushroom[1] > screen_height:
                mushrooms.remove(mushroom)

            # Check collision with player
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_width, player_height)
            mushroom_rect = pygame.Rect(mushroom[0], mushroom[1], 30, 30)  # Use fixed size for mushroom
            if player_rect.colliderect(mushroom_rect):
                # player_lives += 1  # Add one life if collision occurs
                # if player_lives > 3:  # Limit lives to 3
                #     player_lives = 3
                mushrooms.remove(mushroom)
                mushroom_score += 1  # Increase mushroom score when collected

        # Check if it's time to increase enemy speed
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time >= speed_increase_interval:
            enemy_speed += 1  # Increase enemy speed
            start_time = pygame.time.get_ticks()  # Reset the timer

        # Increase mushroom drop rate every 5 seconds up to a maximum of 10
        if pygame.time.get_ticks() - mushroom_drop_rate_timer >= mushroom_drop_rate_interval:
            if initial_mushroom_drop_rate < max_mushroom_drop_rate:
                initial_mushroom_drop_rate += 1
            mushroom_drop_rate_timer = pygame.time.get_ticks()

        # Clear the screen
        screen.blit(background_img, (0, 0))

        # Draw the ground
        screen.blit(ground_img, (0, screen_height - 50))

        # Draw the player
        screen.blit(player_img, player_pos)

        # Draw the green mushroom
        if random.randint(1, 100) <= initial_mushroom_drop_rate:
            mushroom_rect = mushroom_img.get_rect(topleft=(random.randint(0, screen_width - mushroom_img.get_width()), random.randint(0, screen_height - mushroom_img.get_height())))
            screen.blit(mushroom_img, mushroom_rect)

        # Draw the enemies
        for enemy in enemies:
            screen.blit(enemy_img, enemy)

        # Draw the mushrooms
        for mushroom in mushrooms:
            screen.blit(mushroom_img, mushroom)

        # Draw the score
        score_text = score_font.render("Mushroom Score: " + str(mushroom_score), True, BLACK)
        screen.blit(score_text, [10, 10])

        # Draw player's lives
        lives_text = score_font.render("Lives: " + str(player_lives), True, BLACK)
        screen.blit(lives_text, [screen_width - 100, 10])

        # Update the display
        pygame.display.update()

        # Cap the frame rate
        clock.tick(30)

    # Game over state
    while not player_alive:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if the mouse click is within the bounds of the buttons
                if play_again_rect.collidepoint(mouse_pos):
                    player_alive = True
                    # Reset scores and player state
                    mushroom_score = 0
                    player_lives = 3
                    enemy_speed = 5
                    start_time = pygame.time.get_ticks()
                    player_pos = [(screen_width - player_width) / 2, screen_height - 50 - player_height]
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Clear the screen
        screen.blit(background_img, (0, 0))

        # Draw the score
        score_text = score_font.render("Mushroom Score: " + str(mushroom_score), True, BLACK)
        screen.blit(score_text, [10, 10])

        # Draw player's lives
        lives_text = score_font.render("Lives: " + str(player_lives), True, BLACK)
        screen.blit(lives_text, [screen_width - 100, 10])

        # Draw buttons for Play Again and Quit
        play_again_text = "Play Again"
        play_again_font = pygame.font.SysFont(None, 30)
        play_again_rect = pygame.Rect(screen_width // 4, screen_height // 2 - 30, 200, 50)
        pygame.draw.rect(screen, GREEN, play_again_rect)
        draw_text(play_again_text, play_again_font, BLACK, screen, play_again_rect.centerx, play_again_rect.centery)

        quit_text = "Quit"
        quit_font = pygame.font.SysFont(None, 30)
        quit_rect = pygame.Rect(3 * screen_width // 4, screen_height // 2 - 30, 100, 50)
        pygame.draw.rect(screen, RED, quit_rect)
        draw_text(quit_text, quit_font, BLACK, screen, quit_rect.centerx, quit_rect.centery)

        # Update the display
        pygame.display.update()

        # Cap the frame rate
        clock.tick(30)
