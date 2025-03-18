"""数字转换模块的测试用例。"""
from typing import TYPE_CHECKING

import pytest

from src.rmb_converter.number_converter import convert_digit, convert_four_digits, convert_integer

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture


def test_convert_digit() -> None:
    """测试单个数字转换。"""
    assert convert_digit(0) == '零'
    assert convert_digit(1) == '壹'
    assert convert_digit(5) == '伍'
    assert convert_digit(9) == '玖'


def test_convert_four_digits_simple() -> None:
    """测试简单四位数转换。"""
    assert convert_four_digits('1') == '壹'
    assert convert_four_digits('10') == '壹拾'
    assert convert_four_digits('100') == '壹佰'
    assert convert_four_digits('1000') == '壹仟'


def test_convert_four_digits_complex() -> None:
    """测试复杂四位数转换。"""
    assert convert_four_digits('1234') == '壹仟贰佰叁拾肆'
    assert convert_four_digits('1001') == '壹仟零壹'
    assert convert_four_digits('1010') == '壹仟零壹拾'
    assert convert_four_digits('1100') == '壹仟壹佰'


def test_convert_four_digits_zero() -> None:
    """测试含零四位数转换。"""
    assert convert_four_digits('0') == '零'
    assert convert_four_digits('0000') == '零'
    assert convert_four_digits('0001') == '壹'
    assert convert_four_digits('0010') == '壹拾'
    assert convert_four_digits('0100') == '壹佰'


def test_convert_integer_simple() -> None:
    """测试简单整数转换。"""
    assert convert_integer('0') == '零'
    assert convert_integer('1') == '壹'
    assert convert_integer('10') == '壹拾'
    assert convert_integer('100') == '壹佰'
    assert convert_integer('1000') == '壹仟'


def test_convert_integer_large_numbers() -> None:
    """测试大数转换。"""
    assert convert_integer('10000') == '壹万'
    assert convert_integer('100000000') == '壹亿'
    assert convert_integer('1000000000000') == '壹万亿'


def test_convert_integer_complex() -> None:
    """测试复杂整数转换。"""
    assert convert_integer('100010001') == '壹亿零壹万零壹'
    assert convert_integer('100000001') == '壹亿零壹'
    assert convert_integer('100100100') == '壹亿零壹拾万零壹佰'
    assert convert_integer('999999999999') == '玖仟玖佰玖拾玖亿玖仟玖佰玖拾玖万玖仟玖佰玖拾玖' 