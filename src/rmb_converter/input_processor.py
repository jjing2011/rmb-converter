"""输入处理模块，负责验证和处理数字输入。

This module handles input validation and processing for RMB numbers.
"""
from typing import Tuple

# 常量定义
MAX_INTEGER_LENGTH = 12  # 最大整数位数（万亿级）

def validate_number(input_str: str) -> float:
    """
    验证输入字符串是否为合法数字，并检查整数部分是否超过限制。

    Args:
        input_str: 输入的字符串

    Returns:
        float: 转换后的浮点数

    Raises:
        ValueError: 当输入不是有效数字时抛出
        OverflowError: 当整数部分超过12位时抛出
    """
    try:
        # 使用float()函数验证输入是否为合法数字，同时处理正负数、科学记数法等格式
        number = float(input_str)
        
        # 使用abs()处理负数，确保负号不影响位数计算
        # 使用int()去除小数部分，只关注整数位数
        # 使用lstrip('0')去除前导零，确保正确计算位数
        # 例如："-000123.45" -> "123"
        integer_part = str(int(abs(number))).lstrip('0')
        
        if len(integer_part) > MAX_INTEGER_LENGTH:
            raise OverflowError(f"整数部分超出{MAX_INTEGER_LENGTH}位限制")
        return number
    except ValueError:
        raise ValueError("输入必须为有效数字")

def process_number(input_str: str) -> Tuple[str, str]:
    """
    处理输入的数字字符串，返回规范化的整数和小数部分。

    Args:
        input_str: 输入的数字字符串

    Returns:
        Tuple[str, str]: 包含整数部分和小数部分的元组
                        整数部分已去除前导零，小数部分固定两位
                        例如："-000123.45" -> ("123", "45")
                             "-0.1" -> ("0", "10")

    Raises:
        ValueError: 当输入无效时抛出
        OverflowError: 当数字超出范围时抛出
    """
    # 首先验证输入的合法性
    number = validate_number(input_str)
    
    # 使用abs()处理负数，因为人民币大写金额使用"负"字来表示负数
    # 使用.2f格式化确保小数部分始终为两位
    formatted = f"{abs(number):.2f}"
    
    # 分割整数和小数部分
    parts = formatted.split('.')
    
    # 处理整数部分：
    # 1. lstrip('0')去除前导零
    # 2. or '0' 处理特殊情况：如果整数部分全为零，返回"0"而不是空字符串
    return parts[0].lstrip('0') or '0', parts[1] 