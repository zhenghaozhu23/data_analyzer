"""
多文件 Pandas Agent 演示
展示如何使用多个数据文件和字段描述功能
"""
import os
from agents.pandas_agent import PandasAgent
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def demo_single_file():
    """演示：单个文件（向后兼容）"""
    print("\n" + "="*60)
    print("Demo 1: 单个文件（向后兼容）")
    print("="*60 + "\n")
    
    agent = PandasAgent(data_file="sample_data.csv")
    
    queries = [
        "数据有多少行多少列？",
        "显示前3行数据"
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


def demo_multiple_files():
    """演示：多个文件"""
    print("\n" + "="*60)
    print("Demo 2: 多个文件")
    print("="*60 + "\n")
    
    # 创建两个数据文件（第二个是第一个的修改版本）
    import pandas as pd
    
    # 读取原始数据
    df1 = pd.read_csv("sample_data.csv")
    
    # 创建修改后的数据
    df2 = df1.copy()
    df2['工资'] = df2['工资'] * 1.1  # 加薪10%
    
    # 保存为临时文件
    df2.to_csv("sample_data_updated.csv", index=False)
    
    print("创建了两个数据文件：")
    print("  1. sample_data.csv (原始数据)")
    print("  2. sample_data_updated.csv (加薪10%后的数据)")
    
    # 使用多个文件创建agent
    agent = PandasAgent(data_files=["sample_data.csv", "sample_data_updated.csv"])
    
    queries = [
        "对比两个文件的平均工资",
        "计算工资增长了多少"
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
    
    # 清理临时文件
    import os
    if os.path.exists("sample_data_updated.csv"):
        os.remove("sample_data_updated.csv")


def demo_with_descriptions():
    """演示：带字段描述"""
    print("\n" + "="*60)
    print("Demo 3: 带字段描述")
    print("="*60 + "\n")
    
    # 定义字段描述
    column_descriptions = {
        "姓名": "员工姓名",
        "年龄": "员工年龄（岁）",
        "部门": "员工所属部门",
        "工资": "员工月工资（元）"
    }
    
    agent = PandasAgent(
        data_file="sample_data.csv",
        column_descriptions=column_descriptions
    )
    
    print("已加载带有字段描述的数据")
    
    queries = [
        "平均年龄是多少？",
        "工资的平均值是多少元？",
        "哪个部门的人最多？"
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


def demo_shell_command():
    """演示：使用shell命令查询文件"""
    print("\n" + "="*60)
    print("Demo 4: 使用Shell命令查询文件")
    print("="*60 + "\n")
    
    agent = PandasAgent(data_file="sample_data.csv")
    
    # 这些查询会使用shell_command工具
    queries = [
        "使用shell命令查看sample_data.csv的前5行",
        "统计sample_data.csv有多少行",
        "显示sample_data.csv的列名"
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
    print("║" + "     多文件 Pandas Agent 演示".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    
    while True:
        print("\n请选择演示模式：")
        print("1. 单个文件（向后兼容）")
        print("2. 多个文件")
        print("3. 带字段描述")
        print("4. Shell命令查询")
        print("5. 全部演示")
        print("6. 退出")
        
        choice = input("\n请输入选择 (1-6): ").strip()
        
        if choice == "1":
            demo_single_file()
        elif choice == "2":
            demo_multiple_files()
        elif choice == "3":
            demo_with_descriptions()
        elif choice == "4":
            demo_shell_command()
        elif choice == "5":
            demo_single_file()
            demo_multiple_files()
            demo_with_descriptions()
            demo_shell_command()
        elif choice == "6":
            print("\n演示结束，再见！")
            break
        else:
            print("无效的选择，请输入 1-6")


if __name__ == "__main__":
    main()

