import pygame
import os

WIDTH, HEIGHT = 900, 500
ASSETS_FOLDER_PATH = "Assets"
WHITE = (255, 255, 255)
SPACESHIP_SIZE = (55, 40)
FPS = 60

class Display:
    def __init__(self, width, height):
        self.window = pygame.display.set_mode((width, height))
        self.objects = dict()

    def add_object(self, obj, init_position):
        self.objects[obj] = init_position

    def draw(self):
        self.window.fill(WHITE)
        for obj, position in self.objects.items():
            self.window.blit(obj.image, position)
        pygame.display.update()


class SpaceObject:
    def __init__(self, image):
        self.image = pygame.image.load(os.path.join(ASSETS_FOLDER_PATH, image))

    def transform_image(self, scale):
        self.image = pygame.transform.scale(self.image, scale)

    def rotate_image(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)


def main():
    clock = pygame.time.Clock()
    win = Display(WIDTH, HEIGHT)

    yellow_spaceship = SpaceObject("spaceship_yellow.png")
    yellow_spaceship.transform_image(SPACESHIP_SIZE)
    yellow_spaceship.rotate_image(90)

    red_spaceship = SpaceObject("spaceship_red.png")
    red_spaceship.transform_image(SPACESHIP_SIZE)
    red_spaceship.rotate_image(-90)

    yellow = pygame.Rect(100, 300, *SPACESHIP_SIZE)
    red = pygame.Rect(700, 300, *SPACESHIP_SIZE)

    win.add_object(yellow_spaceship, (yellow.x, yellow.y))
    win.add_object(red_spaceship, (red.x, red.y))

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            win.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
