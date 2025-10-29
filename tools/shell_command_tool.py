"""
Shell命令执行工具
执行shell命令行的工具
"""
import subprocess
from typing import Type
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field


class ShellCommandInput(BaseModel):
    """命令行工具输入参数"""
    command: str = Field(description="要执行的shell命令")
    timeout: int = Field(default=30, description="命令超时时间（秒）")


class ShellCommandTool(BaseTool):
    """执行shell命令的工具"""
    name: str = "shell_command"
    description: str = (
        "执行shell命令行命令的工具。"
        "可以执行任何shell命令，如ls、cat、head、tail、wc、find等。"
        "输入应该是包含'command'（要执行的命令）的JSON字符串。"
        "注意：谨慎使用，避免执行可能破坏系统的命令。"
    )
    args_schema: Type[BaseModel] = ShellCommandInput

    def _run(self, command: str, timeout: int = 30) -> str:
        """执行shell命令"""
        try:
            if not command.strip():
                return "错误：命令不能为空"
            
            # 检查危险命令（基本安全检查）
            dangerous_commands = ['rm -rf', 'format', 'dd if=', 'mkfs', 'fdisk', 'mkfs']
            command_lower = command.lower()
            if any(danger in command_lower for danger in dangerous_commands):
                return "错误：该命令可能不安全，已被阻止"
            
            # 执行命令
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='ignore'
            )
            
            output = []
            if result.stdout:
                output.append(f"标准输出:\n{result.stdout}")
            if result.stderr:
                output.append(f"错误输出:\n{result.stderr}")
            if result.returncode != 0:
                output.append(f"退出码: {result.returncode}")
            
            return "\n".join(output) if output else "命令执行完成（无输出）"
            
        except subprocess.TimeoutExpired:
            return f"错误：命令执行超时（>{timeout}秒）"
        except Exception as e:
            return f"执行命令时出错: {str(e)}"

