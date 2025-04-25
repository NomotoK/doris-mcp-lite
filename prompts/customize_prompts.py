from server import mcp


class CustomizePrompts:
    """封装自定义的提示词"""

    def __init__(self):
        pass

    # 1. 自定义数据预处理提示
    @mcp.prompt()
    def data_preprocessing_prompt() -> str:
        """
        自定义数据预处理提示
        """
        return None