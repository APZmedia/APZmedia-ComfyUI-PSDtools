"""
APZmedia PSD Layer Saver Node for ComfyUI (Refactored with psd-tools and PIL)

This node saves up to 10 images as layers in a PSD file, with optional masks for each layer.
Uses PIL and psd-tools instead of pytoshop for better compatibility and performance.
"""

import torch
import os
import logging
from typing import List, Optional, Tuple
# ComfyUI-compatible import pattern
import sys
import os

# Set up logging
logger = logging.getLogger(__name__)

# Add extension root to Python path (ComfyUI standard pattern)
extension_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if extension_root not in sys.path:
    sys.path.insert(0, extension_root)

# Now import utilities using absolute paths from extension root
try:
    from utils.apz_psd_tools_utility import (
        process_layers_to_psd,
        check_psd_tools_available
    )
    print("✅ Successfully imported PSD tools utility functions")
except ImportError as e:
    print(f"Warning: Could not import PSD utilities: {e}")
    # Try alternative import method
    try:
        import importlib.util
        utils_path = os.path.join(extension_root, "utils")
        spec = importlib.util.spec_from_file_location("apz_psd_tools_utility", os.path.join(utils_path, "apz_psd_tools_utility.py"))
        apz_psd_tools_utility = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(apz_psd_tools_utility)
        process_layers_to_psd = apz_psd_tools_utility.process_layers_to_psd
        check_psd_tools_available = apz_psd_tools_utility.check_psd_tools_available
        print("✅ Successfully imported PSD tools utility functions (fallback method)")
    except Exception as e2:
        print(f"Warning: Fallback import also failed: {e2}")
        # Create dummy functions to prevent errors
        def process_layers_to_psd(*args, **kwargs):
            raise ImportError("PSD utilities not available")
        def check_psd_tools_available(*args, **kwargs):
            raise ImportError("PSD utilities not available")


class APZmediaPSDLayerSaverMultilayer:
    """
    ComfyUI node for saving multiple images as PSD layers with masks.
    Uses PIL and psd-tools for better compatibility and performance.
    """
    
    def __init__(self, device="cpu"):
        print("APZmediaPSDLayerSaverMultilayer initialized")
        self.device = device
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "output_dir": ("STRING", {
                    "default": "./output"
                }),
                "filename_prefix": ("STRING", {
                    "default": "output"
                }),
                # Layer 1
                "layer1": ("IMAGE",),
                "mask1": ("MASK",),
                "layer_name1": ("STRING", {"default": "Layer 1"}),
                
                # Layer 2
                "layer2": ("IMAGE",),
                "mask2": ("MASK",),
                "layer_name2": ("STRING", {"default": "Layer 2"}),
                
                # Layer 3
                "layer3": ("IMAGE",),
                "mask3": ("MASK",),
                "layer_name3": ("STRING", {"default": "Layer 3"}),
                
                # Layer 4
                "layer4": ("IMAGE",),
                "mask4": ("MASK",),
                "layer_name4": ("STRING", {"default": "Layer 4"}),
                
                # Layer 5
                "layer5": ("IMAGE",),
                "mask5": ("MASK",),
                "layer_name5": ("STRING", {"default": "Layer 5"}),
                
                # Layer 6
                "layer6": ("IMAGE",),
                "mask6": ("MASK",),
                "layer_name6": ("STRING", {"default": "Layer 6"}),
                
                # Layer 7
                "layer7": ("IMAGE",),
                "mask7": ("MASK",),
                "layer_name7": ("STRING", {"default": "Layer 7"}),
                
                # Layer 8
                "layer8": ("IMAGE",),
                "mask8": ("MASK",),
                "layer_name8": ("STRING", {"default": "Layer 8"}),
                
                # Layer 9
                "layer9": ("IMAGE",),
                "mask9": ("MASK",),
                "layer_name9": ("STRING", {"default": "Layer 9"}),
                
                # Layer 10
                "layer10": ("IMAGE",),
                "mask10": ("MASK",),
                "layer_name10": ("STRING", {"default": "Layer 10"}),
            }
        }
    
    RETURN_TYPES = ()  # OUTPUT_NODE - no return values
    RETURN_NAMES = ()
    FUNCTION = "save_psd_layers"
    CATEGORY = "image/psd"
    OUTPUT_NODE = True  # This is an output node that writes to disk
    
    def save_psd_layers(self, 
                       output_dir=None,
                       filename_prefix=None,
                       # Layer inputs
                       layer1=None, mask1=None, layer_name1=None,
                       layer2=None, mask2=None, layer_name2=None,
                       layer3=None, mask3=None, layer_name3=None,
                       layer4=None, mask4=None, layer_name4=None,
                       layer5=None, mask5=None, layer_name5=None,
                       layer6=None, mask6=None, layer_name6=None,
                       layer7=None, mask7=None, layer_name7=None,
                       layer8=None, mask8=None, layer_name8=None,
                       layer9=None, mask9=None, layer_name9=None,
                       layer10=None, mask10=None, layer_name10=None):
        """
        Saves up to 10 images as layers in a PSD file with optional masks.
        
        Args:
            output_dir: Directory to save the PSD file (default: "./output")
            filename_prefix: Prefix for the filename (default: "output")
            layer1-10: Individual image tensors
            mask1-10: Optional individual masks
            layer_name1-10: Individual layer names
            
        Returns:
            None (OUTPUT_NODE)
        """
        try:
            # Check if psd-tools is available
            check_psd_tools_available()
            
            # Set defaults for optional parameters
            if output_dir is None:
                output_dir = "./output"
            if filename_prefix is None:
                filename_prefix = "output"
            
            # Organize inputs into lists
            layers = [layer1, layer2, layer3, layer4, layer5, layer6, layer7, layer8, layer9, layer10]
            masks = [mask1, mask2, mask3, mask4, mask5, mask6, mask7, mask8, mask9, mask10]
            layer_names = [layer_name1, layer_name2, layer_name3, layer_name4, layer_name5,
                          layer_name6, layer_name7, layer_name8, layer_name9, layer_name10]
            
            # Set default layer names for None values
            for i in range(len(layer_names)):
                if layer_names[i] is None:
                    layer_names[i] = f"Layer {i+1}"
            
            # Filter out None layers and create corresponding lists
            valid_layers = []
            valid_masks = []
            valid_names = []
            
            for i, (layer, mask, name) in enumerate(zip(layers, masks, layer_names)):
                if layer is not None:
                    valid_layers.append(layer)
                    valid_masks.append(mask)
                    valid_names.append(name)
            
            if not valid_layers:
                error_msg = "No layers or masks are being saved"
                print(f"❌ {error_msg}")
                logger.error(error_msg)
                return
            
            print(f"Processing {len(valid_layers)} layers for PSD creation")
            
            # Process layers to PSD
            output_path, success = process_layers_to_psd(
                image_tensors=valid_layers,
                layer_names=valid_names,
                mask_tensors=valid_masks,
                output_dir=output_dir,
                filename_prefix=filename_prefix
            )
            
            if success:
                print(f"Successfully saved PSD file with {len(valid_layers)} layers to: {output_path}")
            else:
                print(f"Failed to save PSD file to: {output_path}")
                
        except Exception as e:
            print(f"Error in save_psd_layers: {e}")
            import traceback
            traceback.print_exc()


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "APZmediaPSDLayerSaverMultilayer": APZmediaPSDLayerSaverMultilayer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APZmediaPSDLayerSaverMultilayer": "APZmedia PSD Multilayer Saver"
}
