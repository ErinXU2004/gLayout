#!/usr/bin/env python3
"""
Compatible test script for polyres.py with gdsfactory version handling
"""

import sys
import os

# Set up paths for VNC environment
sys.path.insert(0, '/foss/designs/glayout/src')

print("=== Compatible polyres.py Test ===")
print(f"Current directory: {os.getcwd()}")

# Test gdsfactory import first
print("\n1. Testing gdsfactory compatibility...")
try:
    import gdsfactory
    print(f"✓ gdsfactory version: {gdsfactory.__version__}")
    
    # Try different import methods
    try:
        from gdsfactory import Component
        print("✓ Component imported from gdsfactory")
    except ImportError:
        try:
            from gdsfactory.typings import Component
            print("✓ Component imported from gdsfactory.typings")
        except ImportError:
            print("✗ Cannot import Component from gdsfactory")
            exit(1)
            
except Exception as e:
    print(f"✗ gdsfactory import failed: {e}")
    exit(1)

# Test glayout import
print("\n2. Testing glayout import...")
try:
    from glayout.primitives.polyres import poly_resistor, add_polyres_labels
    from glayout.pdk.gf180_mapped import gf180_mapped_pdk
    print("✓ glayout imports successful")
except Exception as e:
    print(f"✗ glayout import failed: {e}")
    print("This might be due to gdsfactory version compatibility issues")
    exit(1)

# Generate GDS file
print("\n3. Generating polyresistor GDS...")
try:
    resistor = add_polyres_labels(
        gf180_mapped_pdk, 
        poly_resistor(gf180_mapped_pdk, width=0.8, fingers=1, is_snake=True, n_type=False, silicided=False), 
        1.65, 0.8, 1
    )
    resistor.name = 'POLY_RES_P_UNSAL'
    
    # Save to current directory
    gds_file = 'polyres_test.gds'
    resistor.write_gds(gds_file)
    print(f"✓ GDS file saved: {gds_file}")
    
    # Check if file was created
    if os.path.exists(gds_file):
        file_size = os.path.getsize(gds_file)
        print(f"✓ File exists: {os.path.abspath(gds_file)} (size: {file_size} bytes)")
    else:
        print(f"✗ File not found: {gds_file}")
        
except Exception as e:
    print(f"✗ GDS generation failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Show netlist
print("\n4. Generated netlist:")
if 'netlist' in resistor.info:
    print(resistor.info['netlist'].generate_netlist())
else:
    print("No netlist information available")

print("\n5. Test completed successfully!")
print(f"GDS file: {os.path.abspath('polyres_test.gds')}")
print("View with: klayout polyres_test.gds")

# Test DRC if possible
print("\n6. Testing DRC availability...")
drc_rules = []
try:
    import glob
    drc_rules = glob.glob("/foss/pdks/ciel/gf180mcu/versions/*/gf180mcuC/libs.tech/klayout/macros/gf180mcu_drc.lydrc")
    if drc_rules:
        print(f"✓ Found DRC rules: {drc_rules[0]}")
        print("You can run DRC with:")
        print(f"klayout -b -r '{drc_rules[0]}' polyres_test.gds")
    else:
        print("✗ No DRC rules found")
except Exception as e:
    print(f"✗ DRC check failed: {e}")
