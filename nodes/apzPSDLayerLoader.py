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
    print("✅ Successfully imported PSD loader utility functions")
except ImportError as e:
    print(f"Warning: Could not import PSD loader utilities: {e}")
    # Try alternative import method
    try:
        import importlib.util
        utils_path = os.path.join(extension_root, "utils")
        spec = importlib.util.spec_from_file_location("apz_psd_loader_utility", os.path.join(utils_path, "apz_psd_loader_utility.py"))
        apz_psd_loader_utility = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(apz_psd_loader_utility)
        load_psd_file = apz_psd_loader_utility.load_psd_file
        get_psd_info = apz_psd_loader_utility.get_psd_info
        extract_layer_and_mask = apz_psd_loader_utility.extract_layer_and_mask
        pil_to_tensor = apz_psd_loader_utility.pil_to_tensor
        pil_mask_to_tensor = apz_psd_loader_utility.pil_mask_to_tensor
        list_psd_layers = apz_psd_loader_utility.list_psd_layers
        check_psd_tools_available = apz_psd_loader_utility.check_psd_tools_available
        print("✅ Successfully imported PSD loader utility functions (fallback method)")
    except Exception as e2:
        print(f"Warning: Fallback import also failed: {e2}")
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
                    "default": "./example/Example.psd"
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
            print(f"🔍 Starting PSD layer loading...")
            print(f"📁 PSD file: {psd_file}")
            print(f"📋 Layer index: {layer_index}")
            print(f"🎭 Load mask: {load_mask}")
            
            # Check if psd-tools is available
            check_psd_tools_available()
            print("✅ PSD tools available")
            
            # Load PSD file
            print("📖 Loading PSD file...")
            psd = load_psd_file(psd_file)
            print("✅ PSD file loaded successfully")
            
            # Get PSD info
            psd_info = get_psd_info(psd)
            total_layers = psd_info['layer_count']
            
            print(f"📊 PSD Info: {psd_info['width']}x{psd_info['height']}, {total_layers} layers")
            print(f"📝 Layer names: {psd_info['layer_names']}")
            
            # Check if layer index is valid
            if layer_index >= total_layers:
                error_msg = f"Layer index {layer_index} out of range. PSD has {total_layers} layers (0-{total_layers-1})"
                print(f"❌ {error_msg}")
                raise ValueError(error_msg)
            
            print(f"🎯 Extracting layer {layer_index}...")
            # Extract layer and mask
            pil_image, pil_mask = extract_layer_and_mask(psd, layer_index)
            
            if pil_image is None:
                error_msg = f"Could not extract layer {layer_index}"
                print(f"❌ {error_msg}")
                raise ValueError(error_msg)
            
            print(f"✅ Layer {layer_index} extracted successfully")
            print(f"🖼️ Image size: {pil_image.size}")
            
            # Convert to tensors
            print("🔄 Converting image to tensor...")
            image_tensor = pil_to_tensor(pil_image)
            print(f"✅ Image tensor created: {image_tensor.shape}")
            
            # Handle mask
            if load_mask == "true" and pil_mask is not None:
                print("🔄 Converting mask to tensor...")
                mask_tensor = pil_mask_to_tensor(pil_mask)
                print(f"✅ Mask tensor created: {mask_tensor.shape}")
            else:
                print("🎭 Creating default mask (fully opaque)")
                # Create a default mask (fully opaque)
                mask_tensor = torch.ones((1, pil_image.height, pil_image.width), dtype=torch.float32)
                print(f"✅ Default mask created: {mask_tensor.shape}")
            
            # Get layer name
            layer_name = psd_info['layer_names'][layer_index] if layer_index < len(psd_info['layer_names']) else f"Layer {layer_index}"
            print(f"📝 Layer name: {layer_name}")
            
            print(f"🎉 PSD layer loading completed successfully!")
            print(f"📊 Final result: Image {image_tensor.shape}, Mask {mask_tensor.shape}, Layer '{layer_name}', Total layers: {total_layers}")
            
            return image_tensor, mask_tensor, layer_name, total_layers
            
        except Exception as e:
            print(f"Error in load_psd_layer: {e}")
            import traceback
            traceback.print_exc()
            
            # Return default values on error
            default_image = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
            default_mask = torch.ones((1, 512, 512), dtype=torch.float32)
            
            return default_image, default_mask, "Error", 0


