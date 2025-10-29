"""
基于IPython Kernel的代码执行工具
支持执行Python代码并与kernel交互，所有交互都以notebook形式存储
"""
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from jupyter_client import KernelManager, KernelClient
import queue
import time


class IPythonExecutor:
    """IPython Kernel执行器，将执行记录保存为notebook格式"""
    
    def __init__(self, kernel_name: str = "python3", notebook_path: str = "execution_history.ipynb"):
        """
        初始化IPython执行器
        
        Args:
            kernel_name: Kernel名称，默认为python3
            notebook_path: 保存notebook的文件路径
        """
        self.kernel_name = kernel_name
        self.notebook_path = notebook_path
        self.km = None
        self.kc = None
        self.notebook_data = None
        self._initialize_notebook()
    
    def _initialize_notebook(self):
        """初始化notebook数据结构"""
        if Path(self.notebook_path).exists():
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                self.notebook_data = json.load(f)
        else:
            self.notebook_data = {
                "cells": [],
                "metadata": {
                    "kernelspec": {
                        "display_name": "Python 3",
                        "language": "python",
                        "name": "python3"
                    },
                    "language_info": {
                        "name": "python",
                        "version": "3.x"
                    }
                },
                "nbformat": 4,
                "nbformat_minor": 4
            }
    
    def start_kernel(self):
        """启动kernel"""
        if self.km is None:
            self.km = KernelManager(kernel_name=self.kernel_name)
            self.km.start_kernel()
            self.kc = self.km.client()
            self.kc.start_channels()
            time.sleep(1)  # 等待kernel启动
    
    def stop_kernel(self):
        """停止kernel"""
        if self.kc is not None:
            self.kc.stop_channels()
        if self.km is not None:
            self.km.shutdown_kernel()
        self.km = None
        self.kc = None
    
    def execute_code(self, code: str, cell_type: str = "code", 
                    metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行Python代码并记录到notebook
        
        Args:
            code: 要执行的Python代码
            cell_type: cell类型（code或markdown）
            metadata: 额外的元数据
            
        Returns:
            执行结果字典，包含output、execution_count等
        """
        # 启动kernel（如果还没启动）
        if self.kc is None:
            self.start_kernel()
        
        # 创建新的cell
        execution_count = len([c for c in self.notebook_data['cells'] if c.get('cell_type') == 'code']) + 1
        
        cell = {
            "cell_type": cell_type,
            "metadata": metadata or {},
            "source": code.split('\n'),
        }
        
        result = {
            "execution_count": execution_count,
            "outputs": [],
            "error": None
        }
        
        if cell_type == "code":
            # 执行代码
            msg_id = self.kc.execute(code)
            
            # 获取输出
            outputs = []
            error_output = None
            
            while True:
                try:
                    msg = self.kc.get_iopub_msg(timeout=1)
                    msg_type = msg['msg_type']
                    
                    if msg_type == 'execute_result':
                        outputs.append({
                            "output_type": "execute_result",
                            "execution_count": execution_count,
                            "data": msg['content']['data'],
                            "metadata": msg['content']['metadata']
                        })
                    elif msg_type == 'display_data':
                        outputs.append({
                            "output_type": "display_data",
                            "data": msg['content']['data'],
                            "metadata": msg['content']['metadata']
                        })
                    elif msg_type == 'stream':
                        outputs.append({
                            "output_type": "stream",
                            "name": msg['content']['name'],
                            "text": msg['content']['text']
                        })
                    elif msg_type == 'error':
                        error_output = {
                            "output_type": "error",
                            "ename": msg['content']['ename'],
                            "evalue": msg['content']['evalue'],
                            "traceback": msg['content']['traceback']
                        }
                        break
                    elif msg_type == 'status' and msg['content']['execution_state'] == 'idle':
                        break
                        
                except queue.Empty:
                    # 检查执行状态
                    try:
                        reply_msg = self.kc.get_shell_msg(timeout=1)
                        if reply_msg['parent_header']['msg_id'] == msg_id:
                            if reply_msg['content']['status'] == 'error':
                                error_output = {
                                    "output_type": "error",
                                    "ename": reply_msg['content'].get('ename', 'Unknown'),
                                    "evalue": reply_msg['content'].get('evalue', 'Unknown error'),
                                    "traceback": []
                                }
                            break
                    except queue.Empty:
                        break
            
            cell["execution_count"] = execution_count
            cell["outputs"] = outputs if not error_output else [error_output]
            result["outputs"] = cell["outputs"]
            result["error"] = error_output
        
        # 添加到notebook
        self.notebook_data['cells'].append(cell)
        
        # 保存notebook
        self.save_notebook()
        
        return result
    
    def save_notebook(self):
        """保存notebook到文件"""
        with open(self.notebook_path, 'w', encoding='utf-8') as f:
            json.dump(self.notebook_data, f, indent=2, ensure_ascii=False)
    
    def add_markdown_cell(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        """添加markdown cell到notebook"""
        cell = {
            "cell_type": "markdown",
            "metadata": metadata or {},
            "source": text.split('\n')
        }
        self.notebook_data['cells'].append(cell)
        self.save_notebook()
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """获取执行历史"""
        return self.notebook_data['cells']
    
    def get_notebook_summary(self) -> str:
        """获取notebook摘要"""
        code_cells = [c for c in self.notebook_data['cells'] if c.get('cell_type') == 'code']
        markdown_cells = [c for c in self.notebook_data['cells'] if c.get('cell_type') == 'markdown']
        
        summary = f"Notebook摘要:\n"
        summary += f"- 总共有 {len(self.notebook_data['cells'])} 个cells\n"
        summary += f"- 代码cells: {len(code_cells)}\n"
        summary += f"- Markdown cells: {len(markdown_cells)}\n"
        
        if code_cells:
            summary += f"\n最后的代码执行:\n"
            last_cell = code_cells[-1]
            code = ''.join(last_cell['source']) if isinstance(last_cell['source'], list) else last_cell['source']
            summary += f"```python\n{code}\n```\n"
            
            if last_cell.get('outputs'):
                summary += "输出:\n"
                for output in last_cell['outputs']:
                    if output.get('output_type') == 'stream':
                        summary += output.get('text', '')
                    elif output.get('output_type') == 'execute_result':
                        data = output.get('data', {})
                        if 'text/plain' in data:
                            summary += data['text/plain']
        
        return summary

