"""
@author: Pablo Apiolazza
@title: ComfyUI APZmedia PSD Tools
@nickname: ComfyUI PSD Tools
@description: This extension provides PSD layer saving functionalities with mask support for ComfyUI.
"""

import os
import sys
import traceback
import logging

# Set up logging with console output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Color codes for console output
class Colors:
    ORANGE = '\033[38;5;208m'  # Bright orange
    GREEN = '\033[92m'         # Green
    RED = '\033[91m'           # Red
    YELLOW = '\033[93m'        # Yellow
    BLUE = '\033[94m'          # Blue
    PURPLE = '\033[95m'        # Purple
    CYAN = '\033[96m'          # Cyan
    WHITE = '\033[97m'         # White
    BOLD = '\033[1m'           # Bold
    END = '\033[0m'            # End color

# Add colorful console print statements for immediate visibility
print(f"{Colors.ORANGE}{Colors.BOLD}{'=' * 60}{Colors.END}")
print(f"{Colors.ORANGE}{Colors.BOLD}APZmedia PSD Tools Extension - Starting Load Process{Colors.END}")
print(f"{Colors.ORANGE}{Colors.BOLD}{'=' * 60}{Colors.END}")

# Define the path to the current directory and subdirectories
comfyui_texttools_path = os.path.dirname(os.path.realpath(__file__))
nodes_path = os.path.join(comfyui_texttools_path, "nodes")

print(f"{Colors.CYAN}Extension directory: {Colors.WHITE}{comfyui_texttools_path}{Colors.END}")
print(f"{Colors.CYAN}Nodes directory: {Colors.WHITE}{nodes_path}{Colors.END}")

# Ensure the nodes path is added to sys.path for importing custom nodes
sys.path.append(nodes_path)
print(f"{Colors.CYAN}Added to sys.path: {Colors.WHITE}{nodes_path}{Colors.END}")

# Check if pytoshop is available
try:
    import pytoshop
    print(f"{Colors.GREEN}✅ pytoshop is available{Colors.END}")
except ImportError as e:
    print(f"{Colors.RED}❌ pytoshop not available: {e}{Colors.END}")
    print(f"{Colors.RED}   This will cause node import failures!{Colors.END}")

# Importing custom nodes
APZmediaPSDLayerSaver = None
APZmediaPSDLayerSaverAdvanced = None
APZmediaPSDLayerSaver8Layers = None
APZmediaPSDLayerSaver8LayersAdvanced = None

print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Importing APZmediaPSDLayerSaver ---{Colors.END}")
try:
    from nodes.apzPSDLayerSaver import APZmediaPSDLayerSaver
    print(f"{Colors.GREEN}✅ Successfully imported APZmediaPSDLayerSaver node{Colors.END}")
    logger.info("Successfully imported APZmediaPSDLayerSaver node.")
except Exception as e:
    print(f"{Colors.RED}❌ Failed to import APZmediaPSDLayerSaver node: {e}{Colors.END}")
    logger.error("Failed to import APZmediaPSDLayerSaver node.", exc_info=True)

print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Importing APZmediaPSDLayerSaverAdvanced ---{Colors.END}")
try:
    from nodes.apzPSDLayerSaver import APZmediaPSDLayerSaverAdvanced
    print(f"{Colors.GREEN}✅ Successfully imported APZmediaPSDLayerSaverAdvanced node{Colors.END}")
    logger.info("Successfully imported APZmediaPSDLayerSaverAdvanced node.")
except Exception as e:
    print(f"{Colors.RED}❌ Failed to import APZmediaPSDLayerSaverAdvanced node: {e}{Colors.END}")
    logger.error("Failed to import APZmediaPSDLayerSaverAdvanced node.", exc_info=True)

print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Importing APZmediaPSDLayerSaver8Layers ---{Colors.END}")
try:
    from nodes.apzPSDLayerSaver8Layers import APZmediaPSDLayerSaver8Layers
    print(f"{Colors.GREEN}✅ Successfully imported APZmediaPSDLayerSaver8Layers node{Colors.END}")
    logger.info("Successfully imported APZmediaPSDLayerSaver8Layers node.")
except Exception as e:
    print(f"{Colors.RED}❌ Failed to import APZmediaPSDLayerSaver8Layers node: {e}{Colors.END}")
    logger.error("Failed to import APZmediaPSDLayerSaver8Layers node.", exc_info=True)

print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Importing APZmediaPSDLayerSaver8LayersAdvanced ---{Colors.END}")
try:
    from nodes.apzPSDLayerSaver8Layers import APZmediaPSDLayerSaver8LayersAdvanced
    print(f"{Colors.GREEN}✅ Successfully imported APZmediaPSDLayerSaver8LayersAdvanced node{Colors.END}")
    logger.info("Successfully imported APZmediaPSDLayerSaver8LayersAdvanced node.")
except Exception as e:
    print(f"{Colors.RED}❌ Failed to import APZmediaPSDLayerSaver8LayersAdvanced node: {e}{Colors.END}")
    logger.error("Failed to import APZmediaPSDLayerSaver8LayersAdvanced node.", exc_info=True)

# Utilities should be imported as needed, but not registered as nodes
print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Importing PSD Utilities ---{Colors.END}")
try:
    from utils import apz_psd_conversion
    from utils import apz_psd_mask_utility
    from utils import apz_image_conversion
    print(f"{Colors.GREEN}✅ Successfully imported PSD utility modules{Colors.END}")
    logger.info("Successfully imported PSD utility modules.")
except Exception as e:
    print(f"{Colors.RED}❌ Failed to import PSD utility modules: {e}{Colors.END}")
    logger.error("Failed to import PSD utility modules.", exc_info=True)

# Build node mappings only for successfully imported nodes
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if APZmediaPSDLayerSaver is not None:
    NODE_CLASS_MAPPINGS["APZmediaPSDLayerSaver"] = APZmediaPSDLayerSaver
    NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDLayerSaver"] = "APZmedia PSD Layer Saver"

if APZmediaPSDLayerSaverAdvanced is not None:
    NODE_CLASS_MAPPINGS["APZmediaPSDLayerSaverAdvanced"] = APZmediaPSDLayerSaverAdvanced
    NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDLayerSaverAdvanced"] = "APZmedia PSD Layer Saver Advanced"

if APZmediaPSDLayerSaver8Layers is not None:
    NODE_CLASS_MAPPINGS["APZmediaPSDLayerSaver8Layers"] = APZmediaPSDLayerSaver8Layers
    NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDLayerSaver8Layers"] = "APZmedia PSD Layer Saver (8 Layers)"

if APZmediaPSDLayerSaver8LayersAdvanced is not None:
    NODE_CLASS_MAPPINGS["APZmediaPSDLayerSaver8LayersAdvanced"] = APZmediaPSDLayerSaver8LayersAdvanced
    NODE_DISPLAY_NAME_MAPPINGS["APZmediaPSDLayerSaver8LayersAdvanced"] = "APZmedia PSD Layer Saver (8 Layers Advanced)"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Additional setup, such as threading or other initializations, can be added here if necessary

# Final summary
print(f"\n{Colors.ORANGE}{Colors.BOLD}{'=' * 60}{Colors.END}")
print(f"{Colors.ORANGE}{Colors.BOLD}APZmedia PSD Tools Extension - Load Complete{Colors.END}")
print(f"{Colors.ORANGE}{Colors.BOLD}{'=' * 60}{Colors.END}")

successful_nodes = len(NODE_CLASS_MAPPINGS)
total_nodes = 4

if successful_nodes == total_nodes:
    print(f"{Colors.GREEN}🎉 SUCCESS: All {successful_nodes}/{total_nodes} nodes loaded successfully!{Colors.END}")
else:
    print(f"{Colors.YELLOW}⚠️  PARTIAL: {successful_nodes}/{total_nodes} nodes loaded successfully{Colors.END}")

print(f"{Colors.CYAN}Registered nodes: {Colors.WHITE}{list(NODE_CLASS_MAPPINGS.keys())}{Colors.END}")
print(f"{Colors.CYAN}Node display names: {Colors.WHITE}{list(NODE_DISPLAY_NAME_MAPPINGS.keys())}{Colors.END}")

if successful_nodes > 0:
    print(f"{Colors.GREEN}✅ Look for PSD nodes in ComfyUI under: image/psd{Colors.END}")
    print(f"{Colors.GREEN}✅ Or search for: 'APZmedia' or 'PSD'{Colors.END}")
else:
    print(f"{Colors.RED}❌ No nodes were loaded. Check the errors above.{Colors.END}")

print(f"{Colors.ORANGE}{Colors.BOLD}{'=' * 60}{Colors.END}")

logger.info("ComfyUI PSD Tools extension has been loaded successfully.")
logger.info(f"Registered {len(NODE_CLASS_MAPPINGS)} nodes: {list(NODE_CLASS_MAPPINGS.keys())}")
logger.info(f"Node display names: {list(NODE_DISPLAY_NAME_MAPPINGS.keys())}")
