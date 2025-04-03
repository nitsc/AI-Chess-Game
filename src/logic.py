import sys

import ollama
from zhipuai import ZhipuAI

# 以 (0,0) 为左上角，黑方在上，红方在下的中国象棋初始布局
chessboard = {(0, 0):(False, "car"), (1, 0):(False, "horse"), (2, 0):(False, "elephant"), (3, 0):(False, "officer"), (4, 0):(False, "captain"), (5, 0):(False, "officer"), (6, 0):(False, "elephant"), (7, 0):(False, "horse"), (8, 0):(False, "car"),
              (0, 1): None, (1, 1): None, (2, 1): None, (3, 1): None, (4, 1): None, (5, 1): None, (6, 1): None, (7, 1): None, (8, 1): None,
              (0, 2): None, (1, 2): (False, "cannon"), (2, 2): None, (3, 2): None, (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): (False, "cannon"), (8, 2): None,
              (0, 3): (False, "soldier"), (1, 3): None, (2, 3): (False, "soldier"), (3, 3): None, (4, 3): (False, "soldier"), (5, 3): None, (6, 3): (False, "soldier"), (7, 3): None, (8, 3): (False, "soldier"),
              (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None, (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None, (8, 4): None,
              (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None, (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None, (8, 5): None,
              (0, 6): (True, "soldier"), (1, 6): None, (2, 6): (True, "soldier"), (3, 6): None, (4, 6): (True, "soldier"), (5, 6): None, (6, 6): (True, "soldier"), (7, 6): None, (8, 6): (True, "soldier"),
              (0, 7): None, (1, 7): (True, "cannon"), (2, 7): None, (3, 7): None, (4, 7): None, (5, 7): None, (6, 7): None, (7, 7): (True, "cannon"), (8, 7): None,
              (0, 8): None, (1, 8): None, (2, 8): None, (3, 8): None, (4, 8): None, (5, 8): None, (6, 8): None, (7, 8): None, (8, 8): None,
              (0, 9):(True, "car"), (1, 9):(True, "horse"), (2, 9):(True, "elephant"), (3, 9):(True, "officer"), (4, 9):(True, "captain"), (5, 9):(True, "officer"), (6, 9):(True, "elephant"), (7, 9):(True, "horse"), (8, 9):(True, "car")}

black_half = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
              (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
              (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2),
              (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
              (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4)]

red_half = [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5),
            (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6),
            (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7),
            (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]

red_score = 0
black_score = 0


class Chess:
    def __init__(self):
        pass

    @staticmethod
    def check_general_face_to_face(nx):
        """检查将/帅是否面对面"""
        red_pos = None
        black_pos = None
        for i in range(10):  # 遍历所有行，确定两个将的位置
            if (nx, i) in chessboard and chessboard[(nx, i)] == (True, "captain"):
                red_pos = i
            if (nx, i) in chessboard and chessboard[(nx, i)] == (False, "captain"):
                black_pos = i
        if red_pos is not None and black_pos is not None:
            # 检查两者之间是否有棋子阻挡
            for i in range(red_pos + 1, black_pos):
                if (nx, i) in chessboard and chessboard[(nx, i)] is not None:
                    return False  # 有阻挡，合法
            return True  # 无阻挡，违规
        return False  # 没有形成对脸
    
    @staticmethod
    def red_soldier(x, y, nx, ny):
        """红方士兵规则"""
        def red_soldier_core(x, y, nx, ny):
            """红方士兵规则, 吃黑棋"""
            global red_score
            # 如果新位置是黑棋
            if not chessboard[(nx, ny)][0]:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,ny) 的键值对改为 (True,"soldier") 
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (True,"soldier")
                # 给红方加分
                red_score += 1
                return "CAP-BLACK"
            # 如果新位置是红棋
            elif chessboard[(nx, ny)][0]:
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()

        # 检查是否在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9 ):
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查在哪一方区域
            if (x, y) in red_half:
                # 检查是否在合法的移动范围内
                if (nx, ny) == (x, y - 1):
                    target = chessboard[(nx, ny)]
                    
                    # 检查新位置是空格
                    if target is None:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,ny) 的键值对改为 (True,"soldier") 
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (True,"soldier")
                        return "MOVED"
                    else:
                        return red_soldier_core(x, y, nx, ny)
                else:
                    print("不能走那么多")
                    return "RESELECT"
            elif (x, y) in black_half:
                # 检查是否在合法范围内
                if (nx, ny) == (x, y - 1) or (nx, ny) == (x + 1, y) or (nx, ny) == (x - 1, y):
                    target = chessboard[(nx, ny)]

                    # 检查新位置是空格
                    if target is None:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,ny) 的键值对改为 (True,"soldier") 
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (True,"soldier")
                        return "MOVED"
                    else:
                        return red_soldier_core(x, y, nx, ny)
            else:
                print("意想不到的事情发生了")
                sys.exit()

    @staticmethod
    def black_soldier(x, y, nx, ny):
        """黑方士兵规则"""
        def black_soldier_core(x, y, nx, ny):
            """黑方士兵规则, 吃红棋"""
            # 如果新位置是红棋
            if chessboard[(nx, ny)][0]:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,ny) 的键值对改为 (False,"soldier") 
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (False, "soldier")
                # 给黑方加分
                global black_score
                black_score += 1
                return "CAP-RED"
            # 如果新位置是黑棋
            elif not chessboard[(nx, ny)][0]:
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()

        # 检查是否在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9 ):
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查在哪一方区域
            if (x, y) in black_half:
                # 检查是否在合法的移动范围内
                if (nx, ny) == (x, y + 1):
                    target = chessboard[(nx, ny)]

                    # 检查新位置是空格
                    if target is None:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,ny) 的键值对改为 (False,"soldier")
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (False, "soldier")
                        return "MOVED"
                    else:
                        return black_soldier_core(x, y, nx, ny)
                else:
                    print("不能走那么多")
                    return "RESELECT"
            elif (x, y) in red_half:
                # 检查是否在合法范围内
                if  (nx, ny) == (x, y + 1) or (nx, ny) == (x + 1, y) or (nx, ny) == (x - 1, y):
                    target = chessboard[(nx, ny)]

                    # 检查新位置是空格
                    if target is None:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,ny) 的键值对改为 (False,"soldier")
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (False, "soldier")
                        return "MOVED"
                    else:
                        return black_soldier_core(x, y, nx, ny)
            else:
                print("意想不到的事情发生了")
                sys.exit()

    @staticmethod
    def red_cannon(x, y, nx, ny):
        """红炮移动规则"""
        def red_cannon_count0(x, y, nx, ny):
            """'红炮移动规则,没有炮架"""
            target = chessboard[(nx, ny)]
            # 如果新位置是空的
            if target is None:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,ny) 的键值对改为 (True,"cannon")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (True, "cannon")
                return "MOVED"
            # 如果新位置是黑棋
            elif target[0] is False:
                # 不移动棋子
                print("没有棋子充当炮架")
                return "RESELECT"
            # 如果新位置是红棋
            elif target[0] is True:
                # 不移动棋子
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()

        def red_cannon_count1(x, y, nx, ny):
            """"红炮移动规则,有炮架"""
            global red_score
            target = chessboard[(nx, ny)]
            # 如果新位置是空的
            if target is None:
                print("有棋子阻挡")
                return "RESELECT"
            # 如果新位置是黑棋
            elif target[0] is False:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,ny) 的键值对改为 (True,"cannon")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (True, "cannon")
                red_score += 1
                return "CAP-BLACK"
            # 如果新位置是红棋
            elif target[0] is True:
                # 不移动棋子
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()

        # 检查不在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9 ):
            print("不在棋盘上")
            return "RESELECT"
        # 检查在棋盘上
        else:
            # 检查是垂直移动
            if x == nx and y != ny:
                # 列举 y 和 ny 之间的所有位置
                min_y, max_y = min(y, ny), max(y, ny)
                count = 0

                # 检查是否有棋子挡路
                for current_y in range(min_y + 1, max_y):
                    if chessboard[(x, current_y)] is not None:
                        count += 1

                # 如果中间没有棋子
                if count == 0:
                    return red_cannon_count0(x, y, nx, ny)

                # 如果中间有1个棋子
                elif count == 1:
                    return red_cannon_count1(x, y, nx, ny)

                # 如果中间有大于1个棋子
                elif count > 1:
                    print("中间有多个棋子阻挡")
                    return "RESELECT"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()

            # 如果是水平移动
            if x != nx and y == ny:
                # 列举 x 和 nx 之间的所有位置
                min_x, max_x = min(x, nx), max(x, nx)
                count = 0

                #检查是否有棋子挡路
                for current_x in range(min_x + 1, max_x):
                    if chessboard[(current_x, y)] is not None:
                        count += 1

                # 如果中间没棋子
                if count == 0:
                    return red_cannon_count0(x, y, nx, ny)

                    # 如果中间只有一个棋子
                elif count == 1:
                        return red_cannon_count1(x, y, nx, ny)

                # 如果中间有大于1个棋子
                elif count > 1:
                    print("中间有多个棋子阻挡")
                    return "RESELECT"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                print("要水平或垂直移动")
                return "RESELECT"


    @staticmethod
    def black_cannon(x, y, nx, ny):
        """黑炮移动规则"""
        def black_cannon_count0(x, y, nx, ny):
            """黑袍移动规则, 没有炮架"""
            target = chessboard[(nx, ny)]
            # 如果新位置是空的
            if target is None:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,ny) 的键值对改为 (False,"cannon")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (False, "cannon")
                return "MOVED"
            # 如果新位置是红棋
            elif target[0] is True:
                # 不移动棋子
                print("没有棋子充当炮架")
                return "RESELECT"
            # 如果新位置是黑棋
            elif target[0] is False:
                # 不移动棋子
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()

        def black_cannon_count1(x, y, nx, ny):
            """黑袍移动规则，有炮架"""
            global black_score
            target = chessboard[(nx, ny)]
            # 如果新位置是空的
            if target is None:
                print("有棋子阻挡")
                return "RESELECT"
            # 如果新位置是红棋
            elif target[0] is True:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,ny) 的键值对改为 (False,"cannon")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (False, "cannon")
                black_score += 1
                return "CAP-BLACK"
            # 如果新位置是黑棋
            elif target[0] is False:
                # 不移动棋子
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()

        # 检查不在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9 ):
            print("不在棋盘上")
            return "RESELECT"

        # 检查在棋盘上
        else:
            # 检查是垂直移动
            if x == nx and y != ny:
                # 列举 y 和 ny 之间的所有位置
                min_y, max_y = min(y, ny), max(y, ny)
                count = 0

                # 检查是否有棋子挡路
                for current_y in range(min_y + 1, max_y):
                    if chessboard[(x, current_y)] is not None:
                        count += 1

                # 如果中间没有棋子
                if count == 0:
                    return black_cannon_count0(x, y, nx, ny)

                # 如果中间只有一个棋子
                elif count == 1:
                    return black_cannon_count1(x, y, nx, ny)

                # 如果中间有大于1个棋子
                elif count > 1:
                    print("中间有多个棋子阻挡")
                    return "RESELECT"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()

            # 如果是水平移动
            if x != nx and y == ny:
                # 列举 x 和 nx 之间的所有位置
                min_x, max_x = min(x, nx), max(x, nx)
                count = 0

                # 检查是否有棋子挡路
                for current_x in range(min_x + 1, max_x):
                    if chessboard[(current_x, y)] is not None:
                        count += 1

                # 如果中间没有棋子
                if count == 0:
                    return black_cannon_count0(x, y, nx, ny)

                # 如果中间只有一个棋子
                elif count == 1:
                    return black_cannon_count1(x, y, nx, ny)

                # 如果中间有大于1个棋子
                elif count > 1:
                    print("中间有多个棋子阻挡")
                    return "RESELECT"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                print("要水平或垂直移动")
                return "RESELECT"

    @staticmethod
    def red_car(x, y, nx, ny):
        """红车移动规则"""
        def red_car_core(x, y, nx, ny):
            """红车移动规则, 吃黑棋"""
            global red_score
            target = chessboard[(nx, ny)]
            # 如果新位置是空的
            if target is None:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (x,ny) 的键值对改为 (True,"car")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (True, "car")
                return "MOVED"
            else:
                if target[0] is False:
                    # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (x,ny) 的键值对改为 (True,"car")
                    chessboard[(x, y)] = None
                    chessboard[(nx, ny)] = (True, "car")
                    red_score += 1
                    return "CAP-BLACK"
                # 如果目标位置有红棋
                elif target[0] is True:
                    print("不能吃自己的棋子")
                    return "RESELECT"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()

        # 检查是否在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9 ):
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查是否垂直移动
            if x == nx and y != ny:
                # 列举 y 和 ny 之间的所有位置
                min_y, max_y = min(y, ny), max(y, ny)
                count = 0

                # 检查是否有棋子挡路
                for current_y in range(min_y + 1, max_y):
                    if chessboard[(x, current_y)] is not None:
                        count += 1

                # 如果中间没棋子
                if count == 0:
                    return red_car_core(x, y, nx, ny)

                # 如果中间有棋子
                elif count != 1:
                    print("有棋子阻挡")
                    return "RESELECT"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否水平移动
            elif x != nx and y == ny:
                # 列举 x 和 nx 之间的所有位置
                min_x, max_x = min(x, nx), max(x, nx)
                count = 0

                # 检查是否有棋子挡路
                for current_x in range(min_x+ 1, max_x):
                    if chessboard[(current_x, y)] is not None:
                        count += 1

                # 如果中间没棋子
                if count == 0:
                    return red_car_core(x, y, nx, ny)

                # 如果中间有棋子
                elif count != 1:
                    print("有棋子阻挡")
                    return "RESELECT"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                print("要水平或垂直移动")
                return "RESELECT"

    @staticmethod
    def black_car(x, y, nx, ny):
        """黑车移动规则"""
        def black_car_core(x, y, nx ,ny):
            global black_score
            target = chessboard[(nx, ny)]
            if target is None:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (x,ny) 的键值对改为 (False,"car")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (False, "car")
                return "MOVED"
            # 如果目标位置有红棋
            if target[0] is True:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (x,ny) 的键值对改为 (False,"car")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (False, "car")
                black_score += 1
                return "CAP-RED"
            # 如果目标位置有黑棋
            elif target[0] is None:
                print("不能吃自己的棋子")
                return "RESELECT"

        # 检查是否在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9 ):
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查是否垂直移动
            if x == nx and y != ny:
                # 列举 y 和 ny 之间的所有位置
                min_y, max_y = min(y, ny), max(y, ny)
                count = 0

                # 检查是否有棋子挡路
                for current_y in range(min_y + 1, max_y):
                    if chessboard[(x, current_y)] is not None:
                        count += 1

                # 如果中间没棋子
                if count == 0:
                    return black_car_core(x, y, nx, ny)

                # 如果中间有棋子
                elif count != 0:
                    print("有棋子阻挡")
                    return "RESELECT"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否水平移动
            elif x != nx and y == ny:
                # 列举 x 和 nx 之间的所有位置
                min_x, max_x = min(x, nx), max(x, nx)
                count = 0

                # 检查是否有棋子挡路
                for current_x in range(min_x + 1, max_x):
                    if chessboard[(current_x, y)] is not None:
                        count += 1

                # 如果中间没棋子
                if count == 0:
                    return black_car_core(x, y, nx, ny)

                # 如果中间有棋子
                elif count != 0:
                    print("有棋子阻挡")
                    return "RESELECT"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                print("要水平或垂直移动")
                return "RESELECT"

    @staticmethod
    def red_horse(x, y, nx, ny):
        """红马移动规则"""
        def red_horse_core(x, y, nx, ny):
            global red_score
            target = chessboard[(nx, ny)]
            # 如果新位置是空的
            if target is None:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (True,"horse")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (True, "horse")
                return "MOVED"
            # 如果目标位置有黑棋
            elif target[0] is False:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (True,"horse")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (True, "horse")
                red_score += 1
                return "CAP-BLACK"
            # 如果目标位置有红棋
            elif target[0] is True:
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()

        # 检查是否在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9 ):
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查是否走“日”字 (1)
            if nx == x - 2 and ny == y + 1:
                # 检查没有拌马脚
                if chessboard[(x - 1, y)] is None:
                    return red_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (2)
            elif nx == x - 1 and ny == y + 2:
                # 检查没有拌马脚
                if chessboard[(x - 1, y + 1)] is None:
                    return red_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y + 1)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (3)
            elif nx == x + 2 and ny == y + 1:
                # 检查没有拌马脚
                if chessboard[(x + 1, y)] is None:
                    return red_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (4)
            elif nx == x + 1 and ny == y + 2:
                # 检查没有拌马脚
                if chessboard[(x + 1, y + 1)] is None:
                    return red_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y + 1)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (5)
            elif nx == x - 2 and ny == y - 1:
                # 检查没有拌马脚
                if chessboard[(x - 1, y)] is None:
                    return red_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (6)
            elif nx == x - 1 and ny == y - 2:
                # 检查没有拌马脚
                if chessboard[(x - 1, y - 1)] is None:
                    return red_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y - 1)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (7)
            elif nx == x + 2 and ny == y - 1:
                # 检查没有拌马脚
                if chessboard[(x + 1, y)] is None:
                    return red_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (8)
            elif nx == x + 1 and ny == y - 2:
                # 检查没有拌马脚
                if chessboard[(x + 1, y - 1)] is None:
                    return red_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y - 1)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                print("走法不正确")
                return "RESELECT"


    @staticmethod
    def black_horse(x, y, nx, ny):
        """黑马移动规则"""
        def black_horse_core(x, y, nx, ny):
            global black_score
            target = chessboard[(nx, ny)]
            # 如果新位置是空的
            if target is None:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (False,"horse")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (False, "horse")
                return "MOVED"
            # 如果目标位置有红棋
            elif target[0] is True:
                # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (False,"horse")
                chessboard[(x, y)] = None
                chessboard[(nx, ny)] = (False, "horse")
                black_score += 1
                return "CAP-RED"
            # 如果目标位置有黑棋
            elif target[0] is False:
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()

        # 检查是否在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9 ):
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查是否走“日”字 (1)
            if nx == x - 2 and ny == y + 1:
                # 检查没有拌马脚
                if chessboard[(x - 1, y)] is None:
                    return black_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (2)
            elif nx == x - 1 and ny == y + 2:
                # 检查没有拌马脚
                if chessboard[(x - 1, y + 1)] is None:
                    return black_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y + 1)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (3)
            elif nx == x + 2 and ny == y + 1:
                # 检查没有拌马脚
                if chessboard[(x + 1, y)] is None:
                    return black_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (4)
            elif nx == x + 1 and ny == y + 2:
                # 检查没有拌马脚
                if chessboard[(x + 1, y + 1)] is None:
                    return black_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y + 1)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (5)
            elif nx == x - 2 and ny == y - 1:
                # 检查没有拌马脚
                if chessboard[(x - 1, y)] is None:
                    return black_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (6)
            elif nx == x - 1 and ny == y - 2:
                # 检查没有拌马脚
                if chessboard[(x - 1, y - 1)] is None:
                    return black_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x - 1, y - 1)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (7)
            elif nx == x + 2 and ny == y - 1:
                # 检查没有拌马脚
                if chessboard[(x + 1, y)] is None:
                    return black_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字 (8)
            elif nx == x + 1 and ny == y - 2:
                # 检查没有拌马脚
                if chessboard[(x + 1, y - 1)] is None:
                    return black_horse_core(x, y, nx, ny)
                # 检查拌马脚
                elif chessboard[(x + 1, y - 1)] is not None:
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                print("走法不正确")
                return "RESELECT"

    @staticmethod
    def red_officer(x, y, nx, ny):
        """红士移动规则"""
        global red_score
        # 检查是否在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 ):
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查是否在九宫格内
            if not ( nx in {3, 4, 5} ) and not ( ny in {7, 8, 9} ):
                print("不在九宫格内")
                return "RESELECT"
            else:
                # 检查是否走斜线
                if not ( (nx == x + 1 and ny == y + 1) or (nx == x + 1 and ny == y - 1) or (nx == x - 1 and ny == y + 1) or (
                        nx == x - 1 and ny == y - 1) ):
                    print("走法不正确")
                    return "RESELECT"
                else:
                    target = chessboard[(nx, ny)]
                    # 如果新位置是空的
                    if target is None:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (True,"officer")
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (True, "officer")
                        return "MOVED"
                    # 如果新位置的棋子是黑棋
                    if target[0] is False:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (True,"officer")
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (True, "officer")
                        red_score += 1
                        return "CAP-BLACK"
                    # 如果新位置的棋子是红棋
                    elif target[0] is True:
                        print("不能吃自己的棋子")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()

    @staticmethod
    def black_officer(x, y, nx, ny):
        """黑士移动规则"""
        global black_score
        # 检查是否在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 ):
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查是否在九宫格内
            if not ( nx in {3, 4, 5} ) and not ( ny in {0, 1, 2} ):
                print("不在九宫格内")
                return "RESELECT"
            else:
                # 检查是否走斜线
                if not ( (nx == x + 1 and ny == y + 1) or (nx == x + 1 and ny == y - 1) or (nx == x - 1 and ny == y + 1) or (
                        nx == x - 1 and ny == y - 1) ):
                    print("走法不正确")
                    return "RESELECT"
                else:
                    target = chessboard[(nx, ny)]
                    # 如果新位置是空的
                    if target is None:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (False,"officer")
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (False, "officer")
                        return "MOVED"
                    # 如果新位置的棋子是红棋
                    if target[0] is True:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (False,"officer")
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (False, "officer")
                        black_score += 1
                        return "CAP-RED"
                    # 如果新位置的棋子是黑棋
                    elif target[0] is False:
                        print("不能吃自己的棋子")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()

    @staticmethod
    def red_elephant(x, y, nx, ny):
        """红象移动规则"""
        global red_score
        # 检查是否在棋盘上
        if not ( 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9 ):
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查是否走田字
            if abs(nx - x) != 2 and abs(ny - y) != 2:
                print("走法不正确")
                return "RESELECT"
            else:
                # 检查是否过河
                if not (nx, ny) in red_half:
                    print("过河了")
                    return "RESELECT"
                else:
                    # 检查是否被蹩象脚
                    mx, my = (x + nx) // 2, (y + ny) // 2
                    if (mx, my) in chessboard and chessboard[(mx, my)] is not None:
                        print("被蹩象脚")
                        return "TRIP-ELEPHANT"
                    else:
                        target = chessboard[(nx, ny)]
                        # 如果新位置是空的
                        if target is None:
                            # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (True,"elephant")
                            chessboard[(x, y)] = None
                            chessboard[(nx, ny)] = (True, "elephant")
                            return "MOVED"
                        # 如果新位置的棋子是红棋
                        if target[0] is True:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        # 如果新位置的棋子是黑棋
                        elif target[0] is False:
                            # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (True,"elephant")
                            chessboard[(x, y)] = None
                            chessboard[(nx, ny)] = (True, "elephant")
                            red_score += 1
                            return "CAP-BLACK"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()


    @staticmethod
    def black_elephant(x, y, nx, ny):
        """黑象移动规则"""
        global red_score
        # 检查是否在棋盘上
        if not 0 <= x <= 9 and 0 <= y <= 9 and 0 <= nx <= 9 and 0 <= ny <= 9:
            print("不在棋盘上")
            return "RESELECT"
        else:
            # 检查是否走田字
            if abs(nx - x) != 2 and abs(ny - y) != 2:
                print("走法不正确")
                return "RESELECT"
            else:
                # 检查是否过河
                if not (nx, ny) in black_half:
                    print("过河了")
                    return "NO-CROSS"
                else:
                    # 检查是否被蹩象脚
                    mx, my = (x + nx) // 2, (y + ny) // 2
                    if (mx, my) in chessboard and chessboard[(mx, my)] is not None:
                        print("被蹩象脚")
                        return "TRIP-ELEPHANT"
                    else:
                        target = chessboard[(nx, ny)]
                        # 如果新位置是空的
                        if target is None:
                            # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (False,"elephant")
                            chessboard[(x, y)] = None
                            chessboard[(nx, ny)] = (False, "elephant")
                            return "MOVED"
                        # 如果新位置的棋子是黑棋
                        if target[0] is False:
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        # 如果新位置的棋子是红棋
                        elif target[0] is True:
                            # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (False,"elephant")
                            chessboard[(x, y)] = None
                            chessboard[(nx, ny)] = (False, "elephant")
                            red_score += 1
                            return "CAP-RED"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()


    def red_cap(self, x, y, nx, ny):
        """红将移动规则"""
        global red_score
        # 检查是否在九宫格内
        if not (nx in [3, 4, 5] and ny in [7, 8, 9]):
            print("不在九宫格内")
            return "RESELECT"
        else:
            if self.check_general_face_to_face(nx):
                print("老将对脸，走法不合法")
                return "RESELECT"
            else:
                # 检查是否走直线
                if (nx == x + 1 and ny == y) or (nx == x - 1 and ny == y) or (nx == x and ny == y + 1) or (nx == x and ny == y - 1):
                    target = chessboard[(nx, ny)]
                    # 如果新位置是空的
                    if target is None:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (True,"captain")
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (True, "captain")
                        return "MOVED"
                    # 如果新位置的棋子是黑棋
                    if target[0] is False:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (True,"captain")
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (True, "captain")
                        red_score += 1
                        return "CAP-BLACK"
                     # 如果新位置的棋子是红棋
                    elif target[0] is True:
                        print("不能吃自己的棋子")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
                else:
                    print("走法不正确")
                    return "RESELECT"


    def black_cap(self, x, y, nx, ny):
        """黑将移动规则"""
        global black_score
        # 检查是否在九宫格内
        if not ( nx in [3, 4, 5] and ny in [0, 1, 2]):
            print("不在九宫格内")
            return "RESELECT"
        else:
            if self.check_general_face_to_face(nx):
                print("老将对脸，走法不合法")
                return "RESELECT"
            else:
                # 检查是否走直线
                if (nx == x + 1 and ny == y) or (nx == x - 1 and ny == y) or (nx == x and ny == y + 1) or (nx == x and ny == y - 1):
                    target = chessboard[(nx, ny)]
                    # 如果新位置是空的
                    if target is None:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (False,"captain")
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (False, "captain")
                        return "MOVED"
                    # 如果新位置的棋子是红棋
                    if target[0] is True:
                        # 修改chessboard词典 上的值, 把 (x,y) 的键值对改为 None ,  把 (nx,y) 的键值对改为 (False,"captain")
                        chessboard[(x, y)] = None
                        chessboard[(nx, ny)] = (False, "captain")
                        black_score += 1
                        return "CAP-RED"
                    # 如果新位置的棋子是黑棋
                    elif target[0] is False:
                        print("不能吃自己的棋子")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()



class Operate:
    def __init__(self):
        self.chess = Chess()

    @staticmethod
    def check_red_captain(chessboard):
        """检查红方是否还有将"""
        for pos, (is_red, piece) in chessboard.items():
            if piece == "captain" and is_red:
                return True  # 红方的将还在
        print("红方将领被吃掉！你失败了！再接再厉！")
        return False  # 红方的将已经被吃掉

    @staticmethod
    def check_black_captain(chessboard):
        """检查黑方是否还有将"""
        for pos, (is_red, piece) in chessboard.items():
            if piece == "captain" and not is_red:
                return True  # 黑方的将还在
        print("黑方将领被吃掉！恭喜你胜利了！")
        return False  # 黑方的将已经被吃掉

    # 红方
    def user_move(self, x, y, nx, ny):
        """判断坐标并调用 Chess类 的 对应函数"""
        def report():
            print(f"红方: {red_score}分, 黑方: {black_score}分")

        def check():
            succeed = self.check_black_captain(chessboard)
            if succeed is False:
                return "RED-WIN"
            else:
                return "CONTINUE"

        # 判断棋子类型
        if chessboard[(x, y)] is None:
            print("该位置没有棋子")
        else:
            if chessboard[(x, y)][1] == "car":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    red_car = self.chess.red_car(x, y, nx, ny)
                    message = red_car
                    if message == "RESELECT":
                        print("重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-BLACK":
                        print("红方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("移动成功！")
                        report()
                        return "CONTINUE"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    print("不是你的棋子")
                    return "RESELECT"

            elif chessboard[(x, y)][1] == "horse":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    red_horse = self.chess.red_horse(x, y, nx, ny)
                    message = red_horse
                    if message == "RESELECT":
                        print("重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-BLACK":
                        print("红方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("移动成功！")
                        report()
                        return "CONTINUE"
                    elif message == "TRIP-HORSE":
                        print("拌马脚！")
                        report()
                        return "RESELECT"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    print("不是你的棋子")
                    return "RESELECT"

            elif chessboard[(x, y)][1] == "elephant":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    red_elephant = self.chess.red_elephant(x, y, nx, ny)
                    message = red_elephant
                    if message == "RESELECT":
                        print("重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-BLACK":
                        print("红方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("移动成功！")
                        report()
                        return "CONTINUE"
                    elif message == "TRIP-ELEPHANT":
                        print("拌象脚！")
                        report()
                        return "RESELECT"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    print("不是你的棋子")
                    return "RESELECT"

            elif chessboard[(x, y)][1] == "officer":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    red_officer = self.chess.red_officer(x, y, nx, ny)
                    message = red_officer
                    if message == "RESELECT":
                        print("重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-BLACK":
                        print("红方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("移动成功！")
                        report()
                        return "CONTINUE"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    print("不是你的棋子")
                    return "RESELECT"

            elif chessboard[(x, y)][1] == "captain":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    red_captain = self.chess.red_cap(x, y, nx, ny)
                    message = red_captain
                    if message == "RESELECT":
                        print("重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-BLACK":
                        print("红方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("移动成功！")
                        report()

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    print("不是你的棋子")
                    return "RESELECT"

            elif chessboard[(x, y)][1] == "cannon":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    red_cannon = self.chess.red_cannon(x, y, nx, ny)
                    message =red_cannon
                    if message == "RESELECT":
                        print("重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-BLACK":
                        print("红方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("移动成功！")
                        report()
                        return "CONTINUE"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    print("不是你的棋子")
                    return "RESELECT"

            elif chessboard[(x, y)][1] == "soldier":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    red_soldier = self.chess.red_soldier(x, y, nx, ny)
                    message = red_soldier
                    if message == "RESELECT":
                        print("重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-BLACK":
                        print("红方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("移动成功！")
                        report()
                        return "CONTINUE"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    print("不是你的棋子")
                    return "RESELECT"

    # AI 是黑方
    def ai_move(self, x, y, nx, ny):
        """判断坐标并调用 Chess类 的 对应函数"""
        def report():
            print(f"红方: {red_score}分, 黑方: {black_score}分")

        def check():
            succeed = self.check_red_captain(chessboard)
            if succeed is False:
                return "BLACK-WIN"
            else:
                return "CONTINUE"

        # 判断棋子类型
        if chessboard[(x, y)] is None:
            print("该位置没有棋子")
        else:
            if chessboard[(x, y)][1] == "car":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    print("不是 AI 的棋子")
                    return "RESELECT"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    black_car = self.chess.black_car(x, y, nx, ny)
                    message = black_car
                    if message == "RESELECT":
                        print("AI 重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-RED":
                        print("AI 黑方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("AI 移动成功！")
                        report()
                        return "CONTINUE"

            elif chessboard[(x, y)][1] == "horse":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    print("不是 AI 的棋子")
                    return "RESELECT"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    black_horse = self.chess.black_horse(x, y, nx, ny)
                    message = black_horse
                    if message == "RESELECT":
                        print("AI 重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-RED":
                        print("AI 黑方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("AI 移动成功！")
                        report()
                        return "CONTINUE"
                    elif message == "TRIP-HORSE":
                        print("AI 拌马脚！")
                        report()
                        return "RESELECT"

            elif chessboard[(x, y)][1] == "elephant":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    print("不是 AI 的棋子")
                    return "RESELECT"

                    # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    black_elephant = self.chess.black_elephant(x, y, nx, ny)
                    message = black_elephant
                    if message == "RESELECT":
                        print("AI 重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-RED":
                        print("AI 黑方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("AI 移动成功！")
                        report()
                        return "CONTINUE"
                    elif message == "TRIP-ELEPHANT":
                        print("AI 拌象脚！")
                        report()
                        return "RESELECT"

            elif chessboard[(x, y)][1] == "officer":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    print("不是 AI 的棋子")
                    return "RESELECT"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    black_officer = self.chess.black_officer(x, y, nx, ny)
                    message = black_officer
                    if message == "RESELECT":
                        print("AI 重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-RED":
                        print("AI 黑方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("AI 移动成功！")
                        report()
                        return "CONTINUE"

            elif chessboard[(x, y)][1] == "captain":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    print("不是 AI 的棋子")
                    return "RESELECT"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    black_captain = self.chess.black_cap(x, y, nx, ny)
                    message = black_captain
                    if message == "RESELECT":
                        print("AI 重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-RED":
                        print("AI 黑方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("AI 移动成功！")
                        report()
                        return "CONTINUE"

            elif chessboard[(x, y)][1] == "cannon":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    print("不是 AI 的棋子")
                    return "RESELECT"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    black_cannon = self.chess.black_cannon(x, y, nx, ny)
                    message = black_cannon
                    if message == "RESELECT":
                        print("AI 重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-RED":
                        print("AI 黑方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("AI 移动成功！")
                        report()
                        return "CONTINUE"

            elif chessboard[(x, y)][1] == "soldier":
                # 判断棋子颜色
                if chessboard[(x, y)][0]:
                    print("不是 AI 的棋子")
                    return "RESELECT"

                # 判断棋子颜色
                elif not chessboard[(x, y)][0]:
                    black_soldier = self.chess.black_soldier(x, y, nx, ny)
                    message = black_soldier
                    if message == "RESELECT":
                        print("AI 重新选择棋子")
                        report()
                        return "RESELECT"
                    elif message == "CAP-RED":
                        print("AI 黑方加一分！")
                        report()
                        check()
                    elif message == "MOVED":
                        print("AI 移动成功！")
                        report()
                        return "CONTINUE"
            else:
                print("该位置没有棋子, 请重新选择")
                return "RESELECT"
            
            
            
class AI:
    def __init__(self):
        self.api_key = "hidden"
        self.operate = Operate()

    def zhipuai(self):
        client = ZhipuAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=[
                {"role": "system",
                 "content": "你是一个象棋手, 根据我跟你的棋局状况字典(True 是红棋, False 是黑棋), 给出下一步的走法(你是黑方; 回答格式: x,y,nx,ny),x和y是原来棋子的坐标,nx和ny是新位置的坐标,不需要任何解释. "},
                {"role": "user",
                 "content": f"棋局状况(True 是红棋, False 是黑棋): {chessboard}, 给出下一步的走法(回答格式: x,y,nx,ny),其中x和y是原来棋子的坐标,nx和ny是新位置的坐标,注意规则,不需要任何解释. "}
            ],
        )
        locations = response.choices[0].message.content.split(",")
        x, y, nx, ny = int(locations[0]), int(locations[1]), int(locations[2]), int(locations[3])

        self.operate.ai_move(x, y, nx, ny)

        return x, y, nx, ny

    def deepseek(self):
        res = ollama.chat(
            model="deepseek-r1:14bb", stream=False, messages=[
                {"role": "system",
                 "content": "你是一个象棋手, 根据我给你的棋局状况字典(True 是红棋, False 是黑棋), 给出下一步的走法(你是黑方; 回答格式: x,y,nx,ny),x和y是原来棋子的坐标,nx和ny是新位置的坐标,不需要任何解释. "},
                {"role": "user",
                 "content": f"棋局状况(True 是红棋, False 是黑棋): {chessboard}, 给出下一步的走法(回答格式: x,y,nx,ny),其中x和y是原来棋子的坐标,nx和ny是新位置的坐标,注意规则,不需要任何解释. "}
            ],
            options={"temperature": 0})
        locations = res["message"]["content"].split(",")
        x, y, nx, ny = int(locations[0]), int(locations[1]), int(locations[2]), int(locations[3])

        self.operate.user_move(x, y, nx, ny)

        return x, y, nx, ny
