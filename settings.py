# < 作者：八 18 班周伟安 >
# < 笔名：Data Infintai Eterni >
# < 邮箱：dministrator1st1234567890dddaz@outlook.com >
# < 邮箱：zhoukreanto@gmail.com >

import sys

import ollama
from zhipuai import ZhipuAI



# 棋盘布局, 以左下角的棋子为(0,0), True 是红棋, False 是黑棋
chessboard = {(9, 0): (True, 'car'), (9, 1): (True, 'horse'), (9, 2): (True, 'elephant'), (9, 3): (True, 'officer'),
              (9, 4): (True, 'captain'), (9, 5): (True, 'officer'), (9, 6): (True, 'elephant'), (9, 7): (True, 'horse'),
              (9, 8): (True, 'car'),
              (8, 0): 'none', (8, 1): 'none', (8, 2): 'none', (8, 3): 'none', (8, 4): 'none', (8, 5): 'none',
              (8, 6): 'none', (8, 7): 'none', (8, 8): 'none',
              (7, 0): 'none', (7, 1): (True, 'cannon'), (7, 2): 'none', (7, 3): 'none', (7, 4): 'none', (7, 5): 'none',
              (7, 6): 'none', (7, 7): (True, 'cannon'), (7, 8): 'none',
              (6, 0): (True, 'soldier'), (6, 1): 'none', (6, 2): (True, 'soldier'), (6, 3): 'none',
              (6, 4): (True, 'soldier'), (6, 5): 'none', (6, 6): (True, 'soldier'), (6, 7): 'none',
              (6, 8): (True, 'soldier'),
              (5, 0): 'none', (5, 1): 'none', (5, 2): 'none', (5, 3): 'none', (5, 4): 'none', (5, 5): 'none',
              (5, 6): 'none', (5, 7): 'none', (5, 8): 'none',
              (4, 0): 'none', (4, 1): 'none', (4, 2): 'none', (4, 3): 'none', (4, 4): 'none', (4, 5): 'none',
              (4, 6): 'none', (4, 7): 'none', (4, 8): 'none',
              (3, 0): (False, 'soldier'), (3, 1): 'none', (3, 2): (False, 'soldier'), (3, 3): 'none',
              (3, 4): (False, 'soldier'), (3, 5): 'none', (3, 6): (False, 'soldier'), (3, 7): 'none',
              (3, 8): (False, 'soldier'),
              (2, 0): 'none', (2, 1): (False, 'cannon'), (2, 2): 'none', (2, 3): 'none', (2, 4): 'none', (2, 5): 'none',
              (2, 6): 'none', (2, 7): (False, 'cannon'), (2, 8): 'none',
              (1, 0): 'none', (1, 1): 'none', (1, 2): 'none', (1, 3): 'none', (1, 4): 'none', (1, 5): 'none',
              (1, 6): 'none', (1, 7): 'none', (1, 8): 'none',
              (0, 0): (False, 'car'), (0, 1): (False, 'horse'), (0, 2): (False, 'elephant'), (0, 3): (False, 'officer'),
              (0, 4): (False, 'captain'), (0, 5): (False, 'officer'), (0, 6): (False, 'elephant'),
              (0, 7): (False, 'horse'), (0, 8): (False, 'car')}

# 输入红方的区域坐标
red_half = [(9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8),
            (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8),
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8),
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8)]

# 输入黑的区域坐标
black_half = [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
              (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
              (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
              (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
              (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]



class Chess:
    def __init__(self):
        self.red_score = 0
        self.black_score = 0

    def red_soldier(self, x, y, nx, ny):
        """制定红方士兵的规则"""
        # 检查是否在棋盘上
        if 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查在哪一方区域
            if (x, y) in red_half:
                # 检查是否在合法的移动范围内
                if (nx, ny) == (x + 1, y):
                    # 检查新位置是空格
                    if chessboard[(nx, ny)] == "none":
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"soldier"）
                        chessboard[(x, y)] = "none"
                        chessboard[(nx, ny)] = (True, "soldier")
                        return "MOVED"
                    else:
                        # 如果新位置是黑棋
                        if not chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"soldier"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (True, "soldier")
                            # 给红方加分
                            self.red_score += 1
                            return "CAP-BLACK"
                        # 如果新位置是红棋
                        elif chessboard[(nx, ny)][0]:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                else:
                    print("不能走那么多")
                    return "RESELECT"
            elif (x, y) in black_half:
                # 检查是否在合法范围内
                if (nx, ny) == (x, y + 1) or (nx, ny) == (x, y - 1) or (nx, ny) == (x + 1, y) or (nx, ny) == (x - 1, y):
                    # 如果新位置是空格
                    if chessboard[(nx, ny)] == "none":
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"soldier"）
                        chessboard[(x, y)] = "none"
                        chessboard[(nx, ny)] = (True, "soldier")
                        return "MOVED"
                    else:
                        # 如果新位置是黑棋
                        if not chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"soldier"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (True, "soldier")
                            # 给红方加分
                            self.red_score += 1
                            return "CAP-BLACK"
                        # 如果新位置是红棋
                        elif chessboard[(nx, ny)][0]:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
            else:
                print("意想不到的事情发生了")
                sys.exit()

    def black_soldier(self, x, y, nx, ny):
        """制定黑方士兵的规则"""
        # 检查是否在棋盘上
        if 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            # 检查在哪一方区域
            if (x, y) in black_half:
                # 检查是否在合法的移动范围内
                if (nx, ny) == (x, y + 1):
                    # 检查新位置没有棋子
                    if chessboard[(nx, ny)] == "none":
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"soldier"）
                        chessboard[(x, y)] = "none"
                        chessboard[(nx, ny)] = (False, "soldier")
                        return "MOVED"
                    else:
                        # 如果新位置是红棋
                        if chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"soldier"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (False, "soldier")
                            # 给黑方加分
                            self.black_score += 1
                            return "CAP-RED"
                        # 如果新位置是黑棋
                        elif not chessboard[(nx, ny)][0]:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                else:
                    print("不能走那么多")
                    return "RESELECT"
            elif (x, y) in red_half:
                # 检查是否在合法范围内
                if (nx, ny) == (x, y + 1) or (nx, ny) == (x, y - 1) or (nx, ny) == (x + 1, y) or (nx, ny) == (x - 1, y):
                    # 如果新位置是空格
                    if chessboard[(nx, ny)] == "none":
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"soldier"）
                        chessboard[(x, y)] = "none"
                        chessboard[(nx, ny)] = (False, "soldier")
                        return "MOVED"
                    else:
                        # 如果新位置是红棋
                        if not chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"soldier"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (False, "soldier")
                            # 给黑方加分
                            self.black_score += 1
                            return "CAP-RED"
                        # 如果新位置是黑棋
                        elif chessboard[(nx, ny)][0]:
                            # 不移动棋子

                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
            else:
                print("意想不到的事情发生了")
                sys.exit()
        else:

            print("不在棋盘上")
            return "RESELECT"

    def red_cannon(self, x, y, nx, ny):
        """红炮移动规则"""
        # 检查是否在棋盘上
        if 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            # 检查是垂直移动
            if x == nx and y != ny:
                # 确定y方向上的最小值和最大值
                min_y, max_y = min(y, ny), max(y, ny)
                # 统计中间是否只有一个棋子
                num_pieces = sum(1 for cachey in range(min_y + 1, max_y) if chessboard[(x, cachey)] != "none")

                # 列举出（x,y）和（x,ny）之间的坐标
                for cachey in list(range(y + 1, ny)) if y > ny else list(range(ny + 1, y)):
                    # 如果中间没棋子
                    if chessboard[(x, cachey)] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx, ny)] == "none":
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"cannon"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (True, "cannon")
                            return "MOVED"
                        # 如果新位置是黑棋
                        elif not chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("没有棋子充当炮架")
                            return "RESELECT"
                        # 如果新位置是红棋
                        elif chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间只有一个棋子
                    elif num_pieces == 1:
                        # 如果新位置是空的
                        if chessboard[(nx, ny)] == "none":
                            print("有棋子阻挡")
                            return "RESELECT"
                        # 如果新位置是黑棋
                        elif not chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"cannon"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (True, "cannon")
                            self.red_score += 1
                            return "CAP-BLACK"
                        # 如果新位置是红棋
                        elif chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有大于1个棋子
                    elif num_pieces > 1:
                        print("中间有多个棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            # 如果是水平移动
            if x != nx and y == ny:
                # 确定x方向上的最小值和最大值
                min_x, max_x = min(x, nx), max(x, nx)
                # 统计中间是否只有一个棋子
                num_pieces = sum(1 for cachex in range(min_x + 1, max_x) if chessboard[(cachex, y)] != "none")

                # 列举出（x,y）和（nx,y）之间的坐标
                for cachex in list(range(x + 1, nx)) if x > nx else list(range(nx + 1, x)):
                    # 如果中间没棋子
                    if chessboard[(x, cachex)] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx, nx)] == "none":
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"cannon"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (True, "cannon")
                            return "MOVED"
                        # 如果新位置是黑棋
                        elif not chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("没有棋子充当炮架")
                            return "RESELECT"
                        # 如果新位置是红棋
                        elif chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间只有一个棋子
                    elif num_pieces == 1:
                        # 如果新位置是空的
                        if chessboard[(nx, ny)] == "none":
                            print("有棋子阻挡")
                            return "RESELECT"
                        # 如果新位置是黑棋
                        elif not chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"cannon"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (True, "cannon")
                            self.red_score += 1
                            return "CAP-BLACK"
                        # 如果新位置是红棋
                        elif chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有大于1个棋子
                    elif num_pieces > 1:
                        print("中间有多个棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            else:
                print("要水平或垂直移动")
                return "RESELECT"
        else:

            print("不在棋盘上")
            return "RESELECT"

    def black_cannon(self, x, y, nx, ny):
        """黑炮移动规则"""
        # 检查是否在棋盘上
        if 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            # 检查是垂直移动
            if x == nx and y != ny:
                # 确定y方向上的最小值和最大值
                min_y, max_y = min(y, ny), max(y, ny)
                # 统计中间是否只有一个棋子
                num_pieces = sum(1 for cachey in range(min_y + 1, max_y) if chessboard[(x, cachey)] != "none")

                # 列举出（x,y）和（x,ny）之间的坐标
                for cachey in list(range(y + 1, ny)) if y > ny else list(range(ny + 1, y)):
                    # 如果中间没棋子
                    if chessboard[(x, cachey)] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx, ny)] == "none":
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"cannon"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (False, "cannon")
                            return "MOVED"
                        # 如果新位置是红棋
                        elif chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("没有棋子充当炮架")
                            return "RESELECT"
                        # 如果新位置是黑棋
                        elif not chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间只有一个棋子
                    elif num_pieces == 1:
                        # 如果新位置是空的
                        if chessboard[(nx, ny)] == "none":
                            print("有棋子阻挡")
                            return "RESELECT"
                        # 如果新位置是红棋
                        elif chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"cannon"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (False, "cannon")
                            self.black_score += 1
                            return "CAP-BLACK"
                        # 如果新位置是黑棋
                        elif not chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有大于1个棋子
                    elif num_pieces > 1:
                        print("中间有多个棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            # 如果是水平移动
            if x != nx and y == ny:
                # 确定x方向上的最小值和最大值
                min_x, max_x = min(x, nx), max(x, nx)
                # 统计中间是否只有一个棋子
                num_pieces = sum(1 for cachex in range(min_x + 1, max_x) if chessboard[(cachex, y)] != "none")

                # 列举出（x,y）和（nx,y）之间的坐标
                for cachex in list(range(x + 1, nx)) if x > nx else list(range(nx + 1, x)):
                    # 如果中间没棋子
                    if chessboard[(x, cachex)] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx, nx)] == "none":
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"cannon"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (False, "cannon")
                            return "MOVED"
                        # 如果新位置是红棋
                        elif chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("没有棋子充当炮架")
                            return "RESELECT"
                        # 如果新位置是黑棋
                        elif not chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间只有一个棋子
                    elif num_pieces == 1:
                        # 如果新位置是空的
                        if chessboard[(nx, ny)] == "none":
                            print("有棋子阻挡")
                            return "RESELECT"
                        # 如果新位置是红棋
                        elif not chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"cannon"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (False, "cannon")
                            self.black_score += 1
                            return "CAP-RED"
                        # 如果新位置是黑棋
                        elif not chessboard[(nx, ny)][0]:
                            # 不移动棋子
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有大于1个棋子
                    elif num_pieces > 1:
                        print("中间有多个棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            else:
                print("要水平或垂直移动")
                return "RESELECT"
        else:
            print("不在棋盘上")
            return "RESELECT"

    def red_car(self, x, y, nx, ny):
        """红车移动规则"""
        # 检查是否在棋盘上
        if 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            # 检查是否垂直移动
            if x == nx and y != ny:
                # 列举出（x,y）和（x,ny）之间的坐标
                for cachey in list(range(y + 1, ny)) if y > ny else list(range(ny + 1, y)):
                    print(x, cachey)
                    # 如果中间没棋子
                    if chessboard[(x, cachey)] == "none":
                        # 如果目标位置有黑棋
                        if not chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（x,ny）的键值对改为（True,"car"）
                            chessboard[(x, y)] = "none"
                            chessboard[(x, ny)] = (True, "car")
                            self.red_score += 1
                            return "CAP-BLACK"
                        # 如果目标位置有红棋
                        elif chessboard[(nx, ny)][0]:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        # 如果目标位置是空的
                        elif chessboard[(nx, ny)] == "none":
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（x,ny）的键值对改为（True,"car"）
                            chessboard[(x, y)] = "none"
                            chessboard[(x, ny)] = (True, "car")
                            return "MOVED"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有棋子
                    elif chessboard[(x, cachey)][0] != "none":
                        print("有棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            # 检查是否水平移动
            elif x != nx and y == ny:
                # 列举出（x,y）和（nx,y）之间的坐标
                for cachex in list(range(x + 1, nx)) if x > nx else list(range(nx + 1, x)):
                    # 如果中间没棋子
                    if chessboard[(cachex, y)] == "none":
                        # 如果目标位置有黑棋
                        if not chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"car"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, y)] = (True, "car")
                            self.red_score += 1
                            return "CAP-BLACK"
                        # 如果目标位置有红棋
                        elif chessboard[(nx, ny)][0]:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        # 如果目标位置是空的
                        elif chessboard[(nx, ny)] == "none":
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"car"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, y)] = (True, "car")
                            return "MOVED"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有棋子
                    elif chessboard[(cachex, y)][0] != "none":
                        print("有棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            else:
                print("要水平或垂直移动")
                return "RESELECT"
        else:
            print("不在棋盘上")
            return "RESELECT"

    def black_car(self, x, y, nx, ny):
        """黑车移动规则"""
        # 检查是否在棋盘上
        if 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            # 检查是否垂直移动
            if x == nx and y != ny:
                # 列举出（x,y）和（x,ny）之间的坐标
                for cachey in list(range(y + 1, ny)) if y > ny else list(range(ny + 1, y)):
                    print(x, cachey)
                    # 如果中间没棋子
                    if chessboard[(x, cachey)] == "none":
                        # 如果目标位置有红棋
                        if chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（x,ny）的键值对改为（False,"car"）
                            chessboard[(x, y)] = "none"
                            chessboard[(x, ny)] = (False, "car")
                            self.black_score += 1
                            return "CAP-RED"
                        # 如果目标位置有黑棋
                        elif not chessboard[(nx, ny)][0]:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        # 如果目标位置是空的
                        elif chessboard[(nx, ny)] == "none":
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（x,ny）的键值对改为（False,"car"）
                            chessboard[(x, y)] = "none"
                            chessboard[(x, ny)] = (False, "car")
                            return "MOVED"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有棋子
                    elif chessboard[(x, cachey)][0] != "none":
                        print("有棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            # 检查是否水平移动
            elif x != nx and y == ny:
                # 列举出（x,y）和（nx,y）之间的坐标
                for cachex in list(range(x + 1, nx)) if x > nx else list(range(nx + 1, x)):
                    # 如果中间没棋子
                    if chessboard[(cachex, y)] == "none":
                        # 如果目标位置有红棋
                        if chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"car"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, y)] = (False, "car")
                            self.black_score += 1
                            return "CAP-RED"
                        # 如果目标位置有黑棋
                        elif not chessboard[(nx, ny)][0]:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        # 如果目标位置是空的
                        elif chessboard[(nx, ny)] == "none":
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"car"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, y)] = (False, "car")
                            return "MOVED"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有棋子
                    elif chessboard[(cachex, y)][0] != "none":
                        print("有棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            else:
                print("要水平或垂直移动")
                return "RESELECT"
        else:

            print("不在棋盘上")
            return "RESELECT"

    def red_horse(self, x, y, nx, ny):
        """红马移动规则"""
        def red_horse_go(x, y, nx, ny):
            # 如果目标位置为空
            if chessboard[(nx, ny)] == "none":
                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"horse"）
                chessboard[(x, y)] = "none"
                chessboard[(nx, ny)] = (True, "horse")
                return "MOVED"
            # 如果目标位置有黑棋
            elif not chessboard[(nx, ny)][0]:
                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"horse"）
                chessboard[(x, y)] = "none"
                chessboard[(nx, ny)] = (True, "horse")
                self.red_score += 1
                return "CAP-BLACK"
            # 如果目标位置有红棋
            elif chessboard[(nx, ny)][0]:
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()

        # 检查是否在棋盘上
        if 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            # 检查是否走“日”字（1）
            if nx == x - 2 and ny == y + 1:
                # 检查没有拌马脚
                if chessboard[(x - 1, y)][0] == "none":
                    red_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（2）
            elif nx == x - 1 and ny == y + 2:
                # 检查没有拌马脚
                if chessboard[(x - 1, y + 1)][0] == "none":
                    red_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y + 1)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（3）
            elif nx == x + 2 and ny == y + 1:
                # 检查没有拌马脚
                if chessboard[(x + 1, y)][0] == "none":
                    red_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（4）
            elif nx == x + 1 and ny == y + 2:
                # 检查没有拌马脚
                if chessboard[(x + 1, y + 1)][0] == "none":
                    red_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y + 1)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（5）
            elif nx == x - 2 and ny == y - 1:
                # 检查没有拌马脚
                if chessboard[(x - 1, y)][0] == "none":
                    red_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（6）
            elif nx == x - 1 and ny == y - 2:
                # 检查没有拌马脚
                if chessboard[(x - 1, y - 1)][0] == "none":
                    red_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y - 1)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（7）
            elif nx == x + 2 and ny == y - 1:
                # 检查没有拌马脚
                if chessboard[(x + 1, y)][0] == "none":
                    red_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（8）
            elif nx == x + 1 and ny == y - 2:
                # 检查没有拌马脚
                if chessboard[(x + 1, y - 1)][0] == "none":
                    red_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y - 1)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                print("走法不正确")
                return "RESELECT"
        else:
            print("不在棋盘上")
            return "RESELECT"

    def black_horse(self, x, y, nx, ny):
        """黑马移动规则"""
        def black_horse_go(x, y, nx, ny):
            # 如果目标位置为空
            if chessboard[(nx, ny)] == "none":
                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"horse"）
                chessboard[(x, y)] = "none"
                chessboard[(nx, ny)] = (False, "horse")
                return "MOVED"
            # 如果目标位置有红棋
            elif chessboard[(nx, ny)][0]:
                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"horse"）
                chessboard[(x, y)] = "none"
                chessboard[(nx, ny)] = (False, "horse")
                self.black_score += 1
                return "CAP-RED"
            # 如果目标位置有黑棋
            elif not chessboard[(nx, ny)][0]:
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()

        # 检查是否在棋盘上
        if 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            # 检查是否走“日”字（1）
            if nx == x - 2 and ny == y + 1:
                # 检查没有拌马脚
                if chessboard[(x - 1, y)][0] == "none":
                    black_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（2）
            elif nx == x - 1 and ny == y + 2:
                # 检查没有拌马脚
                if chessboard[(x - 1, y + 1)][0] == "none":
                    black_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y + 1)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（3）
            elif nx == x + 2 and ny == y + 1:
                # 检查没有拌马脚
                if chessboard[(x + 1, y)][0] == "none":
                    black_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（4）
            elif nx == x + 1 and ny == y + 2:
                # 检查没有拌马脚
                if chessboard[(x + 1, y + 1)][0] == "none":
                    black_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y + 1)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（5）
            elif nx == x - 2 and ny == y - 1:
                # 检查没有拌马脚
                if chessboard[(x - 1, y)][0] == "none":
                    black_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（6）
            elif nx == x - 1 and ny == y - 2:
                # 检查没有拌马脚
                if chessboard[(x - 1, y - 1)][0] == "none":
                    black_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y - 1)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（7）
            elif nx == x + 2 and ny == y - 1:
                # 检查没有拌马脚
                if chessboard[(x + 1, y)][0] == "none":
                    black_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（8）
            elif nx == x + 1 and ny == y - 2:
                # 检查没有拌马脚
                if chessboard[(x + 1, y - 1)][0] == "none":
                    black_horse_go(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y - 1)][0] != "none":
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                print("走法不正确")
                return "RESELECT"
        else:
            print("不在棋盘上")
            return "RESELECT"

    def red_officer(self, x, y, nx, ny):
        """红士移动规则"""
        if 0 <= x <= 9 and 0 <= y <= 9:
            # 检查是否在九宫格内
            if 3 <= nx <= 5 and 0 <= ny <= 2:
                # 检查是否走斜线
                if (nx == x + 1 and ny == y + 1) or (nx == x + 1 and ny == y - 1) or (nx == x - 1 and ny == y + 1) or (
                        nx == x - 1 and ny == y - 1):
                    # 如果新位置是空的
                    if chessboard[(nx, ny)][0] == "none":
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"officer"）
                        chessboard[(x, y)] = "none"
                        chessboard[(nx, ny)] = (True, "officer")
                        return "MOVED"
                    # 如果新位置不是空的
                    elif chessboard[(nx, ny)][0] != "none":
                        # 如果新位置的棋子是黑棋
                        if not chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"officer"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (True, "officer")
                            self.red_score += 1
                            return "CAP-BLACK"
                        # 如果新位置的棋子是红棋
                        elif chessboard[(nx, ny)][0]:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
                else:
                    print("走法不正确")
                    return "RESELECT"
            else:
                print("不在棋盘上")
                return "RESELECT"

    def black_officer(self, x, y, nx, ny):
        """黑士移动规则"""
        if 0 <= x <= 9 and 0 <= y <= 9:
            # 检查是否在九宫格内
            if 3 <= nx <= 5 and 7 <= ny <= 9:
                # 检查是否走斜线
                if (nx == x + 1 and ny == y + 1) or (nx == x + 1 and ny == y - 1) or (nx == x - 1 and ny == y + 1) or (
                        nx == x - 1 and ny == y - 1):
                    # 如果新位置是空的
                    if chessboard[(nx, ny)][0] == "none":
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"officer"）
                        chessboard[(x, y)] = "none"
                        chessboard[(nx, ny)] = (False, "officer")
                        return "MOVED"
                    # 如果新位置不是空的
                    elif chessboard[(nx, ny)][0] != "none":
                        # 如果新位置的棋子是红棋
                        if chessboard[(nx, ny)][0]:
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"officer"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (False, "officer")
                            self.black_score += 1
                            return "CAP-RED"
                        # 如果新位置的棋子是黑棋
                        elif not chessboard[(nx, ny)][0]:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
                else:
                    print("走法不正确")
                    return "RESELECT"
            else:
                print("不在九宫格内")
                return "RESELECT"
        else:
            print("不在棋盘上")
            return "RESELECT"

    def red_elephant(self, x, y, nx, ny):
        """红象移动规则"""
        # 检查是否在棋盘上
        if 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            # 检查是否走田字
            if (nx == x + 2 and ny == y + 2) or (nx == x + 2 and ny == y - 2) or (nx == x - 2 and ny == y + 2) or (
                    nx == x - 2 and ny == y - 2):
                # 检查是否过河
                if nx and ny in red_half:
                    # 检查是否被蹩象脚
                    if (x + 1, y) in chessboard and chessboard[(x + 1, y)][0] == "none" and (x - 1, y) in chessboard and \
                            chessboard[(x - 1, y)][0] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx, ny)][0] == "none":
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"elephant"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (True, "elephant")
                            return "MOVED"
                        # 如果新位置不是空的
                        elif chessboard[(nx, ny)][0] != "none":
                            # 如果新位置的棋子是红棋
                            if chessboard[(nx, ny)][0]:
                                print("不能吃自己的棋子")
                                return "RESELECT"
                            # 如果新位置的棋子是黑棋
                            elif not chessboard[(nx, ny)][0]:
                                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"elephant"）
                                chessboard[(x, y)] = "none"
                                chessboard[(nx, ny)] = (True, "elephant")
                                self.red_score += 1
                                return "CAP-BLACK"
                            else:
                                print("意想不到的事情发生了")
                                sys.exit()
                    else:
                        print("被蹩象脚")
                        return "TRIP-ELEPHANT"
                else:
                    print("过河了")
                    return "NO-CROSS"
            else:
                print("走法不正确")
                return "RESELECT"
        else:
            print("不在棋盘上")
            return "RESELECT"

    def black_elephant(self, x, y, nx, ny):
        """黑象移动规则"""
        # 检查是否在棋盘上
        if 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            # 检查是否走田字
            if (nx == x + 2 and ny == y + 2) or (nx == x + 2 and ny == y - 2) or (nx == x - 2 and ny == y + 2) or (
                    nx == x - 2 and ny == y - 2):
                # 检查是否过河
                if nx and ny in black_half:
                    # 检查是否被蹩象脚
                    if (x + 1, y) in chessboard and chessboard[(x + 1, y)][0] == "none" and (x - 1, y) in chessboard and \
                            chessboard[(x - 1, y)][0] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx, ny)][0] == "none":
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"elephant"）
                            chessboard[(x, y)] = "none"
                            chessboard[(nx, ny)] = (False, "elephant")
                            return "MOVED"
                        # 如果新位置不是空的
                        elif chessboard[(nx, ny)][0] != "none":
                            # 如果新位置的棋子是黑棋
                            if not chessboard[(nx, ny)][0]:
                                print("不能吃自己的棋子")
                                return "RESELECT"
                            # 如果新位置的棋子是红棋
                            elif chessboard[(nx, ny)][0]:
                                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"elephant"）
                                chessboard[(x, y)] = "none"
                                chessboard[(nx, ny)] = (False, "elephant")
                                self.red_score += 1
                                return "CAP-RED"
                            else:
                                print("意想不到的事情发生了")
                                sys.exit()
                    else:
                        print("被蹩象脚")
                        return "TRIP-ELEPHANT"
                else:
                    print("过河了")
                    return "NO-CROSS"
            else:
                print("走法不正确")
                return "RESELECT"
        else:
            print("不在棋盘上")
            return "RESELECT"

    def red_cap(self, x, y, nx, ny):
        """红将移动规则"""
        # 检查是否在九宫格内
        if 3 <= nx <= 5 and 0 <= ny <= 2:
            # 检查是否走直线
            if (nx == x + 1 and ny == y) or (nx == x - 1 and ny == y) or (nx == x and ny == y + 1) or (nx == x and ny == y - 1):
                # 如果新位置是空的
                if chessboard[(nx, ny)][0] == "none":
                    # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"captain"）
                    chessboard[(x, y)] = "none"
                    chessboard[(nx, ny)] = (True, "captain")
                    return "MOVED"
                # 如果新位置不是空的
                elif chessboard[(nx, ny)][0] != "none":
                    # 如果新位置的棋子是黑棋
                    if not chessboard[(nx, ny)][0]:
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"captain"）
                        chessboard[(x, y)] = "none"
                        chessboard[(nx, ny)] = (True, "captain")
                        self.red_score += 1
                        return "CAP-BLACK"
                     # 如果新位置的棋子是红棋
                    elif chessboard[(nx, ny)][0]:
                        print("不能吃自己的棋子")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            else:
                print("走法不正确")
                return "RESELECT"
        else:
            print("不在九宫格内")
            return "RESELECT"

    def black_cap(self, x, y, nx, ny):
        """黑将移动规则"""
        # 检查是否在九宫格内
        if 3 <= nx <= 5 and 7 <= ny <= 9:
            # 检查是否走直线
            if (nx == x + 1 and ny == y) or (nx == x - 1 and ny == y) or (nx == x and ny == y + 1) or (nx == x and ny == y - 1):
                # 如果新位置是空的
                if chessboard[(nx, ny)][0] == "none":
                    # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"captain"）
                    chessboard[(x, y)] = "none"
                    chessboard[(nx, ny)] = (False, "captain")
                    return "MOVED"
                # 如果新位置不是空的
                elif chessboard[(nx, ny)][0] != "none":
                    # 如果新位置的棋子是红棋
                    if chessboard[(nx, ny)][0]:
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"captain"）
                        chessboard[(x, y)] = "none"
                        chessboard[(nx, ny)] = (False, "captain")
                        self.black_score += 1
                        return "CAP-RED"
                    # 如果新位置的棋子是黑棋
                    elif not chessboard[(nx, ny)][0]:
                        print("不能吃自己的棋子")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                print("走法不正确")
                return "RESELECT"
        else:
            print("不在九宫格内")
            return "RESELECT"



class Operate:
    def __init__(self):
        self.chess = Chess()
        self.red_score = self.chess.red_score
        self.black_score = self.chess.black_score

    @staticmethod
    def check_red_captain(chessboard):
        """检查红方是否还有将"""
        for pos, (is_red, piece) in chessboard.items():
            if piece == "captain" and is_red:
                return True  # 红方的将还在
        print("红方将领被吃掉！游戏结束！")
        return False  # 红方的将已经被吃掉

    @staticmethod
    def check_black_captain(chessboard):
        """检查黑方是否还有将"""
        for pos, (is_red, piece) in chessboard.items():
            if piece == "captain" and not is_red:
                return True  # 黑方的将还在
        print("黑方将领被吃掉！游戏结束！")
        return False  # 黑方的将已经被吃掉

    # 红方
    def user_move(self, x, y, nx, ny):
        """判断坐标并调用 Chess类 的 对应函数"""
        red_car = self.chess.red_car(x, y, nx, ny)
        red_horse = self.chess.red_horse(x, y, nx, ny)
        red_elephant = self.chess.red_elephant(x, y, nx, ny)
        red_officer = self.chess.red_officer(x, y, nx, ny)
        red_captain = self.chess.red_cap(x, y, nx, ny)
        red_soldier = self.chess.red_soldier(x, y, nx, ny)
        red_cannon = self.chess.red_cannon(x, y, nx, ny)

        
        def report():
            print(f"红方: {self.red_score}分, 黑方: {self.black_score}分")

        # 判断棋子类型
        if chessboard[(x, y)][1] == "car":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                message = red_car
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                self.check_black_captain(chessboard)

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                print("不是你的棋子")
                return "RESELECT"

        elif chessboard[(x, y)][1] == "horse":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                message = red_horse
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                elif message == "TRIP-HORSE":
                    print("拌马脚！")
                    report()
                    return "RESELECT"
                self.check_black_captain(chessboard)

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                print("不是你的棋子")
                return "RESELECT"

        elif chessboard[(x, y)][1] == "elephant":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                message = red_elephant
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                elif message == "TRIP-ELEPHANT":
                    print("拌象脚！")
                    report()
                    return "RESELECT"
                self.check_black_captain(chessboard)

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                print("不是你的棋子")
                return "RESELECT"

        elif chessboard[(x, y)][1] == "officer":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                message = red_officer
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                self.check_black_captain(chessboard)

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                print("不是你的棋子")
                return "RESELECT"

        elif chessboard[(x, y)][1] == "captain":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                message = red_captain
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                self.check_black_captain(chessboard)

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                print("不是你的棋子")
                return "RESELECT"

        elif chessboard[(x, y)][1] == "cannon":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                message =red_cannon
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                self.check_black_captain(chessboard)

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                print("不是你的棋子")
                return "RESELECT"

        elif chessboard[(x, y)][1] == "soldier":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                message = red_soldier
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                self.check_black_captain(chessboard)

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                print("不是你的棋子")
                return "RESELECT"
        else:
            print("该位置没有棋子, 请重新选择")
            return "RESELECT"

    # AI 是黑方
    def ai_move(self, x, y, nx, ny):
        """判断坐标并调用 Chess类 的 对应函数"""
        black_car = self.chess.black_car(x, y, nx, ny)
        black_horse = self.chess.black_horse(x, y, nx, ny)
        black_elephant = self.chess.black_elephant(x, y, nx, ny)
        black_officer = self.chess.black_officer(x, y, nx, ny)
        black_captain = self.chess.black_cap(x, y, nx, ny)
        black_soldier = self.chess.black_soldier(x, y, nx, ny)
        black_cannon = self.chess.black_cannon(x, y, nx, ny)

        def report():
            print(f"红方: {self.red_score}分, 黑方: {self.black_score}分")

        # 判断棋子类型
        if chessboard[(x, y)][1] == "car":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                print("不是 AI 的棋子")
                return "RESELECT"

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                message = black_car
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                self.check_red_captain(chessboard)

        elif chessboard[(x, y)][1] == "horse":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                print("不是 AI 的棋子")
                return "RESELECT"

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                message = black_horse
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                elif message == "TRIP-HORSE":
                    print("拌马脚！")
                    report()
                    return "RESELECT"
                self.check_red_captain(chessboard)

        elif chessboard[(x, y)][1] == "elephant":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                print("不是 AI 的棋子")
                return "RESELECT"

                # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                message = black_elephant
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                elif message == "TRIP-ELEPHANT":
                    print("拌象脚！")
                    report()
                    return "RESELECT"
                self.check_red_captain(chessboard)

        elif chessboard[(x, y)][1] == "officer":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                print("不是 AI 的棋子")
                return "RESELECT"

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                message = black_officer
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                self.check_red_captain(chessboard)

        elif chessboard[(x, y)][1] == "captain":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                print("不是 AI 的棋子")
                return "RESELECT"

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                message = black_captain
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                self.check_red_captain(chessboard)

        elif chessboard[(x, y)][1] == "cannon":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                print("不是 AI 的棋子")
                return "RESELECT"

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                message = black_cannon
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
                self.check_red_captain(chessboard)

        elif chessboard[(x, y)][1] == "soldier":
            # 判断棋子颜色
            if chessboard[(x, y)][0]:
                print("不是 AI 的棋子")
                return "RESELECT"

            # 判断棋子颜色
            elif not chessboard[(x, y)][0]:
                message = black_soldier
                if message == "RESELECT":
                    print("重新选择棋子")
                    report()
                    return "RESELECT"
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    report()
                    return "CONTINUE"
                elif message == "MOVED":
                    print("移动成功！")
                    report()
                    return "CONTINUE"
        else:
            print("该位置没有棋子, 请重新选择")
            return "RESELECT"




class AI:
    def __init__(self):
        self.api_key = "7ba3acc0c43b48d6185c2ac248cf36c6.obqHJa9MQVQbHAH0"
        self.operate = Operate()

    def zhipuai(self):
        client = ZhipuAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=[
                {"role": "system",
                 "content": "你是一个象棋大师, 根据我跟你的棋局状况字典(以左上角的棋子为(0,0), True 是红棋, False 是黑棋), 给出下一步的走法(回答格式: x,y,nx,ny),x和y是原来棋子的坐标,nx和ny是新位置的坐标,不需要任何解释。"},
                {"role": "user",
                 "content": f"棋局状况(以左下角的棋子为(0,0), True 是红棋, False 是黑棋): {chessboard}, 给出下一步的走法(回答格式: x,y,nx,ny),其中x和y是原来棋子的坐标,nx和ny是新位置的坐标,不需要任何解释。"}
            ],
        )
        locations = response.choices[0].message.content.split(",")
        x, y, nx, ny = int(locations[0]), int(locations[1]), int(locations[2]), int(locations[3])

        self.operate.ai_move(x, y, nx, ny)

        print(f"AI选择的原坐标: {x},{y}, AI选择的新坐标: {nx},{ny}")
        print(chessboard)

        return x, y, nx, ny

    def ollama(self, model):
        res = ollama.chat(
            model=model, stream=False, messages=[
                {"role": "system",
                 "content": "你是一个象棋大师, 根据我跟你的棋局状况字典(以左上角的棋子为(0,0), True 是红棋, False 是黑棋), 给出下一步的走法(回答格式: x,y,nx,ny),x和y是原来棋子的坐标,nx和ny是新位置的坐标,不需要任何解释。"},
                {"role": "user",
                 "content": f"棋局状况(以左下角的棋子为(0,0), True 是红棋, False 是黑棋): {chessboard}, 给出下一步的走法(回答格式: x,y,nx,ny),其中x和y是原来棋子的坐标,nx和ny是新位置的坐标,不需要任何解释。"}
            ],
            options={"temperature": 0})
        locations = res["message"]["content"].split(",")
        x, y, nx, ny = int(locations[0]), int(locations[1]), int(locations[2]), int(locations[3])

        self.operate.user_move(x, y, nx, ny)

        print(f"AI选择的原坐标: {x},{y}, AI选择的新坐标: {nx},{ny}")
        print(chessboard)

        return x, y, nx, ny

