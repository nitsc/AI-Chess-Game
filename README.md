# AI Chess Game 🎮🤖

这是一款支持与本地 **DeepSeek R1:671B** 和 API **ChatGLM4-PLUS** 对弈的象棋游戏。游戏提供图形界面、多种玩法和内置音效，带来绝佳的 AI 对弈体验！

## 功能概览

- **AI 对弈**：支持 DeepSeek R1:671B 与 ChatGLM4-PLUS 对弈 🤖
- **图形界面**：通过 `gui.py` 提供简洁易用的界面 🎨
- **精美棋盘和棋子图片**：丰富视觉体验 🎲
- **内置音效**：背景音乐增添乐趣 🎵
- **跨平台支持**：适用于 Windows 与 Linux，内置 Docker 镜像 🚀

## 环境要求

- Python 3.11 及以上版本 🐍
- 所需 Python 库（使用 `requirements.txt` 安装）

## 安装与使用

### Windows

1. **安装依赖**  
   确保安装 Python 3.11+ 后，执行：
   ```bash
   pip install -r requirements.txt
   ```

2. **运行游戏**  
   进入 `src` 文件夹，执行：
   ```bash
   python src/main.py
   ```

### Linux

1. **安装依赖**  
   确保安装 Python 3.11+ 后，执行：
   ```bash
   pip3 install -r requirements.txt
   ```

2. **运行游戏**  
   进入 `src` 文件夹，执行：
   ```bash
   python3 src/main.py
   ```

### Docker 环境运行

项目已提供 Docker 镜像，无需重新构建。

#### Windows

1. 打开命令提示符或 PowerShell，导航到项目根目录。
2. 加载镜像：
   ```bash
   docker load -i docker_img\AIChessGame.tar
   ```
3. 运行容器（镜像名称应为 `eterni-infintai-data/aichessgame`，如有不同请调整）：
   ```bash
   docker run -d --name eterni-infintai-data/aichessgame
   ```

#### Linux

1. 打开终端，导航到项目根目录。
2. 加载镜像：
   ```bash
   docker load -i docker_img/AIChessGame.tar
   ```
3. 运行容器（镜像名称应为 `eterni-infintai-data/aichessgame`，如有不同请调整）：
   ```bash
   docker run -d --name eterni-infintai-data/aichessgame
   ```

运行后，通过 PyGame 窗口即可与 AI 开始精彩对弈！🎉

## 许可证

本项目采用 GNU General Public License v3.0 许可证，详情请参阅 LICENSE 文件 📄
