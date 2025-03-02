# < 作者：八 18 班周伟安 >
# < 笔名：Data Infintai Eterni >
# < 邮箱：dministrator1st1234567890dddaz@outlook.com >
# < 邮箱：zhoukreanto@gmail.com >

import pathlib
import secrets
import pygame
from settings import chessboard
from settings import Operate
from settings import AI

# 获取当前文件路径
current_path = pathlib.Path(__file__).parent

# 获取字体路径
font_path = current_path / "fonts" / "SIMLI.TTF"

# 设置网格线的颜色和宽度
grid_color = (6, 3, 1)
grid_width = 3

# 设置网格的大小
grid_size = 100         # 网格单元的大小

# 初始化 Pygame
pygame.init()

# 设置窗口大小
screen = pygame.display.set_mode((1000, 1100))

# 设置窗口标题
pygame.display.set_caption("AI 中国象棋")

# 加载字体
font = pygame.font.Font(font_path, 80)

# 设置背景颜色
background_color = (239, 188, 84)
screen.fill(background_color)

# 创建文字表面
text = font.render("楚河      汉界", True, (0, 0, 0))
text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

# 定义绘制棋盘的函数
def draw_board():
     screen.fill(background_color)
     # 绘制水平网格线（10条线对应9个格子）
     for y in range(0, 10 * grid_size, grid_size):
          pygame.draw.line(screen, grid_color, (0, y), (screen.get_width(), y), grid_width)
     # 绘制垂直网格线（9条线对应8个格子）
     for x in range(0, 9 * grid_size, grid_size):
          pygame.draw.line(screen, grid_color, (x, 0), (x, screen.get_height()), grid_width)
     # 绘制棋子
     for (x, y), value in chessboard.items():
          if value != 'none':
               draw_x = y * grid_size + 65         # 调整为列坐标，偏移居中
               draw_y = x * grid_size + 65         # 调整为行坐标，偏移居中
               color, kind = value
               if color:         # 红方
                    if kind == 'car':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_rl1.svg.png")
                    elif kind == 'horse':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_hl1.svg.png")
                    elif kind == 'elephant':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_el1.svg.png")
                    elif kind == 'officer':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_al1.svg.png")
                    elif kind == 'captain':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_gl1.svg.png")
                    elif kind == 'soldier':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_sl1.svg.png")
                    elif kind == 'cannon':
                        piece_image = pygame.image.load(current_path / "images" / "Xiangqi_cl1.svg.png")
               if not color:         # 黑方
                    if kind == 'car':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_rd1.svg.png")
                    elif kind == 'horse':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_hd1.svg.png")
                    elif kind == 'elephant':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_ed1.svg.png")
                    elif kind == 'officer':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_ad1.svg.png")
                    elif kind == 'captain':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_gd1.svg.png")
                    elif kind == 'soldier':
                         piece_image = pygame.image.load(current_path / "images" / "Xiangqi_sd1.svg.png")
                    elif kind == 'cannon':
                        piece_image = pygame.image.load(current_path / "images" / "Xiangqi_cd1.svg.png")
               screen.blit(piece_image, (draw_x, draw_y))
     # 绘制文字
     screen.blit(text, text_rect)
     pygame.display.flip()

# 实例化 Operate 和 AI
operate = Operate()
ai = AI()

# 随机决定先手
decider = 0
current_player = "user" if decider == 0 else "ai"
clicks = []

# 初始绘制棋盘
draw_board()

# 游戏主循环
running = True
while running:
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               running = False
          elif event.type == pygame.MOUSEBUTTONDOWN and current_player == "user":
               mouse_x, mouse_y = pygame.mouse.get_pos()
               grid_x = round(mouse_x / grid_size) - 1
               grid_y = round(mouse_y / grid_size) - 1
               clicks.append((grid_y, grid_x))         # (行, 列)
               if len(clicks) == 2:
                    (x, y), (nx, ny) = clicks
                    print("拾起棋子坐标:", (x, y))
                    print("释放棋子坐标:", (nx, ny))
                    status = operate.user_move(x, y, nx, ny)
                    if status == "CONTINUE":
                         current_player = "ai"
                         clicks = []
                    elif status == "RESELECT":
                         clicks = []         # 重新选择
                         print("请重新选择有效的移动")
                    else:
                         print("状态码异常:", status)

     if current_player == "ai":
          while True:
               x, y, nx, ny = ai.zhipuai()
               status = operate.ai_move(x, y, nx, ny)
               if status == "CONTINUE":
                    current_player = "user"
                    break
               elif status == "RESELECT":
                    continue
               else:
                    print("AI 状态码异常:", status)
                    break

     # 每次循环结束时绘制棋盘
     draw_board()

# 退出 Pygame
pygame.quit()