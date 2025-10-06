#!/usr/bin/env python3
"""
VNC-specific test script for polyres.py
"""

import sys
import os

# Set up paths for VNC environment
sys.path.insert(0, '/foss/designs/glayout/src')

print("=== VNC polyres.py Test ===")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Check if polyres.py exists
polyres_path = '/foss/designs/glayout/src/glayout/primitives/polyres.py'
if os.path.exists(polyres_path):
    print(f"✓ Found polyres.py: {polyres_path}")
else:
    print(f"✗ polyres.py not found: {polyres_path}")
    exit(1)

# Test import
print("\n1. Testing imports...")
try:
    from glayout.primitives.polyres import poly_resistor, add_polyres_labels
    from glayout.pdk.gf180_mapped import gf180_mapped_pdk
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    exit(1)

# Generate GDS file
print("\n2. Generating polyresistor GDS...")
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
        print(f"✓ File exists: {os.path.abspath(gds_file)}")
    else:
        print(f"✗ File not found: {gds_file}")
        
except Exception as e:
    print(f"✗ GDS generation failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Show netlist
print("\n3. Generated netlist:")
if 'netlist' in resistor.info:
    print(resistor.info['netlist'].generate_netlist())
else:
    print("No netlist information available")

print("\n4. Test completed successfully!")
print(f"GDS file: {os.path.abspath('polyres_test.gds')}")
print("View with: klayout polyres_test.gds")
