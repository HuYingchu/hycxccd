import nbformat
from nbconvert import RSTExporter
import re

def clean_rst_content(text):
    """清理部分特殊符号，避免rst格式冲突"""
    text = re.sub(r'\\\[', '[', text)  # 处理转义符号
    text = re.sub(r'\\\]', ']', text)
    return text

# 读取 .ipynb 文件
with open("pytutorialEn.ipynb", "r", encoding="utf-8") as f:
    notebook = nbformat.read(f, as_version=4)

# 配置 RST 转换器（跳过Pandoc依赖）
exporter = RSTExporter()
exporter.exclude_input_prompt = True   # 隐藏代码输入提示符
exporter.exclude_output_prompt = True  # 隐藏输出提示符

# 转换为 RST
body, _ = exporter.from_notebook_node(notebook)
body = clean_rst_content(body)  # 清理内容

# 保存为 .rst 文件
with open("output.rst", "w", encoding="utf-8") as f:
    f.write(body)

print("转换完成！已生成 output.rst")