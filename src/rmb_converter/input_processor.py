"""输入处理模块，负责验证和处理数字输入。

This module handles input validation and processing for RMB numbers.
"""
from typing import Tuple


def validate_input(input_str: str) -> float:
    """验证输入字符串是否为合法数字。

    Args:
        input_str: 输入的字符串

    Returns:
        float: 转换后的浮点数

    Raises:
        ValueError: 当输入不是有效数字时抛出
    """
    try:
        return float(input_str)
    except ValueError:
        raise ValueError("输入必须为有效数字")


def check_integer_length(number: float) -> None:
    """检查数字的整数部分是否超过12位（万亿级）。

    Args:
        number: 要检查的数字

    Raises:
        OverflowError: 当整数部分超过12位时抛出
    """
    integer_part = str(int(number)).lstrip('-')
    if len(integer_part) > 12:
        raise OverflowError("整数部分超出万亿级限制")


def process_number(input_str: str) -> Tuple[str, str]:
    """处理输入的数字字符串，返回规范化的整数和小数部分。

    Args:
        input_str: 输入的数字字符串

    Returns:
        Tuple[str, str]: 包含整数部分和小数部分的元组

    Raises:
        ValueError: 当输入无效时抛出
        OverflowError: 当数字超出范围时抛出
    """
    number = validate_input(input_str)
    check_integer_length(number)
    
    # 格式化为两位小数
    formatted = f"{abs(number):.2f}"
    parts = formatted.split('.')
    return parts[0].lstrip('0') or '0', parts[1] 