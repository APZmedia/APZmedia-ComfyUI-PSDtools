"""
PSD Layer and Mask Conversion Utilities for ComfyUI using psd-tools and PIL

This module provides utilities for converting ComfyUI tensors and images
to PSD layer format using the psd-tools library and PIL.
"""

import torch
import numpy as np
from PIL import Image, ImageOps
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


def tensor_to_pil_image(image_tensor: torch.Tensor) -> Image.Image:
    """
    Converts a PyTorch tensor to a PIL Image.
    
    Args:
        image_tensor: PyTorch tensor with shape [B, H, W, C] or [B, C, H, W]
        
    Returns:
        PIL Image in RGB mode
    """
    # Ensure the tensor is on the CPU
    image_tensor = image_tensor.cpu()
    
    # Convert the tensor to [B, H, W, C] format if it's in [B, C, H, W]
    if len(image_tensor.shape) == 4 and image_tensor.shape[1] in [1, 3, 4]:
        image_tensor = image_tensor.permute(0, 2, 3, 1)
    
    # Take the first image from the batch
    img_tensor = image_tensor[0]
    
    # Clamp values to [0, 1] range if they're floating point
    if img_tensor.is_floating_point():
        img_tensor = torch.clamp(img_tensor, 0.0, 1.0)
        # Convert to 8-bit
        img_tensor = (img_tensor * 255).type(torch.uint8)
    else:
        img_tensor = img_tensor.type(torch.uint8)
    
    # Convert to numpy array
    img_np = img_tensor.numpy()
    
    # Handle different channel counts
    if img_np.shape[2] == 1:
        # Grayscale - convert to RGB
        img_np = np.repeat(img_np, 3, axis=2)
    elif img_np.shape[2] == 4:
        # RGBA - convert to RGB (drop alpha)
        img_np = img_np[:, :, :3]
    elif img_np.shape[2] != 3:
        # Unexpected channel count - convert to RGB
        if img_np.shape[2] > 3:
            img_np = img_np[:, :, :3]
        else:
            # Pad with zeros
            padding = np.zeros((img_np.shape[0], img_np.shape[1], 3 - img_np.shape[2]), dtype=img_np.dtype)
            img_np = np.concatenate([img_np, padding], axis=2)
    
    # Create PIL Image
    pil_image = Image.fromarray(img_np, 'RGB')
    
    return pil_image


def tensor_to_pil_mask(mask_tensor: torch.Tensor) -> Image.Image:
    """
    Converts a mask tensor to a PIL Image in grayscale mode.
    
    Args:
        mask_tensor: PyTorch tensor with shape [B, H, W] or [B, 1, H, W]
        
    Returns:
        PIL Image in L (grayscale) mode
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
    
    # Clamp values to [0, 1] range if they're floating point
    if mask.is_floating_point():
        mask = torch.clamp(mask, 0.0, 1.0)
        # Convert to 8-bit
        mask = (mask * 255).type(torch.uint8)
    else:
        mask = mask.type(torch.uint8)
    
    # Convert to numpy array
    mask_np = mask.numpy()
    
    # Create PIL Image
    pil_mask = Image.fromarray(mask_np, 'L')
    
    return pil_mask


def calculate_canvas_size(images: List[Image.Image]) -> Tuple[int, int]:
    """
    Calculates the canvas size based on the maximum width and height of all images.
    
    Args:
        images: List of PIL Images
        
    Returns:
        tuple of (max_width, max_height)
    """
    if not images:
        return 512, 512  # Default size
    
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    
    return max_width, max_height


def center_and_pad_image(image: Image.Image, canvas_width: int, canvas_height: int, 
                        background_color: Tuple[int, int, int] = (0, 0, 0)) -> Image.Image:
    """
    Centers an image on a canvas and pads it with background color.
    
    Args:
        image: PIL Image to center
        canvas_width: Width of the canvas
        canvas_height: Height of the canvas
        background_color: RGB color for padding
        
    Returns:
        PIL Image centered on canvas
    """
    # Create a new image with the canvas size and background color
    canvas = Image.new('RGB', (canvas_width, canvas_height), background_color)
    
    # Calculate position to center the image
    x = (canvas_width - image.width) // 2
    y = (canvas_height - image.height) // 2
    
    # Paste the image onto the canvas
    canvas.paste(image, (x, y))
    
    return canvas


def resize_and_center_mask(mask: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """
    Resizes a mask to match the target image size and centers it.
    
    Args:
        mask: PIL Image mask in L mode
        target_width: Target width
        target_height: Target height
        
    Returns:
        PIL Image mask resized and centered
    """
    # Resize mask to match the target image size using LANCZOS resampling
    resized_mask = mask.resize((target_width, target_height), Image.LANCZOS)
    
    return resized_mask


def create_psd_layer_with_mask(pil_image: Image.Image, layer_name: str, 
                              pil_mask: Optional[Image.Image] = None) -> PixelLayer:
    """
    Creates a PSD layer from a PIL image with optional mask.
    
    Args:
        pil_image: PIL Image in RGB mode
        layer_name: Name for the layer
        pil_mask: Optional PIL Image mask in L mode
        
    Returns:
        psd_tools PixelLayer object
    """
    check_psd_tools_available()
    
    # Create a temporary PSD to get the layer
    temp_psd = PSDImage.new(mode='RGB', size=pil_image.size, color=(0, 0, 0))
    
    # Create the layer from the PIL image
    layer = PixelLayer.frompil(pil_image, temp_psd, layer_name)
    
    # Add mask if provided
    if pil_mask is not None:
        # Convert mask to numpy array
        mask_data = np.array(pil_mask)
        
        # Create mask data structure
        mask_channel_data = ChannelData(
            compression=Compression.RAW,
            data=mask_data.tobytes()
        )
        
        # Create channel info for user layer mask
        channel_info = ChannelInfo(
            id=ChannelID.USER_LAYER_MASK,
            length=len(mask_data.tobytes())
        )
        
        # Add mask to layer
        layer._channels[ChannelID.USER_LAYER_MASK] = mask_channel_data
        layer._record.channel_count = len(layer._channels)
        
        # Create proper mask data structure using MaskData
        mask_data_obj = MaskData(
            top=0,
            left=0,
            bottom=pil_mask.height,
            right=pil_mask.width,
            background_color=0,
            flags=MaskFlags(0)
        )
        
        # Update layer record with mask info
        layer._record.mask_data = mask_data_obj
    
    return layer


def create_psd_from_layers(layers: List[PixelLayer], canvas_width: int, canvas_height: int,
                          background_color: Tuple[int, int, int] = (0, 0, 0)) -> PSDImage:
    """
    Creates a PSD file from a list of layers.
    
    Args:
        layers: List of psd_tools PixelLayer objects
        canvas_width: Width of the canvas
        canvas_height: Height of the canvas
        background_color: RGB color for background
        
    Returns:
        psd_tools PSDImage object
    """
    check_psd_tools_available()
    
    # Create new PSD document
    psd = PSDImage.new(mode='RGB', size=(canvas_width, canvas_height), color=background_color)
    
    # Add layers to PSD
    for layer in layers:
        psd.append(layer)
    
    return psd


def save_psd_file(psd: PSDImage, filepath: str) -> bool:
    """
    Saves a PSD object to a file.
    
    Args:
        psd: psd_tools PSDImage object
        filepath: path where to save the PSD file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        psd.save(filepath)
        return True
    except Exception as e:
        print(f"Error saving PSD file: {e}")
        return False


def generate_unique_filename(base_path: str, output_dir: str = ".") -> str:
    """
    Generates a unique filename by appending numbers if the file exists.
    
    Args:
        base_path: Base file path (e.g., "output.psd")
        output_dir: Output directory
        
    Returns:
        Unique file path
    """
    # Extract filename and extension
    filename = os.path.basename(base_path)
    name, ext = os.path.splitext(filename)
    
    # Start with the original filename
    counter = 0
    while True:
        if counter == 0:
            unique_filename = filename
        else:
            unique_filename = f"{name}_{counter}{ext}"
        
        full_path = os.path.join(output_dir, unique_filename)
        
        if not os.path.exists(full_path):
            return full_path
        
        counter += 1


def process_layers_to_psd(image_tensors: List[torch.Tensor],
                         layer_names: List[str],
                         mask_tensors: Optional[List[torch.Tensor]] = None,
                         output_dir: str = ".",
                         filename_prefix: str = "output") -> Tuple[str, bool]:
    """
    Processes a list of image tensors and creates a PSD file.
    
    Args:
        image_tensors: List of PyTorch tensors with images
        layer_names: List of names for each layer
        mask_tensors: Optional list of PyTorch tensors with masks
        output_dir: Directory to save the PSD file
        filename_prefix: Prefix for the filename
        
    Returns:
        tuple of (output_path, success_boolean)
    """
    try:
        check_psd_tools_available()
        
        # Convert tensors to PIL images
        pil_images = []
        for tensor in image_tensors:
            pil_image = tensor_to_pil_image(tensor)
            pil_images.append(pil_image)
        
        # Calculate canvas size
        canvas_width, canvas_height = calculate_canvas_size(pil_images)
        
        # Process masks if provided
        pil_masks = []
        if mask_tensors:
            for i, mask_tensor in enumerate(mask_tensors):
                if mask_tensor is not None:
                    pil_mask = tensor_to_pil_mask(mask_tensor)
                    # Resize mask to match the corresponding image
                    pil_mask = resize_and_center_mask(pil_mask, pil_images[i].width, pil_images[i].height)
                    pil_masks.append(pil_mask)
                else:
                    pil_masks.append(None)
        else:
            pil_masks = [None] * len(pil_images)
        
        # Create layers
        layers = []
        for i, (pil_image, layer_name) in enumerate(zip(pil_images, layer_names)):
            # Center and pad the image to canvas size
            centered_image = center_and_pad_image(pil_image, canvas_width, canvas_height)
            
            # Get corresponding mask
            pil_mask = pil_masks[i] if i < len(pil_masks) else None
            
            # Resize and center mask if it exists
            if pil_mask is not None:
                pil_mask = resize_and_center_mask(pil_mask, canvas_width, canvas_height)
            
            # Create PSD layer
            layer = create_psd_layer_with_mask(centered_image, layer_name, pil_mask)
            layers.append(layer)
        
        # Create PSD file
        psd = create_psd_from_layers(layers, canvas_width, canvas_height)
        
        # Generate unique filename
        base_filename = f"{filename_prefix}.psd"
        output_path = generate_unique_filename(base_filename, output_dir)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save PSD file
        success = save_psd_file(psd, output_path)
        
        return output_path, success
        
    except Exception as e:
        print(f"Error in process_layers_to_psd: {e}")
        import traceback
        traceback.print_exc()
        return "", False
