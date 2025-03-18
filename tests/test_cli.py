"""命令行接口模块的测试用例。"""
from typing import TYPE_CHECKING

import pytest

from src.rmb_converter.cli import main

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture


def test_main_valid_input(capsys: "CaptureFixture[str]") -> None:
    """测试有效输入的处理。"""
    # 测试整数
    assert main(['100']) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == '壹佰元整'
    
    # 测试小数
    assert main(['100.50']) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == '壹佰元伍角'


def test_main_invalid_input(capsys: "CaptureFixture[str]") -> None:
    """测试无效输入的处理。"""
    # 测试非数字输入
    assert main(['abc']) == 1
    captured = capsys.readouterr()
    assert '错误' in captured.err
    
    # 测试超出范围的数字
    assert main(['1000000000000.00']) == 1
    captured = capsys.readouterr()
    assert '错误' in captured.err


def test_main_no_args(capsys: "CaptureFixture[str]") -> None:
    """测试无参数情况的处理。"""
    with pytest.raises(SystemExit):
        main([])
    captured = capsys.readouterr()
    assert 'error' in captured.err.lower() 