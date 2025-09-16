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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the path to the current directory and subdirectories
comfyui_texttools_path = os.path.dirname(os.path.realpath(__file__))
nodes_path = os.path.join(comfyui_texttools_path, "nodes")

# Ensure the nodes path is added to sys.path for importing custom nodes
sys.path.append(nodes_path)

# Importing custom nodes
APZmediaPSDLayerSaver = None
APZmediaPSDLayerSaverAdvanced = None
APZmediaPSDLayerSaver8Layers = None
APZmediaPSDLayerSaver8LayersAdvanced = None

try:
    from nodes.apzPSDLayerSaver import APZmediaPSDLayerSaver
    logger.info("Successfully imported APZmediaPSDLayerSaver node.")
except Exception as e:
    logger.error("Failed to import APZmediaPSDLayerSaver node.", exc_info=True)

try:
    from nodes.apzPSDLayerSaver import APZmediaPSDLayerSaverAdvanced
    logger.info("Successfully imported APZmediaPSDLayerSaverAdvanced node.")
except Exception as e:
    logger.error("Failed to import APZmediaPSDLayerSaverAdvanced node.", exc_info=True)

try:
    from nodes.apzPSDLayerSaver8Layers import APZmediaPSDLayerSaver8Layers
    logger.info("Successfully imported APZmediaPSDLayerSaver8Layers node.")
except Exception as e:
    logger.error("Failed to import APZmediaPSDLayerSaver8Layers node.", exc_info=True)

try:
    from nodes.apzPSDLayerSaver8Layers import APZmediaPSDLayerSaver8LayersAdvanced
    logger.info("Successfully imported APZmediaPSDLayerSaver8LayersAdvanced node.")
except Exception as e:
    logger.error("Failed to import APZmediaPSDLayerSaver8LayersAdvanced node.", exc_info=True)

# Utilities should be imported as needed, but not registered as nodes
try:
    from utils import apz_psd_conversion
    from utils import apz_psd_mask_utility
    from utils import apz_image_conversion
    logger.info("Successfully imported PSD utility modules.")
except Exception as e:
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

logger.info("ComfyUI PSD Tools extension has been loaded successfully.")
logger.info(f"Registered {len(NODE_CLASS_MAPPINGS)} nodes: {list(NODE_CLASS_MAPPINGS.keys())}")
logger.info(f"Node display names: {list(NODE_DISPLAY_NAME_MAPPINGS.keys())}")
