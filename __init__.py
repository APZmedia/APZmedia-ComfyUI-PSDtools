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
utils_path = os.path.join(comfyui_texttools_path, "utils")

print(f"{Colors.CYAN}Extension directory: {Colors.WHITE}{comfyui_texttools_path}{Colors.END}")
print(f"{Colors.CYAN}Nodes directory: {Colors.WHITE}{nodes_path}{Colors.END}")
print(f"{Colors.CYAN}Utils directory: {Colors.WHITE}{utils_path}{Colors.END}")

# Check if directories exist
if os.path.exists(nodes_path):
    print(f"{Colors.GREEN}✅ Nodes directory exists{Colors.END}")
else:
    print(f"{Colors.RED}❌ Nodes directory does not exist{Colors.END}")

if os.path.exists(utils_path):
    print(f"{Colors.GREEN}✅ Utils directory exists{Colors.END}")
else:
    print(f"{Colors.RED}❌ Utils directory does not exist{Colors.END}")

# Ensure the paths are added to sys.path for importing custom nodes
if nodes_path not in sys.path:
    sys.path.append(nodes_path)
    print(f"{Colors.CYAN}Added nodes to sys.path: {Colors.WHITE}{nodes_path}{Colors.END}")

if utils_path not in sys.path:
    sys.path.append(utils_path)
    print(f"{Colors.CYAN}Added utils to sys.path: {Colors.WHITE}{utils_path}{Colors.END}")

# Also add the main extension directory to sys.path
if comfyui_texttools_path not in sys.path:
    sys.path.append(comfyui_texttools_path)
    print(f"{Colors.CYAN}Added extension to sys.path: {Colors.WHITE}{comfyui_texttools_path}{Colors.END}")

# Automatic dependency installation
print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Automatic Dependency Installation ---{Colors.END}")
if AUTO_INSTALLER_AVAILABLE:
    try:
        print(f"{Colors.CYAN}Checking and installing dependencies automatically...{Colors.END}")
        dependencies_ready = auto_install_dependencies(silent=False)
        if dependencies_ready:
            print(f"{Colors.GREEN}✅ All dependencies are ready!{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠️ Some dependencies may not be available{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error during automatic installation: {e}{Colors.END}")
        logger.error("Error during automatic dependency installation", exc_info=True)
else:
    print(f"{Colors.YELLOW}⚠️ Auto-installer not available, checking dependencies manually...{Colors.END}")

# Check if pytoshop is available (fallback check)
try:
    import pytoshop
    print(f"{Colors.GREEN}✅ pytoshop is available{Colors.END}")
except ImportError as e:
    print(f"{Colors.RED}❌ pytoshop not available: {e}{Colors.END}")
    print(f"{Colors.RED}   This will cause node import failures!{Colors.END}")
    if AUTO_INSTALLER_AVAILABLE:
        print(f"{Colors.YELLOW}   Attempting to install pytoshop...{Colors.END}")
        try:
            from auto_installer import get_installer
            installer = get_installer()
            success = installer.install_package("pytoshop", "pytoshop>=0.1.0", "-I --no-cache-dir")
            if success:
                print(f"{Colors.GREEN}✅ pytoshop installed successfully!{Colors.END}")
            else:
                print(f"{Colors.RED}❌ Failed to install pytoshop{Colors.END}")
        except Exception as install_error:
            print(f"{Colors.RED}❌ Error installing pytoshop: {install_error}{Colors.END}")

# Function to ensure dependencies before node import
def ensure_dependencies_for_nodes():
    """Ensure all dependencies are available before importing nodes"""
    if AUTO_INSTALLER_AVAILABLE:
        try:
            return ensure_dependencies()
        except Exception as e:
            print(f"{Colors.RED}❌ Error ensuring dependencies: {e}{Colors.END}")
            return False
    else:
        # Fallback: check pytoshop manually
        try:
            import pytoshop
            return True
        except ImportError:
            return False

# Function to import node modules with multiple fallback methods
def import_node_module(module_name, class_name, nodes_path):
    """Import a node module using multiple fallback methods"""
    print(f"{Colors.CYAN}Attempting to import {module_name}...{Colors.END}")
    
    # Method 1: Try importing as module from nodes package
    try:
        import importlib
        module = importlib.import_module(f"nodes.{module_name}")
        node_class = getattr(module, class_name)
        print(f"{Colors.GREEN}✅ Successfully imported {class_name} (method 1){Colors.END}")
        return node_class
    except (ImportError, AttributeError) as e1:
        print(f"{Colors.YELLOW}Method 1 failed: {e1}{Colors.END}")
    
    # Method 2: Try importing directly from file
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(nodes_path, f"{module_name}.py"))
        if spec is None:
            raise ImportError(f"Could not load spec for {module_name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        node_class = getattr(module, class_name)
        print(f"{Colors.GREEN}✅ Successfully imported {class_name} (method 2){Colors.END}")
        return node_class
    except (ImportError, AttributeError, FileNotFoundError) as e2:
        print(f"{Colors.YELLOW}Method 2 failed: {e2}{Colors.END}")
    
    # Method 3: Try importing with exec
    try:
        import importlib.util
        file_path = os.path.join(nodes_path, f"{module_name}.py")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Create a new module
        module = importlib.util.module_from_spec(importlib.util.spec_from_loader(module_name, loader=None))
        exec(code, module.__dict__)
        
        node_class = getattr(module, class_name)
        print(f"{Colors.GREEN}✅ Successfully imported {class_name} (method 3){Colors.END}")
        return node_class
    except Exception as e3:
        print(f"{Colors.RED}All import methods failed for {class_name}: {e3}{Colors.END}")
        raise e3

# Importing custom nodes
APZmediaPSDLayerSaver = None
APZmediaPSDLayerSaverAdvanced = None
APZmediaPSDLayerSaver8Layers = None
APZmediaPSDLayerSaver8LayersAdvanced = None

print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Importing APZmediaPSDLayerSaver ---{Colors.END}")
try:
    # Ensure dependencies are available before importing
    if ensure_dependencies_for_nodes():
        APZmediaPSDLayerSaver = import_node_module("apzPSDLayerSaver", "APZmediaPSDLayerSaver", nodes_path)
        logger.info("Successfully imported APZmediaPSDLayerSaver node.")
    else:
        print(f"{Colors.RED}❌ Dependencies not available for APZmediaPSDLayerSaver node{Colors.END}")
        logger.error("Dependencies not available for APZmediaPSDLayerSaver node.")
except Exception as e:
    print(f"{Colors.RED}❌ Failed to import APZmediaPSDLayerSaver node: {e}{Colors.END}")
    logger.error("Failed to import APZmediaPSDLayerSaver node.", exc_info=True)

print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Importing APZmediaPSDLayerSaverAdvanced ---{Colors.END}")
try:
    # Ensure dependencies are available before importing
    if ensure_dependencies_for_nodes():
        APZmediaPSDLayerSaverAdvanced = import_node_module("apzPSDLayerSaver", "APZmediaPSDLayerSaverAdvanced", nodes_path)
        logger.info("Successfully imported APZmediaPSDLayerSaverAdvanced node.")
    else:
        print(f"{Colors.RED}❌ Dependencies not available for APZmediaPSDLayerSaverAdvanced node{Colors.END}")
        logger.error("Dependencies not available for APZmediaPSDLayerSaverAdvanced node.")
except Exception as e:
    print(f"{Colors.RED}❌ Failed to import APZmediaPSDLayerSaverAdvanced node: {e}{Colors.END}")
    logger.error("Failed to import APZmediaPSDLayerSaverAdvanced node.", exc_info=True)

print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Importing APZmediaPSDLayerSaver8Layers ---{Colors.END}")
try:
    # Ensure dependencies are available before importing
    if ensure_dependencies_for_nodes():
        APZmediaPSDLayerSaver8Layers = import_node_module("apzPSDLayerSaver8Layers", "APZmediaPSDLayerSaver8Layers", nodes_path)
        logger.info("Successfully imported APZmediaPSDLayerSaver8Layers node.")
    else:
        print(f"{Colors.RED}❌ Dependencies not available for APZmediaPSDLayerSaver8Layers node{Colors.END}")
        logger.error("Dependencies not available for APZmediaPSDLayerSaver8Layers node.")
except Exception as e:
    print(f"{Colors.RED}❌ Failed to import APZmediaPSDLayerSaver8Layers node: {e}{Colors.END}")
    logger.error("Failed to import APZmediaPSDLayerSaver8Layers node.", exc_info=True)

print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Importing APZmediaPSDLayerSaver8LayersAdvanced ---{Colors.END}")
try:
    # Ensure dependencies are available before importing
    if ensure_dependencies_for_nodes():
        APZmediaPSDLayerSaver8LayersAdvanced = import_node_module("apzPSDLayerSaver8Layers", "APZmediaPSDLayerSaver8LayersAdvanced", nodes_path)
        logger.info("Successfully imported APZmediaPSDLayerSaver8LayersAdvanced node.")
    else:
        print(f"{Colors.RED}❌ Dependencies not available for APZmediaPSDLayerSaver8LayersAdvanced node{Colors.END}")
        logger.error("Dependencies not available for APZmediaPSDLayerSaver8LayersAdvanced node.")
except Exception as e:
    print(f"{Colors.RED}❌ Failed to import APZmediaPSDLayerSaver8LayersAdvanced node: {e}{Colors.END}")
    logger.error("Failed to import APZmediaPSDLayerSaver8LayersAdvanced node.", exc_info=True)

# Utilities should be imported as needed, but not registered as nodes
print(f"\n{Colors.ORANGE}{Colors.BOLD}--- Importing PSD Utilities ---{Colors.END}")
try:
    # Try importing utilities with fallback methods
    print(f"{Colors.CYAN}Attempting to import PSD utility modules...{Colors.END}")
    
    # Method 1: Try importing as modules
    try:
        import utils.apz_psd_conversion as apz_psd_conversion
        import utils.apz_psd_mask_utility as apz_psd_mask_utility
        import utils.apz_image_conversion as apz_image_conversion
        print(f"{Colors.GREEN}✅ Successfully imported PSD utility modules (method 1){Colors.END}")
    except ImportError as e1:
        print(f"{Colors.YELLOW}Method 1 failed: {e1}{Colors.END}")
        
        # Method 2: Try importing directly from files
        try:
            import importlib.util
            
            # Import apz_psd_conversion
            spec1 = importlib.util.spec_from_file_location("apz_psd_conversion", os.path.join(utils_path, "apz_psd_conversion.py"))
            apz_psd_conversion = importlib.util.module_from_spec(spec1)
            spec1.loader.exec_module(apz_psd_conversion)
            
            # Import apz_psd_mask_utility
            spec2 = importlib.util.spec_from_file_location("apz_psd_mask_utility", os.path.join(utils_path, "apz_psd_mask_utility.py"))
            apz_psd_mask_utility = importlib.util.module_from_spec(spec2)
            spec2.loader.exec_module(apz_psd_mask_utility)
            
            # Import apz_image_conversion
            spec3 = importlib.util.spec_from_file_location("apz_image_conversion", os.path.join(utils_path, "apz_image_conversion.py"))
            apz_image_conversion = importlib.util.module_from_spec(spec3)
            spec3.loader.exec_module(apz_image_conversion)
            
            print(f"{Colors.GREEN}✅ Successfully imported PSD utility modules (method 2){Colors.END}")
        except Exception as e2:
            print(f"{Colors.YELLOW}Method 2 failed: {e2}{Colors.END}")
            print(f"{Colors.YELLOW}⚠️ PSD utility modules not available, but nodes may still work{Colors.END}")
    
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

# Show dependency installation status
if AUTO_INSTALLER_AVAILABLE:
    print(f"{Colors.GREEN}✅ Automatic dependency installation is enabled{Colors.END}")
    print(f"{Colors.CYAN}   Dependencies will be installed automatically when needed{Colors.END}")
else:
    print(f"{Colors.YELLOW}⚠️  Automatic dependency installation is not available{Colors.END}")
    print(f"{Colors.CYAN}   Manual installation may be required{Colors.END}")

if successful_nodes > 0:
    print(f"{Colors.GREEN}✅ Look for PSD nodes in ComfyUI under: image/psd{Colors.END}")
    print(f"{Colors.GREEN}✅ Or search for: 'APZmedia' or 'PSD'{Colors.END}")
    print(f"{Colors.GREEN}✅ Dependencies are automatically managed{Colors.END}")
else:
    print(f"{Colors.RED}❌ No nodes were loaded. Check the errors above.{Colors.END}")
    if AUTO_INSTALLER_AVAILABLE:
        print(f"{Colors.YELLOW}   Try restarting ComfyUI to trigger dependency installation{Colors.END}")

print(f"{Colors.ORANGE}{Colors.BOLD}{'=' * 60}{Colors.END}")

logger.info("ComfyUI PSD Tools extension has been loaded successfully.")
logger.info(f"Registered {len(NODE_CLASS_MAPPINGS)} nodes: {list(NODE_CLASS_MAPPINGS.keys())}")
logger.info(f"Node display names: {list(NODE_DISPLAY_NAME_MAPPINGS.keys())}")
