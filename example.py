"""
使用示例：展示如何使用DataAnalyserAgent
"""
import os
from dotenv import load_dotenv
from agent import DataAnalyserAgent

# 加载环境变量
load_dotenv()

def example_grep():
    """演示grep功能"""
    print("=== Grep示例 ===")
    agent = DataAnalyserAgent()
    
    # 在Python文件中搜索特定模式
    result = agent.run(
        "使用grep工具在tools.py文件中搜索包含'class'的行",
        working_directory="."
    )
    print(result)
    print()


def example_pandas():
    """演示pandas功能"""
    print("=== Pandas示例 ===")
    agent = DataAnalyserAgent()
    
    # 读取并分析CSV文件
    result = agent.run(
        "读取sample_data.csv文件，查看前5行数据",
        working_directory="."
    )
    print(result)
    print()
    
    # 描述性统计
    result = agent.run(
        "对sample_data.csv文件进行描述性统计分析",
        working_directory="."
    )
    print(result)
    print()


def example_todo():
    """演示todo功能"""
    print("=== Todo示例 ===")
    agent = DataAnalyserAgent()
    
    # 添加任务
    result = agent.run("添加任务：完成数据分析报告")
    print(result)
    
    result = agent.run("添加任务：整理代码")
    print(result)
    
    # 列出所有任务
    result = agent.run("列出所有任务")
    print(result)
    
    # 完成任务
    result = agent.run("完成任务1")
    print(result)
    
    # 再次列出
    result = agent.run("列出所有任务")
    print(result)
    print()


def example_complex():
    """演示复杂场景：根据todo执行任务"""
    print("=== 复杂场景示例 ===")
    agent = DataAnalyserAgent()
    
    # 多步骤任务
    prompt = """
    请帮我执行以下任务：
    1. 添加一个任务："分析员工数据"
    2. 读取sample_data.csv文件
    3. 找出工资超过10000的员工
    4. 按部门统计平均工资
    5. 完成任务1
    """
    
    result = agent.run(prompt, working_directory=".")
    print(result)
    print()


if __name__ == "__main__":
    # 检查API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("错误：请设置OPENAI_API_KEY环境变量")
        print("请在.env文件中添加：OPENAI_API_KEY=your_api_key")
        exit(1)
    
    # 显示当前配置
    model_name = os.getenv("OPENAI_MODEL", "gpt-4")
    base_url = os.getenv("OPENAI_BASE_URL", "默认OpenAI API")
    print(f"使用模型: {model_name}")
    print(f"API端点: {base_url}")
    print("\n开始运行示例...\n")
    
    # 运行各个示例
    example_grep()
    example_pandas()
    example_todo()
    example_complex()
    
    print("示例运行完成！")

