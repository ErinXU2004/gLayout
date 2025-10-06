#!/usr/bin/env python3
"""
Simple test script for polyres.py in Docker VNC environment
"""

import sys
import os

# Add the source directory to Python path
sys.path.insert(0, '/workspace/src')

print("=== Simple polyres.py Test ===")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Check if polyres.py exists
polyres_path = '/workspace/src/glayout/primitives/polyres.py'
if os.path.exists(polyres_path):
    print(f"✓ Found polyres.py: {polyres_path}")
else:
    print(f"✗ polyres.py not found: {polyres_path}")
    print("Available files in /workspace/src/glayout/primitives/:")
    try:
        for f in os.listdir('/workspace/src/glayout/primitives/'):
            print(f"  - {f}")
    except:
        print("  Directory not found")

# Test import
print("\n1. Testing imports...")
try:
    from glayout.primitives.polyres import poly_resistor, add_polyres_labels
    from glayout.pdk.gf180_mapped import gf180_mapped_pdk
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    print("Trying alternative import method...")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("polyres", polyres_path)
        polyres_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(polyres_module)
        print("✓ Alternative import successful")
    except Exception as e2:
        print(f"✗ Alternative import also failed: {e2}")
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

print("\n3. Test completed!")
print(f"GDS file: {os.path.abspath('polyres_test.gds')}")
print("View with: klayout polyres_test.gds")
