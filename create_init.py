#!/usr/bin/env python3
"""Create the __init__.py file with proper encoding"""

content = '''"""
@author: Pablo Apiolazza
@title: ComfyUI APZmedia PSD Tools
@nickname: ComfyUI PSD Tools
@description: This extension provides PSD layer saving functionalities with mask support for ComfyUI.
"""

import os
import sys
import logging
import importlib.util

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize node mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Get the directory where this __init__.py file is located
extension_root = os.path.dirname(os.path.abspath(__file__))
print(f"Extension root directory: {extension_root}")

# Check for pytoshop availability
try:
    import pytoshop
    PYTOSHOP_AVAILABLE = True
    print("pytoshop is available")
except ImportError:
    PYTOSHOP_AVAILABLE = False
    print("pytoshop not available - PSD nodes will not be registered")
    print("   To install: pip install pytoshop psd-tools")

# Only proceed with node registration if pytoshop is available
if PYTOSHOP_AVAILABLE:
    print("Starting PSD node import process...")
    try:
        # Import PSD nodes using importlib for cross-platform compatibility
        nodes_dir = os.path.join(extension_root, "nodes")
        print(f"Nodes directory: {nodes_dir}")
        
        # Check if nodes directory exists
        if not os.path.exists(nodes_dir):
            print(f"ERROR: Nodes directory not found: {nodes_dir}")
            raise FileNotFoundError(f"Nodes directory not found: {nodes_dir}")
        
        # Import apzPSDLayerSaver
        print("Importing apzPSDLayerSaver...")
        psd_saver_path = os.path.join(nodes_dir, "apzPSDLayerSaver.py")
        print(f"PSD saver path: {psd_saver_path}")
        
        if not os.path.exists(psd_saver_path):
            print(f"ERROR: PSD saver file not found: {psd_saver_path}")
            raise FileNotFoundError(f"PSD saver file not found: {psd_saver_path}")
        
        spec = importlib.util.spec_from_file_location("apzPSDLayerSaver", psd_saver_path)
        psd_saver_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(psd_saver_module)
        print("Successfully imported apzPSDLayerSaver module")
        
        # Import apzPSDLayerSaver8Layers
        print("Importing apzPSDLayerSaver8Layers...")
        psd_8layer_path = os.path.join(nodes_dir, "apzPSDLayerSaver8Layers.py")
        print(f"PSD 8-layer path: {psd_8layer_path}")
        
        if not os.path.exists(psd_8layer_path):
            print(f"ERROR: PSD 8-layer file not found: {psd_8layer_path}")
            raise FileNotFoundError(f"PSD 8-layer file not found: {psd_8layer_path}")
        
        spec = importlib.util.spec_from_file_location("apzPSDLayerSaver8Layers", psd_8layer_path)
        psd_8layer_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(psd_8layer_module)
        print("Successfully imported apzPSDLayerSaver8Layers module")
        
        # Register nodes
        print("Registering PSD nodes...")
        NODE_CLASS_MAPPINGS["APZmediaPSDLayerSaver"] = psd_saver_module.APZmediaPSDLayerSaver
        NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDLayerSaver"] = "APZmedia PSD Layer Saver"
        print("Registered APZmediaPSDLayerSaver")
        
        NODE_CLASS_MAPPINGS["APZmediaPSDLayerSaverAdvanced"] = psd_saver_module.APZmediaPSDLayerSaverAdvanced
        NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDLayerSaverAdvanced"] = "APZmedia PSD Layer Saver Advanced"
        print("Registered APZmediaPSDLayerSaverAdvanced")
        
        NODE_CLASS_MAPPINGS["APZmediaPSDLayerSaver8Layers"] = psd_8layer_module.APZmediaPSDLayerSaver8Layers
        NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDLayerSaver8Layers"] = "APZmedia PSD Layer Saver (8 Layers)"
        print("Registered APZmediaPSDLayerSaver8Layers")
        
        NODE_CLASS_MAPPINGS["APZmediaPSDLayerSaver8LayersAdvanced"] = psd_8layer_module.APZmediaPSDLayerSaver8LayersAdvanced
        NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDLayerSaver8LayersAdvanced"] = "APZmedia PSD Layer Saver (8 Layers Advanced)"
        print("Registered APZmediaPSDLayerSaver8LayersAdvanced")
        
        print(f"Successfully registered {len(NODE_CLASS_MAPPINGS)} PSD nodes")
        logger.info(f"Registered {len(NODE_CLASS_MAPPINGS)} PSD nodes: {list(NODE_CLASS_MAPPINGS.keys())}")
        
    except ImportError as e:
        print(f"Failed to import PSD nodes: {e}")
        logger.error(f"Failed to import PSD nodes: {e}")
    except Exception as e:
        print(f"Error registering PSD nodes: {e}")
        logger.error(f"Error registering PSD nodes: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Skipping PSD node registration - pytoshop not available")
    logger.info("Skipping PSD node registration - pytoshop not available")

print(f"ComfyUI PSD Tools extension loaded - {len(NODE_CLASS_MAPPINGS)} nodes available")
if NODE_CLASS_MAPPINGS:
    print("Available nodes:")
    for key, value in NODE_CLASS_MAPPINGS.items():
        print(f"  - {key}: {value}")
else:
    print("No nodes were registered")
'''

with open('__init__.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('__init__.py created successfully')
