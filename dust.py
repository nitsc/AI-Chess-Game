import sys
import ollama
from zhipuai import ZhipuAI
from matplotlib import patches
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import matplotlib.animation as animation



# 棋盘布局, 以左下角的棋子为(0,0), True 是红棋, False 是黑棋
chessboard = {(0,0):(True, "car"),(0,1):(True,"horse"),(0,2):(True,"elephant"),
            (0,3):(True,"officer"),(0,4):(True,"captain"),(0,5):(True,"officer"),
            (0,6):(True,"elephant"),(0,7):(True,"horse"),(0,8):(True,"car"),
            (1,0):"none",(1,1):"none",(1,2):"none",(1,3):"none",(1,4):"none",
            (1,5):"none",(1,6):"none",(1,7):"none",(1,8):"none",
            (2,0):"none",(2,1):(True,"cannon"),(2,2):"none",(2,3):"none",
            (2,4):"none",(2,5):"none",(2,6):"none",(2,7):(True,"cannon"),(2,8):"none",
            (3,0):(True,"soldier"),(3,1):"none",(3,2):(True,"soldier"),(3,3):"none",
            (3,4):(True,"soldier"),(3,5):"none",(3,6):(True,"soldier"),(3,7):"none",(3,8):(True,"soldier"),
            (4,0):"none",(4,1):"none",(4,2):"none",(4,3):"none",(4,4):"none",(4,5):"none",(4,6):"none",(4,7):"none",(4,8):"none",
            (5,0):"none",(5,1):"none",(5,2):"none",(5,3):"none",(5,4):"none",(5,5):"none",(5,6):"none",(5,7):"none",(5,8):"none",
            (6,0):(False,"soldier"),(6,1):"none",(6,2):(False,"soldier"),(6,3):"none",
            (6,4):(False,"soldier"),(6,5):"none",(6,6):(False,"soldier"),(6,7):"none",(6,8):(False,"soldier"),
            (7,0):"none",(7,1):(False,"cannon"),(7,2):"none",(7,3):"none",
            (7,4):"none",(7,5):"none",(7,6):"none",(7,7):(False,"cannon"),(7,8):"none",
            (8,0):"none",(8,1):"none",(8,2):"none",(8,3):"none",(8,4):"none",(8,5):"none",(8,6):"none",(8,7):"none",(8,8):"none",
            (9,0):(False,"car"),(9,1):(False,"horse"),(9,2):(False,"elephant"),(9,3):(False,"officer"),(9,4):(False,"captain"),
            (9,5):(False,"officer"),(9,6):(False,"elephant"),(9,7):(False,"horse"),(9,8):(False,"car")}

# 输入红方的区域坐标
redhalf=[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),
        (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),
        (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),
        (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),
        (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),
        (5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),]

# 输入黑的区域坐标    
blackhalf=[(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),
        (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),
        (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),
        (8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),
        (9,0),(9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),]

# 红方分数
global redscores
redscores=0

# 黑方分数
global blackscores
blackscores=0

# 拾取情况
select = False

# 颜色映射
color_map = {
    True: "red",  # 红色
    False: "black",  # 黑色
}

# 文字映射
piece_name_map = {
    "car": "车", "horse": "马", "elephant": "象", "officer": "士", "captain": "将",
    "soldier": "兵", "cannon": "炮", "none": "空"
}

global first_click
first_click = None



class Chess:
    def __init__(self):
        global select
        global redscores
        global blackscores
        select = False


    def redsoldier(x,y,nx,ny):
        '''制定红方士兵的规则'''

        # 检查是否在棋盘上
        if x >= 0 and x <= 9 and y >= 0 and y <= 9 and nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9:
            # 检查在哪一方区域
            if (x,y) in redhalf:
                # 检查是否在合法的移动范围内
                if (nx,ny) == (x+1,y):
                    # 检查新位置没有棋子
                    if chessboard[(nx,ny)] == "none":
                        # 移动棋子
                        select = False
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"soldier"）
                        chessboard[(x,y)] = "none"
                        chessboard[(nx,ny)] = (True,"soldier")
                        return "MOVED"
                    else:
                        # 如果新位置是黑棋
                        if chessboard[(nx,ny)][0] == False:
                            # 移动棋子
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"soldier"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (True,"soldier")
                            # 给红方加分
                            redscores += 1
                            return "CAP-BLACK"
                        # 如果新位置是红棋
                        elif chessboard[(nx,ny)][0] == True:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                else:
                    select = False
                    print("不能走那么多")
                    return "RESELECT"
            elif (x,y) in blackhalf:
                # 检查是否在合法范围内
                if (nx,ny) == (x,y+1) or (nx,ny) == (x,y-1) or (nx,ny) == (x+1,y) or (nx,ny) == (x-1,y):
                    # 如果新位置是空格
                    if chessboard[(nx,ny)] == "none":
                        # 移动棋子
                        select = False
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"soldier"）
                        chessboard[(x,y)] = "none"
                        chessboard[(nx,ny)] = (True,"soldier")
                        return "MOVED"
                    else:
                        # 如果新位置是黑棋
                        if chessboard[(nx,ny)][0] == False:
                            # 移动棋子
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"soldier"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (True,"soldier")
                            # 给红方加分
                            redscores += 1
                            return "CAP-BLACK"
                        # 如果新位置是红棋
                        elif chessboard[(nx,ny)][0] == True:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
            else:
                print("意想不到的事情发生了")
                sys.exit()
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"


    def blacksoldier(x,y,nx,ny):
        '''制定黑方士兵的规则'''

        # 检查是否在棋盘上
        if x >= 0 and x <= 9 and y >= 0 and y <= 9 and nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9:
            # 检查在哪一方区域
            if (x,y) in blackhalf:
                # 检查是否在合法的移动范围内
                if (nx,ny) == (x,y+1):
                    # 检查新位置没有棋子
                    if chessboard[(nx,ny)] == "none":
                        # 移动棋子
                        select = False
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"soldier"）
                        chessboard[(x,y)] = "none"
                        chessboard[(nx,ny)] = (False,"soldier")
                        return "MOVED"
                    else:
                        # 如果新位置是红棋
                        if chessboard[(nx,ny)][0] == True:
                            # 移动棋子
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"soldier"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (False,"soldier")
                            # 给黑方加分
                            blackscores += 1
                            return "CAP-RED"
                        # 如果新位置是黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                else:
                    print("不能走那么多")
                    return "RESELECT"
            elif (x,y) in redhalf:
                # 检查是否在合法范围内
                if (nx,ny) == (x,y+1) or (nx,ny) == (x,y-1) or (nx,ny) == (x+1,y) or (nx,ny) == (x-1,y):
                    # 如果新位置是空格
                    if chessboard[(nx,ny)] == "none":
                        # 移动棋子
                        select = False
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"soldier"）
                        chessboard[(x,y)] = "none"
                        chessboard[(nx,ny)] = (False,"soldier")
                        return "MOVED"
                    else:
                        # 如果新位置是红棋
                        if chessboard[(nx,ny)][0] == False:
                            # 移动棋子
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"soldier"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (False,"soldier")
                            # 给黑方加分
                            blackscores += 1
                            return "CAP-RED"
                        # 如果新位置是黑棋
                        elif chessboard[(nx,ny)][0] == True:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
            else:
                print("意想不到的事情发生了")
                sys.exit()
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"


    def redcannon(x,y,nx,ny):
        '''红炮移动规则'''

        # 检查是否在棋盘上
        if x >= 0 and x <= 9 and y >= 0 and y <= 9 and nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9:
            # 检查是垂直移动
            if (x == nx and y != ny):
                # 确定y方向上的最小值和最大值
                min_y, max_y = min(y, ny), max(y, ny)
                # 统计中间是否只有一个棋子
                num_pieces = sum(1 for cachey in range(min_y + 1, max_y) if chessboard[(x, cachey)] != "none")
                # 列举出（x,y）和（x,ny）之间的坐标
                for cachey in list(range(y,ny)):
                    # 如果中间没棋子
                    if chessboard[(x,cachey)] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx,ny)] == "none":
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"cannon"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (True,"cannon")
                            return "MOVED"
                        # 如果新位置是黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            # 不移动棋子
                            select = False
                            print("没有棋子充当炮架")
                            return "RESELECT"
                        # 如果新位置是红棋
                        elif chessboard[(nx,ny)][0] == True:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间只有一个棋子
                    elif num_pieces == 1:
                        # 如果新位置是空的
                        if chessboard[(nx,ny)] == "none":
                            select = False
                            print("有棋子阻挡")
                            return "RESELECT"
                        # 如果新位置是黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            # 吃掉黑棋
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"cannon"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (True,"cannon")
                            redscores += 1
                            return "CAP-BLACK"
                        # 如果新位置是红棋
                        elif chessboard[(nx,ny)][0] == True:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有大于1个棋子
                    elif num_pieces > 1:
                        select = False
                        print("中间有多个棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            # 如果是水平移动
            if (x != nx and y == ny):
                # 确定x方向上的最小值和最大值
                min_x, max_x = min(x, nx), max(x, nx)
                # 统计中间是否只有一个棋子
                num_pieces = sum(1 for cachex in range(min_x + 1, max_x) if chessboard[(cachex, y)] != "none")
                # 列举出（x,y）和（nx,y）之间的坐标
                for cachex in list(range(x,nx)):
                    # 如果中间没棋子
                    if chessboard[(x,cachex)] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx,nx)] == "none":
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"cannon"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (True,"cannon")
                            return "MOVED"
                        # 如果新位置是黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            # 不移动棋子
                            select = False
                            print("没有棋子充当炮架")
                            return "RESELECT"
                        # 如果新位置是红棋
                        elif chessboard[(nx,ny)][0] == True:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间只有一个棋子
                    elif num_pieces == 1:
                        # 如果新位置是空的
                        if chessboard[(nx,ny)] == "none":
                            select = False
                            print("有棋子阻挡")
                            return "RESELECT"
                        # 如果新位置是黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            # 吃掉黑棋
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（True,"cannon"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (True,"cannon")
                            redscores += 1
                            return "CAP-BLACK"
                        # 如果新位置是红棋
                        elif chessboard[(nx,ny)][0] == True:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有大于1个棋子
                    elif num_pieces > 1:
                        select = False
                        print("中间有多个棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            else:
                select = False
                print("要水平或垂直移动")
                return "RESELECT"
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"


    def blackcannon(x,y,nx,ny):
        '''黑炮移动规则'''

        # 检查是否在棋盘上
        if x >= 0 and x <= 9 and y >= 0 and y <= 9 and nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9:
            # 检查是垂直移动
            if (x == nx and y != ny):
                # 确定y方向上的最小值和最大值
                min_y, max_y = min(y, ny), max(y, ny)
                # 统计中间是否只有一个棋子
                num_pieces = sum(1 for cachey in range(min_y + 1, max_y) if chessboard[(x, cachey)] != "none")
                # 列举出（x,y）和（x,ny）之间的坐标
                for cachey in list(range(y,ny)):
                    # 如果中间没棋子
                    if chessboard[(x,cachey)] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx,ny)] == "none":
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"cannon"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (False,"cannon")
                            return "MOVED"
                        # 如果新位置是红棋
                        elif chessboard[(nx,ny)][0] == True:
                            # 不移动棋子
                            select = False
                            print("没有棋子充当炮架")
                            return "RESELECT"
                        # 如果新位置是黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间只有一个棋子
                    elif num_pieces == 1:
                        # 如果新位置是空的
                        if chessboard[(nx,ny)] == "none":
                            select = False
                            print("有棋子阻挡")
                            return "RESELECT"
                        # 如果新位置是红棋
                        elif chessboard[(nx,ny)][0] == True:
                            # 吃掉黑棋
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"cannon"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (False,"cannon")
                            redscores += 1
                            return "CAP-BLACK"
                        # 如果新位置是黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有大于1个棋子
                    elif num_pieces > 1:
                        select = False
                        print("中间有多个棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            # 如果是水平移动
            if (x != nx and y == ny):
                # 确定x方向上的最小值和最大值
                min_x, max_x = min(x, nx), max(x, nx)
                # 统计中间是否只有一个棋子
                num_pieces = sum(1 for cachex in range(min_x + 1, max_x) if chessboard[(cachex, y)] != "none")
                # 列举出（x,y）和（nx,y）之间的坐标
                for cachex in list(range(x,nx)):
                    # 如果中间没棋子
                    if chessboard[(x,cachex)] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx,nx)] == "none":
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"cannon"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (False,"cannon")
                            return "MOVED"
                        # 如果新位置是红棋
                        elif chessboard[(nx,ny)][0] == True:
                            # 不移动棋子
                            select = False
                            print("没有棋子充当炮架")
                            return "RESELECT"
                        # 如果新位置是黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间只有一个棋子
                    elif num_pieces == 1:
                        # 如果新位置是空的
                        if chessboard[(nx,ny)] == "none":
                            select = False
                            print("有棋子阻挡")
                            return "RESELECT"
                        # 如果新位置是红棋
                        elif chessboard[(nx,ny)][0] == False:
                            # 吃掉红棋
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,ny）的键值对改为（False,"cannon"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,ny)] = (False,"cannon")
                            redscores += 1
                            return "CAP-RED"
                        # 如果新位置是黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            # 不移动棋子
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有大于1个棋子
                    elif num_pieces > 1:
                        select = False
                        print("中间有多个棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            else:
                select = False
                print("要水平或垂直移动")
                return "RESELECT"
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"


    def redcar(x,y,nx,ny):
        '''红车移动规则'''

        # 检查是否在棋盘上
        if x >= 0 and x <= 9 and y >= 0 and y <= 9 and nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9:
            # 检查是否垂直移动
            if x == nx and y != ny:
                # 列举出（x,y）和（x,ny）之间的坐标
                for cachey in list(range(y,ny)):
                    # 如果中间没棋子
                    if chessboard[(x,cachey)] == "none":
                        # 如果目标位置有黑棋
                        if chessboard[(nx,ny)][0] == False:
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（x,ny）的键值对改为（True,"car"）
                            chessboard[(x,y)] = "none"
                            chessboard[(x,ny)] = (True,"car")
                            redscores += 1
                            return "CAP-BLACK"
                        # 如果目标位置有红棋
                        elif chessboard[(nx,ny)][0] == True:
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        # 如果目标位置是空的
                        elif chessboard[(nx,ny)] == "none":
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（x,ny）的键值对改为（True,"car"）
                            chessboard[(x,y)] = "none"
                            chessboard[(x,ny)] = (True,"car")
                            return "MOVED"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有棋子
                    elif chessboard[(x,cachey)][0] != "none":
                        select = False
                        print("有棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            # 检查是否水平移动
            elif x != nx and y == ny:
                # 列举出（x,y）和（nx,y）之间的坐标
                for cachex in list(range(x,nx)):
                    # 如果中间没棋子
                    if chessboard[(cachex,y)] == "none":
                        # 如果目标位置有黑棋
                        if chessboard[(nx,ny)][0] == False:
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"car"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,y)] = (True,"car")
                            redscores += 1
                            return "CAP-BLACK"
                        # 如果目标位置有红棋
                        elif chessboard[(nx,ny)][0] == True:
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        # 如果目标位置是空的
                        elif chessboard[(nx,ny)] == "none":
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"car"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,y)] = (True,"car")
                            return "MOVED"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有棋子
                    elif chessboard[(cachex,y)][0] != "none":
                        select = False
                        print("有棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            else:
                select = False
                print("要水平或垂直移动")
                return "RESELECT"
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"


    def blackcar(x,y,nx,ny):
        '''黑车移动规则'''

        # 检查是否在棋盘上
        if x >= 0 and x <= 9 and y >= 0 and y <= 9 and nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9:
            # 检查是否垂直移动
            if x == nx and y != ny:
                # 列举出（x,y）和（x,ny）之间的坐标
                for cachey in list(range(y,ny)):
                    # 如果中间没棋子
                    if chessboard[(x,cachey)] == "none":
                        # 如果目标位置有红棋
                        if chessboard[(nx,ny)][0] == True:
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（x,ny）的键值对改为（Falsee,"car"）
                            chessboard[(x,y)] = "none"
                            chessboard[(x,ny)] = (False,"car")
                            blackscores += 1
                            return "CAP-RED"
                        # 如果目标位置有黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        # 如果目标位置是空的
                        elif chessboard[(nx,ny)] == "none":
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（x,ny）的键值对改为（False,"car"）
                            chessboard[(x,y)] = "none"
                            chessboard[(x,ny)] = (False,"car")
                            return "MOVED"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有棋子
                    elif chessboard[(x,cachey)][0] != "none":
                        select = False
                        print("有棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            # 检查是否水平移动
            elif x != nx and y == ny:
                # 列举出（x,y）和（nx,y）之间的坐标
                for cachex in list(range(x,nx)):
                    # 如果中间没棋子
                    if chessboard[(cachex,y)] == "none":
                        # 如果目标位置有红棋
                        if chessboard[(nx,ny)][0] == True:
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"car"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,y)] = (False,"car")
                            blackscores += 1
                            return "CAP-RED"
                        # 如果目标位置有黑棋
                        elif chessboard[(nx,ny)][0] == False:
                            select = False
                            print("不能吃自己的棋子")
                            return "RESELECT"
                        # 如果目标位置是空的
                        elif chessboard[(nx,ny)] == "none":
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"car"）
                            chessboard[(x,y)] = "none"
                            chessboard[(nx,y)] = (False,"car")
                            return "MOVED"
                        else:
                            print("意想不到的事情发生了")
                            sys.exit()
                    # 如果中间有棋子
                    elif chessboard[(cachex,y)][0] != "none":
                        select = False
                        print("有棋子阻挡")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
            else:
                select = False
                print("要水平或垂直移动")
                return "RESELECT"
        else:
            select = False
            print("不在棋盘上")    
            return "RESELECT" 


    def redhorese(x,y,nx,ny):
        '''红马移动规则'''

        def redhorsego(x,y,nx,ny):
            global select
            global redscores
            global blackscores
            select = False
            # 如果目标位置为空
            if chessboard[(nx,ny)] == "none":
                select = False
                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"horse"）
                chessboard[(x,y)] = "none"
                chessboard[(nx,ny)] = (True,"horse")
                return "MOVED"
            # 如果目标位置有黑棋
            elif chessboard[(nx,ny)][0] == False:
                select = False
                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"horse"）
                chessboard[(x,y)] = "none"
                chessboard[(nx,ny)] = (True,"horse")
                redscores += 1
                return "CAP-BLACK"
            # 如果目标位置有红棋
            elif chessboard[(nx,ny)][0] == True:
                select = False
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()  
        # 检查是否在棋盘上
        if x >= 0 and x <= 9 and y >= 0 and y <= 9 and nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9:
            # 检查是否走“日”字（1）
            if nx == x-2 and ny == y+1:
                # 检查没有拌马脚
                if chessboard[(x-1,y)][0] == "none":
                    redhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x-1,y)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（2）
            elif nx == x-1 and ny == y+2:
                # 检查没有拌马脚
                if chessboard[(x-1,y+1)][0] == "none":
                    redhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x-1,y+1)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（3）
            elif nx == x+2 and ny == y+1:
                # 检查没有拌马脚
                if chessboard[(x+1,y)][0] == "none":
                    redhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x+1,y)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（4）
            elif nx == x+1 and ny == y+2:
                # 检查没有拌马脚
                if chessboard[(x+1,y+1)][0] == "none":
                    redhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x+1,y+1)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（5）
            elif nx == x-2 and ny == y-1:
                # 检查没有拌马脚
                if chessboard[(x-1,y)][0] == "none":
                    redhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x-1,y)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（6）
            elif nx == x-1 and ny == y-2:
                # 检查没有拌马脚
                if chessboard[(x-1,y-1)][0] == "none":
                    redhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x-1,y-1)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（7）
            elif nx == x+2 and ny == y-1:
                # 检查没有拌马脚
                if chessboard[(x+1,y)][0] == "none":
                    redhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x+1,y)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（8）
            elif nx == x+1 and ny == y-2:
                # 检查没有拌马脚
                if chessboard[(x+1,y-1)][0] == "none":
                    redhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x+1,y-1)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                select = False
                print("走法不正确")
                return "RESELECT"
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"
        

    def blackhorese(x,y,nx,ny):
        '''黑马移动规则'''


        def blackhorsego(x,y,nx,ny):
            global select
            global redscores
            global blackscores
            select = False
            # 如果目标位置为空
            if chessboard[(nx,ny)] == "none":
                select = False
                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"horse"）
                chessboard[(x,y)] = "none"
                chessboard[(nx,ny)] = (False,"horse")
                return "MOVED"
            # 如果目标位置有红棋
            elif chessboard[(nx,ny)][0] == True:
                select = False
                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"horse"）
                chessboard[(x,y)] = "none"
                chessboard[(nx,ny)] = (False,"horse")
                blackscores += 1
                return "CAP-RED"
            # 如果目标位置有黑棋
            elif chessboard[(nx,ny)][0] == False:
                select = False
                print("不能吃自己的棋子")
                return "RESELECT"
            else:
                print("意想不到的事情发生了")
                sys.exit()  
        # 检查是否在棋盘上
        if x >= 0 and x <= 9 and y >= 0 and y <= 9 and nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9:
            # 检查是否走“日”字（1）
            if nx == x-2 and ny == y+1:
                # 检查没有拌马脚
                if chessboard[(x-1,y)][0] == "none":
                    blackhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x-1,y)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（2）
            elif nx == x-1 and ny == y+2:
                # 检查没有拌马脚
                if chessboard[(x-1,y+1)][0] == "none":
                    blackhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x-1,y+1)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（3）
            elif nx == x+2 and ny == y+1:
                # 检查没有拌马脚
                if chessboard[(x+1,y)][0] == "none":
                    blackhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x+1,y)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（4）
            elif nx == x+1 and ny == y+2:
                # 检查没有拌马脚
                if chessboard[(x+1,y+1)][0] == "none":
                    blackhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x+1,y+1)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（5）
            elif nx == x-2 and ny == y-1:
                # 检查没有拌马脚
                if chessboard[(x-1,y)][0] == "none":
                    blackhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x-1,y)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（6）
            elif nx == x-1 and ny == y-2:
                # 检查没有拌马脚
                if chessboard[(x-1,y-1)][0] == "none":
                    blackhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x-1,y-1)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（7）
            elif nx == x+2 and ny == y-1:
                # 检查没有拌马脚
                if chessboard[(x+1,y)][0] == "none":
                    blackhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x+1,y)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            # 检查是否走“日”字（8）
            elif nx == x+1 and ny == y-2:
                # 检查没有拌马脚
                if chessboard[(x+1,y-1)][0] == "none":
                    blackhorsego(x,y,nx,ny)
                # 检查拌马脚
                elif chessboard[(x+1,y-1)][0] != "none":
                    select = False
                    print("拌马脚")
                    return "TRIP-HORSE"
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                select = False
                print("走法不正确")
                return "RESELECT"
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"


    def redofficer(x,y,nx,ny):
        '''红士移动规则'''

        # 检查是否在九宫格内
        if nx >= 3 and nx <= 5 and ny >= 0 and ny <= 2:
            # 检查是否走斜线
            if (nx == x+1 and ny == y+1) or (nx == x+1 and ny == y-1) or (nx == x-1 and ny == y+1) or (nx == x-1 and ny == y-1):
                # 如果新位置是空的
                if chessboard[(nx,ny)][0] == "none":
                    # 移动棋子
                    select = False
                    # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"officer"）
                    chessboard[(x,y)] = ("none")
                    chessboard[(nx,ny)] = (True,"officer")
                    return "MOVED"
                # 如果新位置不是空的
                elif chessboard[(nx,ny)][0] != "none":
                    # 如果新位置的棋子是黑棋
                    if chessboard[(nx,ny)][0] == False:
                        # 移动棋子
                        select = False
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"officer"）
                        chessboard[(x,y)] = ("none")
                        chessboard[(nx,ny)] = (True,"officer")
                        redscores += 1
                        return "CAP-BLACK"
                    # 如果新位置的棋子是红棋
                    elif chessboard[(nx,ny)][0] == True:
                        select = False
                        print("不能吃自己的棋子")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                select = False
                print("走法不正确")
                return "RESELECT"
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"


    def blackofficer(x,y,nx,ny):
        '''黑士移动规则'''

        # 检查是否在九宫格内
        if nx >= 3 and nx <= 5 and ny >= 7 and ny <= 9:
            # 检查是否走斜线
            if (nx == x+1 and ny == y+1) or (nx == x+1 and ny == y-1) or (nx == x-1 and ny == y+1) or (nx == x-1 and ny == y-1):
                # 如果新位置是空的
                if chessboard[(nx,ny)][0] == "none":
                    # 移动棋子
                    select = False
                    # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"officer"）
                    chessboard[(x,y)] = ("none")
                    chessboard[(nx,ny)] = (False,"officer")
                    return "MOVED"
                # 如果新位置不是空的
                elif chessboard[(nx,ny)][0] != "none":
                    # 如果新位置的棋子是红棋
                    if chessboard[(nx,ny)][0] == True:
                        # 移动棋子
                        select = False
                        # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"officer"）
                        chessboard[(x,y)] = ("none")
                        chessboard[(nx,ny)] = (False,"officer")
                        blackscores += 1
                        return "CAP-RED"
                    # 如果新位置的棋子是黑棋
                    elif chessboard[(nx,ny)][0] == False:
                        select = False
                        print("不能吃自己的棋子")
                        return "RESELECT"
                    else:
                        print("意想不到的事情发生了")
                        sys.exit()
                else:
                    print("意想不到的事情发生了")
                    sys.exit()
            else:
                select = False
                print("走法不正确")
                return "RESELECT"
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"


    def redelephant(x,y,nx,ny):
        '''红象移动规则'''

        # 检查是否在棋盘上
        if x >= 0 and x <= 8 and y >= 0 and y <= 8 and nx >= 0 and nx <= 8 and ny >= 0 and ny <= 8:
            # 检查是否走田字
            if (nx == x+2 and ny == y+2) or (nx == x+2 and ny == y-2) or (nx == x-2 and ny == y+2) or (nx == x-2 and ny == y-2):
                # 检查是否过河
                if nx and ny in redhalf:
                    # 检查是否被蹩象脚
                    if (x+1,y) in chessboard and chessboard[(x+1,y)][0] == "none" and (x-1,y) in chessboard and chessboard[(x-1,y)][0] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx,ny)][0] == "none":
                            # 移动棋子
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"elephant"）
                            chessboard[(x,y)] = ("none")
                            chessboard[(nx,ny)] = (True,"elephant")
                            return "MOVED"
                        # 如果新位置不是空的
                        elif chessboard[(nx,ny)][0] != "none":
                            # 如果新位置的棋子是红棋
                            if chessboard[(nx,ny)][0] == True:
                                select = False
                                print("不能吃自己的棋子")
                                return "RESELECT"
                            # 如果新位置的棋子是黑棋
                            elif chessboard[(nx,ny)][0] == False:
                                # 移动棋子
                                select = False
                                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（True,"elephant"）
                                chessboard[(x,y)] = ("none")
                                chessboard[(nx,ny)] = (True,"elephant")
                                redscores += 1
                                return "CAP-BLACK"
                            else:
                                print("意想不到的事情发生了")
                                sys.exit()
                    else:
                        select = False
                        print("被蹩象脚")
                        return "TRIP-ELEPHANT"
                else:
                    select = False
                    print("过河了")
                    return "NO-CROSS"
            else:
                select = False
                print("走法不正确")
                return "RESELECT"
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"


    def blackelephant(x,y,nx,ny):
        '''黑象移动规则'''

        # 检查是否在棋盘上
        if x >= 0 and x <= 8 and y >= 0 and y <= 8 and nx >= 0 and nx <= 8 and ny >= 0 and ny <= 8:
            # 检查是否走田字
            if (nx == x+2 and ny == y+2) or (nx == x+2 and ny == y-2) or (nx == x-2 and ny == y+2) or (nx == x-2 and ny == y-2):
                # 检查是否过河
                if nx and ny in blackhalf:
                    # 检查是否被蹩象脚
                    if (x+1,y) in chessboard and chessboard[(x+1,y)][0] == "none" and (x-1,y) in chessboard and chessboard[(x-1,y)][0] == "none":
                        # 如果新位置是空的
                        if chessboard[(nx,ny)][0] == "none":
                            # 移动棋子
                            select = False
                            # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"elephant"）
                            chessboard[(x,y)] = ("none")
                            chessboard[(nx,ny)] = (False,"elephant")
                            return "MOVED"
                        # 如果新位置不是空的
                        elif chessboard[(nx,ny)][0] != "none":
                            # 如果新位置的棋子是黑棋
                            if chessboard[(nx,ny)][0] == False:
                                select = False
                                print("不能吃自己的棋子")
                                return "RESELECT"
                            # 如果新位置的棋子是红棋
                            elif chessboard[(nx,ny)][0] == True:
                                # 移动棋子
                                select = False
                                # 修改chessboard词典 上的值, 把（x,y）的键值对改为“none”,  把（nx,y）的键值对改为（False,"elephant"）
                                chessboard[(x,y)] = ("none")
                                chessboard[(nx,ny)] = (False,"elephant")
                                redscores += 1
                                return "CAP-RED"
                            else:
                                print("意想不到的事情发生了")
                                sys.exit()
                    else:
                        select = False
                        print("被蹩象脚")
                        return "TRIP-ELEPHANT"
                else:
                    select = False
                    print("过河了")
                    return "NO-CROSS"
            else:
                select = False
                print("走法不正确")
                return "RESELECT"
        else:
            select = False
            print("不在棋盘上")
            return "RESELECT"



class Operate:
    def __init__(self):
        pass
    

    def checkcaptain(chessboard):
        '''判断是否将军'''
        captain_pos = None
        captain_color = None

        # 遍历棋盘, 查找将的位置及颜色
        for pos, (is_red, piece) in chessboard.items():
            if piece == "captain":
                captain_pos = pos
                captain_color = is_red  # 记录“将”的颜色（True 为红, False 为黑）
                break

        # 如果没找到“将”, 说明它已经被吃掉
        if captain_pos is None:
            return True  # 被吃掉了, 返回 True

        # 如果找到“将”, 说明将还在棋盘上
        return False  # 将还在, 返回 False
        
    
    def move(x,y,nx,ny):
        '''判断坐标并调用 Chess类 的 对应函数'''
        # 判断棋子类型
        if chessboard[(x,y)][1] == "car":
            # 判断棋子颜色
            if chessboard[(x,y)][0] == True:
                message = Chess.redcar(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
            # 判断棋子颜色
            elif chessboard[(x,y)][0] == False:
                message = Chess.blackcar(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
        elif chessboard[(x,y)][1] == "horse":
            # 判断棋子颜色
            if chessboard[(x,y)][0] == True:
                message = Chess.redhorse(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "TRIP-HORSE":
                    print("拌马脚！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
            # 判断棋子颜色
            elif chessboard[(x,y)][0] == False:
                message = Chess.blackhorse(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "TRIP-HORSE":
                    print("拌马脚！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
        elif chessboard[(x,y)][1] == "elephant":
            # 判断棋子颜色
            if chessboard[(x,y)][0] == True:
                message = Chess.redelephant(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "TRIP-ELEPHANT":
                    print("拌象脚！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
            # 判断棋子颜色
            elif chessboard[(x,y)][0] == False:
                message = Chess.blackelephant(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "TRIP-ELEPHANT":
                    print("拌象脚！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
        elif chessboard[(x,y)][1] == "officer":
            # 判断棋子颜色
            if chessboard[(x,y)][0] == True:
                message = Chess.redofficer(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
            # 判断棋子颜色
            elif chessboard[(x,y)][0] == False:
                message = Chess.blackofficer(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
        elif chessboard[(x,y)][1] == "captain":
            # 判断棋子颜色
            if chessboard[(x,y)][0] == True:
                message = Chess.redcaptain(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
            # 判断棋子颜色
            elif chessboard[(x,y)][0] == False:
                message = Chess.blackcaptain(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
        elif chessboard[(x,y)][1] == "cannon":
            # 判断棋子颜色
            if chessboard[(x,y)][0] == True:
                message = Chess.redcannon(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
            # 判断棋子颜色
            elif chessboard[(x,y)][0] == False:
                message = Chess.blackcannon(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
        elif chessboard[(x,y)][1] == "soldier":
            # 判断棋子颜色
            if chessboard[(x,y)][0] == True:
                message = Chess.redsoldier(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-BLACK":
                    print("红方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
            # 判断棋子颜色
            elif chessboard[(x,y)][0] == False:
                message = Chess.blacksoldier(x,y,nx,ny)
                if message == "RESELECT":
                    print("重新选择棋子")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                    Operate.cmd_select_piece()
                elif message == "CAP-RED":
                    print("黑方加一分！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                elif message == "MOVED":
                    print("移动成功！")
                    print(f"红方: {redscores}分, 黑方: {blackscores}分")
                Operate.checkcaptain(chessboard)
        else:
            print("该位置没有棋子, 请重新选择")
            Operate.cmd_select_piece()


    def cmd_select_piece(ai_sort="zhipai", ollama_model=None):
        # 初始化图形
        fig, ax = plt.subplots(figsize=(10, 10))

        # 绘制棋盘
        def draw_chessboard():
            ax.clear()  # 清除原有内容
            ax.set_xlim(-1, 9)
            ax.set_ylim(-1, 9)
            ax.set_xticks(range(9))
            ax.set_yticks(range(9))
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.grid(True)

            # 绘制格子和棋子
            for (x, y), value in chessboard.items():
                color = "white"  # 默认格子颜色
                label = None

                if value != "none":
                    is_red, piece = value
                    color = color_map.get(is_red, "white")  # 根据棋子的颜色映射
                    label = piece_name_map.get(piece, piece)  # 将英文转换为中文棋子名称

                rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
                ax.add_patch(rect)

                # 在棋盘上显示文字（如果有棋子）
                if label:
                    ax.text(x + 0.5, y + 0.5, label, ha='center', va='center', color='white', fontsize=10)

            # 设置标题
            ax.set_title("中国象棋")

        # 动态刷新棋盘
        def update(frame):
            draw_chessboard()
            plt.draw()  # 强制刷新图形界面

        # 设置动画刷新
        ani = animation.FuncAnimation(fig, update, interval=3000)  # 每3秒刷新一次

        # 添加文本框，用于输入坐标
        ax_input = plt.axes([0.15, 0.01, 0.7, 0.05])
        text_box = TextBox(ax_input, "请输入棋子坐标 (格式: x,y, nx, ny):")

        def submit_callback(text):
            try:
                # 解析输入的坐标
                coords = text.split(',')
                if len(coords) == 4:
                    x, y, nx, ny = map(int, coords)
                    Operate.move(x, y, nx, ny)  # 更新棋盘字典

                    # 根据AI选择调用不同的AI函数
                    if ai_sort == "zhipuai":
                        AI.zhipuai()
                    elif ai_sort == "openai":
                        AI.openai()
                    elif ai_sort == "ollama":
                        AI.ollama(ollama_model)
                    else:
                        print("请输入正确的AI类型")
                        Operate.cmd_select_piece(ai_sort)

                    # 刷新棋盘显示
                    draw_chessboard()
                    plt.draw()  # 强制刷新图形界面

                else:
                    print("请输入正确格式的坐标!")
            except ValueError:
                print("输入无效，请确保输入的是四个整数值，格式为 x,y, nx, ny")

        # 绑定提交按钮的回调
        text_box.on_submit(submit_callback)

        # 显示图形
        plt.show()

                
    def graphic_select_piece(ai_sort="zhipuai", ollama_model=None):
        '''图形化选择棋子'''
        # 初始化图形
        fig, ax = plt.subplots(figsize=(8, 8))

        # 绘制棋盘
        def draw_chessboard(ai_sort="zhipuai", ollama_model=None):
            ax.clear()
            ax.set_xlim(-0.5, 8.5)
            ax.set_ylim(-0.5, 8.5)
            ax.set_xticks(range(9))
            ax.set_yticks(range(9))
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.grid(True)

            # 绘制格子和棋子
            for (x, y), value in chessboard.items():
                color = "white"  # 默认格子颜色
                label = None
                
                if value != "none":
                    is_red, piece = value
                    color = color_map.get(is_red, "white")  # 根据棋子的颜色映射
                    label = piece_name_map.get(piece, piece)  # 将英文转换为中文棋子名称
                
                rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
                ax.add_patch(rect)

                # 在棋盘上显示文字（如果有棋子）
                if label:
                    ax.text(x + 0.5, y + 0.5, label, ha='center', va='center', color='white', fontsize=10)

            # 设置标题
            ax.set_title("中国象棋")


        # 单击事件处理
        def on_click(event, ai_sort="zhipuai", ollama_model=None):
            global first_click  # 声明使用全局变量

            if event.xdata is None or event.ydata is None:
                return
            x, y = int(event.xdata), int(event.ydata)

            # 记录第一次点击的位置
            if first_click is None:
                first_click = (x, y)
                print(f"First click at ({x}, {y})")  # 打印第一次单击的坐标
            else:
                # 第二次点击, 直接返回新的四个坐标
                nx, ny = x, y
                print(f"First click at ({first_click[0]}, {first_click[1]}), Second click at ({nx}, {ny})")
                first_click = None  # 重置第一次点击的坐标
                Operate.move(x,y,nx,ny)
                if ai_sort == "zhipuai":
                    Chess.zhipuai()
                elif ai_sort == "openai":
                    Chess.openai()
                elif ai_sort == "ollama":
                    Chess.ollama(ollama_model)
                else:
                    print("请输入正确的AI类型")

        # 注册事件
        fig.canvas.mpl_connect("button_press_event", on_click)

        # 动态刷新棋盘
        def update(frame):
            draw_chessboard()
            plt.draw()

        # 设置动画刷新
        ani = animation.FuncAnimation(fig, update, interval=3000)  # 每3秒刷新一次

        # 运行并显示图形
        plt.show()



class AI:
    def __init__(self):
        pass
    
    def zhipuai():
        client = ZhipuAI(api_key="")
        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=[
                {"role": "system", "content": "你是一个象棋大师, 根据我跟你的棋局状况字典(以左下角的棋子为(0,0), True 是红棋, False 是黑棋), 给出下一步的走法(回答格式: x,y,nx,ny),x和y是原来棋子的坐标,nx和ny是新位置的坐标,不需要任何解释。"},
                {"role": "user", "content": f"棋局状况(以左下角的棋子为(0,0), True 是红棋, False 是黑棋): {chessboard}, 给出下一步的走法(回答格式: x,y,nx,ny),其中x和y是原来棋子的坐标,nx和ny是新位置的坐标,不需要任何解释。"}
            ],
        )
        locations = response.choices[0].message.content.split(",")
        x,y,nx,ny = int(locations[0]),int(locations[1]),int(locations[2]),int(locations[3])
        Operate.move(x,y,nx,ny)
        print(f"AI选择的原坐标: {x},{y}, AI选择的新坐标: {nx},{ny}")
        print(chessboard)

    def openai(api_key):
        pass
    
    def ollama(model):
        res = ollama.chat(
            model=model,stream=False,messages=[
                {"role": "system", "content": "你是一个象棋大师, 根据我跟你的棋局状况字典(以左下角的棋子为(0,0), True 是红棋, False 是黑棋), 给出下一步的走法(回答格式: x,y,nx,ny),x和y是原来棋子的坐标,nx和ny是新位置的坐标,不需要任何解释。"},
                {"role": "user", "content": f"棋局状况(以左下角的棋子为(0,0), True 是红棋, False 是黑棋): {chessboard}, 给出下一步的走法(回答格式: x,y,nx,ny),其中x和y是原来棋子的坐标,nx和ny是新位置的坐标,不需要任何解释。"}
            ],
            options={"temperature":0})
        locations = res["message"]["content"].split(",")
        x,y,nx,ny = int(locations[0]),int(locations[1]),int(locations[2]),int(locations[3])
        Operate.move(x,y,nx,ny)
        print(res)



class Main:
    def __init__(self):
        pass

    def cmd_play():
        Operate.cmd_select_piece("zhipuai")
    
    def graphic_play():
        Operate.graphic_select_piece("zhipuai")

  
        
if __name__ == "__main__":
    Main.cmd_play()

    
