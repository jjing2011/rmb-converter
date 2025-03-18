"""人民币转换模块的测试用例。"""
from typing import TYPE_CHECKING

import pytest

from src.rmb_converter.converter import convert_decimal, format_rmb, convert_to_rmb

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture


def test_convert_decimal() -> None:
    """测试小数部分转换。"""
    assert convert_decimal('00') == '整'
    assert convert_decimal('10') == '壹角'
    assert convert_decimal('01') == '壹分'
    assert convert_decimal('50') == '伍角'
    assert convert_decimal('05') == '伍分'
    assert convert_decimal('55') == '伍角伍分'
    assert convert_decimal('06') == '陆分'
    assert convert_decimal('60') == '陆角'
    assert convert_decimal('65') == '陆角伍分'


def test_format_rmb() -> None:
    """测试人民币金额格式化。"""
    assert format_rmb('0', '00') == '零元整'
    assert format_rmb('1', '00') == '壹元整'
    assert format_rmb('0', '10') == '壹角'
    assert format_rmb('0', '01') == '壹分'
    assert format_rmb('1', '10') == '壹元壹角'
    assert format_rmb('1', '01') == '壹元零壹分'
    assert format_rmb('100', '00') == '壹佰元整'
    assert format_rmb('100', '10') == '壹佰元壹角'
    assert format_rmb('100', '01') == '壹佰元零壹分'


def test_convert_to_rmb_simple() -> None:
    """测试简单金额转换。"""
    assert convert_to_rmb('0') == '零元整'
    assert convert_to_rmb('1') == '壹元整'
    assert convert_to_rmb('10') == '壹拾元整'
    assert convert_to_rmb('100') == '壹佰元整'
    assert convert_to_rmb('1000') == '壹仟元整'
    assert convert_to_rmb('10000') == '壹万元整'


def test_convert_to_rmb_decimals() -> None:
    """测试带小数的金额转换。"""
    assert convert_to_rmb('0.1') == '壹角'
    assert convert_to_rmb('0.01') == '壹分'
    assert convert_to_rmb('0.10') == '壹角'
    assert convert_to_rmb('1.01') == '壹元零壹分'
    assert convert_to_rmb('1.10') == '壹元壹角'
    assert convert_to_rmb('1.11') == '壹元壹角壹分'


def test_convert_to_rmb_complex() -> None:
    """测试复杂金额转换。"""
    assert convert_to_rmb('100010001.11') == '壹亿零壹万零壹元壹角壹分'
    assert convert_to_rmb('100000001.01') == '壹亿零壹元零壹分'
    assert convert_to_rmb('100100100.10') == '壹亿零壹拾万零壹佰元壹角'
    assert convert_to_rmb('999999999999.99') == '玖仟玖佰玖拾玖亿玖仟玖佰玖拾玖万玖仟玖佰玖拾玖元玖角玖分'


def test_convert_to_rmb_invalid() -> None:
    """测试无效输入的处理。"""
    with pytest.raises(ValueError):
        convert_to_rmb('abc')
    
    with pytest.raises(ValueError):
        convert_to_rmb('1.234')
    
    with pytest.raises(OverflowError):
        convert_to_rmb('1000000000000.00') 