# config.py
import os
from dotenv import load_dotenv
from pathlib import Path
import shutil
import re

# 确定.env路径和.env.example路径
env_dir = Path(__file__).resolve().parent
env_path = env_dir / ".env"
env_example_path = env_dir / ".env.example"


def load_environment():
    """
    加载 .env 配置
    """
    load_dotenv(dotenv_path=env_path)



def ensure_env_file():
    """
    确保 .env 文件存在，如果不存在则从 .env.example 复制
    """
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



# 尝试解析 DORIS_URL（优先级高于单独的 DB_HOST 等）
def parse_doris_url(url: str):
    """
    解析形如 doris://user:pass@host:port/dbname 的连接字符串
    """
    pattern = r"^doris:\/\/(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)\/(?P<database>\w+)$"
    match = re.match(pattern, url)
    if not match:
        raise ValueError("❌ DORIS_URL 格式不正确，应为 doris://user:pass@host:port/dbname")
    return {
        "host": match.group("host"),
        "port": int(match.group("port")),
        "user": match.group("user"),
        "password": match.group("password"),
        "database": match.group("database"),
    }



def get_db_config():
    """
    获取数据库连接配置，优先解析 DORIS_URL
    """
    if os.getenv("DORIS_URL"):
        return parse_doris_url(os.getenv("DORIS_URL"))
    else:
        return {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", 9030)),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", ""),
        }
