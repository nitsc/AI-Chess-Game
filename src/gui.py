import pathlib

import pygame

from logic import chessboard, Operate, AI

# 获取当前文件路径
current_path = pathlib.Path(__file__).parent.parent

# 游戏配置
FONT_PATH = current_path / "assets" / "fonts" / "SIMLI.TTF"
MUSIC_PATH = current_path / "assets" / "music" / "background.mp3"
GRID_COLOR = (6, 3, 1)
GRID_WIDTH = 3
GRID_SIZE = 100
BACKGROUND_COLOR = (239, 188, 84)
SCREEN_SIZE = (1000, 1100)


def get_piece_image_path(color, kind):
    piece_map = {
        "car": "r", "horse": "h", "elephant": "e", "officer": "a",
        "captain": "g", "soldier": "s", "cannon": "c"
    }
    side = "l1" if color else "d1"
    filename = f"Xiangqi_{piece_map[kind]}{side}.svg.png"
    return current_path / "assets" / "images" / filename


class CNChessGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("AI 中国象棋")
        self.font = pygame.font.Font(FONT_PATH, 80)
        self.operate = Operate()
        self.ai = AI()
        self.current_player = "user"
        self.clicks = []
        self.running = True
        self.draw_board()

    def draw_palace(self):
        palace_lines = [
            ((4 * GRID_SIZE, 1), (6 * GRID_SIZE, 2 * GRID_SIZE)),
            ((4 * GRID_SIZE, 2 * GRID_SIZE), (6 * GRID_SIZE, 0)),
            ((4 * GRID_SIZE, 8 * GRID_SIZE), (6 * GRID_SIZE, 10 * GRID_SIZE)),
            ((4 * GRID_SIZE, 10 * GRID_SIZE), (6 * GRID_SIZE, 8 * GRID_SIZE))
        ]
        for start, end in palace_lines:
            pygame.draw.line(self.screen, GRID_COLOR, start, end, GRID_WIDTH)

    def draw_board(self):
        self.screen.fill(BACKGROUND_COLOR)
        for y in range(0, 11 * GRID_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (self.screen.get_width(), y), GRID_WIDTH)
        for x in range(0, 10 * GRID_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, self.screen.get_height()), GRID_WIDTH)
        self.draw_palace()
        self.draw_pieces()
        self.draw_text()
        pygame.display.flip()

    def draw_pieces(self):
        for (x, y), value in chessboard.items():
            if value is not None:
                draw_x = y * GRID_SIZE + 65
                draw_y = x * GRID_SIZE + 65
                color, kind = value
                piece_image = pygame.image.load(get_piece_image_path(color, kind))
                self.screen.blit(piece_image, (draw_x, draw_y))

    def draw_text(self):
        text = self.font.render("楚河      汉界", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)

    def handle_user_move(self, x, y, nx, ny):
        status = self.operate.user_move(x, y, nx, ny)
        print(chessboard)
        if status in ("CONTINUE", None):
            self.current_player = "ai"
        elif status == "RESELECT":
            print("请重新选择有效的移动")
        else:
            print("状态码异常:", status)
        self.clicks.clear()

    def handle_ai_move(self, ai_way):
        while True:
            if ai_way == "1":
                x, y, nx, ny = self.ai.zhipuai()
                status = self.operate.ai_move(x, y, nx, ny)
                print(chessboard)
                if status in ("CONTINUE", None):
                    self.current_player = "user"
                    break
                elif status != "RESELECT":
                    print("AI 状态码异常:", status)
                    break
            elif ai_way == "2":
                x, y, nx, ny = self.ai.deepseek()
                status = self.operate.ai_move(x, y, nx, ny)
                print(chessboard)
                if status in ("CONTINUE", None):
                    self.current_player = "user"
                    break
                elif status != "RESELECT":
                    print("AI 状态码异常:", status)
                    break
            else:
                print("请输入正确的AI模式")
                break

    def run(self):
        ai_way = input("请选择AI模式 (1. GLM4-PLUS API 对战，2. DeepSeek-r1:671b 本地对战)：")

        # 加载音乐文件 (确保文件路径正确)
        pygame.mixer.music.load(MUSIC_PATH)  # 这里是音乐文件路径

        # 设置音乐循环次数，-1表示无限循环
        pygame.mixer.music.play(loops=-1, start=0.0)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.current_player == "user":
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = round(mouse_x / GRID_SIZE) - 1, round(mouse_y / GRID_SIZE) - 1
                    self.clicks.append((grid_y, grid_x))
                    if len(self.clicks) == 2:
                        self.handle_user_move(*self.clicks[0], *self.clicks[1])
            if self.current_player == "ai":
                self.handle_ai_move(ai_way=ai_way)
            self.draw_board()
        pygame.quit()
