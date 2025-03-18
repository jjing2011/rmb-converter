"""命令行接口测试模块。"""
from typing import TYPE_CHECKING

from click.testing import CliRunner

from src.rmb_converter.cli import main

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture


def test_cli_normal_input() -> None:
    """测试正常输入情况。"""
    runner = CliRunner()
    result = runner.invoke(main, ['100.00'])
    assert result.exit_code == 0
    assert result.output.strip() == '壹佰元整'


def test_cli_no_input() -> None:
    """测试无输入情况。"""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 1
    assert '请输入一个数字金额' in result.output


def test_cli_invalid_input() -> None:
    """测试无效输入情况。"""
    runner = CliRunner()
    result = runner.invoke(main, ['abc'])
    assert result.exit_code == 1
    assert '错误' in result.output


def test_cli_overflow_input() -> None:
    """测试超出范围的输入。"""
    runner = CliRunner()
    result = runner.invoke(main, ['1000000000000.00'])
    assert result.exit_code == 1
    assert '错误' in result.output 