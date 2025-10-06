#!/bin/bash
# Quick test script for polyres.py DRC in Docker VNC environment

echo "=== Docker DRC Test for polyres.py ==="

# Set up environment
cd /workspace
export PYTHONPATH="/workspace/src:$PYTHONPATH"

echo "1. Testing imports..."
python3 -c "
import sys
sys.path.insert(0, '/workspace/src')
from glayout.primitives.polyres import poly_resistor, add_polyres_labels
from glayout.pdk.gf180_mapped import gf180_mapped_pdk
print('✓ Imports successful')
"

echo "2. Generating polyresistor GDS..."
python3 -c "
import sys
sys.path.insert(0, '/workspace/src')
from glayout.primitives.polyres import poly_resistor, add_polyres_labels
from glayout.pdk.gf180_mapped import gf180_mapped_pdk

resistor = add_polyres_labels(
    gf180_mapped_pdk, 
    poly_resistor(gf180_mapped_pdk, width=0.8, fingers=1, is_snake=True, n_type=False, silicided=False), 
    1.65, 0.8, 1
)
resistor.name = 'POLY_RES_P_UNSAL'
resistor.write_gds('polyres_test.gds')
print('✓ GDS file saved: polyres_test.gds')
"

echo "3. Finding DRC rules..."
find /foss -name "*drc*" -type f | grep -E "(sky130|gf180)" | head -3

echo "4. Running DRC check..."
DRC_RULE=$(find /foss -name "*gf180mcu_drc.lydrc" | head -1)
if [ -n "$DRC_RULE" ]; then
    echo "Using DRC rule: $DRC_RULE"
    klayout -b -r "$DRC_RULE" polyres_test.gds
else
    echo "No DRC rule found"
fi

echo "5. Test completed!"
echo "GDS file: /workspace/polyres_test.gds"
echo "View with: klayout polyres_test.gds"
