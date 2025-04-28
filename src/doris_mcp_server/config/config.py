# config.py
import os
from dotenv import load_dotenv
from pathlib import Path
import shutil

# 确定.env路径和.env.example路径
env_dir = Path(__file__).resolve().parent
env_path = env_dir / ".env"
env_example_path = env_dir / ".env.example"

# 如果.env不存在，尝试从.env.example复制一份
if not env_path.exists():
    if env_example_path.exists():
        shutil.copy(env_example_path, env_path)
        print(f"未找到 .env 文件，已自动从 .env.example 创建 {env_path}")
        print(f"请根据实际情况编辑 {env_path}，填写正确的数据库连接信息。")
    else:
        raise FileNotFoundError(
            f"❌ 配置文件 {env_path} 不存在，且找不到示例文件 {env_example_path}。\n"
            f"请手动创建 .env 文件或联系开发者提供模板。"
        )

# 加载.env
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