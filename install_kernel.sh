#!/bin/bash

# 安装并注册 Python kernel 的脚本

echo "=== 安装 Python Jupyter Kernel ==="
echo ""

# 检查是否已安装 ipykernel
if ! python -m ipykernel --help &>/dev/null; then
    echo "检测到 ipykernel 未安装，正在安装..."
    pip install ipykernel
else
    echo "✓ ipykernel 已安装"
fi

# 注册 python3 kernel
echo ""
echo "正在注册 python3 kernel..."
python -m ipykernel install --user --name python3 --display-name "Python 3"

echo ""
echo "✓ Kernel 注册完成！"
echo ""
echo "验证安装："
python -m jupyter kernelspec list

echo ""
echo "=== 安装完成 ==="

