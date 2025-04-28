from doris_mcp_server.mcp_app import mcp
from mcp.server.fastmcp.prompts import base



# 1. 简单表格查询模板
@mcp.prompt()
def query_table_overview(table_name: str) -> str:
    """
    查看表格的结构和前几行数据
    """
    return (
        f"请查询 `{table_name}` 表的结构信息，并展示前 10 行数据。"
        f"\n确保格式清晰，使用表格展示内容。"
    )

@mcp.prompt(name = "table_comment_overview", description = "查看表的注释信息")
def query_table_comment(table_name: str) -> str:
    """
    查看表格的注释信息
    """
    return f"请查询 `{table_name}` 表的注释信息，这些信息用于描述表的用途。"

# 2. 汇总统计模板
@mcp.prompt()
def summarize_column(column: str, table: str) -> str:
    """
    统计某列的常见汇总信息
    """
    return f"请统计 `{table}` 表中 `{column}` 列的最大值、最小值、平均值、标准差与总和。"


# 3. 分组聚合模板
@mcp.prompt()
def groupby_analysis(group_col: str, target_col: str, table: str) -> str:
    """
    对某字段进行分组聚合分析
    """
    return (
        f"请对 `{table}` 表按 `{group_col}` 分组，统计每组在 `{target_col}` 上的均值与总和，"
        f"并按总和降序排序。"
    )


# 4. 数据趋势分析模板（近7日、近30日）
@mcp.prompt()
def trend_analysis(date_col: str, metric_col: str, table: str, days: int = 7) -> str:
    """
    绘制最近几天某指标的趋势
    """
    return (
        f"请分析 `{table}` 表中最近 {days} 天的 `{metric_col}` 变化趋势，"
        f"日期字段为 `{date_col}`。可视化建议使用折线图。"
    )


# 5. 多轮对话模板：异常值分析
@mcp.prompt()
def outlier_analysis() -> list[base.Message]:
    return [
        base.UserMessage("我想分析某个表中的异常值"),
        base.AssistantMessage("好的，请告诉我要分析哪个表，以及哪一列？"),
        base.UserMessage("表是 user_metrics，列是 daily_usage"),
        base.AssistantMessage(
            "请稍等，我将检测 `user_metrics` 表中 `daily_usage` 列的异常值，"
            "可能使用箱线图或 3σ 原则。"
        ),
    ]
