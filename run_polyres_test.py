#!/usr/bin/env python3
"""
直接运行polyres.py并生成GDS文件进行DRC测试
"""

import sys
import os
import subprocess

# 设置Python路径
sys.path.insert(0, '/workspace/src')

def run_polyres_script():
    """运行polyres.py脚本"""
    print("=== 运行polyres.py脚本 ===")
    
    try:
        # 直接执行polyres.py的main部分
        polyres_script = """
import numpy as np
np.float_ = np.float64

from gdsfactory.components import rectangle
from gdsfactory import Component
from glayout.pdk.mappedpdk import MappedPDK
from glayout.primitives.via_gen import via_array
from glayout.util.comp_utils import prec_ref_center, movey, align_comp_to_port, movex
from glayout.util.port_utils import add_ports_perimeter
from glayout.pdk.sky130_mapped import sky130_mapped_pdk
from glayout.pdk.gf180_mapped import gf180_mapped_pdk
from glayout.spice import Netlist
from glayout.primitives.guardring import tapring

# 导入polyresistor函数
from glayout.primitives.polyres import poly_resistor, add_polyres_labels

print("✓ 所有导入成功")

# 创建P型非硅化polyresistor
print("创建P型非硅化polyresistor...")
resistor = add_polyres_labels(gf180_mapped_pdk, poly_resistor(gf180_mapped_pdk, width=0.8, fingers=1, is_snake=True, n_type=False, silicided=False), 1.65, 0.8, 1) 
resistor.name = "POLY_RES_P_UNSAL"

# 保存GDS文件
gds_file = "/workspace/polyres_test.gds"
resistor.write_gds(gds_file)
print(f"✓ GDS文件已保存: {gds_file}")

# 显示网表
if 'netlist' in resistor.info:
    print("生成的网表:")
    print(resistor.info['netlist'].generate_netlist())
"""
        
        # 执行脚本
        exec(polyres_script)
        return True
        
    except Exception as e:
        print(f"✗ 运行polyres.py失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_klayout_drc_on_polyres():
    """对polyresistor运行Klayout DRC"""
    print("\n=== 运行Klayout DRC ===")
    
    gds_file = "/workspace/polyres_test.gds"
    if not os.path.exists(gds_file):
        print(f"✗ GDS文件不存在: {gds_file}")
        return False
    
    try:
        # 使用GF180 DRC规则
        drc_script = "/foss/pdks/ciel/gf180mcu/versions/f2e289da6753f26157a308c492cf990fdcd4932d/gf180mcuD/libs.tech/klayout/macros/gf180mcu_drc.lydrc"
        
        if not os.path.exists(drc_script):
            print(f"✗ DRC脚本不存在: {drc_script}")
            return False
        
        # 运行Klayout DRC
        cmd = [
            "/foss/tools/klayout/klayout",
            "-b",  # batch mode
            "-r", drc_script,  # run DRC script
            gds_file
        ]
        
        print(f"运行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print("标准输出:")
            print(result.stdout)
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("✗ DRC运行超时")
        return False
    except Exception as e:
        print(f"✗ DRC运行失败: {e}")
        return False

def main():
    """主函数"""
    print("开始测试polyres.py的DRC功能...")
    print("=" * 50)
    
    # 运行polyres.py脚本
    if not run_polyres_script():
        print("✗ 无法运行polyres.py脚本")
        return
    
    # 运行DRC测试
    drc_result = run_klayout_drc_on_polyres()
    
    # 输出总结
    print("\n" + "=" * 50)
    print("测试总结:")
    print(f"  polyres.py脚本: ✓ 通过")
    print(f"  Klayout DRC: {'✓ 通过' if drc_result else '✗ 失败'}")
    
    if drc_result:
        print("\n🎉 polyres.py DRC测试成功！")
    else:
        print("\n⚠ DRC测试失败，请检查错误信息。")

if __name__ == "__main__":
    main()
