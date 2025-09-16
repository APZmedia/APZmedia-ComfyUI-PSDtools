"""
PSD Layer and Mask Conversion Utilities for ComfyUI

This module provides utilities for converting ComfyUI tensors and images
to PSD layer format using the pytoshop library.
"""

import torch
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional, Union

# Import pytoshop only when needed to avoid import errors
try:
    import pytoshop
    from pytoshop import enums
    from pytoshop.user import nested_layers
    PYTOSHOP_AVAILABLE = True
except ImportError:
    PYTOSHOP_AVAILABLE = False
    pytoshop = None
    enums = None
    nested_layers = None


def check_pytoshop_available():
    """Check if pytoshop is available and raise an error if not"""
    if not PYTOSHOP_AVAILABLE:
        raise ImportError(
            "pytoshop is not installed. Please install it with: pip install pytoshop>=0.1.0\n"
            "Or run the installation script: python install_dependencies.py"
        )

def tensor_to_numpy_array(image_tensor: torch.Tensor) -> np.ndarray:
    """
    Converts a PyTorch tensor to a numpy array suitable for PSD layers.
    
    Args:
        image_tensor: PyTorch tensor with shape [B, H, W, C] or [B, C, H, W]
        
    Returns:
        numpy array with shape [H, W, C] in uint8 format
    """
    # Ensure the tensor is on the CPU and in the correct format
    if image_tensor.is_floating_point():
        image_tensor = (image_tensor * 255).type(torch.uint8)
    
    image_tensor = image_tensor.cpu()
    
    # Convert the tensor to [B, H, W, C] format if it's in [B, C, H, W]
    if len(image_tensor.shape) == 4 and image_tensor.shape[1] == 3 or image_tensor.shape[1] == 4:
        image_tensor = image_tensor.permute(0, 2, 3, 1)
    
    # Take the first image from the batch
    img_tensor = image_tensor[0]
    img_np = img_tensor.numpy().astype(np.uint8)
    
    return img_np


def pil_to_numpy_array(pil_image: Image.Image) -> np.ndarray:
    """
    Converts a PIL image to a numpy array suitable for PSD layers.
    
    Args:
        pil_image: PIL Image object
        
    Returns:
        numpy array with shape [H, W, C] in uint8 format
    """
    # Convert to RGB if not already
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    
    return np.array(pil_image)


def mask_tensor_to_numpy_array(mask_tensor: torch.Tensor) -> np.ndarray:
    """
    Converts a mask tensor to a numpy array suitable for PSD layer masks.
    
    Args:
        mask_tensor: PyTorch tensor with shape [B, H, W] or [B, 1, H, W]
        
    Returns:
        numpy array with shape [H, W] in uint8 format (grayscale)
    """
    # Ensure the tensor is on the CPU
    mask_tensor = mask_tensor.cpu()
    
    # Handle different tensor shapes
    if len(mask_tensor.shape) == 4 and mask_tensor.shape[1] == 1:
        # [B, 1, H, W] -> [B, H, W]
        mask_tensor = mask_tensor.squeeze(1)
    elif len(mask_tensor.shape) == 4 and mask_tensor.shape[1] == 3:
        # [B, 3, H, W] -> [B, H, W] (take first channel)
        mask_tensor = mask_tensor[:, 0, :, :]
    
    # Take the first mask from the batch
    mask = mask_tensor[0]
    
    # Convert to numpy and ensure uint8
    if mask.is_floating_point():
        mask = (mask * 255).type(torch.uint8)
    else:
        mask = mask.type(torch.uint8)
    
    return mask.numpy()


def create_psd_layer(image_data: np.ndarray, 
                    layer_name: str,
                    mask_data: Optional[np.ndarray] = None,
                    opacity: int = 255,
                    blend_mode: str = "normal") -> nested_layers.Layer:
    """
    Creates a PSD layer from image and optional mask data.
    
    Args:
        image_data: numpy array with shape [H, W, C] in uint8 format
        layer_name: name for the layer
        mask_data: optional numpy array with shape [H, W] for layer mask
        opacity: layer opacity (0-255)
        blend_mode: layer blend mode
        
    Returns:
        pytoshop nested_layers.Layer object
    """
    check_pytoshop_available()
    # Convert blend mode string to enum
    blend_mode_enum = getattr(enums.BlendMode, blend_mode.lower(), enums.BlendMode.normal)
    
    # Create the layer
    layer = nested_layers.Layer(
        name=layer_name,
        image_data=image_data,
        opacity=opacity,
        blend_mode=blend_mode_enum
    )
    
    # Add mask if provided
    if mask_data is not None:
        layer.mask_data = mask_data
    
    return layer


def create_psd_from_layers(layers: List[nested_layers.Layer],
                          color_mode: str = "rgb",
                          width: Optional[int] = None,
                          height: Optional[int] = None) -> pytoshop.Psd:
    """
    Creates a PSD file from a list of layers.
    
    Args:
        layers: list of pytoshop nested_layers.Layer objects
        color_mode: color mode for the PSD ("rgb", "cmyk", "grayscale")
        width: optional width override
        height: optional height override
        
    Returns:
        pytoshop.Psd object
    """
    # Convert color mode string to enum
    color_mode_enum = getattr(enums.ColorMode, color_mode.lower(), enums.ColorMode.rgb)
    
    # Create PSD from nested layers
    psd = nested_layers.nested_layers_to_psd(layers, color_mode=color_mode_enum)
    
    return psd


def save_psd_file(psd: pytoshop.Psd, filepath: str) -> bool:
    """
    Saves a PSD object to a file.
    
    Args:
        psd: pytoshop.Psd object
        filepath: path where to save the PSD file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'wb') as f:
            psd.write(f)
        return True
    except Exception as e:
        print(f"Error saving PSD file: {e}")
        return False


def batch_tensors_to_psd_layers(image_tensors: List[torch.Tensor],
                               layer_names: List[str],
                               mask_tensors: Optional[List[torch.Tensor]] = None,
                               opacities: Optional[List[int]] = None,
                               blend_modes: Optional[List[str]] = None) -> List[nested_layers.Layer]:
    """
    Converts a batch of image tensors to PSD layers.
    
    Args:
        image_tensors: list of PyTorch tensors with images
        layer_names: list of names for each layer
        mask_tensors: optional list of PyTorch tensors with masks
        opacities: optional list of opacity values (0-255)
        blend_modes: optional list of blend mode strings
        
    Returns:
        list of pytoshop nested_layers.Layer objects
    """
    layers = []
    
    for i, (image_tensor, layer_name) in enumerate(zip(image_tensors, layer_names)):
        # Convert image tensor to numpy array
        image_data = tensor_to_numpy_array(image_tensor)
        
        # Get mask data if provided
        mask_data = None
        if mask_tensors and i < len(mask_tensors):
            mask_data = mask_tensor_to_numpy_array(mask_tensors[i])
        
        # Get opacity if provided
        opacity = 255
        if opacities and i < len(opacities):
            opacity = opacities[i]
        
        # Get blend mode if provided
        blend_mode = "normal"
        if blend_modes and i < len(blend_modes):
            blend_mode = blend_modes[i]
        
        # Create layer
        layer = create_psd_layer(
            image_data=image_data,
            layer_name=layer_name,
            mask_data=mask_data,
            opacity=opacity,
            blend_mode=blend_mode
        )
        
        layers.append(layer)
    
    return layers


def validate_layer_dimensions(layers: List[nested_layers.Layer]) -> Tuple[bool, str]:
    """
    Validates that all layers have compatible dimensions.
    
    Args:
        layers: list of pytoshop nested_layers.Layer objects
        
    Returns:
        tuple of (is_valid, error_message)
    """
    if not layers:
        return False, "No layers provided"
    
    # Get dimensions of first layer
    first_layer = layers[0]
    expected_height, expected_width = first_layer.image_data.shape[:2]
    
    for i, layer in enumerate(layers[1:], 1):
        layer_height, layer_width = layer.image_data.shape[:2]
        
        if layer_height != expected_height or layer_width != expected_width:
            return False, f"Layer {i} ({layer.name}) has dimensions {layer_width}x{layer_height}, expected {expected_width}x{expected_height}"
    
    return True, "All layers have compatible dimensions"
