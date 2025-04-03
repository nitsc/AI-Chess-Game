### AI Chess Game 🎮🤖  
[📦 GitHub 仓库](https://github.com/nitsc/AI-Chess-Game)  

🔥 **一款支持与本地 DeepSeek R1:14B 🐋 和 API ChatGLM4-PLUS 🐘 对弈的象棋游戏！** 提供精美图形界面、丰富音效，带来沉浸式 AI 对弈体验！🎨🎵  

> ⚠️ **小提醒**：  
> - **AI 可能走错棋**，请多尝试，如多次失败可 **重启程序** 🏃‍♂️  
> - **仅支持 Windows 端** 🪟，其他平台暂不兼容  
> - **请勿频繁使用或尝试窃取 API Key** 🔑（**无法获取更多免费 API**，OpenAI 需信用卡💳）  
> - **如何移动棋子？** 🖱️ 单击拾起，再次单击放下。请观察命令行提示 🖥️  
> - **分数显示异常？** 请查看命令行输出 🖥️  

- **项目开发不易，希望能给高分！** ⭐🎉  

---

## 🌟 特色功能  

🧠 **AI 对弈** - 支持 DeepSeek R1:14B 和 ChatGLM4-PLUS 🔥  
🎨 **直观图形界面** - 通过 `gui.py` 提供流畅操作体验 💡  
🎲 **精美棋盘 & 棋子** - 高质量视觉设计 🖼️  
🎵 **内置音效** - 让对局更具氛围 🎶  
🐘 **ElephantEye 兼容性** - 未来计划支持 **ElephantEye** 作为更强大的 AI 引擎 🏹  
🔗 **UCCI 协议** - 未来将支持 **UCCI**（Universal Chinese Chess Interface）协议，兼容更多 AI 引擎 🏆  

---

## 📌 环境要求  

- **Python 3.11+** 🐍  
- **PyCharm**（建议从 PyCharm Pro 运行，避免意外问题）💻  
- **Python 依赖**（`requirements.txt`）📦
- **API KEY** (🎁[注册赠送2000万tokens体验包](https://www.bigmodel.cn/))

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

## 🎯 未来计划  

✅ **优化 AI 走棋策略** - 让 AI 计算更精准，提高对弈体验 🏹  
✅ **支持 ElephantEye 引擎** - 引入更强的象棋 AI 计算能力 🐘  
✅ **兼容 UCCI 协议** - 实现与更多象棋 AI 引擎的互通 🔗  
✅ **增加联网对战模式** - 未来可能支持 **局域网 / 互联网对弈** 🌐  

---

## 🎭 玩法说明  

🖱️ **单击拾起棋子，第二次单击放下**  
📖 规则参考 [象棋百科](https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9C%8B%E8%B1%A1%E6%A3%8B)  
📽️ 可观看示例视频 (`示例使用.mp4`)  

---

## 📜 许可证  

本项目基于 **GNU General Public License v3.0** 许可协议 📄  
详情请查阅 `LICENSE` 文件  

---

## GitHub 仓库统计徽章

<!-- GitHub 仓库统计徽章 -->
<p align="center">
  <a href="https://github.com/nitsc/AI-Chess-Game">
    <img src="https://img.shields.io/github/languages/top/nitsc/AI-Chess-Game" alt="Top Language">
  </a>
  <a href="https://github.com/nitsc/AI-Chess-Game/stargazers">
    <img src="https://img.shields.io/github/stars/nitsc/AI-Chess-Game?style=social" alt="Stars">
  </a>
  <a href="https://github.com/nitsc/AI-Chess-Game/watchers">
    <img src="https://img.shields.io/github/watchers/nitsc/AI-Chess-Game?style=social" alt="Watchers">
  </a>
  <a href="https://github.com/nitsc/AI-Chess-Game/network/members">
    <img src="https://img.shields.io/github/forks/nitsc/AI-Chess-Game?style=social" alt="Forks">
  </a>
</p>

<p align="center">
  <a href="https://github.com/nitsc">
    <img src="https://img.shields.io/github/followers/nitsc?style=social" alt="Followers">
  </a>
</p>

💖 **欢迎 Star ⭐ 支持项目，Enjoy！🎉**  
