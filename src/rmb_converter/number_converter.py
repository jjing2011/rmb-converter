"""数字转换模块。"""

from functools import lru_cache
from typing import List, Dict, Tuple

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

# 预计算常用的四位数转换结果
COMMON_FOUR_DIGITS: Dict[str, str] = {
    '0': '零',
    '1': '壹',
    '10': '壹拾',
    '100': '壹佰',
    '1000': '壹仟',
    '0001': '壹',
    '0010': '壹拾',
    '0100': '壹佰',
    '1001': '壹仟零壹',
    '1010': '壹仟零壹拾',
    '1100': '壹仟壹佰'
}

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

@lru_cache(maxsize=1024)
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
    
    # 使用join而不是+=
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

    # 预处理：检查后续段是否有非零值
    has_next_nonzero = [False] * len(segments)
    for i in range(len(segments)-2, -1, -1):
        has_next_nonzero[i] = any(int(s) > 0 for s in segments[i+1:])

    result = []
    last_was_zero = False
    
    for i, segment in enumerate(segments):
        converted, needs_zero = _process_segment(segment, len(segments)-i-1, has_next_nonzero[i])
        if converted:
            if last_was_zero and result and not result[-1].endswith('零'):
                result.append('零')
            result.append(converted)
            if needs_zero:
                result.append('零')
            last_was_zero = needs_zero
        elif has_next_nonzero[i] and result and not result[-1].endswith('零'):
            result.append('零')
            last_was_zero = True

    # 使用join连接结果并处理多余的零
    result = ''.join(result)
    while '零零' in result:
        result = result.replace('零零', '零')
    return result.strip('零') 