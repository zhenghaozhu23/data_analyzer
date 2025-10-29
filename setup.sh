#!/bin/bash

echo "=== 数据分析助手 Agent 设置 ==="

# 检查Python版本
python3 --version

# 创建虚拟环境（可选）
echo "创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 创建.env文件
if [ ! -f .env ]; then
    echo "创建.env文件..."
    cp env_example.txt .env
    echo "请编辑.env文件，添加你的OPENAI_API_KEY"
else
    echo ".env文件已存在"
fi

echo ""
echo "设置完成！"
echo ""
echo "使用方法："
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 编辑.env文件: nano .env"
echo "3. 运行agent: python agent.py"
echo ""

