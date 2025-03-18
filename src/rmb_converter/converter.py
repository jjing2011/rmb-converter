"""人民币数字转中文大写转换模块。"""
from functools import lru_cache
from typing import Tuple, Dict

from .input_processor import process_number
from .number_converter import convert_integer, DIGITS

# 货币单位常量
CURRENCY_UNITS = {
    'YUAN': '元',
    'JIAO': '角',
    'FEN': '分',
    'ZHENG': '整'
}

# 预计算常用的小数部分转换结果
COMMON_DECIMALS: Dict[str, str] = {
    '00': '整',
    '10': '壹角',
    '01': '壹分',
    '50': '伍角',
    '05': '伍分',
    '55': '伍角伍分'
}

@lru_cache(maxsize=100)
def convert_decimal(decimal: str) -> str:
    """
    将小数部分转换为中文大写。

    Args:
        decimal: 两位小数字符串

    Returns:
        转换后的中文大写字符串
    """
    # 检查是否在预计算结果中
    if decimal in COMMON_DECIMALS:
        return COMMON_DECIMALS[decimal]
    
    if decimal == '00':
        return CURRENCY_UNITS['ZHENG']
    
    result = []
    jiao = int(decimal[0])
    fen = int(decimal[1])
    
    if jiao > 0:
        result.append(DIGITS[jiao] + CURRENCY_UNITS['JIAO'])
    if fen > 0:
        result.append(DIGITS[fen] + CURRENCY_UNITS['FEN'])
    
    return ''.join(result)

@lru_cache(maxsize=1024)
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
        return f"零{CURRENCY_UNITS['YUAN']}{CURRENCY_UNITS['ZHENG']}"
    
    result = []
    if integer != '0':
        result.append(convert_integer(integer) + CURRENCY_UNITS['YUAN'])
    
    decimal_part = convert_decimal(decimal)
    if decimal_part != CURRENCY_UNITS['ZHENG']:
        if integer != '0' and decimal[0] == '0' and decimal[1] != '0':
            result.append('零')
        result.append(decimal_part)
    else:
        result.append(decimal_part)
    
    return ''.join(result)

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