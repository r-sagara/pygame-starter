import pygame
import os
import operator
from pygame import Rect

WIDTH, HEIGHT = 900, 500
ASSETS_FOLDER_PATH = "Assets"
WHITE = (255, 255, 254)
BLACK = (0, 0, 0)
FPS = 60

BORDER_WIDTH = 10
BORDER_HEIGHT = HEIGHT
BORDER_RECT = Rect(WIDTH//2 - BORDER_WIDTH//2, 0, BORDER_WIDTH, BORDER_HEIGHT)

class Display:
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))
        self.game_objects = list()

    def add_object(self, game_obj):
        self.game_objects.append(game_obj)

    def draw(self):
        self.surface.fill(WHITE)
        pygame.draw.rect(self.surface, BLACK, BORDER_RECT)
        for game_obj in self.game_objects:
            self.surface.blit(game_obj.image, (game_obj.x, game_obj.y))
        pygame.display.update()


class DisplayObject(Rect):
    def __init__(self, init_x=0, init_y=0, width=1, height=1):
        super().__init__(init_x, init_y, width, height)
        self.image = None
        self.angle = 0

    def transform_image(self, scale):
        if self.image:
            self.image = pygame.transform.scale(self.image, scale)

    def rotate_image(self, target_angle):
        if self.image and self.angle != target_angle:
            self.image = pygame.transform.rotate(self.image, target_angle - self.angle)
            self.angle = target_angle


class Spaceship(DisplayObject):
    VELOCITY = 5
    SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

    def __init__(self, image, start_x=0, start_y=0):
        super().__init__(init_x=start_x, init_y=start_y, width=self.SPACESHIP_WIDTH, height=self.SPACESHIP_HEIGHT)
        self.image = pygame.image.load(os.path.join(ASSETS_FOLDER_PATH, image))
        self.transform_image((self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT))

    def move_left(self):
        self.x -= self.VELOCITY
        self.rotate_image(-90)

    def move_right(self):
        self.x += self.VELOCITY
        self.rotate_image(90)

    def move_up(self):
        self.y -= self.VELOCITY
        self.rotate_image(180)

    def move_down(self):
        self.y += self.VELOCITY
        self.rotate_image(0)


class MoveHandler:
    def __init__(self, key_up, key_down, key_left, key_right):
        self.__moves_collection = [
            (key_up, "move_up", "top", operator.gt),
            (key_down, "move_down", "bottom", operator.lt), 
            (key_left, "move_left", "left", operator.gt),
            (key_right, "move_right", "right", operator.lt)
        ]
    
    @property
    def limit_area(self):
        try:
            return self.__limit_area
        except AttributeError:
            return None

    @limit_area.setter
    def limit_area(self, rect: Rect):
        self.__limit_area = rect

    def move(self, spaceship):
        keys_pressed = pygame.key.get_pressed()
        for key, method, side, operator in self.__moves_collection:
            if keys_pressed[key] and operator(getattr(spaceship, side), getattr(self.limit_area, side)):
                getattr(spaceship, method)()


def main():
    clock = pygame.time.Clock()
    win = Display(WIDTH, HEIGHT)

    yellow_spaceship = Spaceship("spaceship_yellow.png", 100, 300)
    yellow_spaceship.rotate_image(90)

    red_spaceship = Spaceship("spaceship_red.png", 700, 300)
    red_spaceship.rotate_image(-90)

    win.add_object(yellow_spaceship)
    win.add_object(red_spaceship)

    controler_1 = MoveHandler(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
    controler_2 = MoveHandler(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
    controler_1.limit_area = Rect(0, 0, BORDER_RECT.left, HEIGHT)
    controler_2.limit_area = Rect(BORDER_RECT.right, 0, BORDER_RECT.left, HEIGHT)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        controler_1.move(yellow_spaceship)
        controler_2.move(red_spaceship)
        
        win.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
