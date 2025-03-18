"""命令行接口模块。"""
import argparse
import sys
from typing import List, Optional

from .converter import convert_to_rmb


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器。

    Returns:
        argparse.ArgumentParser: 配置好的参数解析器
    """
    parser = argparse.ArgumentParser(
        description='将数字金额转换为人民币大写',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'amount',
        help='要转换的金额（支持整数或小数）'
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """命令行程序入口点。

    Args:
        argv: 命令行参数列表，默认为None（使用sys.argv）

    Returns:
        int: 程序退出码
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        result = convert_to_rmb(args.amount)
        print(result)
        return 0
    except (ValueError, OverflowError) as e:
        print(f"错误：{str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main()) 