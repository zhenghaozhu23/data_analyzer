"""
IPython工具测试脚本
"""
import sys


def test_imports():
    """测试导入"""
    print("测试1: 检查依赖导入...")
    try:
        from tools.ipython_executor import IPythonExecutor
        from tools.ipython_tool import IPythonCodeTool, IPythonNotebookTool
        print("✓ 所有模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        print("提示: 请确保已安装 jupyter-client 和 ipykernel")
        print("运行: pip install jupyter-client ipykernel")
        return False


def test_basic_execution():
    """测试基本执行功能"""
    print("\n测试2: 基本代码执行...")
    try:
        from tools.ipython_executor import IPythonExecutor
        
        executor = IPythonExecutor(notebook_path="test_notebook.ipynb")
        print("✓ 执行器创建成功")
        
        result = executor.execute_code("print('Hello from IPython!')")
        print("✓ 代码执行成功")
        
        executor.stop_kernel()
        print("✓ Kernel停止成功")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tools():
    """测试工具功能"""
    print("\n测试3: 工具功能...")
    try:
        from tools.ipython_tool import IPythonCodeTool, IPythonNotebookTool
        
        code_tool = IPythonCodeTool(notebook_path="test_tool.ipynb")
        print("✓ 代码工具创建成功")
        
        result = code_tool._run(code="x = 42\nprint(f'答案是: {x}')")
        print("✓ 工具执行成功")
        print(f"  输出: {result[:100]}...")
        
        notebook_tool = IPythonNotebookTool()
        print("✓ Notebook工具创建成功")
        
        summary = notebook_tool._run(action="summary", notebook_path="test_tool.ipynb")
        print("✓ 获取摘要成功")
        
        # 清理
        code_tool.executor.stop_kernel()
        print("✓ 清理成功")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """测试集成到tools"""
    print("\n测试4: 集成测试...")
    try:
        import tools
        
        all_tools = tools.get_all_tools(enable_ipython=True)
        print(f"✓ 获取到 {len(all_tools)} 个工具")
        
        tool_names = [tool.name for tool in all_tools]
        if "ipython_execute" in tool_names and "ipython_notebook" in tool_names:
            print("✓ IPython工具已成功集成")
            return True
        else:
            print(f"✗ 未找到IPython工具，当前工具: {tool_names}")
            return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("IPython工具测试")
    print("=" * 60)
    
    results = []
    
    # 测试1: 导入
    results.append(test_imports())
    
    if results[-1]:
        # 测试2: 基本执行
        results.append(test_basic_execution())
        
        # 测试3: 工具功能
        results.append(test_tools())
        
        # 测试4: 集成测试
        results.append(test_integration())
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✓ 所有测试通过！")
        return 0
    else:
        print("✗ 部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())

