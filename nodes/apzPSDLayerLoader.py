"""
APZmedia PSD Layer Loader Node for ComfyUI

This node loads PSD files and extracts specific layers with their masks.
"""

import torch
import os
from typing import List, Optional, Tuple
# ComfyUI-compatible import pattern
import sys
import os

# Add extension root to Python path (ComfyUI standard pattern)
extension_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if extension_root not in sys.path:
    sys.path.insert(0, extension_root)

# Now import utilities using absolute paths from extension root
try:
    from utils.apz_psd_loader_utility import (
        load_psd_file,
        get_psd_info,
        extract_layer_and_mask,
        pil_to_tensor,
        pil_mask_to_tensor,
        list_psd_layers,
        check_psd_tools_available
    )
except ImportError as e:
    print(f"Warning: Could not import PSD loader utilities: {e}")
    # Create dummy functions to prevent errors
    def load_psd_file(*args, **kwargs):
        raise ImportError("PSD loader utilities not available")
    def get_psd_info(*args, **kwargs):
        raise ImportError("PSD loader utilities not available")
    def extract_layer_and_mask(*args, **kwargs):
        raise ImportError("PSD loader utilities not available")
    def pil_to_tensor(*args, **kwargs):
        raise ImportError("PSD loader utilities not available")
    def pil_mask_to_tensor(*args, **kwargs):
        raise ImportError("PSD loader utilities not available")
    def list_psd_layers(*args, **kwargs):
        raise ImportError("PSD loader utilities not available")
    def check_psd_tools_available(*args, **kwargs):
        raise ImportError("PSD loader utilities not available")


class APZmediaPSDLayerLoader:
    """
    ComfyUI node for loading PSD files and extracting layers with masks.
    """
    
    def __init__(self, device="cpu"):
        print("APZmediaPSDLayerLoader initialized")
        self.device = device
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "psd_file": ("STRING", {
                    "default": "./input.psd"
                }),
                "layer_index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 999,
                    "step": 1
                }),
            },
            "optional": {
                "load_mask": (["true", "false"], {"default": "true"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "INT")
    RETURN_NAMES = ("image", "mask", "layer_name", "layer_count")
    FUNCTION = "load_psd_layer"
    CATEGORY = "image/psd"
    
    def load_psd_layer(self, 
                      psd_file: str,
                      layer_index: int,
                      load_mask: str = "true") -> Tuple[torch.Tensor, torch.Tensor, str, int]:
        """
        Loads a PSD file and extracts a specific layer with its mask.
        
        Args:
            psd_file: Path to the PSD file
            layer_index: Index of the layer to extract (0-based)
            load_mask: Whether to load the mask ("true" or "false")
            
        Returns:
            Tuple of (image_tensor, mask_tensor, layer_name, total_layer_count)
        """
        try:
            # Check if psd-tools is available
            check_psd_tools_available()
            
            # Load PSD file
            psd = load_psd_file(psd_file)
            
            # Get PSD info
            psd_info = get_psd_info(psd)
            total_layers = psd_info['layer_count']
            
            print(f"Loaded PSD: {psd_info['width']}x{psd_info['height']}, {total_layers} layers")
            
            # Check if layer index is valid
            if layer_index >= total_layers:
                raise ValueError(f"Layer index {layer_index} out of range. PSD has {total_layers} layers (0-{total_layers-1})")
            
            # Extract layer and mask
            pil_image, pil_mask = extract_layer_and_mask(psd, layer_index)
            
            if pil_image is None:
                raise ValueError(f"Could not extract layer {layer_index}")
            
            # Convert to tensors
            image_tensor = pil_to_tensor(pil_image)
            
            # Handle mask
            if load_mask == "true" and pil_mask is not None:
                mask_tensor = pil_mask_to_tensor(pil_mask)
            else:
                # Create a default mask (fully opaque)
                mask_tensor = torch.ones((1, pil_image.height, pil_image.width), dtype=torch.float32)
            
            # Get layer name
            layer_name = psd[layer_index].name if layer_index < len(psd) else f"Layer {layer_index}"
            
            print(f"Extracted layer '{layer_name}' with size {pil_image.size}")
            if pil_mask is not None:
                print(f"Extracted mask with size {pil_mask.size}")
            
            return image_tensor, mask_tensor, layer_name, total_layers
            
        except Exception as e:
            print(f"Error in load_psd_layer: {e}")
            import traceback
            traceback.print_exc()
            
            # Return default values on error
            default_image = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
            default_mask = torch.ones((1, 512, 512), dtype=torch.float32)
            return default_image, default_mask, "Error", 0


class APZmediaPSDInfoLoader:
    """
    ComfyUI node for loading PSD file information and listing layers.
    """
    
    def __init__(self, device="cpu"):
        print("APZmediaPSDInfoLoader initialized")
        self.device = device
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "psd_file": ("STRING", {
                    "default": "./input.psd"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT", "INT", "INT", "STRING")
    RETURN_NAMES = ("layer_list", "width", "height", "layer_count", "color_mode")
    FUNCTION = "load_psd_info"
    CATEGORY = "image/psd"
    
    def load_psd_info(self, psd_file: str) -> Tuple[str, int, int, int, str]:
        """
        Loads PSD file information and returns layer details.
        
        Args:
            psd_file: Path to the PSD file
            
        Returns:
            Tuple of (layer_list_string, width, height, layer_count, color_mode)
        """
        try:
            # Check if psd-tools is available
            check_psd_tools_available()
            
            # Load PSD file
            psd = load_psd_file(psd_file)
            
            # Get PSD info
            psd_info = get_psd_info(psd)
            
            # Get layer information
            layers_info = list_psd_layers(psd)
            
            # Create layer list string
            layer_list_lines = []
            for i, layer_info in enumerate(layers_info):
                if 'error' in layer_info:
                    layer_list_lines.append(f"{i}: ERROR - {layer_info['error']}")
                else:
                    mask_info = " (with mask)" if layer_info['has_mask'] else ""
                    bbox_info = ""
                    if layer_info['bbox']:
                        bbox = layer_info['bbox']
                        bbox_info = f" [{bbox['width']}x{bbox['height']}]"
                    layer_list_lines.append(f"{i}: {layer_info['name']}{mask_info}{bbox_info}")
            
            layer_list_string = "\n".join(layer_list_lines)
            
            print(f"PSD Info: {psd_info['width']}x{psd_info['height']}, {psd_info['layer_count']} layers, {psd_info['color_mode']}")
            
            return (
                layer_list_string,
                psd_info['width'],
                psd_info['height'],
                psd_info['layer_count'],
                psd_info['color_mode']
            )
            
        except Exception as e:
            print(f"Error in load_psd_info: {e}")
            import traceback
            traceback.print_exc()
            
            # Return default values on error
            return "Error loading PSD file", 0, 0, 0, "unknown"


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "APZmediaPSDLayerLoader": APZmediaPSDLayerLoader,
    "APZmediaPSDInfoLoader": APZmediaPSDInfoLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APZmediaPSDLayerLoader": "APZmedia PSD Layer Loader",
    "APZmediaPSDInfoLoader": "APZmedia PSD Info Loader"
}
