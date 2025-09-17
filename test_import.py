#!/usr/bin/env python3
"""
Test script to verify import methods work
"""

import os
import sys
import importlib.util

# Set up paths
extension_root = os.path.dirname(os.path.abspath(__file__))
nodes_path = os.path.join(extension_root, "nodes")
utils_path = os.path.join(extension_root, "utils")

print(f"Extension directory: {extension_root}")
print(f"Nodes directory: {nodes_path}")
print(f"Utils directory: {utils_path}")

# Add paths to sys.path
if nodes_path not in sys.path:
    sys.path.insert(0, nodes_path)
if utils_path not in sys.path:
    sys.path.insert(0, utils_path)
if extension_root not in sys.path:
    sys.path.insert(0, extension_root)

# Test pytoshop availability
try:
    import pytoshop
    print("✅ pytoshop is available")
    PYTOSHOP_AVAILABLE = True
except ImportError:
    print("❌ pytoshop not available")
    PYTOSHOP_AVAILABLE = False

if PYTOSHOP_AVAILABLE:
    # Test Method 1: Direct import
    try:
        print("\n--- Testing Method 1: Direct import ---")
        import nodes.apzPSDLayerSaver as psd_saver_module
        APZmediaPSDLayerSaver = psd_saver_module.APZmediaPSDLayerSaver
        print("✅ Method 1: Direct import successful")
    except Exception as e:
        print(f"❌ Method 1 failed: {e}")
        
        # Test Method 2: importlib.util
        try:
            print("\n--- Testing Method 2: importlib.util ---")
            psd_saver_path = os.path.join(nodes_path, "apzPSDLayerSaver.py")
            spec = importlib.util.spec_from_file_location("apzPSDLayerSaver", psd_saver_path)
            psd_saver_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(psd_saver_module)
            APZmediaPSDLayerSaver = psd_saver_module.APZmediaPSDLayerSaver
            print("✅ Method 2: importlib.util successful")
        except Exception as e2:
            print(f"❌ Method 2 failed: {e2}")
            
            # Test Method 3: exec
            try:
                print("\n--- Testing Method 3: exec ---")
                psd_saver_path = os.path.join(nodes_path, "apzPSDLayerSaver.py")
                with open(psd_saver_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                namespace = {}
                exec(code, namespace)
                APZmediaPSDLayerSaver = namespace.get('APZmediaPSDLayerSaver')
                if APZmediaPSDLayerSaver:
                    print("✅ Method 3: exec successful")
                else:
                    print("❌ Method 3: Classes not found in namespace")
            except Exception as e3:
                print(f"❌ Method 3 failed: {e3}")

print("\n--- Test Complete ---")
