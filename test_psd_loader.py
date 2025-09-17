#!/usr/bin/env python3
"""
Test script for the PSD Layer Loader node.
This script tests the PSD loading functionality.
"""

import sys
import os
import torch
import numpy as np
from PIL import Image

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_psd_loader_utilities():
    """Test the PSD loader utility functions."""
    print("Testing PSD loader utility functions...")
    
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
        
        # Test 1: Check psd-tools availability
        print("  Testing psd-tools availability...")
        check_psd_tools_available()
        print("    ✓ psd-tools is available")
        
        # Test 2: Test PIL to tensor conversion
        print("  Testing PIL to tensor conversion...")
        test_image = Image.new('RGB', (128, 128), (255, 0, 0))
        image_tensor = pil_to_tensor(test_image)
        print(f"    ✓ Image tensor shape: {image_tensor.shape}")
        
        # Test 3: Test PIL mask to tensor conversion
        print("  Testing PIL mask to tensor conversion...")
        test_mask = Image.new('L', (128, 128), 128)
        mask_tensor = pil_mask_to_tensor(test_mask)
        print(f"    ✓ Mask tensor shape: {mask_tensor.shape}")
        
        print("  All utility function tests passed!")
        return True
        
    except ImportError as e:
        print(f"  Import error: {e}")
        return False
    except Exception as e:
        print(f"  Error testing utilities: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_psd_loading():
    """Test PSD file loading with the test files we created earlier."""
    print("Testing PSD file loading...")
    
    try:
        from utils.apz_psd_loader_utility import (
            load_psd_file,
            get_psd_info,
            extract_layer_and_mask,
            pil_to_tensor,
            pil_mask_to_tensor,
            list_psd_layers
        )
        
        # Look for test PSD files
        test_files = []
        for file in os.listdir('.'):
            if file.endswith('.psd') and 'test' in file.lower():
                test_files.append(file)
        
        if not test_files:
            print("  No test PSD files found. Creating a test PSD...")
            # Create a simple test PSD using our saver
            from utils.apz_psd_tools_utility import process_layers_to_psd
            
            # Create test images
            test_images = []
            for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
                img_array = np.full((100, 100, 3), color, dtype=np.uint8)
                img_tensor = torch.from_numpy(img_array).unsqueeze(0).float() / 255.0
                test_images.append(img_tensor)
            
            layer_names = ["Red Layer", "Green Layer", "Blue Layer"]
            
            # Create PSD
            output_path, success = process_layers_to_psd(
                image_tensors=test_images,
                layer_names=layer_names,
                mask_tensors=None,
                output_dir=".",
                filename_prefix="test_loader"
            )
            
            if success:
                test_files = [output_path]
                print(f"  Created test PSD: {output_path}")
            else:
                print("  Failed to create test PSD")
                return False
        
        # Test loading the first PSD file
        psd_file = test_files[0]
        print(f"  Testing with PSD file: {psd_file}")
        
        # Load PSD
        psd = load_psd_file(psd_file)
        
        # Get PSD info
        psd_info = get_psd_info(psd)
        print(f"    PSD Info: {psd_info['width']}x{psd_info['height']}, {psd_info['layer_count']} layers")
        
        # List layers
        layers_info = list_psd_layers(psd)
        print(f"    Layers:")
        for layer_info in layers_info:
            if 'error' not in layer_info:
                mask_info = " (with mask)" if layer_info['has_mask'] else ""
                print(f"      {layer_info['index']}: {layer_info['name']}{mask_info}")
        
        # Test extracting first layer
        if psd_info['layer_count'] > 0:
            print("    Testing layer extraction...")
            pil_image, pil_mask = extract_layer_and_mask(psd, 0)
            
            if pil_image is not None:
                image_tensor = pil_to_tensor(pil_image)
                print(f"      ✓ Extracted layer image: {pil_image.size}, tensor shape: {image_tensor.shape}")
                
                if pil_mask is not None:
                    mask_tensor = pil_mask_to_tensor(pil_mask)
                    print(f"      ✓ Extracted layer mask: {pil_mask.size}, tensor shape: {mask_tensor.shape}")
                else:
                    print("      ✓ No mask found for this layer")
            else:
                print("      ✗ Failed to extract layer image")
                return False
        
        print("  PSD loading tests passed!")
        return True
        
    except Exception as e:
        print(f"  Error in PSD loading: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_loader_nodes():
    """Test the ComfyUI loader nodes."""
    print("Testing ComfyUI loader nodes...")
    
    try:
        from nodes.apzPSDLayerLoader import APZmediaPSDLayerLoader, APZmediaPSDInfoLoader
        
        # Look for test PSD files
        test_files = []
        for file in os.listdir('.'):
            if file.endswith('.psd') and 'test' in file.lower():
                test_files.append(file)
        
        if not test_files:
            print("  No test PSD files found for node testing")
            return False
        
        psd_file = test_files[0]
        print(f"  Testing with PSD file: {psd_file}")
        
        # Test PSD Info Loader
        print("    Testing PSD Info Loader...")
        info_loader = APZmediaPSDInfoLoader()
        layer_list, width, height, layer_count, color_mode = info_loader.load_psd_info(psd_file)
        
        print(f"      PSD Info: {width}x{height}, {layer_count} layers, {color_mode}")
        print(f"      Layer list:\n{layer_list}")
        
        # Test PSD Layer Loader
        if layer_count > 0:
            print("    Testing PSD Layer Loader...")
            layer_loader = APZmediaPSDLayerLoader()
            
            # Test loading first layer
            image_tensor, mask_tensor, layer_name, total_layers = layer_loader.load_psd_layer(
                psd_file=psd_file,
                layer_index=0,
                load_mask="true"
            )
            
            print(f"      Loaded layer '{layer_name}' (index 0 of {total_layers})")
            print(f"      Image tensor shape: {image_tensor.shape}")
            print(f"      Mask tensor shape: {mask_tensor.shape}")
        
        print("  ComfyUI loader node tests passed!")
        return True
        
    except Exception as e:
        print(f"  Error testing loader nodes: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("Testing PSD Layer Loader")
    print("=" * 60)
    
    # Test 1: Utility functions
    print("\n1. Testing utility functions...")
    if not test_psd_loader_utilities():
        print("  ✗ Utility function tests failed")
        return False
    print("  ✓ Utility function tests passed")
    
    # Test 2: PSD loading
    print("\n2. Testing PSD file loading...")
    if not test_psd_loading():
        print("  ✗ PSD loading tests failed")
        return False
    print("  ✓ PSD loading tests passed")
    
    # Test 3: ComfyUI nodes
    print("\n3. Testing ComfyUI loader nodes...")
    if not test_loader_nodes():
        print("  ✗ ComfyUI loader node tests failed")
        return False
    print("  ✓ ComfyUI loader node tests passed")
    
    print("\n" + "=" * 60)
    print("All PSD loader tests passed! The PSD loader nodes are working correctly.")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
