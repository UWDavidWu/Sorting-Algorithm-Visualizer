
import pygame
import random
import math
pygame.init()

class setting:
    BLACK = 0,0,0
    WHITE = 255,255,255
    RED = 255,0,0
    GREEN = 0,255,0
    BLUE = 0,0,255
    GREY = 128,128,128
    BACKGROUND_COLOR = WHITE
    FONT = pygame.font.SysFont("comicsans", 30)
    LARGE_FONT = pygame.font.SysFont("comicsans", 60)
    SIDE_PAD = 100
    TOP_PAD = 150

    GRADIENTS =[GREEN
                ,BLUE
                ,RED]

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithms Visualizer")
        self.set_lst(lst)

    
    def set_lst(self, lst):
        self.lst = lst
        self.max_value = max(self.lst)
        self.min_value = min(self.lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(self.lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_value - self.min_value))

        self.start_x = self.SIDE_PAD //2

def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    controls = draw_info.FONT.render("Press R to generate new list", True, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width // 2 - controls.get_width() // 2, 5))
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i,val in enumerate(draw_info.lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_value) * draw_info.block_height
        color = draw_info.GRADIENTS[i % len(draw_info.GRADIENTS)]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()

def generate_starting_list(n ,min_value, max_value):
    lst = []
    for _ in range(n):
        lst.append(random.randint(min_value, max_value))
    return lst

def bubble_sort(draw_info):
    lst = draw_info.lst
    for i in range(len(lst) -1):
        for j in range(len(lst) - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j:draw_info.WHITE, j + 1:draw_info.BLACK},True)
                yield True
                

def main():
    run = True
    
    clock = pygame.time.Clock()
    sorting = False
    sorting_algo = bubble_sort
    sorting_algo_generator = None

    draw_info = setting(800, 600, generate_starting_list(50, 0, 100))

    while run:
        clock.tick(60)
        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(50, 0, 100)
                draw_info.set_lst(lst)
                sorting == False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algo(draw_info)

    pygame.quit()


if __name__ == "__main__":
    main()