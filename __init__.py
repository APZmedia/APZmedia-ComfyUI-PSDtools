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

print(f"{Colors.ORANGE}{'='*60}{Colors.END}")
print(f"{Colors.ORANGE}APZmedia PSD Tools Extension - Starting Load Process{Colors.END}")
print(f"{Colors.ORANGE}{'='*60}{Colors.END}")

# Import automatic dependency installer
try:
    from auto_installer import auto_install_dependencies, ensure_dependencies
    AUTO_INSTALLER_AVAILABLE = True
    print(f"{Colors.GREEN}✅ Auto-installer imported successfully{Colors.END}")
except ImportError as e:
    AUTO_INSTALLER_AVAILABLE = False
    print(f"{Colors.YELLOW}⚠️ Auto-installer not available: {e}{Colors.END}")
    print(f"{Colors.CYAN}   This is normal if auto_installer.py is missing{Colors.END}")
except Exception as e:
    AUTO_INSTALLER_AVAILABLE = False
    print(f"{Colors.RED}❌ Error importing auto-installer: {e}{Colors.END}")

# Check for required dependencies
PYTOSHOP_AVAILABLE = False
try:
    import pytoshop
    PYTOSHOP_AVAILABLE = True
    print(f"{Colors.GREEN}✅ pytoshop is available{Colors.END}")
except ImportError:
    PYTOSHOP_AVAILABLE = False
    print(f"{Colors.YELLOW}⚠️ pytoshop not available{Colors.END}")
except Exception as e:
    PYTOSHOP_AVAILABLE = False
    print(f"{Colors.RED}❌ Error checking pytoshop: {e}{Colors.END}")

# Auto-install dependencies if needed
if not PYTOSHOP_AVAILABLE and AUTO_INSTALLER_AVAILABLE:
    print(f"\n{Colors.ORANGE}--- Automatic Dependency Installation ---{Colors.END}")
    print("Checking and installing dependencies automatically...")
    try:
        success = auto_install_dependencies(silent=False)
        if success:
            # Try importing pytoshop again
            try:
                import pytoshop
                PYTOSHOP_AVAILABLE = True
                print(f"{Colors.GREEN}✅ pytoshop is now available after installation{Colors.END}")
            except ImportError:
                print(f"{Colors.YELLOW}⚠️ pytoshop still not available after installation{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠️ Some dependencies failed to install{Colors.END}")
            print(f"{Colors.CYAN}   Manual installation: pip install -r requirements.txt{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error during auto-installation: {e}{Colors.END}")
        print(f"{Colors.CYAN}   Manual installation: pip install -r requirements.txt{Colors.END}")
elif not PYTOSHOP_AVAILABLE:
    print(f"{Colors.YELLOW}⚠️ pytoshop not available - PSD nodes will not be registered{Colors.END}")
    print(f"{Colors.CYAN}   To install: pip install -r requirements.txt{Colors.END}")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize node mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Extension paths
extension_root = os.path.dirname(os.path.abspath(__file__))
nodes_path = os.path.join(extension_root, "nodes")
utils_path = os.path.join(extension_root, "utils")

print(f"Extension directory: {extension_root}")
print(f"Nodes directory: {nodes_path}")
print(f"Utils directory: {utils_path}")

# Check if directories exist
if os.path.exists(nodes_path):
    print(f"{Colors.GREEN}✅ Nodes directory exists{Colors.END}")
else:
    print(f"{Colors.RED}❌ Nodes directory not found{Colors.END}")

if os.path.exists(utils_path):
    print(f"{Colors.GREEN}✅ Utils directory exists{Colors.END}")
else:
    print(f"{Colors.RED}❌ Utils directory not found{Colors.END}")

# Add paths to sys.path for imports
if nodes_path not in sys.path:
    sys.path.insert(0, nodes_path)
    print(f"Added nodes to sys.path: {nodes_path}")

if utils_path not in sys.path:
    sys.path.insert(0, utils_path)
    print(f"Added utils to sys.path: {utils_path}")

if extension_root not in sys.path:
    sys.path.insert(0, extension_root)
    print(f"Added extension to sys.path: {extension_root}")

# Only proceed with node registration if pytoshop is available
if PYTOSHOP_AVAILABLE:
    print(f"\n{Colors.ORANGE}--- Importing PSD Nodes ---{Colors.END}")
    
    # Import PSD nodes
    try:
        print("Attempting to import apzPSDLayerSaver...")
        import nodes.apzPSDLayerSaver as psd_saver_module
        APZmediaPSDLayerSaver = psd_saver_module.APZmediaPSDLayerSaver
        APZmediaPSDLayerSaverAdvanced = psd_saver_module.APZmediaPSDLayerSaverAdvanced
        print(f"{Colors.GREEN}✅ Successfully imported APZmediaPSDLayerSaver (method 1){Colors.END}")
        logger.info("Successfully imported APZmediaPSDLayerSaver node.")
    except Exception as e:
        print(f"{Colors.RED}❌ Failed to import APZmediaPSDLayerSaver node: {e}{Colors.END}")
        APZmediaPSDLayerSaver = None
        APZmediaPSDLayerSaverAdvanced = None

    try:
        print("Attempting to import apzPSDLayerSaver8Layers...")
        import nodes.apzPSDLayerSaver8Layers as psd_8layer_module
        APZmediaPSDLayerSaver8Layers = psd_8layer_module.APZmediaPSDLayerSaver8Layers
        APZmediaPSDLayerSaver8LayersAdvanced = psd_8layer_module.APZmediaPSDLayerSaver8LayersAdvanced
        print(f"{Colors.GREEN}✅ Successfully imported APZmediaPSDLayerSaver8Layers (method 1){Colors.END}")
        logger.info("Successfully imported APZmediaPSDLayerSaver8Layers node.")
    except Exception as e:
        print(f"{Colors.RED}❌ Failed to import APZmediaPSDLayerSaver8Layers node: {e}{Colors.END}")
        APZmediaPSDLayerSaver8Layers = None
        APZmediaPSDLayerSaver8LayersAdvanced = None

    # Register nodes if successfully imported
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

else:
    print(f"\n{Colors.YELLOW}--- Skipping Node Registration (pytoshop not available) ---{Colors.END}")
    print(f"{Colors.CYAN}   Install dependencies and restart ComfyUI to enable PSD nodes{Colors.END}")

# Final summary
print(f"\n{Colors.ORANGE}{'='*60}{Colors.END}")
print(f"{Colors.ORANGE}APZmedia PSD Tools Extension - Load Complete{Colors.END}")
print(f"{Colors.ORANGE}{'='*60}{Colors.END}")

if NODE_CLASS_MAPPINGS:
    print(f"{Colors.GREEN}🎉 SUCCESS: {len(NODE_CLASS_MAPPINGS)}/{len(NODE_CLASS_MAPPINGS)} nodes loaded successfully!{Colors.END}")
    print(f"Registered nodes: {list(NODE_CLASS_MAPPINGS.keys())}")
    print(f"Node display names: {list(NODE_DISPLAY_NAME_MAPPINGS.values())}")
    print(f"{Colors.GREEN}✅ Look for PSD nodes in ComfyUI under: image/psd{Colors.END}")
    print(f"{Colors.GREEN}✅ Or search for: 'APZmedia' or 'PSD'{Colors.END}")
else:
    print(f"{Colors.YELLOW}⚠️ No nodes were loaded{Colors.END}")
    print(f"{Colors.CYAN}   Install dependencies: pip install pytoshop psd-tools{Colors.END}")

print(f"{Colors.ORANGE}{'='*60}{Colors.END}")

logger.info("ComfyUI PSD Tools extension has been loaded successfully.")
if NODE_CLASS_MAPPINGS:
    logger.info(f"Registered {len(NODE_CLASS_MAPPINGS)} nodes: {list(NODE_CLASS_MAPPINGS.keys())}")
    logger.info(f"Node display names: {list(NODE_DISPLAY_NAME_MAPPINGS.values())}")
else:
    logger.info("No nodes registered - dependencies not available")