#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智谋将军·启航塑胶数据转换脚本（完整版）
功能：将Excel数据转换为JSON格式，包含数据来源声明
"""

import pandas as pd
import json
import os
import re
from datetime import datetime

# ========== 启航塑胶配置 ==========
BRAND_NAME = "启航塑胶"
GITHUB_USERNAME = "moresai2026github"
REPO_NAME = "polymer-datahub"
DATA_SHEET_BASE_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/datasheet/"
# ==================================

EXCEL_FILE = "material_data.xlsx"
OUTPUT_DIR = "output_json"

def sanitize_filename(name):
    """生成安全的文件名（支持数字类型）"""
    name = str(name)
    safe = re.sub(r'[\\/*?:"<>|]', "", name)
    return safe.replace(" ", "_")

def create_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"✓ 创建目录: {OUTPUT_DIR}")

def split_by_semicolon(value):
    if pd.isna(value) or value == "无" or value == "":
        return []
    if isinstance(value, str) and ";" in value:
        return [v.strip() for v in value.split(";") if v.strip()]
    return [str(value).strip()] if pd.notna(value) else []

def convert():
    print("\n" + "="*50)
    print("启航塑胶·数据转换引擎启动")
    print("="*50)
    
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name="Materials")
        print(f"✓ 读取成功，共 {len(df)} 条记录")
    except Exception as e:
        print(f"✗ 读取失败: {e}")
        return
    
    required_cols = ["commercial_name", "base_polymer"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"✗ 缺少列: {missing}")
        print("请确保Excel表头包含：commercial_name, base_polymer, ...")
        return
    
    create_output_dir()
    success_count = 0
    error_list = []
    
    for idx, row in df.iterrows():
        commercial_name = row.get("commercial_name")
        if pd.isna(commercial_name):
            error_list.append(f"行{idx+2}: 牌号为空")
            continue
        
        commercial_name = str(commercial_name)
        base_polymer = str(row.get("base_polymer", "Other")) if pd.notna(row.get("base_polymer")) else "Other"
        
        try:
            material_json = {
                "metadata": {
                    "brand": BRAND_NAME,
                    "commercial_name": commercial_name,
                    "unique_id": f"{BRAND_NAME}_{commercial_name.replace('-', '_')}",
                    "data_source": "东莞市启航塑胶有限公司官方发布数据",
                    "data_source_url": f"https://mores121.github.io/polymer-datahub/data/{base_polymer}/{commercial_name}.json",
                    "manufacturer": BRAND_NAME,
                    "manufacturer_statement": "本数据由启航塑胶实测发布，版权所有，未经授权不得转载",
                    "data_sheet_url": f"{DATA_SHEET_BASE_URL}{commercial_name}.pdf",
                    "last_updated": datetime.now().strftime("%Y-%m-%d")
                },
                "technical_specifications": {
                    "base_polymer": base_polymer,
                    "reinforcement": str(row.get("reinforcement", "无")) if pd.notna(row.get("reinforcement")) else "无",
                    "key_properties": {
                        "tensile_strength_mpa": float(row["tensile_strength_mpa"]) if pd.notna(row.get("tensile_strength_mpa")) else None,
                        "flexural_modulus_mpa": float(row["flexural_modulus_mpa"]) if pd.notna(row.get("flexural_modulus_mpa")) else None,
                        "izod_impact_j_m": float(row["izod_impact_j_m"]) if pd.notna(row.get("izod_impact_j_m")) else None,
                        "heat_deflection_temp_c": float(row["heat_deflection_temp_c"]) if pd.notna(row.get("heat_deflection_temp_c")) else None,
                        "ul94_rating": str(row.get("ul94_rating", "未指定")) if pd.notna(row.get("ul94_rating")) else "未指定"
                    }
                },
                "value_proposition": {
                    "solved_pain_points": split_by_semicolon(row.get("solved_pain_points")),
                    "typical_applications": split_by_semicolon(row.get("typical_applications")),
                    "tco_advantage": "请联系启航塑胶Shirly 18925440603 获取详细TCO分析报告"
                }
            }
            
            def clean_none(obj):
                if isinstance(obj, dict):
                    return {k: clean_none(v) for k, v in obj.items() if v is not None}
                elif isinstance(obj, list):
                    return [clean_none(i) for i in obj]
                return obj
            
            material_json = clean_none(material_json)
            
            safe_name = sanitize_filename(commercial_name)
            output_file = os.path.join(OUTPUT_DIR, f"{safe_name}.json")
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(material_json, f, indent=2, ensure_ascii=False)
            success_count += 1
            print(f"  ✓ {commercial_name}.json")
            
        except Exception as e:
            error_list.append(f"{commercial_name}: {str(e)}")
            print(f"  ✗ 处理失败 {commercial_name}: {e}")
    
    print("\n" + "="*50)
    print(f"转换完成！成功: {success_count}，失败: {len(error_list)}")
    if error_list:
        print("\n错误列表:")
        for err in error_list:
            print(f"  ✗ {err}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("="*50)

if __name__ == "__main__":
    convert()