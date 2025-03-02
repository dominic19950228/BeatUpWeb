import json
import re

def parse_slk(file_path, output_json):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    data = {}
    results = []
    
    # 解析 SLK
    for line in lines:
        if line.startswith("C;"):
            match = re.findall(r'X(\d+);Y(\d+);K(?:"([^"]+)"|(\d+))', line)
            if match:
                col, row, str_val, num_val = match[0]
                col, row = int(col), int(row)
                value = str_val if str_val else (int(num_val) if num_val else None)
                
                if row not in data:
                    data[row] = {}
                data[row][col] = value
    
    # 轉換為 JSON 格式
    for row in sorted(data.keys()):
        if 4 in data[row] and 5 in data[row]:
            d_value = data[row].get(4)
            e_value = data[row].get(5)
            f_value = data[row].get(6, 5)  # 預設 n=5
            
            if e_value == 'n' and isinstance(d_value, int) and isinstance(f_value, int):
                results.append({"n": f_value, "t": d_value})
            elif e_value == 's' and isinstance(d_value, int):
                results.append({"n": 5, "t": d_value})
    
    # 寫入 JSON 文件
    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=2)
    
    print(f"JSON file saved to {output_json}")

# 使用範例
parse_slk("data.slk", "output.json")