"""人民币数字转中文大写转换模块。"""
from typing import Tuple

from .input_processor import process_number
from .number_converter import convert_integer, DIGITS


def convert_decimal(decimal: str) -> str:
    """
    将小数部分转换为中文大写。

    Args:
        decimal: 两位小数字符串

    Returns:
        转换后的中文大写字符串
    """
    if decimal == '00':
        return '整'
    
    result = ''
    jiao = int(decimal[0])
    fen = int(decimal[1])
    
    if jiao > 0:
        result += DIGITS[jiao] + '角'
    if fen > 0:
        result += DIGITS[fen] + '分'
    
    return result


def format_rmb(integer: str, decimal: str) -> str:
    """
    格式化人民币金额。

    Args:
        integer: 整数部分
        decimal: 小数部分

    Returns:
        格式化后的人民币金额字符串
    """
    if integer == '0' and decimal == '00':
        return '零元整'
    
    result = ''
    if integer != '0':
        result += convert_integer(integer) + '元'
    
    decimal_part = convert_decimal(decimal)
    if decimal_part != '整':
        if integer != '0' and decimal[0] == '0' and decimal[1] != '0':
            result += '零'
        result += decimal_part
    else:
        result += decimal_part
    
    return result


def convert_to_rmb(amount: str) -> str:
    """将数字金额转换为人民币大写。

    Args:
        amount: 数字金额字符串

    Returns:
        str: 人民币大写字符串

    Raises:
        ValueError: 当输入无效时抛出
        OverflowError: 当数字超出范围时抛出
    """
    if '.' in amount:
        parts = amount.split('.')
        if len(parts) > 2 or len(parts[1]) > 2:
            raise ValueError("小数位数不能超过2位")
    
    integer_part, decimal_part = process_number(amount)
    return format_rmb(integer_part, decimal_part) 