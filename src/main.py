from gui import CNChessGame

if __name__ == "__main__":
    print('''
        # < 作者：八 18 班 周伟安 >
        # < 笔名: Data Infintai Eterni >
        # < Github: https://github.com/nitsc >
        # < 邮箱: dministrator1st1234567890dddaz@outlook.com >
        # < 邮箱: zhoukreanto@gmail.com >
        # < 帮助: 请查看 README.md 或 text\注意事项.txt > \n '''
          )
    ai_way = input("请选择AI模式 (1. GLM4-PLUS API 对战; 2. DeepSeek-r1:14b 本地对战):")
    game = CNChessGame()
    game.run(ai_way=ai_way)
