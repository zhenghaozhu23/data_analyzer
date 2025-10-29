"""
Pandas数据处理工具
使用pandas进行数据处理操作
"""
import pandas as pd
from typing import Type
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field


class PandasInput(BaseModel):
    """Pandas工具输入参数"""
    operation: str = Field(description="要执行的操作（read_csv, describe, filter, groupby等）")
    file_path: str = Field(default="", description="CSV文件路径")
    query: str = Field(default="", description="查询或操作的具体内容")
    output_format: str = Field(default="table", description="输出格式：table, csv, json")


class PandasTool(BaseTool):
    """使用pandas操作数据的工具"""
    name: str = "pandas_operation"
    description: str = (
        "使用pandas进行数据处理操作。"
        "支持的操作：read_csv（读取CSV文件）, describe（描述统计）, "
        "filter（筛选数据）, groupby（分组聚合）, sort（排序）等。"
        "输入应该是包含'operation'（操作类型）和相关参数的JSON字符串。"
    )
    args_schema: Type[BaseModel] = PandasInput

    def _run(self, operation: str, file_path: str = "", query: str = "", output_format: str = "table") -> str:
        """执行pandas操作"""
        try:
            if operation == "read_csv":
                if not file_path:
                    return "错误：需要提供file_path参数"
                df = pd.read_csv(file_path)
                return f"成功读取文件，共 {len(df)} 行, {len(df.columns)} 列\n列名: {', '.join(df.columns.tolist())}"
            
            elif operation == "describe":
                if not file_path:
                    return "错误：需要提供file_path参数"
                df = pd.read_csv(file_path)
                return f"数据统计信息:\n{df.describe().to_string()}"
            
            elif operation == "head":
                if not file_path:
                    return "错误：需要提供file_path参数"
                df = pd.read_csv(file_path)
                n = int(query) if query.isdigit() else 5
                return f"前{n}行数据:\n{df.head(n).to_string()}"
            
            elif operation == "filter":
                if not file_path:
                    return "错误：需要提供file_path参数"
                df = pd.read_csv(file_path)
                if query:
                    # 尝试执行查询
                    filtered_df = df.query(query)
                    return f"筛选结果（共{len(filtered_df)}行）:\n{filtered_df.to_string()}"
                return df.to_string()
            
            elif operation == "groupby":
                if not file_path:
                    return "错误：需要提供file_path参数"
                df = pd.read_csv(file_path)
                # 示例：按指定列分组并计算平均值
                result = df.groupby(query).mean()
                return f"分组聚合结果:\n{result.to_string()}"
            
            elif operation == "sort":
                if not file_path:
                    return "错误：需要提供file_path参数"
                df = pd.read_csv(file_path)
                parts = query.split(',')
                column = parts[0].strip()
                ascending = parts[1].strip().lower() == 'true' if len(parts) > 1 else True
                sorted_df = df.sort_values(by=column, ascending=ascending)
                return f"排序结果（按{column}）：\n{sorted_df.to_string()}"
            
            elif operation == "columns":
                if not file_path:
                    return "错误：需要提供file_path参数"
                df = pd.read_csv(file_path)
                return f"列名列表:\n{', '.join(df.columns.tolist())}"
            
            else:
                return f"未知操作: {operation}. 支持的操作: read_csv, describe, head, filter, groupby, sort, columns"
                
        except Exception as e:
            return f"执行pandas操作时出错: {str(e)}"

