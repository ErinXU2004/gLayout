#!/usr/bin/env python3
"""
Simple test script for polyres.py in Docker VNC environment
"""

import sys
import os

# Add the source directory to Python path
# Try multiple possible paths
possible_paths = [
    '/workspace/src',
    '/foss/designs/glayout/src',
    '/foss/designs/src',
    './src',
    '../src'
]

for path in possible_paths:
    if os.path.exists(path):
        sys.path.insert(0, path)
        print(f"✓ Added to Python path: {path}")
        break

print("=== Simple polyres.py Test ===")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Check if polyres.py exists in multiple locations
possible_polyres_paths = [
    '/workspace/src/glayout/primitives/polyres.py',
    '/foss/designs/glayout/src/glayout/primitives/polyres.py',
    '/foss/designs/src/glayout/primitives/polyres.py',
    './src/glayout/primitives/polyres.py',
    '../src/glayout/primitives/polyres.py'
]

polyres_path = None
for path in possible_polyres_paths:
    if os.path.exists(path):
        polyres_path = path
        print(f"✓ Found polyres.py: {path}")
        break

if not polyres_path:
    print("✗ polyres.py not found in any expected location")
    print("Searching for glayout directories...")
    for base_path in ['/workspace', '/foss/designs/glayout', '/foss/designs', '.', '..']:
        glayout_path = os.path.join(base_path, 'src', 'glayout')
        if os.path.exists(glayout_path):
            print(f"  Found glayout at: {glayout_path}")
            try:
                primitives_path = os.path.join(glayout_path, 'primitives')
                if os.path.exists(primitives_path):
                    print(f"    Primitives directory: {primitives_path}")
                    for f in os.listdir(primitives_path):
                        print(f"      - {f}")
            except:
                pass

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
