# 数据分析助手 Agent

基于 Langchain 的智能数据分析助手，支持文件搜索、数据处理和任务管理。

## 功能特性

1. **Grep工具** - 使用grep命令在文件中搜索特定模式
2. **Pandas工具** - 使用pandas进行数据处理和分析
3. **Todo工具** - 管理任务列表，根据todo执行任务
4. **IPython工具** - 基于IPython Kernel执行Python代码，所有交互保存为Notebook格式

## 安装

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 安装并注册 Python kernel（为 IPython 工具使用）：
```bash
python -m ipykernel install --user --name python3 --display-name "Python 3"
```

3. 设置环境变量：
```bash
cp env_example.txt .env
# 编辑.env文件，配置你的模型参数
```

**环境变量配置说明**：
- `OPENAI_API_KEY`: OpenAI API密钥（必需）
- `OPENAI_MODEL`: 模型名称（默认：gpt-4）
- `OPENAI_TEMPERATURE`: 模型温度参数（默认：0.3）
- `OPENAI_BASE_URL`: 自定义API端点（可选，用于本地部署或其他OpenAI兼容服务）

## 使用方法

### 方式1：交互式对话

```bash
python agent.py
```

### 方式2：在代码中使用

```python
from agent import DataAnalyserAgent

agent = DataAnalyserAgent()
result = agent.run("帮我分析sample_data.csv文件")
print(result)
```

### 方式3：运行示例

```bash
python example.py
```

### 方式4：Pandas Agent Demo (旧版，基于LangChain)

```bash
python pandas_demo.py
```

**Pandas Agent 详细说明**: [PANDAS_AGENT_README.md](PANDAS_AGENT_README.md)

### 方式5：Pandas Agent (新版，基于IPython)

```bash
# 使用默认的sample_data.csv
python agents/pandas_agent.py

# 指定数据文件
python agents/pandas_agent.py your_data.csv

# 运行演示
python pandas_agent_demo.py
```

**新Pandas Agent 详细说明**: [PANDAS_AGENT_DEMO.md](PANDAS_AGENT_DEMO.md)

## 使用示例

### 1. Grep文件搜索

```python
# 搜索文件中的特定模式
agent.run("在tools.py文件中搜索包含'class'的行")
```

### 2. Pandas数据处理

```python
# 读取CSV文件
agent.run("读取sample_data.csv文件")

# 描述性统计
agent.run("对sample_data.csv进行描述性统计")

# 数据筛选
agent.run("找出工资超过10000的员工")

# 分组聚合
agent.run("按部门统计平均工资")
```

### 3. Todo任务管理

```python
# 添加任务
agent.run("添加任务：完成数据分析")

# 列出任务
agent.run("列出所有任务")

# 完成任务
agent.run("完成任务1")

# 清空任务
agent.run("清空任务列表")
```

### 4. IPython代码执行

```python
# 执行任意Python代码
agent.run("执行Python代码：import math; print(math.pi)")

# 数据分析（使用pandas）
agent.run("""
import pandas as pd
import numpy as np
data = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6]})
print(data.describe())
""")

# 查看执行历史
agent.run("查看代码执行历史")
```

所有执行的代码都会自动保存到 `execution_history.ipynb` 文件中。

**详细说明**: [IPYTHON_README.md](IPYTHON_README.md)

### 5. 复杂场景

```python
# 多步骤任务
agent.run("""
请帮我执行以下任务：
1. 添加任务："分析员工数据"
2. 读取sample_data.csv文件
3. 找出工资超过10000的员工
4. 按部门统计平均工资
5. 完成任务1
""")
```

## 项目结构

```
data_analyser/
├── agent.py              # Agent主程序
├── tools.py              # 自定义工具实现
├── ipython_example.py    # IPython使用示例
├── test_ipython.py       # IPython测试脚本
├── pandas_demo.py        # Pandas Agent演示
├── example.py            # 使用示例
├── test_config.py        # 配置测试脚本
├── requirements.txt      # 依赖包列表
├── setup.sh             # 快速安装脚本
├── CONFIG.md            # 详细配置文档
├── PANDAS_AGENT_README.md  # Pandas Agent说明
├── IPYTHON_README.md     # IPython工具说明
├── env_example.txt      # 环境变量示例
├── README.md            # 项目文档
├── sample_data.csv      # 示例数据文件
├── tools/               # 工具模块
│   ├── __init__.py
│   ├── ipython_executor.py    # IPython Kernel执行器
│   └── ipython_tool.py         # IPython工具（Agent集成）
├── agents/              # Agent模块
│   ├── __init__.py
│   └── pandas_agent.py  # Pandas Agent (基于IPython)
├── pandas_agent_demo.py # Pandas Agent演示
└── test_files/          # 测试文件目录
    └── sample.txt       # 示例文本文件
```

## 工具说明

### GrepTool
- **功能**: 使用grep命令搜索文件内容
- **参数**: pattern（搜索模式）, file_path（文件路径）, case_sensitive（是否区分大小写）

### PandasTool
- **功能**: 使用pandas进行数据处理
- **操作**: read_csv, describe, head, filter, groupby, sort, columns

### TodoTool
- **功能**: 管理任务列表
- **操作**: add（添加）, list（列表）, complete（完成）, clear（清空）

### IPythonCodeTool
- **功能**: 执行任意Python代码
- **特性**: 支持完整的Python环境，代码自动保存为notebook格式
- **详细说明**: 见 [IPYTHON_README.md](IPYTHON_README.md)

### IPythonNotebookTool
- **功能**: 管理代码执行历史和notebook
- **操作**: summary（获取摘要）, history（获取历史）, clear（清空）

## 环境要求

- Python 3.8+
- OpenAI API Key或兼容的API端点
- 已安装grep命令（Mac/Linux自带，Windows需要安装Git或使用WSL）

## 配置说明

### 使用OpenAI API
```env
OPENAI_API_KEY=sk-xxxxx
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.3
```

### 使用本地部署的模型（如Ollama）
```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=llama2
OPENAI_BASE_URL=http://localhost:11434/v1
```

### 使用其他OpenAI兼容服务
```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=your-model-name
OPENAI_BASE_URL=https://your-api-endpoint.com/v1
```

**详细配置说明请参考**: [CONFIG.md](CONFIG.md)

## 测试配置

运行测试脚本验证配置是否正确：

```bash
python test_config.py
```

这将显示当前的配置信息并尝试创建Agent。

## 注意事项

1. 需要有效的OpenAI API密钥或可访问的API端点
2. Grep工具需要系统支持grep命令
3. 建议使用Python虚拟环境
4. 可以通过环境变量灵活切换不同的模型服务
5. `.env`文件不要提交到版本控制系统
6. IPython 工具需要安装并注册 Python kernel（见安装步骤2）
7. 如果遇到 "No such kernel" 错误，运行：`python -m ipykernel install --user --name python3`

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

