import pygame
import os
import operator
from pygame import Rect

WIDTH, HEIGHT = 900, 500
ASSETS_FOLDER_PATH = "Assets"
MAX_BULLETS = 3
BULLET_VELOCITY = 7

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

BORDER_WIDTH = 10
BORDER_HEIGHT = HEIGHT

YELLOW_FIRE = pygame.USEREVENT + 1
RED_FIRE = pygame.USEREVENT + 2

YELLOW_HIT = pygame.USEREVENT + 3
RED_HIT = pygame.USEREVENT + 4


class Display:
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))
        self.game_objects = list()

    def add_object(self, game_obj):
        self.game_objects.append(game_obj)

    def remove_object(self, game_obj):
        if game_obj in self.game_objects:
            self.game_objects.remove(game_obj)

    def draw(self):
        for game_obj in self.game_objects:
            if hasattr(game_obj, "image"):
                #pygame.draw.rect(self.surface, BLACK, game_obj)
                self.surface.blit(game_obj.image, (game_obj.x, game_obj.y))             
            elif isinstance(game_obj, Rect):
                pygame.draw.rect(self.surface, game_obj.color, game_obj)      
        pygame.display.update()


class DisplayObject(Rect):
    def __init__(self, init_x=0, init_y=0, width=1, height=1, image_path=None, color=None):
        super().__init__(init_x, init_y, width, height)
        if image_path:
            self.image = pygame.image.load(os.path.join(ASSETS_FOLDER_PATH, image_path))
            self.transform_image((width, height))
        if color:
            self.color = color
        self.angle = 0

    def transform_image(self, scale):
        if self.image:
            self.image = pygame.transform.scale(self.image, scale)

    def rotate_image(self, target_angle):
        if self.image and self.angle != target_angle:
            rotated_image = pygame.transform.rotate(self.image, target_angle - self.angle)
            rotated_image_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=self.topleft).center)
            self.image = rotated_image
            self.topleft = rotated_image_rect.topleft
            self.width, self.height = rotated_image_rect.width, rotated_image_rect.height
            self.angle = target_angle


class Health(DisplayObject):
    WIDTH, HEIGHT = 100, 5

    def __init__(self, start_x, start_y, color):
        super().__init__(init_x=start_x, init_y=start_y, width=self.BULLET_WIDTH, height=self.BULLET_HEIGHT, color=color)


class Bullet(DisplayObject):
    WIDTH, HEIGHT = 20, 6

    def __init__(self, start_x, start_y, color):
        super().__init__(width=self.WIDTH, height=self.HEIGHT, color=color)
        self.center = start_x, start_y

    def move(self, direction):
        self.x += direction


class Spaceship(DisplayObject):
    VELOCITY = 5
    WIDTH, HEIGHT = 55, 40

    def __init__(self, start_x=0, start_y=0, image=None):
        super().__init__(init_x=start_x, init_y=start_y, width=self.WIDTH, height=self.HEIGHT, image_path=image)
        self.health = 10

    def move_left(self):
        self.x -= self.VELOCITY 
        #self.rotate_image(-90)

    def move_right(self):
        self.x += self.VELOCITY
        #self.rotate_image(90)

    def move_up(self):
        self.y -= self.VELOCITY
        #self.rotate_image(180)

    def move_down(self):
        self.y += self.VELOCITY
        #self.rotate_image(0)


class ControlHandler:
    def __init__(self, key_up, key_down, key_left, key_right, move_limit_area, key_shot, player, spaceship, window):
        self.__moves_collection = [
            (key_up, "move_up", "top", operator.gt),
            (key_down, "move_down", "bottom", operator.lt), 
            (key_left, "move_left", "left", operator.gt),
            (key_right, "move_right", "right", operator.lt)
        ]
        self.__key_shot = key_shot
        self.__spaceship = spaceship
        self.move_limit_area = move_limit_area
        self.player = player
        self.bullets_to_move = []
        self.window = window
        if self.player == "yellow":
            self.direction = BULLET_VELOCITY
            self.event_fire = YELLOW_FIRE
            self.event_hit_enemy = RED_HIT
        elif self.player == "red":
            self.direction = -BULLET_VELOCITY
            self.event_fire = RED_FIRE
            self.event_hit_enemy = YELLOW_HIT
        else:
            raise AttributeError(f"Wrong player is set: {self.player}, expected players: yellow, red")

    def handle_move(self, keys_pressed):
        for key, method, side, operator in self.__moves_collection:
            if keys_pressed[key] and operator(getattr(self.__spaceship, side), getattr(self.move_limit_area, side)):
                getattr(self.__spaceship, method)()

    def handle_shot(self, event_key):
        if event_key == self.__key_shot and len(self.bullets_to_move) < MAX_BULLETS:
            bullet = Bullet(*self.__spaceship.image.get_rect(topleft=self.__spaceship.topleft).center, color=RED)
            self.bullets_to_move.append(bullet)
            self.window.add_object(bullet)

    def handle_bullets(self, vs):      
        for bullet in self.bullets_to_move:
            bullet.move(self.direction)
            if bullet.colliderect(vs) or not self.window.surface.get_rect().contains(bullet):
                if vs.colliderect(bullet):
                    vs.health -= 1
                    if vs.health == 0:
                        winner_text = f"{self.player.upper()} WIN"
                self.bullets_to_move.remove(bullet)
                self.window.remove_object(bullet)


def main():
    clock = pygame.time.Clock()
    win = Display(WIDTH, HEIGHT)

    yellow_spaceship = Spaceship(100, 300, image="spaceship_yellow.png")
    yellow_spaceship.rotate_image(90)

    red_spaceship = Spaceship(700, 300, image="spaceship_red.png")
    red_spaceship.rotate_image(-90)

    space = DisplayObject(width=WIDTH, height=HEIGHT, image_path="space.png")
    border = DisplayObject(WIDTH//2 - BORDER_WIDTH//2, 0, BORDER_WIDTH, BORDER_HEIGHT, color=BLACK)

    win.add_object(space)
    win.add_object(border)
    win.add_object(yellow_spaceship)
    win.add_object(red_spaceship)
    win.add_object(yellow_spaceship.health)
    win.add_object(red_spaceship.health)
    # TODO try to draw rectangles instead fonts

    controller_1 = ControlHandler(
        pygame.K_w, 
        pygame.K_s, 
        pygame.K_a, 
        pygame.K_d,
        Rect(0, 0, border.left, HEIGHT),
        pygame.K_LCTRL,
        player="yellow",
        spaceship=yellow_spaceship,
        window=win)

    controller_2 = ControlHandler(
        pygame.K_UP, 
        pygame.K_DOWN, 
        pygame.K_LEFT, 
        pygame.K_RIGHT,
        Rect(border.right, 0, border.left, HEIGHT),
        pygame.K_RCTRL,
        player="red",
        spaceship=red_spaceship,
        window=win)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                controller_1.handle_shot(event.key)
                controller_2.handle_shot(event.key)

        keys_pressed = pygame.key.get_pressed()
        controller_1.handle_move(keys_pressed)
        controller_2.handle_move(keys_pressed)

        controller_1.handle_bullets(vs=red_spaceship)
        controller_2.handle_bullets(vs=yellow_spaceship)
        win.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
