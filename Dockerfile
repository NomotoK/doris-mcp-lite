FROM python:3.12-slim

# 安装基础依赖
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# 设置工作目录
WORKDIR /app

# 拷贝代码
COPY . .

# 安装项目依赖
RUN pip install --upgrade pip
RUN pip install .

# 暴露端口
EXPOSE 8080

# 启动 MCP 服务器
CMD ["python", "server.py"]