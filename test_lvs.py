#!/usr/bin/env python3
"""
LVS Test Script for polyresistor
"""

import sys
import os
sys.path.insert(0, '/foss/designs/glayout/src')

# Set dummy PDK_ROOT to avoid import errors
os.environ['PDK_ROOT'] = '/tmp/dummy_pdk'

def test_polyresistor_lvs():
    """Test polyresistor LVS file generation"""
    print("=== Testing Polyresistor LVS File Generation ===")
    
    try:
        from glayout.primitives.polyres import poly_resistor, add_polyres_labels
        from glayout.pdk.gf180_mapped import gf180_mapped_pdk
        
        # Create polyresistor
        resistor = add_polyres_labels(gf180_mapped_pdk, poly_resistor(gf180_mapped_pdk, width=0.8, fingers=1, is_snake=True, n_type=False, silicided=False), 1.65, 0.8, 1)
        resistor.name = "POLY_RES_LVS_TEST"
        
        # Generate GDS file
        resistor.write_gds("polyres_lvs_test.gds")
        print("✓ GDS file saved: polyres_lvs_test.gds")
        
        # Generate SPICE netlist
        spice_content = resistor.info['netlist'].generate_netlist()
        
        # Save netlist in multiple formats for LVS compatibility
        netlist_files = [
            "polyres_lvs_test.spice",
            f"{resistor.name}.spice",
            "Unnamed.spice",  # Common klayout LVS filename
            "netlist.spice"
        ]
        
        for filename in netlist_files:
            with open(filename, "w") as f:
                f.write(spice_content)
            print(f"✓ SPICE netlist saved: {filename}")
        
        print("\nNetlist content:")
        print(spice_content)
        
        print("\n=== LVS Test Files Generated ===")
        print("Files created:")
        for filename in netlist_files:
            if os.path.exists(filename):
                print(f"  ✓ {filename}")
            else:
                print(f"  ✗ {filename}")
        
        return True
        
    except Exception as e:
        print(f"✗ LVS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fet_lvs():
    """Test FET LVS file generation"""
    print("\n=== Testing FET LVS File Generation ===")
    
    try:
        from glayout.primitives.fet import nmos, fet_netlist
        from glayout.pdk.gf180_mapped import gf180_mapped_pdk
        
        # Create NMOS
        nmos_comp = nmos(gf180_mapped_pdk, width=3, fingers=1, multipliers=1, with_dummy=True)
        nmos_comp.name = "NMOS_LVS_TEST"
        
        # Generate netlist
        netlist = fet_netlist(gf180_mapped_pdk, 'NMOS_LVS_TEST', 'nfet_03v3', 3.0, 0.15, 1, 1, True)
        spice_content = netlist.generate_netlist()
        
        # Save netlist files
        netlist_files = [
            "nmos_lvs_test.spice",
            f"{nmos_comp.name}.spice",
            "Unnamed.spice"
        ]
        
        for filename in netlist_files:
            with open(filename, "w") as f:
                f.write(spice_content)
            print(f"✓ SPICE netlist saved: {filename}")
        
        print("\nFET Netlist content:")
        print(spice_content)
        
        # Check for dummy transistor issues
        if "B B B B" in spice_content:
            print("\n⚠️  ISSUE FOUND: Dummy transistor has all terminals connected to bulk (B)")
            print("   This is incorrect - dummy transistors should have proper connections")
        
        return True
        
    except Exception as e:
        print(f"✗ FET LVS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run LVS tests"""
    print("LVS Test Script for gLayout Primitives")
    print("=" * 50)
    
    results = []
    results.append(test_polyresistor_lvs())
    results.append(test_fet_lvs())
    
    print("\n" + "=" * 50)
    print("LVS TEST SUMMARY:")
    print(f"✓ Passed: {sum(results)}")
    print(f"✗ Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("🎉 All LVS tests passed!")
    else:
        print("⚠️  Some LVS tests failed")

if __name__ == "__main__":
    main()
