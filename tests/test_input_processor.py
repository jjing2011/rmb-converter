"""输入处理模块的测试用例。"""
from typing import TYPE_CHECKING

import pytest

from src.rmb_converter.input_processor import validate_number, process_number

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture


def test_validate_number_valid_numbers() -> None:
    """测试有效数字输入的验证。"""
    assert validate_number("123.45") == 123.45
    assert validate_number("-123.45") == -123.45
    assert validate_number("0") == 0.0
    assert validate_number("1e5") == 100000.0


def test_validate_number_invalid_numbers() -> None:
    """测试无效数字输入的验证。"""
    with pytest.raises(ValueError, match="输入必须为有效数字"):
        validate_number("abc")
    
    with pytest.raises(ValueError, match="输入必须为有效数字"):
        validate_number("12.34.56")
    
    with pytest.raises(ValueError, match="输入必须为有效数字"):
        validate_number("")


def test_validate_number_length() -> None:
    """测试数字长度验证。"""
    # 有效长度
    validate_number("999999999999.99")  # 12位
    validate_number("1.23")  # 1位
    validate_number("0")  # 1位
    validate_number("-999999999999.99")  # 12位

    # 超出长度限制
    with pytest.raises(OverflowError, match="整数部分超出12位限制"):
        validate_number("1000000000000.0")  # 13位
    
    with pytest.raises(OverflowError, match="整数部分超出12位限制"):
        validate_number("-1000000000000.0")  # 13位


def test_process_number_valid() -> None:
    """测试数字处理功能。"""
    assert process_number("123.456") == ("123", "46")
    assert process_number("0.1") == ("0", "10")
    assert process_number("1000") == ("1000", "00")
    assert process_number("-123.45") == ("123", "45")
    assert process_number("0") == ("0", "00")


def test_process_number_invalid() -> None:
    """测试数字处理功能的异常情况。"""
    with pytest.raises(ValueError, match="输入必须为有效数字"):
        process_number("invalid")
    
    with pytest.raises(OverflowError, match="整数部分超出12位限制"):
        process_number("1000000000000.00")


def test_process_number_negative() -> None:
    """测试负数处理的特殊情况。"""
    assert process_number("-0") == ("0", "00")
    assert process_number("-0.0") == ("0", "00")
    assert process_number("-000123.45") == ("123", "45")
    assert process_number("-0.45") == ("0", "45")
    assert process_number("-1.00") == ("1", "00") 