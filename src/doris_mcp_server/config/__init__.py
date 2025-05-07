from .config import ensure_env_file, load_environment, get_db_config
import os

DB_CONFIG = None
MCP_SERVER_NAME = None
DEBUG = None

def init_config():
    global DB_CONFIG, MCP_SERVER_NAME, DEBUG
    ensure_env_file()
    load_environment()
    DB_CONFIG = get_db_config()
    MCP_SERVER_NAME = os.getenv("MCP_SERVER_NAME", "DorisAnalytics")
    DEBUG = os.getenv("DEBUG", "false").lower() in ["1", "true", "yes"]

__all__ = ["DB_CONFIG", "MCP_SERVER_NAME", "DEBUG"]