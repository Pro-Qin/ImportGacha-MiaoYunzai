import json

def categorize_gacha(input_file):
    # 读取原始数据
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print('''
        ----------------
        错误!请检查文件名及其原文件是否存在!
        ----------------
        ''')
        return 0
    
    gacha_list = data['list']
    
    # 定义映射关系：gacha_type -> 输出文件名
    target_types = {
        '200': '常驻祈愿(200)',
        '301': '角色(301)',  # 301和400合并到"角色"
        '302': '武器活动祈愿(302)',
        '400': '角色(301)',
        '500': '混池(500)'
        
    }
    
    # 按文件名分组（自动合并相同文件名）
    groups = {}
    for gacha_type, filename in target_types.items():
        if filename not in groups:
            groups[filename] = []
    
    # 遍历条目进行分类
    for item in gacha_list:
        gacha_type = item.get('gacha_type')
        if gacha_type in target_types:
            # 移除uigf_gacha_type字段
            item.pop('uigf_gacha_type', None)
            # 获取目标文件名
            filename = target_types[gacha_type]
            groups[filename].append(item)
        else:
            print(f"警告：发现未定义的gacha_type `{gacha_type}`，已跳过该条目")
    
    # 写入文件
    for filename, items in groups.items():
        output_file = f'{filename}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
            print(f"已生成文件：{output_file}")


if __name__ == "__main__":
    categorize_gacha(input('输入要分析的原文件名::'))