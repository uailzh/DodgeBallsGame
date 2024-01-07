import pygame
import time
import random
import sys


def initialize_pygame():
    pygame.init()
    pygame.font.init()


initialize_pygame()

WIDTH, HEIGHT = 1000, 800

# Load the "You Lost" message background
lost_background = pygame.transform.scale(pygame.image.load("lost.png"), (WIDTH, HEIGHT))

BG = pygame.transform.scale(pygame.image.load("back_game.png"), (WIDTH, HEIGHT))

# Load the player image with transparency
player_image = pygame.image.load("messi4.png")
player_image = pygame.transform.scale(player_image, (80, 120))  # Double the size
player_image.set_colorkey((255, 255, 255))  # Set white as the transparent color

# Load the star image with transparency
star_image = pygame.image.load("ball.png")
star_image = pygame.transform.scale(star_image, (40, 60))
star_image.set_colorkey((255, 255, 255))  # Set white as the transparent color

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60  # Adjust the player rectangle size

PLAYER_VEL = 5
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)


def draw_background(win):
    win.blit(BG, (0, 0))


def draw_start_screen(win):
    draw_background(win)

    start_caption = FONT.render("Let's play a game, dodge the balls!", 1, "white")
    start_button = pygame.Rect(WIDTH / 4, HEIGHT / 2, WIDTH / 2, HEIGHT / 4)

    pygame.draw.rect(win, (0, 128, 255), start_button)
    win.blit(start_caption, (WIDTH / 2 - start_caption.get_width() / 2, HEIGHT / 3))

    # Add text to the button
    start_button_text = FONT.render("START!", 1, "white")
    win.blit(start_button_text, (start_button.x + start_button.width / 2 - start_button_text.get_width() / 2,
                                 start_button.y + start_button.height / 2 - start_button_text.get_height() / 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return


def draw_player(win, player, elapsed_time):
    win.blit(player_image, (player.x, player.y, PLAYER_WIDTH, PLAYER_HEIGHT))


def draw_star(win, star):
    win.blit(star_image, (star.x, star.y))


def draw(win, player, elapsed_time, stars):
    draw_background(win)

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    win.blit(time_text, (10, 10))

    draw_player(win, player, elapsed_time)

    for star in stars:
        draw_star(win, star)

    pygame.display.update()


def show_loss_screen(win):
    win.blit(lost_background, (0, 0))
    lost_text = FONT.render("Poor Ronaldo... He is crying in his car", 1, "gold")
    lost_text_rect = lost_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    win.blit(lost_text, lost_text_rect)

    # Add "START AGAIN" button (twice smaller)
    start_again_button = pygame.Rect(WIDTH / 4, HEIGHT / 4 + HEIGHT / 10, WIDTH / 2, HEIGHT / 16)
    pygame.draw.rect(win, (0, 128, 255), start_again_button)
    start_again_text = FONT.render("START AGAIN", 1, "white")
    win.blit(start_again_text, (start_again_button.x + start_again_button.width / 2 - start_again_text.get_width() / 2,
                                start_again_button.y + start_again_button.height / 2 - start_again_text.get_height() / 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_again_button.collidepoint(event.pos):
                    return True  # Start the game again


def main():
    while True:
        win = pygame.display.set_mode((WIDTH, HEIGHT))  # Create a new display surface
        draw_start_screen(win)

        run = True

        player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - 50, PLAYER_WIDTH,
                             PLAYER_HEIGHT)  # Adjusted starting y-coordinate
        clock = pygame.time.Clock()
        start_time = time.time()
        elapsed_time = 0

        star_add_increment = 2000
        star_count = 0

        stars = []
        hit = False

        while run:
            star_count += clock.tick(60)
            elapsed_time = time.time() - start_time

            if star_count > star_add_increment:
                for _ in range(3):
                    star_x = random.randint(0, WIDTH - PLAYER_WIDTH)
                    star = pygame.Rect(star_x, -PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
                    stars.append(star)

                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
                player.x += PLAYER_VEL

            for star in stars[:]:
                star.y += STAR_VEL
                if star.y > HEIGHT:
                    stars.remove(star)
                elif star.colliderect(player):
                    stars.remove(star)
                    hit = True
                    break

            if hit:
                if show_loss_screen(win):
                    break  # Start the game again

            draw(win, player, elapsed_time, stars)


if __name__ == "__main__":
    main()
