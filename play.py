import pygame, sys
sys.path.append("D:\\chinesechess")
from settings import chessboard, piece_name_map, Operate

# 初始化pygame
pygame.init()

# 棋盘参数
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 900  # 屏幕大小
CELL_SIZE = 80  # 棋盘单元格大小
MARGIN = 50  # 棋盘边距
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chinese Chess")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 颜色映射
color_map = {
    True: RED,  # 红色
    False: BLACK  # 黑色
}

# 加载字体
FONT = pygame.font.SysFont("simhei", 40)  # 使用中文字体

# 绘制棋盘
def draw_board():
    SCREEN.fill(WHITE)

    # 绘制网格
    for row in range(10):
        y = MARGIN + row * CELL_SIZE
        pygame.draw.line(SCREEN, BLACK, (MARGIN, y), (MARGIN + 8 * CELL_SIZE, y), 2)

    for col in range(9):
        x = MARGIN + col * CELL_SIZE
        pygame.draw.line(SCREEN, BLACK, (x, MARGIN), (x, MARGIN + 9 * CELL_SIZE), 2)

    # 绘制河界
    river_text = FONT.render("楚河     汉界", True, BLACK)
    SCREEN.blit(river_text, (MARGIN + 2.5 * CELL_SIZE, MARGIN + 4.5 * CELL_SIZE - 20))

# 绘制棋子
def draw_pieces():
    for (pos, piece) in chessboard.items():
        x, y = pos
        center_x = MARGIN + y * CELL_SIZE
        center_y = MARGIN + x * CELL_SIZE

        if piece != 'none':
            color, name = piece
            piece_color = color_map[color]
            pygame.draw.circle(SCREEN, piece_color, (center_x, center_y), CELL_SIZE // 3)
            text = FONT.render(piece_name_map[name], True, WHITE)
            text_rect = text.get_rect(center=(center_x, center_y))
            SCREEN.blit(text, text_rect)

# 获取点击的棋盘坐标
def get_board_position(mouse_pos):
    x, y = mouse_pos
    col = (x - MARGIN) // CELL_SIZE
    row = (y - MARGIN) // CELL_SIZE
    if 0 <= col < 9 and 0 <= row < 10:
        return row, col
    return None

# 主循环
def main():
    clock = pygame.time.Clock()
    running = True
    selected_piece = None
    first_click = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键单击
                    board_pos = get_board_position(event.pos)
                    if board_pos:
                        if first_click is None:
                            first_click = board_pos
                            print(f"第一次单击位置: {first_click}")
                        else:
                            print(f"第二次单击位置: {board_pos}")
                            Operate.move(first_click[0], first_click[1], board_pos[0], board_pos[1])
                            first_click = None
        draw_board()
        draw_pieces()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
