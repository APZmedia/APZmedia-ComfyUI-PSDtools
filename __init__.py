"""
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

# Check for psd-tools availability
try:
    from psd_tools import PSDImage
    PSD_TOOLS_AVAILABLE = True
    print("psd-tools is available")
except ImportError:
    PSD_TOOLS_AVAILABLE = False
    print("psd-tools not available - PSD nodes will not be registered")
    print("   To install: pip install psd-tools")

# Only proceed with node registration if psd-tools is available
if PSD_TOOLS_AVAILABLE:
    print("Starting PSD node import process...")
    try:
        # Import PSD nodes using importlib for cross-platform compatibility
        nodes_dir = os.path.join(extension_root, "nodes")
        print(f"Nodes directory: {nodes_dir}")
        
        # Check if nodes directory exists
        if not os.path.exists(nodes_dir):
            print(f"ERROR: Nodes directory not found: {nodes_dir}")
            raise FileNotFoundError(f"Nodes directory not found: {nodes_dir}")
        
        
        # Import apzPSDLayerSaverRefactored
        print("Importing apzPSDLayerSaverRefactored...")
        psd_refactored_path = os.path.join(nodes_dir, "apzPSDLayerSaverRefactored.py")
        print(f"PSD refactored path: {psd_refactored_path}")
        
        if not os.path.exists(psd_refactored_path):
            print(f"ERROR: PSD refactored file not found: {psd_refactored_path}")
            raise FileNotFoundError(f"PSD refactored file not found: {psd_refactored_path}")
        
        spec = importlib.util.spec_from_file_location("apzPSDLayerSaverRefactored", psd_refactored_path)
        psd_refactored_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(psd_refactored_module)
        print("Successfully imported apzPSDLayerSaverRefactored module")
        
        # Import apzPSDLayerLoader
        print("Importing apzPSDLayerLoader...")
        psd_loader_path = os.path.join(nodes_dir, "apzPSDLayerLoader.py")
        print(f"PSD loader path: {psd_loader_path}")
        
        if not os.path.exists(psd_loader_path):
            print(f"ERROR: PSD loader file not found: {psd_loader_path}")
            raise FileNotFoundError(f"PSD loader file not found: {psd_loader_path}")
        
        spec = importlib.util.spec_from_file_location("apzPSDLayerLoader", psd_loader_path)
        psd_loader_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(psd_loader_module)
        print("Successfully imported apzPSDLayerLoader module")
        
        # Register nodes
        print("Registering PSD nodes...")
        NODE_CLASS_MAPPINGS["APZmediaPSDLayerSaver"] = psd_refactored_module.APZmediaPSDLayerSaverRefactored
        NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDLayerSaver"] = "APZmedia PSD Layer Saver"
        print("Registered APZmediaPSDLayerSaver")
        
        NODE_CLASS_MAPPINGS["APZmediaPSDLayerLoader"] = psd_loader_module.APZmediaPSDLayerLoader
        NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDLayerLoader"] = "APZmedia PSD Layer Loader"
        print("Registered APZmediaPSDLayerLoader")
        
        NODE_CLASS_MAPPINGS["APZmediaPSDInfoLoader"] = psd_loader_module.APZmediaPSDInfoLoader
        NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDInfoLoader"] = "APZmedia PSD Info Loader"
        print("Registered APZmediaPSDInfoLoader")
        
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
    print("Skipping PSD node registration - psd-tools not available")
    logger.info("Skipping PSD node registration - psd-tools not available")

print(f"ComfyUI PSD Tools extension loaded - {len(NODE_CLASS_MAPPINGS)} nodes available")
if NODE_CLASS_MAPPINGS:
    print("Available nodes:")
    for key, value in NODE_CLASS_MAPPINGS.items():
        print(f"  - {key}: {value}")
else:
    print("No nodes were registered")
