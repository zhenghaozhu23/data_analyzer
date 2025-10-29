"""
Pandas Agent 演示
基于IPython Executor的Pandas数据分析Agent
"""
import os
from agents.pandas_agent import PandasAgent
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def demo_basic_queries():
    """演示：基础数据分析查询"""
    print("\n" + "="*60)
    print("Demo 1: 基础数据分析查询")
    print("="*60 + "\n")
    
    # 创建agent（使用sample_data.csv）
    agent = PandasAgent(data_file="sample_data.csv")
    
    # 基础查询
    queries = [
        "读取数据并显示前5行",
        "数据有多少行多少列？",
        "显示每个部门的平均工资",
        "找出工资最高的员工",
        "按工资排序显示所有员工"
    ]
    
    for query in queries:
        print(f"\n{'─'*60}")
        print(f"问题: {query}")
        print(f"{'─'*60}")
        try:
            response = agent.run(query)
            print(f"回答: {response}\n")
        except Exception as e:
            print(f"错误: {str(e)}\n")


def demo_advanced_analysis():
    """演示：高级数据分析"""
    print("\n" + "="*60)
    print("Demo 2: 高级数据分析")
    print("="*60 + "\n")
    
    agent = PandasAgent(data_file="sample_data.csv")
    
    # 高级查询
    queries = [
        "统计每个部门有多少员工",
        "计算年龄和工资的相关性",
        "找出工资在平均工资以上的员工",
        "按部门分组，计算每个部门的平均年龄和工资"
    ]
    
    for query in queries:
        print(f"\n{'─'*60}")
        print(f"问题: {query}")
        print(f"{'─'*60}")
        try:
            response = agent.run(query)
            print(f"回答: {response}\n")
        except Exception as e:
            print(f"错误: {str(e)}\n")


def interactive_mode():
    """交互模式"""
    print("\n" + "="*60)
    print("Demo 3: 交互模式")
    print("="*60 + "\n")
    
    agent = PandasAgent(data_file="sample_data.csv")
    agent.chat()


def main():
    """主函数"""
    # 检查API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("错误：请设置OPENAI_API_KEY环境变量")
        print("请在.env文件中添加：OPENAI_API_KEY=your_api_key")
        return
    
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "     基于 IPython 的 Pandas Agent 演示".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    
    while True:
        print("\n请选择演示模式：")
        print("1. 基础数据分析查询")
        print("2. 高级数据分析")
        print("3. 交互模式")
        print("4. 全部演示")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == "1":
            demo_basic_queries()
        elif choice == "2":
            demo_advanced_analysis()
        elif choice == "3":
            interactive_mode()
        elif choice == "4":
            demo_basic_queries()
            demo_advanced_analysis()
        elif choice == "5":
            print("\n演示结束，再见！")
            break
        else:
            print("无效的选择，请输入 1-5")


if __name__ == "__main__":
    main()
