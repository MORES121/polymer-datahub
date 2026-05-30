#!/usr/bin/env python3
"""
自动分类脚本 - 按材料类型整理JSON文件
"""

import json
import os
import shutil

SOURCE_DIR = "output_json"
TARGET_BASE = "data"

POLYMER_MAP = {
    "ABS": "ABS",
    "POM": "POM", 
    "PC": "PC",
    "PMMA": "PMMA",
    "PBT": "PBT",
    "PA6": "PA6",
    "PA66": "PA66",
    "PPA": "PPA",
    "PPS": "PPS"
}

def classify():
    print("\n" + "="*50)
    print("启航塑胶·自动分类引擎启动")
    print("="*50)
    
    if not os.path.exists(SOURCE_DIR):
        print(f"✗ 目录不存在: {SOURCE_DIR}")
        print("请先运行 excel_to_json.py 生成JSON文件")
        return
    
    moved = 0
    unknown_list = []
    
    for filename in os.listdir(SOURCE_DIR):
        if not filename.endswith('.json'):
            continue
        
        filepath = os.path.join(SOURCE_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            polymer = data.get("technical_specifications", {}).get("base_polymer", "Other")
            
            target_dir = TARGET_BASE
            found = False
            for key in POLYMER_MAP:
                if key in polymer.upper():
                    target_dir = os.path.join(TARGET_BASE, POLYMER_MAP[key])
                    found = True
                    break
            
            if not found:
                target_dir = os.path.join(TARGET_BASE, "Other")
                unknown_list.append(filename)
            
            os.makedirs(target_dir, exist_ok=True)
            shutil.copy2(filepath, os.path.join(target_dir, filename))
            moved += 1
            print(f"  ✓ {filename} → {target_dir}/")
        except Exception as e:
            print(f"  ✗ {filename}: {e}")
    
    print("\n" + "="*50)
    print(f"分类完成！共 {moved} 个文件")
    if unknown_list:
        print(f"\n未识别的材料 ({len(unknown_list)}个):")
        for f in unknown_list:
            print(f"  - {f}")
    print("="*50)

if __name__ == "__main__":
    classify()