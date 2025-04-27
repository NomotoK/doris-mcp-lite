# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# 加载当前目录下的.env文件
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# 读取配置项
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 9030)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", ""),
}

MCP_SERVER_NAME = os.getenv("MCP_SERVER_NAME", "DorisAnalytics")
DEBUG = os.getenv("DEBUG", "false").lower() in ["1", "true", "yes"]