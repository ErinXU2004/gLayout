# Docker DRC Testing Guide

This folder contains instructions for testing polyres.py DRC compliance using Docker container's built-in tools.

## Available Tools in Docker Container

The IIC-OSIC-TOOLS Docker container includes the following EDA tools:

- **Klayout**: For GDS file viewing and DRC checking
- **Magic**: For layout editing and DRC verification  
- **Netgen**: For LVS (Layout vs Schematic) checking
- **PDK Rules**: Pre-installed DRC rules for SKY130 and GF180

## Quick Test Steps

### 1. Access VNC Desktop
- Open browser: `http://localhost:6080`
- Password: `osic`

### 2. Update Code
```bash
cd /workspace
git pull origin main
export PYTHONPATH="/workspace/src:$PYTHONPATH"
```

### 3. Test polyres.py Import
```bash
python3 -c "
import sys
sys.path.insert(0, '/workspace/src')
from glayout.primitives.polyres import poly_resistor, add_polyres_labels
from glayout.pdk.gf180_mapped import gf180_mapped_pdk
print('✓ Import successful')
"
```

### 4. Generate GDS File
```bash
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
```

### 5. View GDS File
```bash
klayout polyres_test.gds &
```

### 6. Run DRC Check
```bash
# Find available DRC rules
find /foss -name "*drc*" -type f | grep -E "(sky130|gf180)" | head -5

# Run DRC with Klayout
klayout -b -r /foss/pdks/ciel/gf180mcu/versions/*/gf180mcuD/libs.tech/klayout/macros/gf180mcu_drc.lydrc polyres_test.gds
```

### 7. Run LVS Check
```bash
# Find LVS rules
find /foss -name "*lvs*" -type f | head -5

# Run LVS with Netgen
netgen -batch lvs polyres_test.gds polyres_test.gds /foss/pdks/ciel/gf180mcu/versions/*/gf180mcuD/libs.tech/netgen/gf180mcu_setup.tcl
```

## Available PDK Rules

### SKY130
- DRC: `/foss/pdks/ciel/sky130/versions/*/sky130A/libs.tech/klayout/macros/run_drc_full.lydrc`
- LVS: `/foss/pdks/ciel/sky130/versions/*/sky130A/libs.tech/netgen/sky130A_setup.tcl`

### GF180
- DRC: `/foss/pdks/ciel/gf180mcu/versions/*/gf180mcuD/libs.tech/klayout/macros/gf180mcu_drc.lydrc`
- LVS: `/foss/pdks/ciel/gf180mcu/versions/*/gf180mcuD/libs.tech/netgen/gf180mcu_setup.tcl`

## Troubleshooting

### If Import Fails
- Check Python path: `echo $PYTHONPATH`
- Verify file exists: `ls -la /workspace/src/glayout/primitives/polyres.py`

### If DRC Fails
- Check GDS file: `ls -la polyres_test.gds`
- Verify DRC rule exists: `ls -la /foss/pdks/ciel/gf180mcu/versions/*/gf180mcuD/libs.tech/klayout/macros/gf180mcu_drc.lydrc`

### If Tools Not Found
- Check tool paths: `which klayout magic netgen`
- Restart container if needed
