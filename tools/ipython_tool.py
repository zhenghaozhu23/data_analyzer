"""
IPython执行工具 - 用于Agent的代码执行
"""
from typing import Type, Optional
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from tools.ipython_executor import IPythonExecutor
from datetime import datetime
import uuid
from pathlib import Path


class IPythonCodeInput(BaseModel):
    """IPython代码执行工具输入参数"""
    code: str = Field(description="要执行的Python代码")
    execute: bool = Field(default=True, description="是否立即执行代码")
    add_markdown: bool = Field(default=False, description="是否为结果添加markdown说明")


class IPythonCodeTool(BaseTool):
    """使用IPython kernel执行Python代码的工具"""
    name: str = "ipython_execute"
    description: str = (
        "执行Python代码的工具。"
        "可以执行任意的Python代码，包括数据分析和可视化。"
        "所有执行的代码都会自动保存到notebook文件中。"
        "输入应该是包含'code'（要执行的代码）的JSON字符串。"
    )
    args_schema: Type[BaseModel] = IPythonCodeInput
    executor: Optional[IPythonExecutor] = None
    notebook_path: str = "execution_history.ipynb"
    
    def __init__(self, notebook_path: str = "execution_history.ipynb", **kwargs):
        super().__init__(**kwargs)
        self.notebook_path = notebook_path
        if self.executor is None:
            self.executor = IPythonExecutor(notebook_path=notebook_path)
    
    def _run(self, code: str, execute: bool = True, add_markdown: bool = False) -> str:
        """执行代码"""
        try:
            if not code.strip():
                return "错误：代码不能为空"
            
            # 添加markdown注释（可选）
            if add_markdown:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.executor.add_markdown_cell(f"## 执行时间: {timestamp}\n\n执行以下代码：")
            
            # 执行代码
            result = self.executor.execute_code(code)
            
            # 收集输出
            output_text = []
            
            if result.get("error"):
                error = result["error"]
                output_text.append(f"错误: {error['ename']}")
                output_text.append(f"{error['evalue']}")
                if error.get('traceback'):
                    output_text.append("\n".join(error['traceback']))
            
            if result.get("outputs"):
                for output in result["outputs"]:
                    output_type = output.get('output_type')
                    
                    if output_type == 'stream':
                        text = output.get('text', '')
                        output_text.append(text)
                    
                    elif output_type == 'execute_result':
                        data = output.get('data', {})
                        # 优先显示text/plain格式
                        if 'text/plain' in data:
                            output_text.append(data['text/plain'])
                        elif 'text/html' in data:
                            output_text.append(data['text/html'])
                        elif 'image/png' in data:
                            output_text.append(f"[图像输出 - base64长度: {len(data['image/png'])}]")
                        else:
                            output_text.append(str(data))
                    
                    elif output_type == 'display_data':
                        data = output.get('data', {})
                        if 'text/plain' in data:
                            output_text.append(data['text/plain'])
            
            result_str = "\n".join(output_text)
            
            if not result_str.strip():
                result_str = "代码执行完成（无输出）"
            
            return f"代码执行结果:\n{result_str}"
            
        except Exception as e:
            return f"执行代码时出错: {str(e)}"
    
    def __del__(self):
        """清理资源"""
        if self.executor:
            self.executor.stop_kernel()


class IPythonNotebookInput(BaseModel):
    """Notebook操作输入参数"""
    action: str = Field(description="操作类型：summary（获取摘要）, history（获取历史）, clear（清空）")
    notebook_path: str = Field(default="execution_history.ipynb", description="Notebook文件路径")


class IPythonNotebookTool(BaseTool):
    """管理notebook的工具"""
    name: str = "ipython_notebook"
    description: str = (
        "管理代码执行历史和notebook的工具。"
        "支持的操作：summary（获取notebook摘要）, history（获取完整历史）, clear（清空历史）。"
        "输入应该是包含'action'（操作类型）的JSON字符串。"
    )
    args_schema: Type[BaseModel] = IPythonNotebookInput
    
    def _run(self, action: str, notebook_path: str = "execution_history.ipynb") -> str:
        """执行notebook操作"""
        try:
            executor = IPythonExecutor(notebook_path=notebook_path)
            
            if action == "summary":
                return executor.get_notebook_summary()
            
            elif action == "history":
                cells = executor.get_execution_history()
                if not cells:
                    return "Notebook为空"
                
                result = f"Notebook包含 {len(cells)} 个cells:\n\n"
                for i, cell in enumerate(cells, 1):
                    cell_type = cell.get('cell_type', 'unknown')
                    source = cell.get('source', [])
                    if isinstance(source, list):
                        code = '\n'.join(source)
                    else:
                        code = source
                    
                    result += f"### Cell {i} ({cell_type}):\n"
                    result += f"```\n{code}\n```\n"
                    result += f"---\n"
                
                return result
            
            elif action == "clear":
                executor.notebook_data['cells'] = []
                executor.save_notebook()
                return "Notebook已清空"
            
            else:
                return f"未知操作: {action}. 支持的操作: summary, history, clear"
                
        except Exception as e:
            return f"执行notebook操作时出错: {str(e)}"

