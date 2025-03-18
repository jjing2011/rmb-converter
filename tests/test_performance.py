"""性能测试模块。"""
import time
from typing import List, Tuple

from src.rmb_converter.converter import convert_to_rmb

def test_conversion_performance(iterations: int = 1000) -> Tuple[float, List[str]]:
    """
    测试转换性能。

    Args:
        iterations: 执行次数

    Returns:
        Tuple[float, List[str]]: 执行时间和结果列表
    """
    test_numbers = [
        "1234567.89",
        "100010001.11",
        "999999999999.99",
        "0.01",
        "100000000.00"
    ]
    
    results = []
    start_time = time.time()
    
    for _ in range(iterations):
        for num in test_numbers:
            results.append(convert_to_rmb(num))
    
    end_time = time.time()
    total_time = end_time - start_time
    
    return total_time, results

if __name__ == '__main__':
    execution_time, _ = test_conversion_performance()
    print(f"执行1000次转换耗时: {execution_time:.2f}秒") 