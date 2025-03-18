"""人民币数字转中文大写模块的测试用例。"""
from typing import TYPE_CHECKING

import pytest

from src.rmb_converter.chinese_currency import (
    convert_digit,
    convert_four_digits,
    convert_integer,
    convert_decimal,
    format_rmb,
    convert_to_rmb,
)

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture


def test_convert_digit() -> None:
    """测试个位数字转换。"""
    assert convert_digit(0) == '零'
    assert convert_digit(1) == '壹'
    assert convert_digit(5) == '伍'
    assert convert_digit(9) == '玖'


def test_convert_four_digits() -> None:
    """测试四位数字转换。"""
    # 测试预计算结果
    assert convert_four_digits('0') == '零'
    assert convert_four_digits('1') == '壹'
    assert convert_four_digits('10') == '壹拾'
    assert convert_four_digits('100') == '壹佰'
    assert convert_four_digits('1000') == '壹仟'
    
    # 测试一般情况
    assert convert_four_digits('1234') == '壹仟贰佰叁拾肆'
    assert convert_four_digits('1001') == '壹仟零壹'
    assert convert_four_digits('1010') == '壹仟零壹拾'
    assert convert_four_digits('1100') == '壹仟壹佰'
    
    # 测试零的处理
    assert convert_four_digits('1001') == '壹仟零壹'
    assert convert_four_digits('1010') == '壹仟零壹拾'
    assert convert_four_digits('1100') == '壹仟壹佰'
    assert convert_four_digits('0001') == '壹'
    assert convert_four_digits('0010') == '壹拾'
    assert convert_four_digits('0100') == '壹佰'


def test_convert_integer() -> None:
    """测试整数转换。"""
    # 测试零
    assert convert_integer('0') == '零'
    
    # 测试个位数
    assert convert_integer('1') == '壹'
    assert convert_integer('9') == '玖'
    
    # 测试十位数
    assert convert_integer('10') == '壹拾'
    assert convert_integer('20') == '贰拾'
    
    # 测试百位数
    assert convert_integer('100') == '壹佰'
    assert convert_integer('101') == '壹佰零壹'
    
    # 测试千位数
    assert convert_integer('1000') == '壹仟'
    assert convert_integer('1001') == '壹仟零壹'
    
    # 测试万位数
    assert convert_integer('10000') == '壹万'
    assert convert_integer('10001') == '壹万零壹'
    assert convert_integer('10010') == '壹万零壹拾'
    assert convert_integer('10100') == '壹万零壹佰'
    assert convert_integer('11000') == '壹万壹仟'
    
    # 测试亿位数
    assert convert_integer('100000000') == '壹亿'
    assert convert_integer('100000001') == '壹亿零壹'
    assert convert_integer('100010000') == '壹亿零壹万'
    
    # 测试特殊零的处理
    assert convert_integer('100100100') == '壹亿零壹拾万零壹佰'
    assert convert_integer('101000000') == '壹亿零壹佰万'
    assert convert_integer('100001000') == '壹亿零壹仟'


def test_convert_decimal() -> None:
    """测试小数部分转换。"""
    # 测试预计算结果
    assert convert_decimal('00') == '整'
    assert convert_decimal('10') == '壹角'
    assert convert_decimal('01') == '壹分'
    assert convert_decimal('50') == '伍角'
    assert convert_decimal('05') == '伍分'
    assert convert_decimal('55') == '伍角伍分'
    
    # 测试一般情况
    assert convert_decimal('25') == '贰角伍分'
    assert convert_decimal('30') == '叁角'
    assert convert_decimal('03') == '叁分'
    assert convert_decimal('99') == '玖角玖分'


def test_format_rmb() -> None:
    """测试人民币金额格式化。"""
    # 测试零元
    assert format_rmb('0', '00') == '零元整'
    
    # 测试整数金额
    assert format_rmb('1', '00') == '壹元整'
    assert format_rmb('10', '00') == '壹拾元整'
    assert format_rmb('100', '00') == '壹佰元整'
    
    # 测试小数金额
    assert format_rmb('0', '10') == '壹角'
    assert format_rmb('0', '01') == '壹分'
    assert format_rmb('0', '50') == '伍角'
    
    # 测试复杂金额
    assert format_rmb('1234', '56') == '壹仟贰佰叁拾肆元伍角陆分'
    assert format_rmb('1000', '10') == '壹仟元壹角'
    assert format_rmb('1000', '01') == '壹仟元零壹分'
    assert format_rmb('10000', '00') == '壹万元整'


def test_convert_to_rmb() -> None:
    """测试完整的人民币转换功能。"""
    # 测试整数
    assert convert_to_rmb('0') == '零元整'
    assert convert_to_rmb('1') == '壹元整'
    assert convert_to_rmb('10') == '壹拾元整'
    assert convert_to_rmb('100') == '壹佰元整'
    
    # 测试小数
    assert convert_to_rmb('0.1') == '壹角'
    assert convert_to_rmb('0.01') == '壹分'
    assert convert_to_rmb('0.5') == '伍角'
    assert convert_to_rmb('0.05') == '伍分'
    
    # 测试复杂数字
    assert convert_to_rmb('1234.56') == '壹仟贰佰叁拾肆元伍角陆分'
    assert convert_to_rmb('1000.10') == '壹仟元壹角'
    assert convert_to_rmb('1000.01') == '壹仟元零壹分'
    assert convert_to_rmb('10000.00') == '壹万元整'
    
    # 测试科学记数法
    assert convert_to_rmb('1e3') == '壹仟元整'
    assert convert_to_rmb('1.5e3') == '壹仟伍佰元整'
    
    # 测试负数
    assert convert_to_rmb('-1234.56') == '壹仟贰佰叁拾肆元伍角陆分'
    assert convert_to_rmb('-1000.10') == '壹仟元壹角'
    
    # 测试异常情况
    with pytest.raises(ValueError, match="输入必须为有效数字"):
        convert_to_rmb('abc')
    
    with pytest.raises(OverflowError, match="整数部分超出12位限制"):
        convert_to_rmb('1000000000000.00') 