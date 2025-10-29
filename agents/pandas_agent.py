"""
基于IPython的Pandas Agent
使用IPythonExecutor执行pandas代码操作数据文件
"""
import os
import sys
from typing import Optional, List, Dict, Any
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from tools import IPythonCodeTool, IPythonNotebookTool
import pandas as pd
from pathlib import Path
import ipykernel
# 加载环境变量
load_dotenv()


def _ensure_ipykernel_installed():
    """确保 ipykernel 已安装并注册"""
    try:
        import ipykernel
    except ImportError:
        print("错误：未找到 ipykernel，正在安装...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ipykernel"])
        import ipykernel
    
    # 确保 kernel 已注册
    try:
        from jupyter_client.kernelspec import KernelSpecManager
        ksm = KernelSpecManager()
        kernels = ksm.list_kernel_specs()
        if 'python3' not in kernels:
            print("正在注册 python3 kernel...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "ipykernel", "install", "--user", "--name", "python3", "--display-name", "Python 3"])
    except Exception as e:
        print(f"警告：无法自动配置 kernel: {e}")
        print("请手动运行: python -m ipykernel install --user --name python3")


# 尝试确保 kernel 已安装
try:
    _ensure_ipykernel_installed()
except Exception as e:
    print(f"警告：kernel 配置检查失败: {e}")


class PandasAgent:
    """基于IPython的Pandas Agent，通过执行Python代码操作数据"""
    
    def __init__(self, 
                 data_file: Optional[str] = None,
                 data_files: Optional[List[str]] = None,
                 column_descriptions: Optional[Dict[str, str]] = None,
                 model_name: Optional[str] = None, 
                 temperature: Optional[float] = None,
                 api_key: Optional[str] = None, 
                 base_url: Optional[str] = None,
                 notebook_path: str = "pandas_execution_history.ipynb"):
        """
        初始化Pandas Agent
        
        Args:
            data_file: 单个数据文件路径（CSV、Excel等，向后兼容）
            data_files: 多个数据文件路径列表
            column_descriptions: 字段描述字典，格式：{列名: 描述}
            model_name: 模型名称（默认从环境变量读取）
            temperature: 模型温度参数（默认从环境变量读取）
            api_key: API密钥（默认从环境变量读取）
            base_url: API基础URL（默认从环境变量读取）
            notebook_path: notebook保存路径
        """
        # 从环境变量读取配置
        model_name = model_name or os.getenv("OPENAI_MODEL", "gpt-4")
        temperature = temperature or float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        base_url = base_url or os.getenv("OPENAI_BASE_URL")
        
        # 构建LLM配置参数
        llm_params = {
            "model_name": model_name,
            "temperature": temperature,
            "api_key": api_key
        }
        
        # 如果提供了base_url，则添加到配置中
        if base_url:
            llm_params["base_url"] = base_url
        
        # 初始化LLM
        self.llm = ChatOpenAI(**llm_params)
        
        # 处理数据文件：支持单个文件（向后兼容）和多个文件
        if data_files:
            self.data_files = data_files
        elif data_file:
            self.data_files = [data_file]
        else:
            self.data_files = []
        
        # 存储字段描述
        self.column_descriptions = column_descriptions or {}
        
        # 初始化工具
        self.ipython_tool = IPythonCodeTool(notebook_path=notebook_path)
        self.notebook_tool = IPythonNotebookTool()
        self.tools = [self.ipython_tool, self.notebook_tool]
        
        # 创建prompt模板
        self.prompt = self._create_prompt()
        
        # 创建agent
        self.agent = create_openai_tools_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # 创建agent执行器
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=15
        )
        
        # 如果提供了数据文件，加载并查看基本信息
        if self.data_files:
            self._initialize_data()
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """创建prompt模板"""
        data_info = ""
        
        # 处理多个文件
        if self.data_files:
            file_infos = []
            for i, file_path in enumerate(self.data_files, 1):
                if Path(file_path).exists():
                    try:
                        df = pd.read_csv(file_path)
                        columns = df.columns.tolist()
                        
                        # 如果有字段描述，添加到列信息中
                        column_list = []
                        for col in columns:
                            if col in self.column_descriptions:
                                column_list.append(f"{col} ({self.column_descriptions[col]})")
                            else:
                                column_list.append(col)
                        
                        file_infos.append(f"""
文件{i}: {file_path}
  - 数据行数: {len(df)}
  - 数据列: {', '.join(column_list)}
""")
                    except Exception as e:
                        file_infos.append(f"文件{i}: {file_path} (读取出错: {str(e)})")
                else:
                    file_infos.append(f"文件{i}: {file_path} (文件不存在)")
            
            data_info = "可用的数据文件:\n" + "\n".join(file_infos)
        
        prompt_content = f"""你是一个专门使用pandas进行数据分析的AI助手。

{data_info}

你可以通过以下方式帮助用户：
1. 使用Python代码读取和操作数据文件
2. 进行数据筛选、分组、聚合、排序等操作
3. 进行统计分析、可视化
4. 数据清洗和预处理

重要提示：
- 使用 `ipython_execute` 工具来执行Python代码
- 代码执行的第一个cell应该导入必要的库（如 pandas, matplotlib, seaborn 等）
- 如果提供了数据文件，可以通过 `pd.read_csv('文件路径')` 来读取
- 所有执行的代码都会自动保存到notebook中
- 使用 `ipython_notebook` 工具的 `summary` 操作可以查看执行历史

代码编写规范：
1. 导入所有需要的库
2. 读取数据文件
3. 进行数据操作
4. 显示结果（使用print或直接返回结果）

当前工作目录：.
"""
        
        return ChatPromptTemplate.from_messages([
            ("system", prompt_content),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
    
    def _initialize_data(self):
        """初始化数据文件"""
        if not self.data_files:
            return
        
        print(f"正在加载 {len(self.data_files)} 个数据文件...")
        
        # 遍历所有文件
        for i, file_path in enumerate(self.data_files, 1):
            print(f"\n文件 {i}: {file_path}")
            
            # 尝试读取数据基本信息
            try:
                if Path(file_path).exists():
                    df = pd.read_csv(file_path)
                    print(f"  ✓ 成功加载: {len(df)} 行, {len(df.columns)} 列")
                    
                    # 显示列信息（如果有描述，显示描述）
                    columns = df.columns.tolist()
                    column_info = []
                    for col in columns:
                        if col in self.column_descriptions:
                            column_info.append(f"{col} ({self.column_descriptions[col]})")
                        else:
                            column_info.append(col)
                    
                    print(f"  列名: {', '.join(column_info)}")
                else:
                    print(f"  ⚠ 文件不存在")
            except Exception as e:
                print(f"  ⚠ 读取数据文件时出错: {str(e)}")
    
    def run(self, query: str) -> str:
        """
        执行数据分析查询
        
        Args:
            query: 用户查询
            
        Returns:
            查询结果
        """
        return self.agent_executor.invoke({
            "input": query
        })["output"]
    
    def chat(self):
        """交互式对话模式"""
        print("\n=== Pandas数据分析Agent ===")
        if self.data_files:
            print(f"已加载 {len(self.data_files)} 个数据文件")
            for i, file_path in enumerate(self.data_files, 1):
                print(f"  {i}. {file_path}")
        print("支持功能：数据分析、筛选、分组、聚合、统计等")
        print("输入 'exit' 或 'quit' 退出")
        print("输入 'summary' 查看执行历史摘要")
        print("输入 'history' 查看完整执行历史\n")
        
        while True:
            user_input = input("你: ").strip()
            
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("再见！")
                break
            
            if not user_input:
                continue
            
            # 特殊命令：查看历史
            if user_input.lower() == 'summary':
                try:
                    summary = self.notebook_tool._run(action="summary")
                    print(f"\n{summary}\n")
                    continue
                except Exception as e:
                    print(f"\n错误: {str(e)}\n")
                    continue
            
            if user_input.lower() == 'history':
                try:
                    history = self.notebook_tool._run(action="history")
                    print(f"\n{history}\n")
                    continue
                except Exception as e:
                    print(f"\n错误: {str(e)}\n")
                    continue
            
            # 执行查询
            try:
                response = self.run(user_input)
                print(f"\n助手: {response}\n")
            except Exception as e:
                print(f"\n错误: {str(e)}\n")
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'ipython_tool') and self.ipython_tool:
            if hasattr(self.ipython_tool, 'executor') and self.ipython_tool.executor:
                self.ipython_tool.executor.stop_kernel()


def main():
    """主函数 - 演示Pandas Agent"""
    import sys
    
    # 检查API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("错误：请设置OPENAI_API_KEY环境变量")
        print("请在.env文件中添加：OPENAI_API_KEY=your_api_key")
        return
    
    # 获取命令行参数
    data_files = ["sample_data.csv"]
    if len(sys.argv) > 1:
        # 支持多个文件，用逗号分隔
        data_files = [f.strip() for f in sys.argv[1].split(',') if f.strip()]
    
    # 检查数据文件是否存在
    existing_files = [f for f in data_files if Path(f).exists()]
    if not existing_files:
        print(f"警告：所有数据文件都不存在")
        data_files = []
    else:
        data_files = existing_files
        if len(data_files) < len(sys.argv) - 1:
            print(f"警告：部分文件不存在，已加载 {len(data_files)} 个有效文件")
    
    # 获取配置信息
    model_name = os.getenv("OPENAI_MODEL", "gpt-4")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    print(f"使用模型: {model_name}")
    if base_url:
        print(f"API端点: {base_url}")
    
    # 创建agent
    agent = PandasAgent(data_files=data_files if data_files else None)
    
    # 进入对话模式
    agent.chat()


if __name__ == "__main__":
    main()
