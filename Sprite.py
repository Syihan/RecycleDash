import pygame


class Sprite(pygame.sprite.Sprite):
    destructible = False  # destructibility
    identity = 0          # type (0 = barrier, 1 = player, 2 = recyclable collectible, 3 = non-recyclable collectible, 4 = collected)

    def __init__(self, image, xpos, ypos, width, height, identity=0):
        super().__init__()

        # identity of the element
        self.identity = identity

        # set the width and height
        self.width = width
        self.height = height

        # set the image
        self.image = pygame.image.load(image)

        # fetch rectangle object that has dimensions of the image
        self.rect = self.image.get_rect()

        # set the starting location
        self.rect.topleft = [xpos, ypos]

        # scale image down to manageable size
        self.image = pygame.transform.smoothscale(self.image, (width, height))

        # scale hitbox to new size
        self.rect = self.rect.clip(pygame.Rect(xpos, ypos, width, height))
