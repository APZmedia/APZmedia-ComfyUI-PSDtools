"""
APZmedia PSD Layer Saver Node for ComfyUI

This node saves multiple images as layers in a PSD file, with optional masks for each layer.
"""

import torch
import os
from typing import List, Optional, Tuple
# Import utilities with fallback methods
try:
    from utils.apz_psd_conversion import (
        tensor_to_numpy_array,
        create_psd_layer,
        create_psd_from_layers,
        save_psd_file,
        batch_tensors_to_psd_layers,
        validate_layer_dimensions
    )
    from utils.apz_psd_mask_utility import PSDMaskUtility
except ImportError:
    # Fallback: try importing from the extension directory
    import sys
    import os
    extension_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    utils_dir = os.path.join(extension_dir, "utils")
    if utils_dir not in sys.path:
        sys.path.append(utils_dir)
    
    try:
        from apz_psd_conversion import (
            tensor_to_numpy_array,
            create_psd_layer,
            create_psd_from_layers,
            save_psd_file,
            batch_tensors_to_psd_layers,
            validate_layer_dimensions
        )
        from apz_psd_mask_utility import PSDMaskUtility
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
        def batch_tensors_to_psd_layers(*args, **kwargs):
            raise ImportError("PSD utilities not available")
        def validate_layer_dimensions(*args, **kwargs):
            raise ImportError("PSD utilities not available")
        class PSDMaskUtility:
            def __init__(self, *args, **kwargs):
                raise ImportError("PSD utilities not available")


class APZmediaPSDLayerSaver:
    """
    ComfyUI node for saving images as PSD layers with masks.
    """
    
    def __init__(self, device="cpu"):
        print("APZmediaPSDLayerSaver initialized")
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
                "images": ("IMAGE",),
                "layer_names": ("STRING", {
                    "multiline": True, 
                    "default": "Layer 1\nLayer 2\nLayer 3"
                }),
                "output_path": ("STRING", {
                    "default": "./output.psd"
                }),
                "color_mode": (cls._color_modes, {"default": "rgb"}),
            },
            "optional": {
                "masks": ("MASK",),
                "opacities": ("STRING", {
                    "multiline": True,
                    "default": "255\n255\n255"
                }),
                "blend_modes": ("STRING", {
                    "multiline": True,
                    "default": "normal\nnormal\nnormal"
                }),
                "background_color": ("STRING", {
                    "default": "#FFFFFF"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("output_path", "success")
    FUNCTION = "save_psd_layers"
    CATEGORY = "image/psd"
    
    def save_psd_layers(self, 
                       images: torch.Tensor,
                       layer_names: str,
                       output_path: str,
                       color_mode: str = "rgb",
                       masks: Optional[torch.Tensor] = None,
                       opacities: str = "255",
                       blend_modes: str = "normal",
                       background_color: str = "#FFFFFF") -> Tuple[str, bool]:
        """
        Saves images as layers in a PSD file with optional masks.
        
        Args:
            images: tensor with shape [B, H, W, C] containing images
            layer_names: newline-separated string of layer names
            output_path: path where to save the PSD file
            color_mode: color mode for the PSD file
            masks: optional tensor with shape [B, H, W] containing masks
            opacities: newline-separated string of opacity values (0-255)
            blend_modes: newline-separated string of blend mode names
            background_color: hex color string for background
            
        Returns:
            tuple of (output_path, success_boolean)
        """
        try:
            # Parse input strings
            layer_name_list = [name.strip() for name in layer_names.split('\n') if name.strip()]
            opacity_list = [int(op.strip()) for op in opacities.split('\n') if op.strip()]
            blend_mode_list = [mode.strip() for mode in blend_modes.split('\n') if mode.strip()]
            
            # Ensure we have enough names for all images
            num_images = images.shape[0]
            while len(layer_name_list) < num_images:
                layer_name_list.append(f"Layer {len(layer_name_list) + 1}")
            
            # Ensure we have enough opacities
            while len(opacity_list) < num_images:
                opacity_list.append(255)
            
            # Ensure we have enough blend modes
            while len(blend_mode_list) < num_images:
                blend_mode_list.append("normal")
            
            # Process masks if provided
            mask_list = None
            if masks is not None:
                mask_list = []
                for i in range(masks.shape[0]):
                    mask = masks[i:i+1]  # Keep batch dimension
                    processed_mask = PSDMaskUtility.process_mask_for_psd(mask)
                    mask_list.append(processed_mask)
            
            # Convert images to list of tensors
            image_tensors = [images[i:i+1] for i in range(num_images)]
            
            # Create PSD layers
            layers = batch_tensors_to_psd_layers(
                image_tensors=image_tensors,
                layer_names=layer_name_list,
                mask_tensors=mask_list,
                opacities=opacity_list,
                blend_modes=blend_mode_list
            )
            
            # Validate layer dimensions
            is_valid, error_msg = validate_layer_dimensions(layers)
            if not is_valid:
                print(f"Warning: {error_msg}")
                # Continue anyway, pytoshop might handle it
            
            # Create PSD file
            psd = create_psd_from_layers(layers, color_mode=color_mode)
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Save PSD file
            success = save_psd_file(psd, output_path)
            
            if success:
                print(f"Successfully saved PSD file with {len(layers)} layers to: {output_path}")
                return output_path, True
            else:
                print(f"Failed to save PSD file to: {output_path}")
                return output_path, False
                
        except Exception as e:
            print(f"Error in save_psd_layers: {e}")
            import traceback
            traceback.print_exc()
            return output_path, False


class APZmediaPSDLayerSaverAdvanced:
    """
    Advanced ComfyUI node for saving images as PSD layers with more control options.
    """
    
    def __init__(self, device="cpu"):
        print("APZmediaPSDLayerSaverAdvanced initialized")
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
                "images": ("IMAGE",),
                "layer_names": ("STRING", {
                    "multiline": True, 
                    "default": "Layer 1\nLayer 2\nLayer 3"
                }),
                "output_path": ("STRING", {
                    "default": "./output.psd"
                }),
                "color_mode": (cls._color_modes, {"default": "rgb"}),
                "create_background_layer": (["true", "false"], {"default": "true"}),
            },
            "optional": {
                "masks": ("MASK",),
                "opacities": ("STRING", {
                    "multiline": True,
                    "default": "255\n255\n255"
                }),
                "blend_modes": ("STRING", {
                    "multiline": True,
                    "default": "normal\nnormal\nnormal"
                }),
                "background_color": ("STRING", {
                    "default": "#FFFFFF"
                }),
                "background_opacity": ("INT", {
                    "default": 255,
                    "min": 0,
                    "max": 255
                }),
                "layer_offsets": ("STRING", {
                    "multiline": True,
                    "default": "0,0\n0,0\n0,0"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "BOOLEAN", "INT")
    RETURN_NAMES = ("output_path", "success", "layer_count")
    FUNCTION = "save_psd_layers_advanced"
    CATEGORY = "image/psd"
    
    def save_psd_layers_advanced(self, 
                                images: torch.Tensor,
                                layer_names: str,
                                output_path: str,
                                color_mode: str = "rgb",
                                create_background_layer: str = "true",
                                masks: Optional[torch.Tensor] = None,
                                opacities: str = "255",
                                blend_modes: str = "normal",
                                background_color: str = "#FFFFFF",
                                background_opacity: int = 255,
                                layer_offsets: str = "0,0") -> Tuple[str, bool, int]:
        """
        Advanced PSD layer saving with background layer and offset support.
        
        Args:
            images: tensor with shape [B, H, W, C] containing images
            layer_names: newline-separated string of layer names
            output_path: path where to save the PSD file
            color_mode: color mode for the PSD file
            create_background_layer: whether to create a background layer
            masks: optional tensor with shape [B, H, W] containing masks
            opacities: newline-separated string of opacity values (0-255)
            blend_modes: newline-separated string of blend mode names
            background_color: hex color string for background
            background_opacity: opacity for background layer
            layer_offsets: newline-separated string of "x,y" offsets
            
        Returns:
            tuple of (output_path, success_boolean, layer_count)
        """
        try:
            # Parse input strings
            layer_name_list = [name.strip() for name in layer_names.split('\n') if name.strip()]
            opacity_list = [int(op.strip()) for op in opacities.split('\n') if op.strip()]
            blend_mode_list = [mode.strip() for mode in blend_modes.split('\n') if mode.strip()]
            
            # Parse layer offsets
            offset_list = []
            for offset_str in layer_offsets.split('\n'):
                if offset_str.strip():
                    try:
                        x, y = map(int, offset_str.strip().split(','))
                        offset_list.append((x, y))
                    except:
                        offset_list.append((0, 0))
                else:
                    offset_list.append((0, 0))
            
            # Ensure we have enough values for all images
            num_images = images.shape[0]
            while len(layer_name_list) < num_images:
                layer_name_list.append(f"Layer {len(layer_name_list) + 1}")
            
            while len(opacity_list) < num_images:
                opacity_list.append(255)
            
            while len(blend_mode_list) < num_images:
                blend_mode_list.append("normal")
            
            while len(offset_list) < num_images:
                offset_list.append((0, 0))
            
            # Process masks if provided
            mask_list = None
            if masks is not None:
                mask_list = []
                for i in range(masks.shape[0]):
                    mask = masks[i:i+1]  # Keep batch dimension
                    processed_mask = PSDMaskUtility.process_mask_for_psd(mask)
                    mask_list.append(processed_mask)
            
            # Convert images to list of tensors
            image_tensors = [images[i:i+1] for i in range(num_images)]
            
            # Create PSD layers
            layers = batch_tensors_to_psd_layers(
                image_tensors=image_tensors,
                layer_names=layer_name_list,
                mask_tensors=mask_list,
                opacities=opacity_list,
                blend_modes=blend_mode_list
            )
            
            # Add background layer if requested
            if create_background_layer == "true":
                # Get image dimensions from first layer
                first_image = tensor_to_numpy_array(image_tensors[0])
                height, width = first_image.shape[:2]
                
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
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Save PSD file
            success = save_psd_file(psd, output_path)
            
            layer_count = len(layers)
            
            if success:
                print(f"Successfully saved PSD file with {layer_count} layers to: {output_path}")
                return output_path, True, layer_count
            else:
                print(f"Failed to save PSD file to: {output_path}")
                return output_path, False, layer_count
                
        except Exception as e:
            print(f"Error in save_psd_layers_advanced: {e}")
            import traceback
            traceback.print_exc()
            return output_path, False, 0
    
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
