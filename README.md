### AI Chess Game 🎮🤖  
[📦 GitHub 仓库](https://github.com/nitsc/AI-Chess-Game)  

🔥 **一款支持与本地 DeepSeek R1:14B 🐋 和 API ChatGLM4-PLUS 🐘 对弈的象棋游戏！** 提供精美图形界面、丰富音效，带来沉浸式 AI 对弈体验！🎨🎵  

> ⚠️ **小提醒**：  
> - 语言模型可能会走错棋，请不要频繁调用或尝试窃取 API Key 🛑  
> - **无法获取更多免费的 API Key**（OpenAI 可能不错，但需要信用卡💳）  
> - **长时间无法走棋？** 重新运行程序！  
> - **分数显示异常？** 请查看命令行输出 🖥️  

---

## 🌟 特色功能  

🧠 **AI 对弈** - 支持 DeepSeek R1:14B 和 ChatGLM4-PLUS 🔥  
🎨 **直观图形界面** - 通过 `gui.py` 提供流畅操作体验 💡  
🎲 **精美棋盘 & 棋子** - 高质量视觉设计 🖼️  
🎵 **内置音效** - 让对局更具氛围 🎶  

---

## 📌 环境要求  

- **Python 3.11+** 🐍  
- **PyCharm**（建议从 PyCharm Pro  运行，避免意外问题）💻  
- **Python 依赖**（`requirements.txt`）📦  

---

## 🚀 安装与运行  

### 🪟 Windows 用户  

1️⃣ **安装依赖**  
```bash
pip install -r requirements.txt
```

2️⃣ **运行游戏**  
```bash
python src/main.py
```

3️⃣ **选择模式**（推荐 **选项 1**）🔢  

---

## 🐑 使用 Ollama 运行 DeepSeek R1 14B  

如果想使用 **Ollama 本地推理**（不仅限于 DeepSeek R1:14B 🐋，可修改 `logic.py` 实现 AI）  

1️⃣ [🔗 下载 Ollama](https://ollama.com/) 并安装 📥  
2️⃣ 启动 Ollama 服务  
```bash
ollama serve
```
3️⃣ 拉取 DeepSeek R1 14B 模型（可替换为其他模型, 但需要修改源代码）🚀  
```bash
ollama pull deepseek-r1:14b
```
4️⃣ 运行游戏 🎮  
5️⃣ **选择选项 2** 🔢  

🎯 **然后就可以通过 PyGame 窗口，与 AI 进行一场精彩对弈！😊**  

---

## 🎭 玩法说明  

🖱️ **单击拾起棋子，第二次单击放下**  
📖 规则参考 [象棋百科](https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9C%8B%E8%B1%A1%E6%A3%8B)  
📽️ 可观看示例视频 (`示例使用.mp4`)  

---

## 📜 许可证  

本项目基于 **GNU General Public License v3.0** 许可协议 📄  
详情请查阅 `LICENSE` 文件  

💖 **欢迎 Star ⭐ 支持项目，Enjoy！🎉**