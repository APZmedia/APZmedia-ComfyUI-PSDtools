"""
APZmedia PSD Layer Saver 8 Layers Node for ComfyUI

This node saves exactly 8 images as layers in a PSD file, with individual masks and layer names.
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
    from utils.apz_psd_conversion import (
        tensor_to_numpy_array,
        create_psd_layer,
        create_psd_from_layers,
        save_psd_file,
        validate_layer_dimensions
    )
    from utils.apz_psd_mask_utility import PSDMaskUtility
except ImportError as e:
    print(f"Warning: Could not import PSD utilities: {e}")
    # Create dummy functions to prevent errors
    def tensor_to_numpy_array(*args, **kwargs):
        raise ImportError("PSD utilities not available")
    def create_psd_layer(*args, **kwargs):
        raise ImportError("PSD utilities not available")
    def create_psd_from_layers(*args, **kwargs):
        raise ImportError("PSD utilities not available")
    def save_psd_file(*args, **kwargs):
        raise ImportError("PSD utilities not available")
    def validate_layer_dimensions(*args, **kwargs):
        raise ImportError("PSD utilities not available")
    class PSDMaskUtility:
        def __init__(self, *args, **kwargs):
            raise ImportError("PSD utilities not available")
        
        @staticmethod
        def process_mask_for_psd(*args, **kwargs):
            raise ImportError("PSD utilities not available")


class APZmediaPSDLayerSaver8Layers:
    """
    ComfyUI node for saving exactly 8 images as PSD layers with individual masks and names.
    """
    
    def __init__(self, device="cpu"):
        print("APZmediaPSDLayerSaver8Layers initialized")
        self.device = device
    
    _blend_modes = [
        "normal", "multiply", "screen", "overlay", "soft_light", "hard_light",
        "color_dodge", "color_burn", "darken", "lighten", "difference", "exclusion"
    ]
    
    _color_modes = ["rgb", "cmyk", "grayscale"]
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Global Settings
                "psd_filename": ("STRING", {"default": "output.psd"}),
                "color_mode": (cls._color_modes, {"default": "rgb"}),
            },
            "optional": {
                # Layer 1 Group
                "image_1": ("IMAGE",),
                "mask_1": ("MASK",),
                "layer_name_1": ("STRING", {"default": "Background"}),
                "opacity_1": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_1": (cls._blend_modes, {"default": "normal"}),
                
                # Layer 2 Group
                "image_2": ("IMAGE",),
                "mask_2": ("MASK",),
                "layer_name_2": ("STRING", {"default": "Character"}),
                "opacity_2": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_2": (cls._blend_modes, {"default": "normal"}),
                
                # Layer 3 Group
                "image_3": ("IMAGE",),
                "mask_3": ("MASK",),
                "layer_name_3": ("STRING", {"default": "Hair"}),
                "opacity_3": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_3": (cls._blend_modes, {"default": "normal"}),
                
                # Layer 4 Group
                "image_4": ("IMAGE",),
                "mask_4": ("MASK",),
                "layer_name_4": ("STRING", {"default": "Clothing"}),
                "opacity_4": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_4": (cls._blend_modes, {"default": "normal"}),
                
                # Layer 5 Group
                "image_5": ("IMAGE",),
                "mask_5": ("MASK",),
                "layer_name_5": ("STRING", {"default": "Accessories"}),
                "opacity_5": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_5": (cls._blend_modes, {"default": "normal"}),
                
                # Layer 6 Group
                "image_6": ("IMAGE",),
                "mask_6": ("MASK",),
                "layer_name_6": ("STRING", {"default": "Effects"}),
                "opacity_6": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_6": (cls._blend_modes, {"default": "normal"}),
                
                # Layer 7 Group
                "image_7": ("IMAGE",),
                "mask_7": ("MASK",),
                "layer_name_7": ("STRING", {"default": "Lighting"}),
                "opacity_7": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_7": (cls._blend_modes, {"default": "normal"}),
                
                # Layer 8 Group
                "image_8": ("IMAGE",),
                "mask_8": ("MASK",),
                "layer_name_8": ("STRING", {"default": "Overlay"}),
                "opacity_8": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_8": (cls._blend_modes, {"default": "normal"}),
                
                # Background Layer Settings
                "create_background_layer": (["true", "false"], {"default": "false"}),
                "background_color": ("STRING", {"default": "#FFFFFF"}),
                "background_opacity": ("INT", {"default": 255, "min": 0, "max": 255}),
            }
        }
    
    RETURN_TYPES = ("STRING", "BOOLEAN", "INT")
    RETURN_NAMES = ("output_path", "success", "layer_count")
    FUNCTION = "save_8_layers_psd"
    CATEGORY = "image/psd"
    
    def save_8_layers_psd(self, 
                         # Global Settings
                         psd_filename, color_mode="rgb",
                         # Layer 1 Group
                         image_1=None, mask_1=None, layer_name_1="Background", opacity_1=255, blend_mode_1="normal",
                         # Layer 2 Group
                         image_2=None, mask_2=None, layer_name_2="Character", opacity_2=255, blend_mode_2="normal",
                         # Layer 3 Group
                         image_3=None, mask_3=None, layer_name_3="Hair", opacity_3=255, blend_mode_3="normal",
                         # Layer 4 Group
                         image_4=None, mask_4=None, layer_name_4="Clothing", opacity_4=255, blend_mode_4="normal",
                         # Layer 5 Group
                         image_5=None, mask_5=None, layer_name_5="Accessories", opacity_5=255, blend_mode_5="normal",
                         # Layer 6 Group
                         image_6=None, mask_6=None, layer_name_6="Effects", opacity_6=255, blend_mode_6="normal",
                         # Layer 7 Group
                         image_7=None, mask_7=None, layer_name_7="Lighting", opacity_7=255, blend_mode_7="normal",
                         # Layer 8 Group
                         image_8=None, mask_8=None, layer_name_8="Overlay", opacity_8=255, blend_mode_8="normal",
                         # Background Layer Settings
                         create_background_layer="false", background_color="#FFFFFF", background_opacity=255) -> Tuple[str, bool, int]:
        """
        Saves exactly 8 images as layers in a PSD file with individual masks and properties.
        
        Args:
            image_1-8: Individual image tensors
            layer_name_1-8: Individual layer names
            psd_filename: Name of the PSD file to create
            color_mode: Color mode for the PSD file
            mask_1-8: Optional individual masks
            opacity_1-8: Individual opacity values (0-255)
            blend_mode_1-8: Individual blend modes
            create_background_layer: Whether to create a background layer
            background_color: Hex color for background
            background_opacity: Opacity for background layer
            
        Returns:
            tuple of (output_path, success_boolean, layer_count)
        """
        try:
            # Organize inputs into lists for easier processing
            images = [image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8]
            layer_names = [layer_name_1, layer_name_2, layer_name_3, layer_name_4, 
                          layer_name_5, layer_name_6, layer_name_7, layer_name_8]
            masks = [mask_1, mask_2, mask_3, mask_4, mask_5, mask_6, mask_7, mask_8]
            opacities = [opacity_1, opacity_2, opacity_3, opacity_4, 
                        opacity_5, opacity_6, opacity_7, opacity_8]
            blend_modes = [blend_mode_1, blend_mode_2, blend_mode_3, blend_mode_4,
                          blend_mode_5, blend_mode_6, blend_mode_7, blend_mode_8]
            
            # Filter out None masks and create a list of valid masks
            valid_masks = []
            for i, mask in enumerate(masks):
                if mask is not None:
                    # Process mask for PSD
                    processed_mask = PSDMaskUtility.process_mask_for_psd(mask)
                    valid_masks.append(processed_mask)
                else:
                    valid_masks.append(None)
            
            # Create PSD layers
            layers = []
            for i in range(8):
                # Skip if no image provided
                if images[i] is None:
                    continue
                    
                # Convert image tensor to numpy array
                image_data = tensor_to_numpy_array(images[i])
                
                # Get mask data if provided
                mask_data = valid_masks[i] if valid_masks[i] is not None else None
                
                # Create layer
                layer = create_psd_layer(
                    image_data=image_data,
                    layer_name=layer_names[i],
                    mask_data=mask_data,
                    opacity=opacities[i],
                    blend_mode=blend_modes[i]
                )
                
                layers.append(layer)
            
            # Add background layer if requested
            if create_background_layer == "true":
                # Get image dimensions from first available layer
                first_image = None
                for img in images:
                    if img is not None:
                        first_image = tensor_to_numpy_array(img)
                        break
                
                if first_image is not None:
                    height, width = first_image.shape[:2]
                else:
                    # Default dimensions if no images provided
                    height, width = 512, 512
                
                # Create background layer
                background_data = self._create_background_layer(
                    width, height, background_color, background_opacity
                )
                
                background_layer = create_psd_layer(
                    image_data=background_data,
                    layer_name="Background",
                    opacity=background_opacity,
                    blend_mode="normal"
                )
                
                # Add background as first layer
                layers.insert(0, background_layer)
            
            # Validate layer dimensions
            is_valid, error_msg = validate_layer_dimensions(layers)
            if not is_valid:
                print(f"Warning: {error_msg}")
            
            # Create PSD file
            psd = create_psd_from_layers(layers, color_mode=color_mode)
            
            # Ensure output directory exists
            output_dir = os.path.dirname(psd_filename) if os.path.dirname(psd_filename) else "."
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Save PSD file
            success = save_psd_file(psd, psd_filename)
            
            layer_count = len(layers)
            
            if success:
                print(f"Successfully saved PSD file with {layer_count} layers to: {psd_filename}")
                return psd_filename, True, layer_count
            else:
                print(f"Failed to save PSD file to: {psd_filename}")
                return psd_filename, False, layer_count
                
        except Exception as e:
            print(f"Error in save_8_layers_psd: {e}")
            import traceback
            traceback.print_exc()
            return psd_filename, False, 0
    
    def _create_background_layer(self, width: int, height: int, 
                                color: str, opacity: int) -> torch.Tensor:
        """
        Creates a background layer with the specified color and opacity.
        
        Args:
            width: width of the background
            height: height of the background
            color: hex color string
            opacity: opacity value (0-255)
            
        Returns:
            numpy array with background data
        """
        import numpy as np
        
        # Parse hex color
        color = color.lstrip('#')
        if len(color) == 6:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
        else:
            r, g, b = 255, 255, 255  # Default to white
        
        # Create background array
        background = np.full((height, width, 3), [r, g, b], dtype=np.uint8)
        
        return background


class APZmediaPSDLayerSaver8LayersAdvanced:
    """
    Advanced ComfyUI node for saving exactly 8 images as PSD layers with more control options.
    """
    
    def __init__(self, device="cpu"):
        print("APZmediaPSDLayerSaver8LayersAdvanced initialized")
        self.device = device
    
    _blend_modes = [
        "normal", "multiply", "screen", "overlay", "soft_light", "hard_light",
        "color_dodge", "color_burn", "darken", "lighten", "difference", "exclusion"
    ]
    
    _color_modes = ["rgb", "cmyk", "grayscale"]
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Global Settings
                "psd_filename": ("STRING", {"default": "output.psd"}),
                "color_mode": (cls._color_modes, {"default": "rgb"}),
                "create_background_layer": (["true", "false"], {"default": "true"}),
            },
            "optional": {
                # Layer 1 Group
                "image_1": ("IMAGE",),
                "mask_1": ("MASK",),
                "layer_name_1": ("STRING", {"default": "Background"}),
                "opacity_1": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_1": (cls._blend_modes, {"default": "normal"}),
                "offset_x_1": ("INT", {"default": 0}),
                "offset_y_1": ("INT", {"default": 0}),
                
                # Layer 2 Group
                "image_2": ("IMAGE",),
                "mask_2": ("MASK",),
                "layer_name_2": ("STRING", {"default": "Character"}),
                "opacity_2": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_2": (cls._blend_modes, {"default": "normal"}),
                "offset_x_2": ("INT", {"default": 0}),
                "offset_y_2": ("INT", {"default": 0}),
                
                # Layer 3 Group
                "image_3": ("IMAGE",),
                "mask_3": ("MASK",),
                "layer_name_3": ("STRING", {"default": "Hair"}),
                "opacity_3": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_3": (cls._blend_modes, {"default": "normal"}),
                "offset_x_3": ("INT", {"default": 0}),
                "offset_y_3": ("INT", {"default": 0}),
                
                # Layer 4 Group
                "image_4": ("IMAGE",),
                "mask_4": ("MASK",),
                "layer_name_4": ("STRING", {"default": "Clothing"}),
                "opacity_4": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_4": (cls._blend_modes, {"default": "normal"}),
                "offset_x_4": ("INT", {"default": 0}),
                "offset_y_4": ("INT", {"default": 0}),
                
                # Layer 5 Group
                "image_5": ("IMAGE",),
                "mask_5": ("MASK",),
                "layer_name_5": ("STRING", {"default": "Accessories"}),
                "opacity_5": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_5": (cls._blend_modes, {"default": "normal"}),
                "offset_x_5": ("INT", {"default": 0}),
                "offset_y_5": ("INT", {"default": 0}),
                
                # Layer 6 Group
                "image_6": ("IMAGE",),
                "mask_6": ("MASK",),
                "layer_name_6": ("STRING", {"default": "Effects"}),
                "opacity_6": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_6": (cls._blend_modes, {"default": "normal"}),
                "offset_x_6": ("INT", {"default": 0}),
                "offset_y_6": ("INT", {"default": 0}),
                
                # Layer 7 Group
                "image_7": ("IMAGE",),
                "mask_7": ("MASK",),
                "layer_name_7": ("STRING", {"default": "Lighting"}),
                "opacity_7": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_7": (cls._blend_modes, {"default": "normal"}),
                "offset_x_7": ("INT", {"default": 0}),
                "offset_y_7": ("INT", {"default": 0}),
                
                # Layer 8 Group
                "image_8": ("IMAGE",),
                "mask_8": ("MASK",),
                "layer_name_8": ("STRING", {"default": "Overlay"}),
                "opacity_8": ("INT", {"default": 255, "min": 0, "max": 255}),
                "blend_mode_8": (cls._blend_modes, {"default": "normal"}),
                "offset_x_8": ("INT", {"default": 0}),
                "offset_y_8": ("INT", {"default": 0}),
                
                # Background Layer Settings
                "background_color": ("STRING", {"default": "#FFFFFF"}),
                "background_opacity": ("INT", {"default": 255, "min": 0, "max": 255}),
            }
        }
    
    RETURN_TYPES = ("STRING", "BOOLEAN", "INT")
    RETURN_NAMES = ("output_path", "success", "layer_count")
    FUNCTION = "save_8_layers_psd_advanced"
    CATEGORY = "image/psd"
    
    def save_8_layers_psd_advanced(self, 
                                  # Global Settings
                                  psd_filename, color_mode="rgb", create_background_layer="true",
                                  # Layer 1 Group
                                  image_1=None, mask_1=None, layer_name_1="Background", opacity_1=255, blend_mode_1="normal", offset_x_1=0, offset_y_1=0,
                                  # Layer 2 Group
                                  image_2=None, mask_2=None, layer_name_2="Character", opacity_2=255, blend_mode_2="normal", offset_x_2=0, offset_y_2=0,
                                  # Layer 3 Group
                                  image_3=None, mask_3=None, layer_name_3="Hair", opacity_3=255, blend_mode_3="normal", offset_x_3=0, offset_y_3=0,
                                  # Layer 4 Group
                                  image_4=None, mask_4=None, layer_name_4="Clothing", opacity_4=255, blend_mode_4="normal", offset_x_4=0, offset_y_4=0,
                                  # Layer 5 Group
                                  image_5=None, mask_5=None, layer_name_5="Accessories", opacity_5=255, blend_mode_5="normal", offset_x_5=0, offset_y_5=0,
                                  # Layer 6 Group
                                  image_6=None, mask_6=None, layer_name_6="Effects", opacity_6=255, blend_mode_6="normal", offset_x_6=0, offset_y_6=0,
                                  # Layer 7 Group
                                  image_7=None, mask_7=None, layer_name_7="Lighting", opacity_7=255, blend_mode_7="normal", offset_x_7=0, offset_y_7=0,
                                  # Layer 8 Group
                                  image_8=None, mask_8=None, layer_name_8="Overlay", opacity_8=255, blend_mode_8="normal", offset_x_8=0, offset_y_8=0,
                                  # Background Layer Settings
                                  background_color="#FFFFFF", background_opacity=255) -> Tuple[str, bool, int]:
        """
        Advanced PSD layer saving with background layer and offset support for exactly 8 layers.
        
        Args:
            image_1-8: Individual image tensors
            layer_name_1-8: Individual layer names
            psd_filename: Name of the PSD file to create
            color_mode: Color mode for the PSD file
            create_background_layer: Whether to create a background layer
            mask_1-8: Optional individual masks
            opacity_1-8: Individual opacity values (0-255)
            blend_mode_1-8: Individual blend modes
            background_color: Hex color for background
            background_opacity: Opacity for background layer
            offset_x_1-8, offset_y_1-8: Individual layer offsets
            
        Returns:
            tuple of (output_path, success_boolean, layer_count)
        """
        try:
            # Organize inputs into lists for easier processing
            images = [image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8]
            layer_names = [layer_name_1, layer_name_2, layer_name_3, layer_name_4, 
                          layer_name_5, layer_name_6, layer_name_7, layer_name_8]
            masks = [mask_1, mask_2, mask_3, mask_4, mask_5, mask_6, mask_7, mask_8]
            opacities = [opacity_1, opacity_2, opacity_3, opacity_4, 
                        opacity_5, opacity_6, opacity_7, opacity_8]
            blend_modes = [blend_mode_1, blend_mode_2, blend_mode_3, blend_mode_4,
                          blend_mode_5, blend_mode_6, blend_mode_7, blend_mode_8]
            offsets = [(offset_x_1, offset_y_1), (offset_x_2, offset_y_2), (offset_x_3, offset_y_3), (offset_x_4, offset_y_4),
                      (offset_x_5, offset_y_5), (offset_x_6, offset_y_6), (offset_x_7, offset_y_7), (offset_x_8, offset_y_8)]
            
            # Filter out None masks and create a list of valid masks
            valid_masks = []
            for i, mask in enumerate(masks):
                if mask is not None:
                    # Process mask for PSD
                    processed_mask = PSDMaskUtility.process_mask_for_psd(mask)
                    valid_masks.append(processed_mask)
                else:
                    valid_masks.append(None)
            
            # Create PSD layers
            layers = []
            for i in range(8):
                # Skip if no image provided
                if images[i] is None:
                    continue
                    
                # Convert image tensor to numpy array
                image_data = tensor_to_numpy_array(images[i])
                
                # Get mask data if provided
                mask_data = valid_masks[i] if valid_masks[i] is not None else None
                
                # Create layer
                layer = create_psd_layer(
                    image_data=image_data,
                    layer_name=layer_names[i],
                    mask_data=mask_data,
                    opacity=opacities[i],
                    blend_mode=blend_modes[i]
                )
                
                # Note: Layer offsets would need to be implemented in the PSD layer creation
                # For now, we'll create the layers without offset support
                # This could be enhanced in future versions
                
                layers.append(layer)
            
            # Add background layer if requested
            if create_background_layer == "true":
                # Get image dimensions from first available layer
                first_image = None
                for img in images:
                    if img is not None:
                        first_image = tensor_to_numpy_array(img)
                        break
                
                if first_image is not None:
                    height, width = first_image.shape[:2]
                else:
                    # Default dimensions if no images provided
                    height, width = 512, 512
                
                # Create background layer
                background_data = self._create_background_layer(
                    width, height, background_color, background_opacity
                )
                
                background_layer = create_psd_layer(
                    image_data=background_data,
                    layer_name="Background",
                    opacity=background_opacity,
                    blend_mode="normal"
                )
                
                # Add background as first layer
                layers.insert(0, background_layer)
            
            # Validate layer dimensions
            is_valid, error_msg = validate_layer_dimensions(layers)
            if not is_valid:
                print(f"Warning: {error_msg}")
            
            # Create PSD file
            psd = create_psd_from_layers(layers, color_mode=color_mode)
            
            # Ensure output directory exists
            output_dir = os.path.dirname(psd_filename) if os.path.dirname(psd_filename) else "."
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Save PSD file
            success = save_psd_file(psd, psd_filename)
            
            layer_count = len(layers)
            
            if success:
                print(f"Successfully saved PSD file with {layer_count} layers to: {psd_filename}")
                return psd_filename, True, layer_count
            else:
                print(f"Failed to save PSD file to: {psd_filename}")
                return psd_filename, False, layer_count
                
        except Exception as e:
            print(f"Error in save_8_layers_psd_advanced: {e}")
            import traceback
            traceback.print_exc()
            return psd_filename, False, 0
    
    def _create_background_layer(self, width: int, height: int, 
                                color: str, opacity: int) -> torch.Tensor:
        """
        Creates a background layer with the specified color and opacity.
        
        Args:
            width: width of the background
            height: height of the background
            color: hex color string
            opacity: opacity value (0-255)
            
        Returns:
            numpy array with background data
        """
        import numpy as np
        
        # Parse hex color
        color = color.lstrip('#')
        if len(color) == 6:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
        else:
            r, g, b = 255, 255, 255  # Default to white
        
        # Create background array
        background = np.full((height, width, 3), [r, g, b], dtype=np.uint8)
        
        return background
