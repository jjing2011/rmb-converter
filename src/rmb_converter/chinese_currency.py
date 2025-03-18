"""人民币数字转中文大写转换模块。

此模块提供了将数字转换为中文大写金额的功能，包括：
1. 数字到中文大写的基础转换
2. 人民币金额的格式化
3. 完整的货币金额转换服务
"""
from functools import lru_cache
from typing import List, Dict, Tuple

from .input_processor import process_number

# 数字到中文大写的映射
DIGITS: Dict[int, str] = {
    0: '零',
    1: '壹',
    2: '贰',
    3: '叁',
    4: '肆',
    5: '伍',
    6: '陆',
    7: '柒',
    8: '捌',
    9: '玖'
}

# 个十百千的单位
UNITS: List[str] = ['', '拾', '佰', '仟']

# 万亿兆的单位
LARGE_UNITS: List[str] = ['', '万', '亿', '万亿']

# 货币单位常量
CURRENCY_UNITS = {
    'YUAN': '元',
    'JIAO': '角',
    'FEN': '分',
    'ZHENG': '整'
}

def _generate_four_digits_cache() -> Dict[str, str]:
    """
    生成四位数的预计算缓存。
    包括：
    1. 0-100 的所有数字
    2. 1000-9999 中的整千、整百数字
    """
    cache = {}
    
    # 处理 0-100
    for i in range(101):
        num_str = str(i)
        result = []
        num = int(num_str)
        if num == 0:
            cache['0'] = '零'
            continue
            
        digits = str(num).zfill(4)
        last_was_zero = True
        
        for j, digit in enumerate(digits):
            digit_int = int(digit)
            if digit_int == 0:
                if not last_was_zero and j < 3 and any(int(d) > 0 for d in digits[j+1:]):
                    result.append('零')
                last_was_zero = True
            else:
                result.append(DIGITS[digit_int] + UNITS[3 - j])
                last_was_zero = False
        
        cache[num_str] = ''.join(result).rstrip('零')
    
    # 处理整千、整百数字
    for i in range(1, 10):
        # 整千
        num_str = str(i * 1000)
        cache[num_str] = DIGITS[i] + '仟'
        
        # 整百
        num_str = str(i * 100)
        cache[num_str] = DIGITS[i] + '佰'
    
    return cache

def _generate_decimal_cache() -> Dict[str, str]:
    """
    生成小数部分（角分）的预计算缓存。
    包括所有可能的两位小数（00-99）。
    """
    cache = {}
    
    # 处理特殊情况
    cache['00'] = CURRENCY_UNITS['ZHENG']
    
    # 处理所有其他情况
    for i in range(1, 100):
        jiao = i // 10
        fen = i % 10
        result = []
        
        if jiao > 0:
            result.append(DIGITS[jiao] + CURRENCY_UNITS['JIAO'])
        if fen > 0:
            result.append(DIGITS[fen] + CURRENCY_UNITS['FEN'])
        
        cache[f'{i:02d}'] = ''.join(result)
    
    return cache

# 预计算常用的四位数转换结果
COMMON_FOUR_DIGITS = _generate_four_digits_cache()

# 预计算所有小数部分转换结果
COMMON_DECIMALS = _generate_decimal_cache()

@lru_cache(maxsize=128)
def convert_digit(digit: int) -> str:
    """
    将个位数字转换为中文大写。

    Args:
        digit: 0-9的数字

    Returns:
        转换后的中文大写字符串
    """
    return DIGITS[digit]

def convert_four_digits(number: str) -> str:
    """
    将四位以内的数字转换为中文大写。

    Args:
        number: 四位以内的数字字符串

    Returns:
        转换后的中文大写字符串
    """
    # 检查是否在预计算结果中
    if number in COMMON_FOUR_DIGITS:
        return COMMON_FOUR_DIGITS[number]
    
    result = []
    num = int(number)
    if num == 0:
        return '零'
    
    # 补齐四位
    number = number.zfill(4)
    last_was_zero = True
    
    for i, digit in enumerate(number):
        digit_int = int(digit)
        if digit_int == 0:
            if not last_was_zero and i < 3 and any(int(d) > 0 for d in number[i+1:]):
                result.append('零')
            last_was_zero = True
        else:
            result.append(DIGITS[digit_int] + UNITS[3 - i])
            last_was_zero = False
    
    return ''.join(result).rstrip('零')

@lru_cache(maxsize=1024)
def _process_segment(segment: str, position: int, has_next_nonzero: bool) -> Tuple[str, bool]:
    """
    处理数字段，返回转换结果和是否需要添加零。

    Args:
        segment: 数字段
        position: 位置（用于确定单位）
        has_next_nonzero: 后面是否还有非零数字

    Returns:
        Tuple[str, bool]: 转换结果和是否需要添加零
    """
    segment_value = int(segment)
    if segment_value == 0:
        return '', has_next_nonzero
    
    result = convert_four_digits(segment)
    needs_zero = result.endswith('零') and has_next_nonzero
    if position > 0:
        result += LARGE_UNITS[position]
    
    return result, needs_zero

@lru_cache(maxsize=1024)
def convert_integer(number: str) -> str:
    """
    将整数转换为中文大写。

    Args:
        number: 要转换的整数字符串

    Returns:
        转换后的中文大写字符串
    """
    if number == '0':
        return '零'

    # 从右向左每4位分割
    segments: List[str] = []
    while number:
        segments.append(number[-4:])
        number = number[:-4]
    segments.reverse()

    result = []
    last_was_zero = False
    
    for i, segment in enumerate(segments):
        segment_value = int(segment)
        if segment_value == 0:
            # 如果后面还有非零数字，且上一个字符不是零，添加零
            if i < len(segments) - 1 and any(int(s) > 0 for s in segments[i+1:]):
                if not (result and result[-1].endswith('零')):
                    result.append('零')
            last_was_zero = True
            continue
        
        # 当前段的处理
        converted = convert_four_digits(str(segment_value))
        
        # 处理零的连接
        if last_was_zero and result and not result[-1].endswith('零'):
            result.append('零')
        result.append(converted)
        
        # 添加单位（万、亿等）
        if i < len(segments) - 1:
            result.append(LARGE_UNITS[len(segments) - i - 1])
            # 检查是否需要在单位后添加零
            next_segment = int(segments[i + 1])
            if next_segment > 0 and next_segment < 1000:
                result.append('零')
        
        # 更新零的状态
        last_was_zero = converted.endswith('零')

    # 合并结果并处理多余的零
    result = ''.join(result)
    while '零零' in result:
        result = result.replace('零零', '零')
    return result.strip('零')

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
    """
    将数字金额转换为人民币大写格式。

    Args:
        amount: 数字金额字符串

    Returns:
        str: 人民币大写金额

    Raises:
        ValueError: 当输入格式无效时抛出
        OverflowError: 当数字超出范围时抛出
    """
    integer_part, decimal_part = process_number(amount)
    return format_rmb(integer_part, decimal_part) 