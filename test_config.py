"""
测试环境变量配置是否正确加载
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_env_vars():
    """测试环境变量是否已正确配置"""
    print("=== 环境变量配置测试 ===\n")
    
    # 检查必需配置
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ OPENAI_API_KEY 未配置或使用默认值")
    else:
        print(f"✅ OPENAI_API_KEY: {api_key[:10]}...")
    
    # 检查可选配置
    model = os.getenv("OPENAI_MODEL", "gpt-4")
    print(f"✅ OPENAI_MODEL: {model}")
    
    temperature = os.getenv("OPENAI_TEMPERATURE", "0.3")
    print(f"✅ OPENAI_TEMPERATURE: {temperature}")
    
    base_url = os.getenv("OPENAI_BASE_URL", "未设置（使用默认OpenAI API）")
    if base_url != "未设置（使用默认OpenAI API）":
        print(f"✅ OPENAI_BASE_URL: {base_url}")
    else:
        print(f"✅ OPENAI_BASE_URL: {base_url}")
    
    print("\n=== 配置验证完成 ===")
    
    # 尝试创建agent
    print("\n正在创建 Agent...")
    try:
        from agent import DataAnalyserAgent
        agent = DataAnalyserAgent()
        print("✅ Agent 创建成功！")
        print(f"   使用模型: {model}")
        if base_url != "未设置（使用默认OpenAI API）":
            print(f"   API端点: {base_url}")
    except Exception as e:
        print(f"❌ Agent 创建失败: {str(e)}")
        print("   请检查你的配置是否正确")


if __name__ == "__main__":
    test_env_vars()

