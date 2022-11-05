import pygame
import os

WIDTH, HEIGHT = 900, 500
ASSETS_FOLDER_PATH = "Assets"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
FPS = 60

class Display:
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))
        self.game_objects = list()

    def add_object(self, game_obj):
        self.game_objects.append(game_obj)

    def draw(self):
        self.surface.fill(WHITE)
        for game_obj in self.game_objects:
            self.surface.blit(game_obj.image, (game_obj.x, game_obj.y))
        pygame.display.update()


class SpaceObject:
    velocity = 5

    def __init__(self, image, start_x=0, start_y=0):
        self.image = pygame.image.load(os.path.join(ASSETS_FOLDER_PATH, image))
        self.x = start_x
        self.y = start_y

    def transform_image(self, scale):
        self.image = pygame.transform.scale(self.image, scale)

    def rotate_image(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)


def main():
    clock = pygame.time.Clock()
    win = Display(WIDTH, HEIGHT)

    yellow_spaceship = SpaceObject("spaceship_yellow.png", 100, 300)
    yellow_spaceship.transform_image((SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    yellow_spaceship.rotate_image(90)

    red_spaceship = SpaceObject("spaceship_red.png", 700, 300)
    red_spaceship.transform_image((SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    red_spaceship.rotate_image(-90)

    win.add_object(yellow_spaceship)
    win.add_object(red_spaceship)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            keys_pressed = pygame.key.get_pressed()
            win.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
