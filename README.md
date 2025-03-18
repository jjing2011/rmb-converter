# RMB Converter

将数字金额转换为人民币大写的Python工具。

## 功能特点

- 支持整数和小数的转换
- 支持到万亿级别的数字
- 严格的输入验证
- 完整的单元测试覆盖
- 友好的命令行界面

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/rmb-converter.git
cd rmb-converter

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .
```

## 使用方法

### 命令行使用

```bash
python main.py 1234.56
# 输出：壹仟贰佰叁拾肆元伍角陆分

python main.py 1000000.01
# 输出：壹佰万元零壹分
```

### 作为模块使用

```python
from rmb_converter.converter import convert_to_rmb

result = convert_to_rmb('1234.56')
print(result)  # 输出：壹仟贰佰叁拾肆元伍角陆分
```

## 开发

### 运行测试

```bash
pytest
```

### 代码风格检查

```bash
ruff check .
```

## 许可证

MIT License
