from doris_mcp_server.mcp_app import mcp

# 1. 自定义数据预处理提示
@mcp.prompt()
def customize_prompt() -> str:
    """
    自定义提示
    """
    return None