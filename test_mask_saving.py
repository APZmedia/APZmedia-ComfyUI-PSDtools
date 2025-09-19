#!/usr/bin/env python3
"""
Test script to verify mask saving functionality in APZmedia PSD Tools
"""

import torch
import numpy as np
from PIL import Image
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our utilities
try:
    from utils.apz_psd_tools_utility import process_layers_to_psd
    print("✅ Successfully imported PSD utilities")
except ImportError as e:
    print(f"❌ Failed to import PSD utilities: {e}")
    sys.exit(1)

def create_test_image(width=512, height=512, color=(255, 0, 0)):
    """Create a test image tensor"""
    # Create RGB image
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:, :] = color
    
    # Convert to tensor format [B, H, W, C]
    tensor = torch.from_numpy(image).unsqueeze(0).float() / 255.0
    return tensor

def create_test_mask(width=512, height=512, mask_type="circle"):
    """Create a test mask tensor"""
    mask = np.zeros((height, width), dtype=np.uint8)
    
    if mask_type == "circle":
        # Create circular mask
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 4
        
        y, x = np.ogrid[:height, :width]
        mask_circle = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
        mask[mask_circle] = 255
        
    elif mask_type == "gradient":
        # Create gradient mask
        for i in range(height):
            mask[i, :] = int(255 * (i / height))
    
    elif mask_type == "stripes":
        # Create striped mask
        for i in range(0, height, 20):
            mask[i:i+10, :] = 255
    
    # Convert to tensor format [B, H, W]
    tensor = torch.from_numpy(mask).unsqueeze(0).float() / 255.0
    return tensor

def test_mask_saving():
    """Test the mask saving functionality"""
    print("🧪 Starting mask saving test...")
    
    # Create test images
    red_image = create_test_image(512, 512, (255, 0, 0))
    green_image = create_test_image(512, 512, (0, 255, 0))
    blue_image = create_test_image(512, 512, (0, 0, 255))
    
    # Create test masks
    circle_mask = create_test_mask(512, 512, "circle")
    gradient_mask = create_test_mask(512, 512, "gradient")
    stripe_mask = create_test_mask(512, 512, "stripes")
    
    print(f"📊 Created test data:")
    print(f"  - Red image: {red_image.shape}")
    print(f"  - Green image: {green_image.shape}")
    print(f"  - Blue image: {blue_image.shape}")
    print(f"  - Circle mask: {circle_mask.shape}")
    print(f"  - Gradient mask: {gradient_mask.shape}")
    print(f"  - Stripe mask: {stripe_mask.shape}")
    
    # Test 1: Images with masks
    print("\n🧪 Test 1: Images with masks")
    image_tensors = [red_image, green_image, blue_image]
    mask_tensors = [circle_mask, gradient_mask, stripe_mask]
    layer_names = ["Red Circle", "Green Gradient", "Blue Stripes"]
    
    output_path, success = process_layers_to_psd(
        image_tensors=image_tensors,
        layer_names=layer_names,
        mask_tensors=mask_tensors,
        output_dir="./test_output",
        filename_prefix="test_with_masks"
    )
    
    if success:
        print(f"✅ Test 1 PASSED: Created PSD with masks at {output_path}")
    else:
        print(f"❌ Test 1 FAILED: Could not create PSD with masks")
    
    # Test 2: Images without masks
    print("\n🧪 Test 2: Images without masks")
    output_path, success = process_layers_to_psd(
        image_tensors=image_tensors,
        layer_names=layer_names,
        mask_tensors=None,
        output_dir="./test_output",
        filename_prefix="test_without_masks"
    )
    
    if success:
        print(f"✅ Test 2 PASSED: Created PSD without masks at {output_path}")
    else:
        print(f"❌ Test 2 FAILED: Could not create PSD without masks")
    
    # Test 3: Mixed masks (some None, some provided)
    print("\n🧪 Test 3: Mixed masks")
    mixed_masks = [circle_mask, None, stripe_mask]  # Middle layer has no mask
    mixed_names = ["Red Circle", "Green No Mask", "Blue Stripes"]
    
    output_path, success = process_layers_to_psd(
        image_tensors=image_tensors,
        layer_names=mixed_names,
        mask_tensors=mixed_masks,
        output_dir="./test_output",
        filename_prefix="test_mixed_masks"
    )
    
    if success:
        print(f"✅ Test 3 PASSED: Created PSD with mixed masks at {output_path}")
    else:
        print(f"❌ Test 3 FAILED: Could not create PSD with mixed masks")
    
    print("\n🎉 Mask saving tests completed!")
    print("📁 Check the ./test_output directory for generated PSD files")
    print("💡 Open the PSD files in Photoshop to verify masks are properly applied")

if __name__ == "__main__":
    test_mask_saving()
