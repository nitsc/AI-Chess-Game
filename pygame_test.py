import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Chessboard")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 定义棋盘大小
BOARD_SIZE = 10
CELL_SIZE = 60

# 定义棋子
chessboard = {
    (0, 0): (True, "car"), (0, 1): (True, "horse"), (0, 2): (True, "elephant"),
    (0, 3): (True, "officer"), (0, 4): (True, "captain"), (0, 5): (True, "officer"),
    (0, 6): (True, "elephant"), (0, 7): (True, "horse"), (0, 8): (True, "car"),
    (1, 0): "none", (1, 1): "none", (1, 2): "none", (1, 3): "none", (1, 4): "none",
    (1, 5): "none", (1, 6): "none", (1, 7): "none", (1, 8): "none",
    (2, 0): "none", (2, 1): (True, "cannon"), (2, 2): "none", (2, 3): "none",
    (2, 4): "none", (2, 5): "none", (2, 6): "none", (2, 7): (True, "cannon"), (2, 8): "none",
    (3, 0): (True, "soldier"), (3, 1): "none", (3, 2): (True, "soldier"), (3, 3): "none",
    (3, 4): (True, "soldier"), (3, 5): "none", (3, 6): (True, "soldier"), (3, 7): "none", (3, 8): (True, "soldier"),
    (4, 0): "none", (4, 1): "none", (4, 2): "none", (4, 3): "none", (4, 4): "none", (4, 5): "none", (4, 6): "none", (4, 7): "none", (4, 8): "none",
    (5, 0): "none", (5, 1): "none", (5, 2): "none", (5, 3): "none", (5, 4): "none", (5, 5): "none", (5, 6): "none", (5, 7): "none", (5, 8): "none",
    (6, 0): (False, "soldier"), (6, 1): "none", (6, 2): (False, "soldier"), (6, 3): "none",
    (6, 4): (False, "soldier"), (6, 5): "none", (6, 6): (False, "soldier"), (6, 7): "none", (6, 8): (False, "soldier"),
    (7, 0): "none", (7, 1): (False, "cannon"), (7, 2): "none", (7, 3): "none",
    (7, 4): "none", (7, 5): "none", (7, 6): "none", (7, 7): (False, "cannon"), (7, 8): "none",
    (8, 0): "none", (8, 1): "none", (8, 2): "none", (8, 3): "none", (8, 4): "none", (8, 5): "none", (8, 6): "none", (8, 7): "none", (8, 8): "none",
    (9, 0): (False, "car"), (9, 1): (False, "horse"), (9, 2): (False, "elephant"), (9, 3): (False, "officer"), (9, 4): (False, "captain"),
    (9, 5): (False, "officer"), (9, 6): (False, "elephant"), (9, 7): (False, "horse"), (9, 8): (False, "car")
}

# 绘制棋盘
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE if (row + col) % 2 == 0 else BLACK, rect)

# 绘制棋子
def draw_pieces():
    for position, piece in chessboard.items():
        if piece != "none":
            color = RED if piece[0] else BLACK
            pygame.draw.circle(screen, color, (position[1] * CELL_SIZE + CELL_SIZE // 2, position[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)
    draw_board()
    draw_pieces()
    pygame.display.flip()
