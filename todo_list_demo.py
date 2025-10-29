"""
Todo List功能演示
展示如何使用Todo Tool进行任务管理
"""
from agent import DataAnalyserAgent
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def demo_todo_list():
    """演示Todo List功能"""
    
    # 检查API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("错误：请设置OPENAI_API_KEY环境变量")
        print("请在.env文件中添加：OPENAI_API_KEY=your_api_key")
        return
    
    print("=== Todo List 自动执行功能演示 ===")
    print("\n这个演示展示了Agent如何自动使用Todo List管理并执行任务。")
    print("\nAgent会：")
    print("1. 自动将复杂任务分解为多个子任务")
    print("2. 创建任务列表")
    print("3. 自动逐个执行所有任务")
    print("4. 跟踪每个任务的状态")
    print("5. 返回最终结果")
    print("\n**注意：你只需要提出任务需求，Agent会自动完成所有步骤！**")
    print("\n开始演示...\n")
    
    # 创建agent
    agent = DataAnalyserAgent()
    
    # 演示示例 - 展示自动化执行
    examples = [
        "帮我分析一个数据分析项目，包含以下步骤：1. 检查数据文件是否存在 2. 读取和探索数据 3. 进行数据清洗 4. 统计分析 5. 生成可视化图表",
        # 注意：上面的请求会自动创建todo list并逐个执行，不需要额外的命令
    ]
    
    print("执行以下示例：")
    for i, example in enumerate(examples, 1):
        print(f"\n示例 {i}: {example}")
        print("-" * 60)
        
        try:
            response = agent.run(example)
            print(f"\n助手: {response}\n")
        except Exception as e:
            print(f"\n错误: {str(e)}\n")
        
        # 交互式提示
        if i < len(examples):
            input("\n按回车继续...")
    
    print("\n演示完成！")
    print("\n现在你可以使用以下方式与Agent交互：")
    print("\n方式1：直接提出复杂任务，让Agent自动分解并执行")
    print("  例如：'帮我分析销售数据，包括读取、清洗、统计和可视化'")
    print("\n方式2：手动管理任务（高级用法）")
    print("  - 创建任务：'添加任务：XXX'")
    print("  - 查看任务：'显示任务列表'")
    print("  - 开始任务：'更新任务1为进行中'")
    print("  - 完成任务：'更新任务1为已完成'")
    print("\n**推荐使用方式1，Agent会自动处理所有细节！**")


if __name__ == "__main__":
    demo_todo_list()

