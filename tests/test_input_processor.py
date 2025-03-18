"""输入处理模块的测试用例。"""
from typing import TYPE_CHECKING

import pytest

from src.rmb_converter.input_processor import validate_input, check_integer_length, process_number

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture


def test_validate_input_valid_numbers() -> None:
    """测试有效数字输入的验证。"""
    assert validate_input("123.45") == 123.45
    assert validate_input("-123.45") == -123.45
    assert validate_input("0") == 0.0
    assert validate_input("1e5") == 100000.0


def test_validate_input_invalid_numbers() -> None:
    """测试无效数字输入的验证。"""
    with pytest.raises(ValueError, match="输入必须为有效数字"):
        validate_input("abc")
    
    with pytest.raises(ValueError, match="输入必须为有效数字"):
        validate_input("12.34.56")
    
    with pytest.raises(ValueError, match="输入必须为有效数字"):
        validate_input("")


def test_check_integer_length_valid() -> None:
    """测试有效整数长度的检查。"""
    check_integer_length(999999999999.99)  # 12位
    check_integer_length(1.23)  # 1位
    check_integer_length(0)  # 1位
    check_integer_length(-999999999999.99)  # 12位


def test_check_integer_length_invalid() -> None:
    """测试无效整数长度的检查。"""
    with pytest.raises(OverflowError, match="整数部分超出万亿级限制"):
        check_integer_length(1000000000000.0)  # 13位
    
    with pytest.raises(OverflowError, match="整数部分超出万亿级限制"):
        check_integer_length(-1000000000000.0)  # 13位


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
    
    with pytest.raises(OverflowError, match="整数部分超出万亿级限制"):
        process_number("1000000000000.00") 