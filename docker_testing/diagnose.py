#!/usr/bin/env python3
"""
Diagnostic script for VNC Docker environment
"""

import sys
import os

print("=== Docker VNC Environment Diagnosis ===")
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

print("\n=== Directory Structure ===")
for path in ['/workspace', '/foss/designs', '/foss/designs/glayout', '.']:
    if os.path.exists(path):
        print(f"✓ {path} exists")
        try:
            contents = os.listdir(path)
            print(f"  Contents: {contents[:10]}...")  # Show first 10 items
        except:
            print(f"  Cannot list contents")
    else:
        print(f"✗ {path} does not exist")

print("\n=== Looking for glayout ===")
glayout_found = False
for base in ['/workspace', '/foss/designs/glayout', '/foss/designs', '.', '..']:
    glayout_path = os.path.join(base, 'src', 'glayout')
    if os.path.exists(glayout_path):
        print(f"✓ Found glayout at: {glayout_path}")
        glayout_found = True
        
        # Check primitives directory
        primitives_path = os.path.join(glayout_path, 'primitives')
        if os.path.exists(primitives_path):
            print(f"  ✓ Primitives directory exists")
            try:
                files = os.listdir(primitives_path)
                print(f"  Files: {files}")
                if 'polyres.py' in files:
                    print(f"  ✓ polyres.py found!")
                else:
                    print(f"  ✗ polyres.py not found")
            except:
                print(f"  ✗ Cannot list primitives directory")
        else:
            print(f"  ✗ Primitives directory not found")
        
        # Add to Python path
        sys.path.insert(0, os.path.join(base, 'src'))
        print(f"  ✓ Added to Python path: {os.path.join(base, 'src')}")

if not glayout_found:
    print("✗ glayout not found in any expected location")

print(f"\n=== Python Path ===")
for i, path in enumerate(sys.path):
    print(f"{i}: {path}")

print("\n=== Testing Import ===")
try:
    from glayout.primitives.polyres import poly_resistor
    print("✓ Successfully imported poly_resistor")
except Exception as e:
    print(f"✗ Import failed: {e}")

print("\n=== Diagnosis Complete ===")
