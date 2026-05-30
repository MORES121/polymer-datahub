#!/usr/bin/env python3
"""
数据验证脚本：检查所有JSON是否符合Schema规范
"""

import json
import os
import jsonschema
from jsonschema import validate

MATERIAL_SCHEMA = {
    "type": "object",
    "required": ["metadata", "technical_specifications", "value_proposition"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["brand", "commercial_name", "unique_id"],
            "properties": {
                "brand": {"type": "string"},
                "commercial_name": {"type": "string"},
                "unique_id": {"type": "string"},
                "data_sheet_url": {"type": "string"},
                "last_updated": {"type": "string"}
            }
        },
        "technical_specifications": {
            "type": "object",
            "required": ["base_polymer"],
            "properties": {
                "base_polymer": {"type": "string"},
                "reinforcement": {"type": "string"},
                "key_properties": {"type": "object"}
            }
        },
        "value_proposition": {
            "type": "object",
            "properties": {
                "solved_pain_points": {"type": "array"},
                "typical_applications": {"type": "array"},
                "tco_advantage": {"type": "string"}
            }
        }
    }
}

def validate_json_files(directory="output_json"):
    print("\n" + "="*50)
    print("启航塑胶·数据验证引擎启动")
    print("="*50)
    
    if not os.path.exists(directory):
        print(f"✗ 目录不存在: {directory}")
        print("请先运行 excel_to_json.py 生成JSON文件")
        return
    
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    print(f"找到 {len(json_files)} 个JSON文件")
    
    if len(json_files) == 0:
        print("✗ 没有找到JSON文件")
        return
    
    valid_count = 0
    invalid_files = []
    
    for filename in json_files:
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            validate(instance=data, schema=MATERIAL_SCHEMA)
            valid_count += 1
            print(f"  ✓ 验证通过: {filename}")
        except jsonschema.exceptions.ValidationError as e:
            invalid_files.append(f"{filename}: {e.message}")
            print(f"  ✗ 验证失败: {filename}")
        except Exception as e:
            invalid_files.append(f"{filename}: {str(e)}")
            print(f"  ✗ 读取失败: {filename}")
    
    print("\n" + "="*50)
    print(f"验证完成！有效: {valid_count}，无效: {len(invalid_files)}")
    if invalid_files:
        print("\n无效文件详情:")
        for err in invalid_files:
            print(f"  ✗ {err}")
    print("="*50)

if __name__ == "__main__":
    validate_json_files()