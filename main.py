import pygame
from random import randint

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
font = pygame.font.Font("font/Pixeltype.ttf", 50)

running = True
is_playing = False
score = 0
last_spawn_time = 0
spawn_interval = 1500  

GROUND_Y = 300
JUMP_GRAVITY_START_SPEED = -20
PLAYER_HEIGHT = 150

def display_score():
    current_time = pygame.time.get_ticks() // 1000
    score_surf = font.render(f"Score: {score}", False, "Black")
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

sky_surf = pygame.image.load("graphics/level/sky.png").convert()
ground_surf = pygame.image.load("graphics/level/ground.png").convert()

def scale_image(image, height):
    aspect_ratio = image.get_width() / image.get_height()
    new_width = int(height * aspect_ratio)
    return pygame.transform.scale(image, (new_width, height))

player_walk_1 = scale_image(pygame.image.load("graphics/player/player_walk_1.png").convert_alpha(), PLAYER_HEIGHT)
player_walk_2 = scale_image(pygame.image.load("graphics/player/player_walk_2.png").convert_alpha(), PLAYER_HEIGHT)
player_walk_3 = scale_image(pygame.image.load("graphics/player/player_walk_3.png").convert_alpha(), PLAYER_HEIGHT)
player_walk_4 = scale_image(pygame.image.load("graphics/player/player_walk_4.png").convert_alpha(), PLAYER_HEIGHT)
player_walk_5 = scale_image(pygame.image.load("graphics/player/player_walk_5.png").convert_alpha(), PLAYER_HEIGHT)
player_jump = scale_image(pygame.image.load("graphics/player/player_jump.png").convert_alpha(), PLAYER_HEIGHT)

player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5]
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(50, GROUND_Y))
player_gravity_speed = 0

enemy_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
enemy_list = []

def spawn_enemy():
    enemy_rect = enemy_surf.get_rect(bottomleft=(randint(900, 1100), GROUND_Y))
    enemy_list.append(enemy_rect)

def display_start_screen():
    title_surf = font.render("Dino Game", False, "Black")
    title_rect = title_surf.get_rect(center=(400, 150))
    instruction_surf = font.render("Press SPACE to Start", False, "Black")
    instruction_rect = instruction_surf.get_rect(center=(400, 250))
    screen.blit(title_surf, title_rect)
    screen.blit(instruction_surf, instruction_rect)

while running:
    screen.fill((94, 129, 162))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if is_playing:
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                and player_rect.bottom >= GROUND_Y
            ):
                player_gravity_speed = JUMP_GRAVITY_START_SPEED
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                score = 0
                enemy_list.clear()

    if is_playing:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND_Y))

        score = display_score()

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_interval:
            spawn_enemy()
            last_spawn_time = current_time

        for enemy_rect in enemy_list:
            enemy_rect.x -= 5
            screen.blit(enemy_surf, enemy_rect)

        enemy_list = [enemy for enemy in enemy_list if enemy.right > 0]

        if player_rect.bottom < GROUND_Y:
            player_surf = player_jump
        else:
            player_index += 0.1
            if player_index >= len(player_walk):
                player_index = 0
            player_surf = player_walk[int(player_index)]

        player_gravity_speed += 1
        player_rect.y += player_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        if any(player_rect.colliderect(enemy) for enemy in enemy_list):
            is_playing = False

    else:
        display_start_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
