"""
PSD Layer and Mask Loading Utilities for ComfyUI using psd-tools and PIL

This module provides utilities for loading PSD files and extracting layers and masks
using the psd-tools library and PIL.
"""

import torch
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional, Union
import os

# Import psd-tools only when needed to avoid import errors
try:
    from psd_tools import PSDImage
    from psd_tools.api.layers import PixelLayer
    from psd_tools.constants import ColorMode, ChannelID
    from psd_tools.psd.layer_and_mask import MaskData, ChannelInfo, ChannelData, MaskFlags
    from psd_tools.constants import Compression
    PSD_TOOLS_AVAILABLE = True
except ImportError:
    PSD_TOOLS_AVAILABLE = False
    PSDImage = None
    PixelLayer = None
    ColorMode = None
    ChannelID = None
    ChannelData = None
    ChannelInfo = None
    MaskData = None
    MaskFlags = None
    Compression = None


def check_psd_tools_available():
    """Check if psd-tools is available and raise an error if not"""
    if not PSD_TOOLS_AVAILABLE:
        raise ImportError(
            "psd-tools is not installed. Please install it with: pip install psd-tools>=1.9.0\n"
            "Or run the installation script: python install_dependencies.py"
        )


def load_psd_file(filepath: str) -> PSDImage:
    """
    Loads a PSD file from disk.
    
    Args:
        filepath: Path to the PSD file
        
    Returns:
        psd_tools PSDImage object
        
    Raises:
        FileNotFoundError: If the PSD file doesn't exist
        Exception: If there's an error loading the PSD file
    """
    check_psd_tools_available()
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"PSD file not found: {filepath}")
    
    try:
        psd = PSDImage.open(filepath)
        return psd
    except Exception as e:
        raise Exception(f"Error loading PSD file {filepath}: {e}")


def get_psd_info(psd: PSDImage) -> dict:
    """
    Gets information about a PSD file.
    
    Args:
        psd: psd_tools PSDImage object
        
    Returns:
        Dictionary with PSD information
    """
    return {
        'width': psd.width,
        'height': psd.height,
        'color_mode': psd.color_mode.name if hasattr(psd.color_mode, 'name') else str(psd.color_mode),
        'layer_count': len(psd),
        'layer_names': [layer.name for layer in psd]
    }


def pil_to_tensor(pil_image: Image.Image) -> torch.Tensor:
    """
    Converts a PIL Image to a ComfyUI IMAGE tensor.
    
    Args:
        pil_image: PIL Image in RGB mode
        
    Returns:
        PyTorch tensor with shape [1, H, W, C] in float32 format [0, 1]
    """
    # Convert to RGB if not already
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    
    # Convert to numpy array
    img_array = np.array(pil_image, dtype=np.float32) / 255.0
    
    # Convert to tensor and add batch dimension
    tensor = torch.from_numpy(img_array).unsqueeze(0)
    
    return tensor


def pil_mask_to_tensor(pil_mask: Image.Image) -> torch.Tensor:
    """
    Converts a PIL Image mask to a ComfyUI MASK tensor.
    
    Args:
        pil_mask: PIL Image in L (grayscale) mode
        
    Returns:
        PyTorch tensor with shape [1, H, W] in float32 format [0, 1]
    """
    # Convert to grayscale if not already
    if pil_mask.mode != 'L':
        pil_mask = pil_mask.convert('L')
    
    # Convert to numpy array
    mask_array = np.array(pil_mask, dtype=np.float32) / 255.0
    
    # Convert to tensor and add batch dimension
    tensor = torch.from_numpy(mask_array).unsqueeze(0)
    
    return tensor


def extract_layer_image(psd: PSDImage, layer_index: int) -> Optional[Image.Image]:
    """
    Extracts the image data from a specific layer.
    
    Args:
        psd: psd_tools PSDImage object
        layer_index: Index of the layer to extract (0-based)
        
    Returns:
        PIL Image in RGB mode, or None if layer not found
    """
    try:
        if layer_index < 0 or layer_index >= len(psd):
            return None
        
        layer = psd[layer_index]
        
        # Check if it's a pixel layer
        if not isinstance(layer, PixelLayer):
            print(f"Layer {layer_index} is not a pixel layer (type: {type(layer)})")
            return None
        
        # Get the PIL image from the layer
        pil_image = layer.topil()
        
        # Convert to RGB if needed
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        return pil_image
        
    except Exception as e:
        print(f"Error extracting layer {layer_index}: {e}")
        return None


def extract_layer_mask(psd: PSDImage, layer_index: int) -> Optional[Image.Image]:
    """
    Extracts the mask data from a specific layer.
    
    Args:
        psd: psd_tools PSDImage object
        layer_index: Index of the layer to extract (0-based)
        
    Returns:
        PIL Image in L (grayscale) mode, or None if no mask found
    """
    try:
        if layer_index < 0 or layer_index >= len(psd):
            return None
        
        layer = psd[layer_index]
        
        # Check if it's a pixel layer
        if not isinstance(layer, PixelLayer):
            print(f"Layer {layer_index} is not a pixel layer (type: {type(layer)})")
            return None
        
        # Check if layer has a mask
        if not hasattr(layer, '_record') or not hasattr(layer._record, 'mask_data') or layer._record.mask_data is None:
            return None
        
        # Check if layer has mask channels
        if not hasattr(layer, '_channels') or ChannelID.USER_LAYER_MASK not in layer._channels:
            return None
        
        # Get the mask channel data
        mask_channel = layer._channels[ChannelID.USER_LAYER_MASK]
        
        # Get the mask data
        if hasattr(mask_channel, 'data'):
            mask_data = mask_channel.data
        else:
            return None
        
        # Convert bytes to numpy array
        mask_array = np.frombuffer(mask_data, dtype=np.uint8)
        
        # Get mask dimensions from the mask data record
        mask_info = layer._record.mask_data
        mask_width = mask_info.right - mask_info.left
        mask_height = mask_info.bottom - mask_info.top
        
        # Reshape the array
        if len(mask_array) == mask_width * mask_height:
            mask_array = mask_array.reshape((mask_height, mask_width))
        else:
            print(f"Warning: Mask data size {len(mask_array)} doesn't match expected size {mask_width * mask_height}")
            return None
        
        # Create PIL Image
        pil_mask = Image.fromarray(mask_array, 'L')
        
        return pil_mask
        
    except Exception as e:
        print(f"Error extracting mask from layer {layer_index}: {e}")
        return None


def extract_layer_and_mask(psd: PSDImage, layer_index: int) -> Tuple[Optional[Image.Image], Optional[Image.Image]]:
    """
    Extracts both image and mask from a specific layer.
    
    Args:
        psd: psd_tools PSDImage object
        layer_index: Index of the layer to extract (0-based)
        
    Returns:
        Tuple of (PIL Image, PIL Mask) or (None, None) if extraction fails
    """
    image = extract_layer_image(psd, layer_index)
    mask = extract_layer_mask(psd, layer_index)
    
    return image, mask


def get_layer_info(psd: PSDImage, layer_index: int) -> dict:
    """
    Gets information about a specific layer.
    
    Args:
        psd: psd_tools PSDImage object
        layer_index: Index of the layer (0-based)
        
    Returns:
        Dictionary with layer information
    """
    try:
        if layer_index < 0 or layer_index >= len(psd):
            return {'error': f'Layer index {layer_index} out of range (0-{len(psd)-1})'}
        
        layer = psd[layer_index]
        
        info = {
            'index': layer_index,
            'name': layer.name,
            'type': type(layer).__name__,
            'visible': layer.visible if hasattr(layer, 'visible') else True,
            'opacity': layer.opacity if hasattr(layer, 'opacity') else 255,
            'blend_mode': layer.blend_mode.name if hasattr(layer, 'blend_mode') and hasattr(layer.blend_mode, 'name') else str(layer.blend_mode) if hasattr(layer, 'blend_mode') else 'normal',
            'has_mask': False,
            'bbox': None
        }
        
        # Get bounding box
        if hasattr(layer, 'bbox'):
            bbox = layer.bbox
            info['bbox'] = {
                'left': bbox.left,
                'top': bbox.top,
                'right': bbox.right,
                'bottom': bbox.bottom,
                'width': bbox.right - bbox.left,
                'height': bbox.bottom - bbox.top
            }
        
        # Check for mask
        if hasattr(layer, '_record') and hasattr(layer._record, 'mask_data') and layer._record.mask_data is not None:
            info['has_mask'] = True
        
        return info
        
    except Exception as e:
        return {'error': f'Error getting layer info: {e}'}


def list_psd_layers(psd: PSDImage) -> List[dict]:
    """
    Lists all layers in a PSD file with their information.
    
    Args:
        psd: psd_tools PSDImage object
        
    Returns:
        List of dictionaries with layer information
    """
    layers_info = []
    
    for i in range(len(psd)):
        layer_info = get_layer_info(psd, i)
        layers_info.append(layer_info)
    
    return layers_info
