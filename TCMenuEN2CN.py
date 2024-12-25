import re
import os

# 获取用户输入的文件路径
source_file = input("请输入 WCMD_CHN.INC 文件路径: ").strip()
target_file = input("请输入 TCFullMenu_EN.mnu 文件路径: ").strip()

# 输出文件路径：与 TCFullMenu.mnu 文件同目录，文件名为 TCFullMenu_CN.mnu
output_file = os.path.join(os.path.dirname(target_file), "TCFullMenu_CN.mnu")

# 正则表达式：提取带数字的命令或视图模式
source_pattern = r'(\d+)\s*=\s*"(.*?)"'
# 匹配目标文件中的 MENUITEM 和数字
target_pattern = r'(\s*)(MENUITEM\s)"(.*?)",\s(\d+)'  # 匹配缩进
popup_pattern = r'(\s*)(POPUP\s)"(.*?)"'  # 匹配POPUP行

# 解析源文件，提取数字和双引号内容
source_dict = {}
with open(source_file, "r") as src:
    for line in src:
        # 处理带数字的行
        match = re.search(source_pattern, line)
        if match:
            number, content = match.groups()
            source_dict[number] = content
        # 处理没有数字的行
        else:
            key_value = line.split("=", 1)
            if len(key_value) == 2:
                key, value = key_value
                key = key.strip()
                value = value.strip().strip('"')
                source_dict[key] = value

# 逐行读取目标文本，查找匹配的数字并替换内容
result_lines = []
with open(target_file, "r", encoding="utf-8") as tgt:
    for line in tgt:
        # 跳过以 ; 开头的行
        if line.strip().startswith(";"):
            result_lines.append(line.rstrip()) # 保留原行
            continue

        # 处理POPUP行
        popup_match = re.search(popup_pattern, line)
        if popup_match:
            indent, prefix, target_content = popup_match.groups()
            if target_content in source_dict:
                # 获取对应内容
                new_content = source_dict[target_content]
                if new_content:  # 如果内容不为空
                    # 替换POPUP双引号中的内容
                    new_line = f'{indent}{prefix}"{new_content}"'
                    result_lines.append(new_line)
                else:
                    # 内容为空，保留原行
                    result_lines.append(line.rstrip())
            else:
                result_lines.append(line.rstrip())  # 保留原行
        # 处理MENUITEM行
        else:
            match = re.search(target_pattern, line)
            if match:
                indent, prefix, target_content, target_number = match.groups()
                if target_number in source_dict:
                    # 获取对应内容
                    new_content = source_dict[target_number]
                    if new_content:  # 如果内容不为空
                        # 替换MENUITEM双引号中的内容
                        new_line = f'{indent}{prefix}"{new_content}", {target_number}'
                        result_lines.append(new_line)
                    else:
                        # 内容为空，保留原行
                        result_lines.append(line.rstrip())                    
                else:
                    result_lines.append(line.rstrip())  # 保留原行
            else:
                result_lines.append(line.rstrip())  # 保留原行

# 将结果写入输出文件
with open(output_file, "w") as out:
    out.writelines(line + '\n' for line in result_lines)

print(f"处理完成，结果已保存到 {output_file}")

# 保持控制台打开，等待用户输入退出
input("Press Enter to exit...")
