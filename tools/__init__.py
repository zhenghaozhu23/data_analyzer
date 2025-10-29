"""
Tools模块
包含所有Agent使用的工具
"""
# 导入IPython工具
from .ipython_executor import IPythonExecutor
from .ipython_tool import IPythonCodeTool, IPythonNotebookTool

# 导入基础工具
from .shell_command_tool import ShellCommandTool
from .pandas_tool import PandasTool
from .todo_tool import TodoTool

__all__ = [
    'IPythonExecutor', 
    'IPythonCodeTool', 
    'IPythonNotebookTool',
    'ShellCommandTool',
    'PandasTool',
    'TodoTool',
]


def get_all_tools(enable_ipython: bool = True):
    """
    获取所有工具
    
    Args:
        enable_ipython: 是否启用IPython代码执行工具
    
    Returns:
        工具列表
    """
    tools = [
        ShellCommandTool(),
        PandasTool(),
        TodoTool(),
    ]
    
    # 添加IPython工具
    if enable_ipython:
        try:
            tools.extend([
                IPythonCodeTool(),
                IPythonNotebookTool()
            ])
        except Exception as e:
            print(f"警告：IPython工具未启用，原因: {e}")
    
    return tools

