# 使用官方的 Python 3.11 镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置 PyPI 镜像源
ENV PIP_INDEX_URL=https://mirrors.pku.edu.cn/pypi/web/simple

# 复制本地代码到容器内的工作目录
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设定容器启动时运行的命令
CMD ["python", "main.py"]
