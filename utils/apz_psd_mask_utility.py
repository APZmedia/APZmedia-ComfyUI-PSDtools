"""
PSD Mask Handling Utilities for ComfyUI

This module provides utilities for handling masks in PSD layers,
including mask processing, validation, and manipulation.
"""

import torch
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional, Union
import pytoshop
from pytoshop import enums


class PSDMaskUtility:
    """
    Utility class for handling masks in PSD layers.
    """
    
    @staticmethod
    def normalize_mask(mask: np.ndarray, 
                      target_range: Tuple[int, int] = (0, 255)) -> np.ndarray:
        """
        Normalizes a mask to the target range.
        
        Args:
            mask: numpy array with mask data
            target_range: tuple of (min_value, max_value) for normalization
            
        Returns:
            normalized mask as numpy array
        """
        min_val, max_val = target_range
        
        # Handle different input ranges
        if mask.max() <= 1.0 and mask.min() >= 0.0:
            # Assume normalized [0, 1] range
            mask = mask * (max_val - min_val) + min_val
        elif mask.max() <= 255 and mask.min() >= 0:
            # Already in [0, 255] range, just ensure correct type
            pass
        else:
            # Normalize to target range
            mask_min, mask_max = mask.min(), mask.max()
            if mask_max > mask_min:
                mask = (mask - mask_min) / (mask_max - mask_min) * (max_val - min_val) + min_val
            else:
                mask = np.full_like(mask, min_val)
        
        return mask.astype(np.uint8)
    
    @staticmethod
    def create_inverted_mask(mask: np.ndarray) -> np.ndarray:
        """
        Creates an inverted version of the mask.
        
        Args:
            mask: numpy array with mask data
            
        Returns:
            inverted mask as numpy array
        """
        return 255 - mask
    
    @staticmethod
    def combine_masks(masks: List[np.ndarray], 
                     operation: str = "union") -> np.ndarray:
        """
        Combines multiple masks using the specified operation.
        
        Args:
            masks: list of numpy arrays with mask data
            operation: operation to use ("union", "intersection", "difference")
            
        Returns:
            combined mask as numpy array
        """
        if not masks:
            raise ValueError("No masks provided")
        
        if len(masks) == 1:
            return masks[0]
        
        result = masks[0].copy()
        
        for mask in masks[1:]:
            if operation == "union":
                result = np.maximum(result, mask)
            elif operation == "intersection":
                result = np.minimum(result, mask)
            elif operation == "difference":
                result = np.maximum(result - mask, 0)
            else:
                raise ValueError(f"Unknown operation: {operation}")
        
        return result
    
    @staticmethod
    def apply_mask_to_image(image: np.ndarray, 
                           mask: np.ndarray,
                           background_color: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
        """
        Applies a mask to an image, setting unmasked areas to background color.
        
        Args:
            image: numpy array with image data [H, W, C]
            mask: numpy array with mask data [H, W]
            background_color: RGB color for unmasked areas
            
        Returns:
            masked image as numpy array
        """
        # Ensure mask is 3D for broadcasting
        if len(mask.shape) == 2:
            mask = np.expand_dims(mask, axis=2)
        
        # Normalize mask to [0, 1] range
        mask_normalized = mask.astype(np.float32) / 255.0
        
        # Create background
        background = np.full_like(image, background_color, dtype=np.uint8)
        
        # Apply mask
        result = image * mask_normalized + background * (1 - mask_normalized)
        
        return result.astype(np.uint8)
    
    @staticmethod
    def create_alpha_channel_from_mask(mask: np.ndarray) -> np.ndarray:
        """
        Creates an alpha channel from a mask.
        
        Args:
            mask: numpy array with mask data [H, W]
            
        Returns:
            alpha channel as numpy array [H, W]
        """
        return mask.copy()
    
    @staticmethod
    def add_alpha_to_image(image: np.ndarray, 
                          alpha: np.ndarray) -> np.ndarray:
        """
        Adds an alpha channel to an RGB image.
        
        Args:
            image: numpy array with RGB image data [H, W, 3]
            alpha: numpy array with alpha data [H, W]
            
        Returns:
            RGBA image as numpy array [H, W, 4]
        """
        if image.shape[2] == 4:
            # Already has alpha, replace it
            result = image.copy()
            result[:, :, 3] = alpha
        else:
            # Add alpha channel
            result = np.dstack([image, alpha])
        
        return result
    
    @staticmethod
    def validate_mask_dimensions(mask: np.ndarray, 
                                expected_shape: Tuple[int, int]) -> Tuple[bool, str]:
        """
        Validates that a mask has the expected dimensions.
        
        Args:
            mask: numpy array with mask data
            expected_shape: tuple of (height, width)
            
        Returns:
            tuple of (is_valid, error_message)
        """
        if len(mask.shape) != 2:
            return False, f"Mask should be 2D, got {len(mask.shape)}D"
        
        height, width = mask.shape
        expected_height, expected_width = expected_shape
        
        if height != expected_height or width != expected_width:
            return False, f"Mask dimensions {width}x{height} don't match expected {expected_width}x{expected_height}"
        
        return True, "Mask dimensions are valid"
    
    @staticmethod
    def process_mask_for_psd(mask: Union[torch.Tensor, np.ndarray, Image.Image],
                           target_shape: Optional[Tuple[int, int]] = None) -> np.ndarray:
        """
        Processes a mask from various input formats for use in PSD layers.
        
        Args:
            mask: mask in various formats (tensor, numpy array, or PIL Image)
            target_shape: optional target shape (height, width) for resizing
            
        Returns:
            processed mask as numpy array [H, W] in uint8 format
        """
        # Convert to numpy array
        if isinstance(mask, torch.Tensor):
            mask = mask.cpu().numpy()
            if len(mask.shape) == 4:
                mask = mask[0]  # Take first from batch
            if len(mask.shape) == 3:
                mask = mask[0]  # Take first channel
        elif isinstance(mask, Image.Image):
            mask = np.array(mask.convert('L'))  # Convert to grayscale
        
        # Ensure 2D
        if len(mask.shape) != 2:
            raise ValueError(f"Expected 2D mask, got {len(mask.shape)}D")
        
        # Normalize to [0, 255]
        mask = PSDMaskUtility.normalize_mask(mask)
        
        # Resize if target shape provided
        if target_shape:
            from PIL import Image
            pil_mask = Image.fromarray(mask)
            pil_mask = pil_mask.resize((target_shape[1], target_shape[0]), Image.LANCZOS)
            mask = np.array(pil_mask)
        
        return mask.astype(np.uint8)
    
    @staticmethod
    def create_layer_mask_data(mask: np.ndarray,
                              mask_type: str = "layer_mask") -> dict:
        """
        Creates mask data structure for PSD layer.
        
        Args:
            mask: numpy array with mask data
            mask_type: type of mask ("layer_mask", "vector_mask", "clipping_mask")
            
        Returns:
            dictionary with mask data for PSD layer
        """
        return {
            "mask_data": mask,
            "mask_type": mask_type,
            "mask_enabled": True,
            "mask_default_color": 0,  # Black
            "mask_flags": 0
        }
    
    @staticmethod
    def batch_process_masks(masks: List[Union[torch.Tensor, np.ndarray, Image.Image]],
                           target_shape: Optional[Tuple[int, int]] = None) -> List[np.ndarray]:
        """
        Processes a batch of masks for use in PSD layers.
        
        Args:
            masks: list of masks in various formats
            target_shape: optional target shape for resizing
            
        Returns:
            list of processed masks as numpy arrays
        """
        processed_masks = []
        
        for i, mask in enumerate(masks):
            try:
                processed_mask = PSDMaskUtility.process_mask_for_psd(mask, target_shape)
                processed_masks.append(processed_mask)
            except Exception as e:
                print(f"Error processing mask {i}: {e}")
                # Create a default mask (fully opaque)
                if target_shape:
                    default_mask = np.full(target_shape, 255, dtype=np.uint8)
                else:
                    default_mask = np.full((100, 100), 255, dtype=np.uint8)
                processed_masks.append(default_mask)
        
        return processed_masks
