import sys
from Camera import Camera
from Sprite import *


# CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GAME_WIDTH = 8000


# SPRITE CONSTANTS
START_X = 40
START_Y = 400
CHARACTER_WIDTH = 114
CHARACTER_HEIGHT = RECYCLABLE_HEIGHT = NON_RECYCLABLE_HEIGHT = 100
PLAYER_SPEED = 7
RECYCLABLE_WIDTH = 47
NON_RECYCLABLE_WIDTH = 129
BLOCK_DIMENSIONS = 100
SIGN_WIDTH = 300
BACKGROUND_IMAGE = "images/Background.png"
CHARACTER_IMAGE = "sprites/Character.png"
RECYCLABLE_IMAGE = "sprites/Water.png"
NON_RECYCLABLE_IMAGE = "sprites/Food.png"


# MECHANICS
LEVEL = [
    "                                              WWWF        FFF   F       F W F 7  ",
    "  0      4    5         6        F    GGGGGGG    F          W       W     W   7  ",
    "  123             WWWWW                F W DD             W    GGG   W        7  ",
    "                 GGGG W          W GGGGGG  DLGGGGG     WW    GGRDLGG  W       7  ",
    "      GGG      GGRDDD W   FF   GGGGRDDD FWWWWW       GGGG   GRDDDDDLGGGGGGG   7  ",
    "GGGGGGRDLGGGGGGRDDDDDGGGGGGGGGGRDDDDDDLGGGGGGGGGGGGGGRDDLGGGRDDDDDDDDDDDDDLGGGGGG",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
    ]


# GLOBALS
clock = pygame.time.Clock()
background = Sprite(BACKGROUND_IMAGE, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 0)
character = Sprite(CHARACTER_IMAGE, START_X, START_Y, CHARACTER_WIDTH, CHARACTER_HEIGHT, 1)
sprites_list = pygame.sprite.Group()
sprites_list.add(character)


# MAIN METHOD
def main():

    # Local Variables
    camera = Camera(complex_camera, GAME_WIDTH, WINDOW_HEIGHT)
    up = down = False       # Indicates the jumping movement
    left = right = False    # Indicates character direction
    game_is_running = True  # Indicates when program is running
    x = y = 0               # Sprite position variables
    score = 0               # Keeps track of the current score

    # Build the level
    for row in LEVEL:
        for col in row:

            # Barriers
            if col == "G":
                grass = Platform(x, y, "Grass")
                sprites_list.add(grass)
            if col == "D":
                dirt = Platform(x, y, "Dirt")
                sprites_list.add(dirt)
            if col == "L":
                left_edge = Platform(x, y, "Left Edge")
                sprites_list.add(left_edge)
            if col == "R":
                right_edge = Platform(x, y, "Right Edge")
                sprites_list.add(right_edge)
            if col == "T":
                two_edge = Platform(x, y, "Two Edge")
                sprites_list.add(two_edge)

            # Collectibles
            if col == "W":
                water = Sprite(RECYCLABLE_IMAGE, x, y, RECYCLABLE_WIDTH, RECYCLABLE_HEIGHT, 2)
                sprites_list.add(water)
            if col == "F":
                food = Sprite(NON_RECYCLABLE_IMAGE, x, y, NON_RECYCLABLE_WIDTH, NON_RECYCLABLE_HEIGHT, 3)
                sprites_list.add(food)

            # Reminders and Signs
            if col == "0":
                recycle_dash_sign = Sprite("sprites/Recycle Dash Sign.png", x, y, SIGN_WIDTH, BLOCK_DIMENSIONS, 4)
                sprites_list.add(recycle_dash_sign)
            if col == "1":
                left_button = Sprite("sprites/Left Button.png", x, y, BLOCK_DIMENSIONS, BLOCK_DIMENSIONS, 4)
                sprites_list.add(left_button)
            if col == "2":
                up_button = Sprite("sprites/Up Button.png", x, y, BLOCK_DIMENSIONS, BLOCK_DIMENSIONS, 4)
                sprites_list.add(up_button)
            if col == "3":
                right_button = Sprite("sprites/Right Button.png", x, y, BLOCK_DIMENSIONS, BLOCK_DIMENSIONS, 4)
                sprites_list.add(right_button)
            if col == "4":
                fly_indefinitely_sign = Sprite("sprites/Fly Indefinitely Sign.png", x, y, SIGN_WIDTH, BLOCK_DIMENSIONS, 4)
                sprites_list.add(fly_indefinitely_sign)
            if col == "5":
                collect_sign = Sprite("sprites/Collect Sign.png", x, y, SIGN_WIDTH, BLOCK_DIMENSIONS, 4)
                sprites_list.add(collect_sign)
            if col == "6":
                avoid_sign = Sprite("sprites/Avoid Sign.png", x, y, SIGN_WIDTH, BLOCK_DIMENSIONS, 4)
                sprites_list.add(avoid_sign)
            if col == "7":
                finish_sign = Sprite("sprites/Finish Sign.png", x, y, BLOCK_DIMENSIONS, BLOCK_DIMENSIONS, 4)
                sprites_list.add(finish_sign)
            x += BLOCK_DIMENSIONS
        y += BLOCK_DIMENSIONS
        x = 0

    # Game execution
    while True:

        # Read input
        for event in pygame.event.get():

            # If the game is closed, turn off the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()

            # If a button is pressed...
            if event.type == pygame.KEYDOWN:
                # If A is pressed, set character direction left
                if event.key == pygame.K_a:
                    left = True
                # If D is pressed, set character direction right
                if event.key == pygame.K_d:
                    right = True
                # If W is pressed, jump
                if event.key == pygame.K_w:
                    up = True
                    down = False

            # Once the user lets go of the key, set character direction to nothing
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = False
                if event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_w:
                    up = False
                down = True

        # Runs the actual game
        if game_is_running:

            # Determines if game is over
            if GAME_WIDTH - 200 < character.rect.centerx < GAME_WIDTH:
                game_is_running = False

            # Acquires the list of sprites
            sprites_to_modify = sprites_list.sprites()
            for sprite in sprites_to_modify:
                # Player manipulations
                if sprite.identity == 1:
                    # Get the list of objects colliding with the current sprite
                    hit_list = pygame.sprite.spritecollide(sprite, sprites_list, False)
                    # Update positions (using pixel-perfect movement)
                    if sprite.rect.bottom <= WINDOW_HEIGHT and sprite.rect.top >= 0 and sprite.rect.right <= GAME_WIDTH and\
                            sprite.rect.left >= 0:
                        # Movement
                        if sprite.identity == 1:
                            x_speed = 0
                            y_speed = 0
                            if left and not down:
                                x_speed += -PLAYER_SPEED
                            if right and not down:
                                x_speed += PLAYER_SPEED
                            if up:
                                y_speed -= PLAYER_SPEED
                            if down:
                                y_speed += PLAYER_SPEED

                            character.rect.centerx += x_speed
                            character.rect.centery += y_speed

                            # Collision handling for player
                            for hit in hit_list:
                                # If a barrier has been hit...
                                if hit.identity == 0:
                                    if down and not pygame.sprite.collide_rect(hit, character):
                                        y_speed += 5
                                        character.rect.centery += y_speed
                                    # If the player was moving right, move the player back
                                    if x_speed > 0:
                                        while pygame.sprite.collide_rect(character, hit):
                                            character.rect.centerx -= 1
                                    # If the player was moving left, move the player back
                                    if x_speed < 0:
                                        while pygame.sprite.collide_rect(character, hit):
                                            character.rect.centerx += 1
                                    # If the player was moving up, move the player down
                                    if y_speed < 0:
                                        while pygame.sprite.collide_rect(character, hit):
                                            character.rect.centery += 1
                                    # If the player was moving down, move the player up
                                    if y_speed > 0:
                                        while pygame.sprite.collide_rect(character, hit):
                                            character.rect.centery -= 1
                                            down = False
                                # If a collectible has been hit
                                if hit.identity == 2 or hit.identity == 3:
                                    hit.image = pygame.image.load("sprites/Blank.png")
                                    if hit.identity == 2:
                                        hit.identity = 4
                                        score += 1
                                    if hit.identity == 3:
                                        hit.identity = 4
                                        score -= 1

                    # Position adjustments
                    # If an object is destructible and it hits a wall, get rid of it
                    while sprite.rect.bottom > WINDOW_HEIGHT:
                        sprite.rect.y -= 1
                    while sprite.rect.top < 0:
                        sprite.rect.y += 1
                        down = False
                    while sprite.rect.right > GAME_WIDTH:
                        sprite.rect.x -= 1
                    while sprite.rect.left < 0:
                        sprite.rect.x += 1

            # Updates screen for every passing frame
            display_score(score)
            screen.fill((0, 0, 0))
            screen.blit(background.image, background.rect)
            camera.update(character)  # Allows camera to follow the player

            # Draw everything over the .draw() function (more control with camera)
            for sprite in sprites_list:
                screen.blit(sprite.image, camera.apply(sprite))
            screen.blit(character.image, camera.apply(character))
            pygame.display.flip()
            clock.tick(240)

        # Displays the Game Over screen
        else:
            game_over(score)


# DISPLAYS THE SCORE
def display_score(count):
    font = pygame.font.SysFont(None, 45)
    text = font.render("Score: " + str(count), True, (0, 0, 255))
    screen.blit(text, (WINDOW_WIDTH - 150, 20))
    pygame.display.update()


# GAME OVER SCREEN
def game_over(count):
    screen.fill((0, 0, 0))
    myfont1 = pygame.font.SysFont(None, 32)
    text1 = myfont1.render("Congratulations! Your final score is " + str(count) + "!", True, (255, 255, 255))
    text2 = myfont1.render("Press ESC to exit", True, (255, 255, 255))
    screen.blit(text1, (100, (WINDOW_HEIGHT / 2) - 20))
    screen.blit(text2, (100, (WINDOW_HEIGHT / 2) + 20))
    pygame.display.flip()


# Creates complex camera which will auto-fit to the boundaries of the screen
def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + (WINDOW_WIDTH/2), -t + (WINDOW_HEIGHT/2), w, h  # center player

    l = min(0, l)                                 # Stop scrolling at the left edge
    l = max(-(camera.width - WINDOW_WIDTH), l)    # Stop scrolling at the right edge
    t = max(-(camera.height - WINDOW_HEIGHT), t)  # Stop scrolling at the bottom
    t = min(0, t)                                 # Stop scrolling at the top

    return pygame.Rect(l, t, w, h)


# Creates barriers in the level
class Platform(Sprite):
    def __init__(self, x, y, element_type):
        if element_type == "Grass":
            element_image = "sprites/Grass Block.png"
        if element_type == "Dirt":
            element_image = "sprites/Dirt Block.png"
        if element_type == "Left Edge":
            element_image = "sprites/Left Edge.png"
        if element_type == "Right Edge":
            element_image = "sprites/Right Edge.png"
        if element_type == "Two Edge":
            element_image = "sprites/Two Edge.png"
        Sprite.__init__(self, element_image, x, y, BLOCK_DIMENSIONS, BLOCK_DIMENSIONS)

    def update(self):
        pass


# ACTION
# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Recycle Dash!")

# Run game
main()
