"""性能测试模块。"""
import random
import time
from typing import List, Dict, Any

from src.rmb_converter.chinese_currency import convert_to_rmb

def generate_test_cases(count: int = 1000) -> List[str]:
    """
    生成测试用例。

    Args:
        count: 测试用例数量

    Returns:
        List[str]: 测试用例列表
    """
    cases = []
    for _ in range(count):
        # 生成1到11位的随机整数
        integer = random.randint(1, 99999999999)
        # 生成0到99的随机小数
        decimal = random.randint(0, 99)
        # 组合成金额字符串
        amount = f"{integer}.{decimal:02d}"
        cases.append(amount)
    return cases

def test_performance() -> Dict[str, Any]:
    """
    测试转换性能。
    
    Returns:
        Dict[str, Any]: 性能测试结果
    """
    # 生成测试用例
    test_cases = generate_test_cases()
    
    # 预热缓存
    for case in test_cases[:10]:
        convert_to_rmb(case)
    
    # 计时开始
    start_time = time.time()
    
    # 执行转换
    for case in test_cases:
        convert_to_rmb(case)
    
    # 计算耗时
    duration = time.time() - start_time
    
    # 计算平均耗时（毫秒）
    avg_time = (duration / len(test_cases)) * 1000
    
    print(f"\n性能测试结果:")
    print(f"总用例数: {len(test_cases)}")
    print(f"总耗时: {duration:.2f}秒")
    print(f"平均耗时: {avg_time:.2f}毫秒")
    
    return {
        "total_cases": len(test_cases),
        "duration": duration,
        "avg_time_ms": avg_time
    }

def test_performance_different_scenarios() -> Dict[str, Dict[str, Any]]:
    """
    测试不同场景下的转换性能。
    
    Returns:
        Dict[str, Dict[str, Any]]: 各场景测试结果
    """
    scenarios = {
        "小数": [f"0.{i:02d}" for i in range(100)],  # 测试小数部分
        "整数": [str(i) for i in range(1, 101)],     # 测试预计算的整数
        "大数": [f"{10**i}" for i in range(12)],     # 测试大数处理
        "复杂数": [f"{i}.{j:02d}" for i in range(1000, 1100) for j in range(0, 100, 10)]  # 测试复杂情况
    }
    
    results = {}
    
    for scenario_name, cases in scenarios.items():
        # 预热缓存
        for case in cases[:5]:
            convert_to_rmb(case)
        
        # 计时开始
        start_time = time.time()
        
        # 执行转换
        for case in cases:
            convert_to_rmb(case)
        
        # 计算耗时
        duration = time.time() - start_time
        avg_time = (duration / len(cases)) * 1000
        
        print(f"\n{scenario_name}测试结果:")
        print(f"用例数: {len(cases)}")
        print(f"总耗时: {duration:.3f}秒")
        print(f"平均耗时: {avg_time:.3f}毫秒")
        
        results[scenario_name] = {
            "total_cases": len(cases),
            "duration": duration,
            "avg_time_ms": avg_time
        }
    
    return results

def test_performance_stress() -> Dict[str, Any]:
    """
    压力测试。
    
    Returns:
        Dict[str, Any]: 压力测试结果
    """
    # 生成大量数据，但为了减少执行时间，控制数量
    test_cases = generate_test_cases(3000)
    
    # 预热缓存
    for case in test_cases[:50]:
        convert_to_rmb(case)
    
    # 多次重复执行
    iterations = 3  # 减少迭代次数
    times = []
    
    for i in range(iterations):
        start_time = time.time()
        for case in test_cases:
            convert_to_rmb(case)
        duration = time.time() - start_time
        times.append(duration)
        
        print(f"\n第 {i+1} 轮测试:")
        print(f"总耗时: {duration:.3f}秒")
        print(f"平均耗时: {(duration/len(test_cases))*1000:.3f}毫秒")
    
    print(f"\n总体结果:")
    print(f"最快耗时: {min(times):.3f}秒")
    print(f"最慢耗时: {max(times):.3f}秒")
    print(f"平均耗时: {sum(times)/len(times):.3f}秒")
    
    return {
        "iterations": iterations,
        "total_cases": len(test_cases),
        "min_time": min(times),
        "max_time": max(times),
        "avg_time": sum(times)/len(times),
        "all_times": times
    }

def run_all_tests() -> None:
    """运行所有性能测试。"""
    print("=" * 50)
    print("开始基本性能测试")
    print("=" * 50)
    test_performance()
    
    print("\n" + "=" * 50)
    print("开始不同场景性能测试")
    print("=" * 50)
    test_performance_different_scenarios()
    
    print("\n" + "=" * 50)
    print("开始压力测试")
    print("=" * 50)
    test_performance_stress()
    
    print("\n" + "=" * 50)
    print("所有性能测试完成")
    print("=" * 50)

if __name__ == '__main__':
    run_all_tests() 