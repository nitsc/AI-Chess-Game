from gui import CNChessGame

if __name__ == "__main__":
    print('''
        # < 笔名：Data Infintai Eterni >
        # < Github：https://github.com/nitsc >
        # < 邮箱：dministrator1st1234567890dddaz@outlook.com >
        # < 邮箱：zhoukreanto@gmail.com\n '''
          )
    ai_way = input("请选择AI模式 (1. GLM4-PLUS API 对战，2. DeepSeek-r1:14b 本地对战)：")
    game = CNChessGame()
    game.run(ai_way=ai_way)
