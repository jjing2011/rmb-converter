"""命令行接口模块。"""
import sys
from typing import Optional

import click

from .chinese_currency import convert_to_rmb

@click.command()
@click.argument('amount', required=False)
def main(amount: Optional[str] = None) -> int:
    """
    命令行入口函数。

    Args:
        amount: 要转换的金额字符串

    Returns:
        int: 退出码
    """
    if not amount:
        click.echo("请输入一个数字金额", err=True)
        sys.exit(1)
    
    try:
        result = convert_to_rmb(amount)
        click.echo(result)
        return 0
    except (ValueError, OverflowError) as e:
        click.echo(f"错误: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    sys.exit(main()) 