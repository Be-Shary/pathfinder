import sys, time, pygame
from math import floor

pygame.init()

WIDTH = 640
HEIGHT = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (20, 200, 20)
BLUE = (20, 20, 200)
ORANGE = (200, 100, 20)
RED = (200, 20, 20)
CELL = 20
ROWS = 20
COLS  = 32

maze = []
path = []

start = ()
end = ()
draw_map = False
draw_path = False
set_start = False
set_end = False
set_maze = False
set_restart = True

screen = pygame.display.set_mode((WIDTH,HEIGHT))
font = pygame.font.SysFont(None, 30)


class Node:
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos


def draw_box(x, y, COLOR):
    pygame.draw.rect(screen,COLOR,(x * CELL, y * CELL, CELL-1, CELL-1))


def make_maze(ROWS,COLS):
    for y in range(ROWS):
        empty = []
        for x in range(COLS):
            empty.append(0)
        maze.append(empty)
    return maze



def draw_maze(maze):
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] == 0:
                draw_box(x, y, GREEN)
            elif maze[y][x] == 1:
                draw_box(x, y, RED)


def find_way(maze, start, end):
    global img
    open_list = []
    close_list = []
    startNode = Node(None, start)
    endNode = Node(None, end)
    open_list.append(startNode)
    moves = ((1, 0), (-1, 0), (0, 1), (0, -1))

    while len(open_list) > 0:
        current_index = 0
        current_node = open_list[0]

        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index
        close_list.append(current_node)
        open_list.pop(current_index)

        if current_node == endNode:
            path = []
            while current_node != startNode:
                path.append(current_node.pos)
                current_node = current_node.parent
            return path[::-1]

        childes = []
        for move in moves:
            new_pos = ((move[0] + current_node.pos[0]), (move[1] + current_node.pos[1]))
            if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] > (len(maze[0]) - 1) or new_pos[1] > (len(maze) - 1):
                continue
            if maze[new_pos[1]][new_pos[0]] != 0:
                continue

            new_node = Node(current_node, (new_pos[0], new_pos[1]))

            new_node.g = current_node.g + 1
            new_node.h = (new_node.pos[0] - endNode.pos[0]) ** 2 + (new_node.pos[1] - endNode.pos[1]) ** 2
            new_node.f = new_node.g + new_node.h

            nonode = True
            for node in close_list:
                if node == new_node:
                    nonode = False

            if nonode:
                childes.append(new_node)

        for child in childes:

            for index, node in enumerate(open_list):
                if node == child:
                    if child.g > node.g:
                        break
                    close_list.append(node)
                    open_list.pop(index)

            draw_box(current_node.pos[0], current_node.pos[1], WHITE)

            for node in close_list:
                draw_box(node.pos[0], node.pos[1], GREY)

            node = current_node
            while node != startNode:
                draw_box(node.pos[0], node.pos[1], BLUE)
                node = node.parent

            pygame.display.update()
            time.sleep(0.1)

            open_list.append(child)

    img = font.render("No path to end point!", True, (255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    mouse = pygame.mouse.get_pos()
    mouse_x, mouse_y = (floor(mouse[0]/CELL), floor(mouse[1]/CELL))

    if not set_start and not set_end and not set_maze and set_restart:
        maze = []
        maze = make_maze(ROWS,COLS)
        set_restart = False
        draw_map = False

    if not draw_map:
        map = draw_maze(maze)
        draw_map = True

    if pygame.mouse.get_pressed() == (1 ,0 ,0):
        if not set_start:
            start = (mouse_x, mouse_y)
            set_start = True
            time.sleep(0.2)
        elif not set_end:
            end = (mouse_x, mouse_y)
            set_end = True
            time.sleep(0.2)
        else:
            if start != (mouse_x, mouse_y) != end:
                if not mouse_x < 0 and not mouse_x > len(maze[0]) - 1 and not mouse_y < 0 and not mouse_y > len(maze) - 1:
                    maze[mouse_y][mouse_x] = 1

    if not draw_path:
        screen.fill((0, 0, 0))
        map = draw_maze(maze)

    img = font.render("Chose START point!", True, (255, 255, 255))

    if set_start:
        img = font.render("Chose END point!", True, (255, 255, 255))
        draw_box(start[0], start[1], BLUE)
    if set_end:
        img = font.render("Make a maze. Press Space to start!", True, (255, 255, 255))
        draw_box(end[0], end[1], ORANGE)

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        set_maze = True
        img = font.render("Searching best path!", True, (255, 255, 255))

    if set_start and set_end and set_maze and not set_restart:
        path = find_way(maze, start, end)
        draw_path = True
        set_restart = True

    if draw_path:
        if path != None:
            for step in path:
                draw_box(step[0], step[1], BLUE)

        draw_box(start[0], start[1], BLUE)
        draw_box(end[0], end[1], ORANGE)

    if set_start and set_end and set_maze and set_restart:
        img = font.render("Press R to reset map!", True, (255, 255, 255))
        if pygame.key.get_pressed()[pygame.K_r]:
            set_start = False
            set_end = False
            set_maze = False
            draw_path = False

    screen.blit(img, (10, HEIGHT - 40))
    pygame.display.update()

