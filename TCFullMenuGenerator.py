import re
import os

# 输入文件路径
input_file = input("请输入 TOTALCMD.INC 文件路径: ").strip()

# 输出文件路径：与输入文件同目录，文件名为 TCFullMenu_EN.mnu
output_file = os.path.join(os.path.dirname(input_file), "TCFullMenu_EN.mnu")

# 处理逻辑
result_lines = []
first_popup = True  # 用于标记是否是第一次遇到数字为 0 的行

with open(input_file, "r", encoding="utf-8") as infile:
    for line in infile:
        # 去掉空行和多余空格
        line = line.strip()
        if not line:
            continue
        
        # 匹配行中的内容
        match = re.match(r'(.*?)=(\d+)(?:;(.+))?', line)
        if match:
            prefix, number, content = match.groups()
            number = int(number)
            
            if number == 0:

                # 提取字母和空格，排除其他符号
                extracted_letters = re.sub(r'[^a-zA-Z ]', '', prefix)
                # 跳过特定内容"Commands with Parameters", 而且忽略大小写
                if extracted_letters.lower() == "commands with parameters".lower():
                    continue

                # 如果不是第一次出现数字为 0，则添加 END_POPUP
                if not first_popup:
                    result_lines.append("END_POPUP")
                first_popup = False  # 标记已经遇到过数字为 0   
                
                result_lines.append(f'POPUP "{extracted_letters}"')
            else:
                if content == None:
                    # 输出格式为 ";    MENUITEM "<内容>", <数字>"
                    result_lines.append(f';    MENUITEM "{content}", {number}')   
                else:
                    # 输出格式为 "    MENUITEM "<内容>", <数字>"
                    result_lines.append(f'    MENUITEM "{content}", {number}')

# 最后添加 END_POPUP（如果有多个 POPUP 块）
if not first_popup:
    result_lines.append("END_POPUP")

# 将结果写入输出文件
with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.writelines(line + '\n' for line in result_lines)

print(f"处理完成，结果已保存到 {output_file}")

# 保持控制台打开，等待用户输入退出
input("Press Enter to exit...")

