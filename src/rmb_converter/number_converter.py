"""数字转换模块。"""

from typing import List

# 数字到中文大写的映射
DIGITS = {
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
UNITS = ['', '拾', '佰', '仟']

# 万亿兆的单位
LARGE_UNITS = ['', '万', '亿', '万亿']

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
    result = ''
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
                result += '零'
            last_was_zero = True
        else:
            result += DIGITS[digit_int] + UNITS[3 - i]
            last_was_zero = False
    
    # 去掉末尾的零
    result = result.rstrip('零')
    return result

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

    result = ''
    
    for i, segment in enumerate(segments):
        segment_value = int(segment)
        if segment_value == 0:
            # 如果当前段为0，且不是最后一段，且后面还有非0段，则添加一个零
            if i < len(segments) - 1 and any(int(s) > 0 for s in segments[i + 1:]):
                if not result.endswith('零'):
                    result += '零'
        else:
            segment_str = convert_four_digits(segment)
            # 如果结果不为空，且当前段不是完整的4位数，需要在前面加零
            if result and len(segment.lstrip('0')) < 4 and not result.endswith('零'):
                result += '零'
            
            result += segment_str
            # 添加单位（万、亿等）
            if i < len(segments) - 1:
                result += LARGE_UNITS[len(segments) - i - 1]
                # 如果当前段的末尾是零，且后面还有非零数字，添加零
                if segment_str.endswith('零') and any(int(s) > 0 for s in segments[i + 1:]):
                    result += '零'

    # 处理连续的零
    while '零零' in result:
        result = result.replace('零零', '零')
    result = result.strip('零')

    return result 