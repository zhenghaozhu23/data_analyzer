"""
基于Langchain的智能Agent
支持grep搜索、pandas数据处理和todo任务管理
"""
import os
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from tools import get_all_tools

# 加载环境变量
load_dotenv()


class DataAnalyserAgent:
    """数据分析器Agent"""
    
    def __init__(self, model_name: str = None, temperature: float = None, 
                 api_key: str = None, base_url: str = None):
        """
        初始化Agent
        
        Args:
            model_name: 模型名称（默认从环境变量读取）
            temperature: 模型温度参数（默认从环境变量读取）
            api_key: API密钥（默认从环境变量读取）
            base_url: API基础URL（默认从环境变量读取）
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
        
        # 获取所有工具
        self.tools = get_all_tools()
        
        # 创建prompt模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个智能数据分析助手，可以帮助用户：
1. 使用pandas进行数据处理和分析
2. 执行Python代码进行数据分析
3. 使用todo list管理复杂任务并自动执行

**重要工作流程：**
当用户提出一个复杂任务时，你必须：
1. 先使用 todo_list 工具的 "add" 操作将任务分解为多个子任务并添加到列表
2. 使用 todo_list 工具的 "list" 操作查看任务列表
3. 从第一个任务开始，逐一执行：
   a. 使用 "update" 操作将任务状态更新为 "in_progress"
   b. 执行该任务的具体工作（调用其他工具）
   c. 使用 "update" 操作将任务状态更新为 "completed"
4. 继续执行下一个任务，直到所有任务完成
5. 最后使用 "list" 操作显示所有已完成的任务
6. 给出最终总结和结果

**任务执行原则：**
- 必须按照任务列表的顺序逐个执行
- 每个任务执行前都要更新状态为 "in_progress"
- 每个任务完成后都要更新状态为 "completed"
- 不要跳过任何任务
- 执行完成后必须返回最终结果

当你分析数据时，应该：
- 先读取数据查看基本结构
- 进行必要的描述性统计
- 根据用户需求进行筛选、分组或排序
- 提供清晰的分析结果和建议

当前工作目录：{working_directory}
"""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
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
            max_iterations=50  # 增加迭代次数以支持完整执行多个任务
        )
    
    def run(self, user_input: str, working_directory: str = ".") -> str:
        """
        执行用户请求
        
        Args:
            user_input: 用户输入
            working_directory: 工作目录
            
        Returns:
            执行结果
        """
        response = self.agent_executor.invoke({
            "input": user_input,
            "working_directory": working_directory
        })
        return response["output"]
    
    def chat(self):
        """交互式对话模式"""
        print("=== 数据分析助手 Agent ===")
        print("支持功能：grep搜索、pandas数据处理、todo管理")
        print("输入 'exit' 或 'quit' 退出\n")
        
        while True:
            user_input = input("你: ")
            
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("再见！")
                break
            
            if not user_input.strip():
                continue
            
            try:
                response = self.run(user_input)
                print(f"\n助手: {response}\n")
            except Exception as e:
                print(f"\n错误: {str(e)}\n")


def main():
    """主函数"""
    # 检查API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("错误：请设置OPENAI_API_KEY环境变量")
        print("请在.env文件中添加：OPENAI_API_KEY=your_api_key")
        return
    
    # 获取配置信息
    model_name = os.getenv("OPENAI_MODEL", "gpt-4")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    print(f"使用模型: {model_name}")
    if base_url:
        print(f"API端点: {base_url}")
    
    # 创建agent
    agent = DataAnalyserAgent()
    
    # 进入对话模式
    agent.chat()


if __name__ == "__main__":
    main()

