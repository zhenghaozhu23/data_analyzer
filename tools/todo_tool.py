"""
Todo List任务管理工具
用于管理和追踪任务列表
"""
import json
import os
from typing import Type, List, Dict, Any
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from pathlib import Path


class TodoTask(BaseModel):
    """任务模型"""
    id: int = Field(description="任务ID")
    description: str = Field(description="任务描述")
    status: str = Field(description="任务状态：pending, in_progress, completed, cancelled")
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status
        }


class TodoListInput(BaseModel):
    """Todo工具输入参数"""
    action: str = Field(description="操作类型：add（添加任务）, complete（完成任务）, list（列出任务）, remove（删除任务）, clear（清空列表）, update（更新任务状态）")
    task_id: int = Field(default=None, description="任务ID（用于complete, remove, update操作）")
    description: str = Field(default="", description="任务描述（用于add操作）")
    status: str = Field(default="pending", description="任务状态：pending, in_progress, completed, cancelled（用于update操作）")


class TodoTool(BaseTool):
    """Todo任务列表管理工具"""
    name: str = "todo_list"
    description: str = (
        "管理任务列表（todo list）的工具。"
        "支持的操作："
        "- add：添加新任务"
        "- list：列出所有任务"
        "- complete：标记任务为完成"
        "- remove：删除任务"
        "- clear：清空所有任务"
        "- update：更新任务状态"
        "任务状态包括：pending（待完成）、in_progress（进行中）、completed（已完成）、cancelled（已取消）。"
        "输入应该是包含'action'（操作类型）和相关参数的JSON字符串。"
    )
    args_schema: Type[BaseModel] = TodoListInput
    
    def __init__(self, storage_file: str = "todo_list.json", **kwargs):
        super().__init__(**kwargs)
        self._storage_file = storage_file
        self._tasks: List[TodoTask] = []
        self._load_tasks()
    
    def _load_tasks(self) -> None:
        """从文件加载任务"""
        try:
            if os.path.exists(self._storage_file):
                with open(self._storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._tasks = [
                        TodoTask(**task_data) 
                        for task_data in data.get('tasks', [])
                    ]
            else:
                self._tasks = []
        except Exception as e:
            print(f"加载任务列表失败: {e}")
            self._tasks = []
    
    def _save_tasks(self) -> None:
        """保存任务到文件"""
        try:
            # 如果文件路径包含目录，创建目录
            dir_path = os.path.dirname(self._storage_file)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            with open(self._storage_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'tasks': [task.to_dict() for task in self._tasks]
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存任务列表失败: {e}")
    
    def _get_next_id(self) -> int:
        """获取下一个可用的任务ID"""
        if not self._tasks:
            return 1
        return max(task.id for task in self._tasks) + 1
    
    def _run(
        self, 
        action: str, 
        task_id: int = None, 
        description: str = "", 
        status: str = "pending"
    ) -> str:
        """执行todo操作"""
        try:
            action = action.lower()
            
            if action == "add":
                if not description.strip():
                    return "错误：任务描述不能为空"
                
                new_task = TodoTask(
                    id=self._get_next_id(),
                    description=description.strip(),
                    status="pending"
                )
                self._tasks.append(new_task)
                self._save_tasks()
                return f"成功添加任务 #{new_task.id}: {new_task.description}"
            
            elif action == "list":
                if not self._tasks:
                    return "当前没有任务"
                
                # 按状态分组显示
                pending = [t for t in self._tasks if t.status == "pending"]
                in_progress = [t for t in self._tasks if t.status == "in_progress"]
                completed = [t for t in self._tasks if t.status == "completed"]
                cancelled = [t for t in self._tasks if t.status == "cancelled"]
                
                result = "=== Todo List ===\n\n"
                
                if pending:
                    result += f"📋 待完成 ({len(pending)}):\n"
                    for task in pending:
                        result += f"  [{task.id}] {task.description}\n"
                    result += "\n"
                
                if in_progress:
                    result += f"🔄 进行中 ({len(in_progress)}):\n"
                    for task in in_progress:
                        result += f"  [{task.id}] {task.description}\n"
                    result += "\n"
                
                if completed:
                    result += f"✅ 已完成 ({len(completed)}):\n"
                    for task in completed:
                        result += f"  [{task.id}] {task.description}\n"
                    result += "\n"
                
                if cancelled:
                    result += f"❌ 已取消 ({len(cancelled)}):\n"
                    for task in cancelled:
                        result += f"  [{task.id}] {task.description}\n"
                
                result += f"\n总计: {len(self._tasks)} 个任务"
                return result
            
            elif action == "complete":
                if task_id is None:
                    return "错误：需要提供task_id参数"
                
                task = next((t for t in self._tasks if t.id == task_id), None)
                if not task:
                    return f"错误：找不到任务 #{task_id}"
                
                task.status = "completed"
                self._save_tasks()
                return f"成功完成任务 #{task_id}: {task.description}"
            
            elif action == "remove":
                if task_id is None:
                    return "错误：需要提供task_id参数"
                
                task = next((t for t in self._tasks if t.id == task_id), None)
                if not task:
                    return f"错误：找不到任务 #{task_id}"
                
                description = task.description
                self._tasks.remove(task)
                self._save_tasks()
                return f"成功删除任务 #{task_id}: {description}"
            
            elif action == "clear":
                count = len(self._tasks)
                self._tasks = []
                self._save_tasks()
                return f"成功清空所有任务（共删除 {count} 个任务）"
            
            elif action == "update":
                if task_id is None:
                    return "错误：需要提供task_id参数"
                
                if status not in ["pending", "in_progress", "completed", "cancelled"]:
                    return f"错误：无效的状态 '{status}'。有效状态：pending, in_progress, completed, cancelled"
                
                task = next((t for t in self._tasks if t.id == task_id), None)
                if not task:
                    return f"错误：找不到任务 #{task_id}"
                
                old_status = task.status
                task.status = status
                self._save_tasks()
                
                status_map = {
                    "pending": "待完成",
                    "in_progress": "进行中",
                    "completed": "已完成",
                    "cancelled": "已取消"
                }
                
                return f"成功更新任务 #{task_id} 的状态: {status_map.get(old_status, old_status)} → {status_map.get(status, status)}"
            
            elif action == "start":
                # 便捷方法：开始任务
                if task_id is None:
                    return "错误：需要提供task_id参数"
                
                task = next((t for t in self._tasks if t.id == task_id), None)
                if not task:
                    return f"错误：找不到任务 #{task_id}"
                
                task.status = "in_progress"
                self._save_tasks()
                return f"开始执行任务 #{task_id}: {task.description}"
            
            else:
                return f"未知操作: {action}. 支持的操作: add, list, complete, remove, clear, update, start"
                
        except Exception as e:
            return f"执行todo操作时出错: {str(e)}"

