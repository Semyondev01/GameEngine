from math import *
import time
import pygame


# default configuration
width = 1200
height = 800
hw = width / 2
h_height = height / 2
block_size = 100
# Ray Casting Settings
FOV = pi / 2
half_FOV = FOV / 2
max_depth = width // block_size
num_rays =  1200
delta_ray = FOV / (num_rays - 1)
dist = num_rays / (2 * tan(half_FOV))
coefficient = dist * block_size * 2
scale = width // num_rays
dpcf = 2

#font
pygame.font.init()
f1 = pygame.font.SysFont('arial', 36)

cur_time = time.time_ns()

def transp_map(map, bs):
    if bs == 0:
        bs = block_size
    block_map = set()
    y_block_pos = 0
    for row in map:
        x_block_pos = 0
        for column in list(row):
            if column == "W":
                block_map.add((x_block_pos, y_block_pos))
            x_block_pos += bs
        y_block_pos += bs
    return block_map
def draw_map(map, bs):
    return transp_map(map, bs)
# map settings
txt_map = ["WWWWWWWWWWWW",
            "W..........W",
            "W..........W",
            "W.......WWWW",
            "W..........W",
            "W..........W",
            "W..........W",
            "WWWWWWWWWWWW",
            ]
# block_map = draw_map(txt_map, 0)


def create_window(width, height):
    return pygame.display.set_mode((width, height))

def quit_checking():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
def draw_floor(display, r,g,b, player):
    pygame.draw.rect(display, (r, g, b), (0, h_height - player.ver_a, width, h_height + player.ver_a))
def draw_sky(display, r,g,b, player):
    pygame.draw.rect(display, (r, g, b), (0, 0, width, h_height - player.ver_a))
def display_map_on_top(display, color, block_map):
    [pygame.draw.rect(display, pygame.Color(color), (x, y, block_size, block_size), 1) for x, y in block_map]
def display_player_spot_on_top(display, color, player):
    pygame.draw.circle(display, pygame.Color(color), (player.x, player.y), 10)
def show_fps(display, showing_method, FPS, clock):
    if showing_method == "corner":
        FPS = f1.render(FPS, False,
                          (0, 180, 0))
        display.blit(FPS, (0,0))
    elif showing_method == "title":
        pygame.display.set_caption("FPS: " + FPS)
    elif showing_method == "mixed":
        pygame.display.set_caption("FPS: " + FPS)
        FPS = f1.render(FPS, False,
                        (0, 180, 0))
        display.blit(FPS, (0, 0))
    else:
        print("Wrong argument in function 'show_fps()'")
        quit()
    clock.tick(0)

def init():
    display = create_window(width, height)
    clock = pygame.time.Clock()
    player = Player()

    cur_time = time.time_ns()
    return display, clock, player
def delta_time():
    global cur_time
    delta = (time.time_ns() - cur_time) / 1000000000
    cur_time = time.time_ns()
    return delta


import pygame.key


class Player:
    def __init__(self):
        self.x = hw
        self.y = h_height
        self.angle = 0
        self.delta = 0
        self.speed = 500
        self.ver_a = 0

    def move(self):
        key = pygame.key.get_pressed()
        cos_a, sin_a = cos(self.angle), sin(self.angle)

        if key[pygame.K_LEFT]:
            self.angle -= 3 * self.delta
        if key[pygame.K_RIGHT]:
            self.angle += 3 * self.delta
        if key[pygame.K_UP]:
            self.ver_a -= 1500 * self.delta
        if key[pygame.K_DOWN]:
            self.ver_a += 1500 * self.delta

        if key[pygame.K_w]:
            self.x += cos_a * self.delta * self.speed
            self.y += sin_a * self.delta * self.speed
        if key[pygame.K_s]:
            self.x -= cos_a * self.delta * self.speed
            self.y -= sin_a * self.delta * self.speed
        if key[pygame.K_a]:
            self.x += sin_a * self.delta * self.speed
            self.y -= cos_a * self.delta * self.speed
        if key[pygame.K_d]:
            self.x -= sin_a * self.delta * self.speed
            self.y += cos_a * self.delta * self.speed
def ray_casting(display, player, block_map):
    in_block_pos = {'left': player.x - player.x // block_size * block_size,
                    'top': player.y - player.y // block_size * block_size,
                    'right': block_size - (player.x - player.x // block_size * block_size),
                    'bottom': block_size - (player.y - player.y // block_size * block_size)}

    for ray in range(num_rays):
        cur_angle = player.angle - half_FOV + delta_ray * ray
        cos_a, sin_a = cos(cur_angle), sin(cur_angle)
        vd, hd = 0, 0
        founded = False


        # Vertical
        for dep in range(max_depth):
            if cos_a > 0:
                vd = in_block_pos['right'] / cos_a + block_size / cos_a * dep + 1
            elif cos_a < 0:
                vd = in_block_pos['left'] / -cos_a + block_size / -cos_a * dep + 1

            x, y = vd * cos_a + player.x, vd * sin_a + player.y
            fixed_x, fixed_y = x // block_size * block_size, y // block_size * block_size
            if (fixed_x, fixed_y) in block_map:
                founded = True
                break

        # Horizontal
        for dep in range(max_depth):
            if sin_a > 0:
                hd = in_block_pos['bottom'] / sin_a + block_size / sin_a * dep + 1
            elif sin_a < 0:
                hd = in_block_pos['top'] / -sin_a + block_size / -sin_a * dep + 1

            x, y = hd * cos_a + player.x, hd * sin_a + player.y
            fixed_x, fixed_y = x // block_size * block_size, y // block_size * block_size
            if (fixed_x, fixed_y) in block_map:
                founded = True
                break


        if founded:
            ray_size = min(vd, hd) * dpcf
            ray_size *= cos(player.angle - cur_angle)
            height_c = coefficient / (ray_size + 0.0001)
            c =  255 / (1 + ray_size**2*0.000001)
            color = (c, c, c)
            pygame.draw.rect(display, color, (ray * scale, (h_height - height_c // 2) - player.ver_a, scale, height_c))

