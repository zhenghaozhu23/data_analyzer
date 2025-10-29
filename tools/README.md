# Tools模块

包含所有Agent使用的工具实现。

## 目录结构

```
tools/
├── __init__.py              # 模块初始化
├── ipython_executor.py      # IPython Kernel执行器
└── ipython_tool.py          # IPython Agent工具
```

## 模块说明

### ipython_executor.py
基于IPython Kernel的代码执行器，负责：
- 启动和管理IPython kernel
- 执行Python代码
- 捕获输出和错误
- 将执行记录保存为Jupyter Notebook格式

### ipython_tool.py
Agent集成工具，包括：
- `IPythonCodeTool` - 执行Python代码
- `IPythonNotebookTool` - 管理notebook

## 使用方式

### 从tools模块导入

```python
from tools import IPythonExecutor, IPythonCodeTool, IPythonNotebookTool
```

### 或者从子模块导入

```python
from tools.ipython_executor import IPythonExecutor
from tools.ipython_tool import IPythonCodeTool, IPythonNotebookTool
```

## 完整示例

```python
from tools import IPythonCodeTool

# 创建工具
tool = IPythonCodeTool(notebook_path="my_notebook.ipynb")

# 执行代码
result = tool._run(code="print('Hello, World!')")
print(result)
```

## 集成到Agent

```python
from agent import DataAnalyserAgent

agent = DataAnalyserAgent()
# IPython工具已自动加载
agent.run("执行Python代码：import math; print(math.pi)")
```

## 依赖

```bash
pip install jupyter-client ipykernel
```

## 详细文档

- [IPython工具详细说明](../../IPYTHON_README.md)
- [功能总结](../../IPYTHON_FEATURE_SUMMARY.md)

