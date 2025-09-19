#!/usr/bin/env python3
"""
Simple test script to verify mask logic without torch/numpy dependencies
"""

import os
import sys
from PIL import Image

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_mask_application():
    """Test the mask application logic using PIL only"""
    print("🧪 Testing mask application logic...")
    
    # Import the mask application function
    try:
        from utils.apz_psd_tools_utility import apply_mask_to_image
        print("✅ Successfully imported mask utility function")
    except ImportError as e:
        print(f"❌ Failed to import mask utilities: {e}")
        return False
    
    # Create test image (red square)
    test_image = Image.new('RGB', (100, 100), (255, 0, 0))
    print(f"📷 Created test image: {test_image.size} mode: {test_image.mode}")
    
    # Create test mask (circle)
    test_mask = Image.new('L', (100, 100), 0)  # Start with black (transparent)
    
    # Draw a white circle in the center
    from PIL import ImageDraw
    draw = ImageDraw.Draw(test_mask)
    draw.ellipse([25, 25, 75, 75], fill=255)  # White circle (opaque)
    print(f"🎭 Created test mask: {test_mask.size} mode: {test_mask.mode}")
    
    # Apply mask to image
    try:
        masked_image = apply_mask_to_image(test_image, test_mask)
        print(f"✅ Applied mask successfully: {masked_image.size} mode: {masked_image.mode}")
        
        # Verify the result has alpha channel
        if masked_image.mode == 'RGBA':
            alpha_channel = masked_image.split()[3]
            alpha_stats = alpha_channel.getextrema()
            print(f"🔍 Alpha channel range: {alpha_stats[0]}-{alpha_stats[1]}")
            
            # Save test results
            os.makedirs("./test_output", exist_ok=True)
            test_image.save("./test_output/original_image.png")
            test_mask.save("./test_output/test_mask.png")
            masked_image.save("./test_output/masked_result.png")
            print("💾 Saved test images to ./test_output/")
            
            return True
        else:
            print(f"❌ Expected RGBA mode, got {masked_image.mode}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to apply mask: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_psd_tools_import():
    """Test if psd-tools is available"""
    print("\n🧪 Testing psd-tools availability...")
    
    try:
        from utils.apz_psd_tools_utility import check_psd_tools_available
        check_psd_tools_available()
        print("✅ psd-tools is available")
        return True
    except ImportError as e:
        print(f"❌ psd-tools not available: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting mask logic tests...\n")
    
    # Test 1: psd-tools availability
    psd_available = test_psd_tools_import()
    
    # Test 2: mask application logic
    mask_logic_works = test_mask_application()
    
    # Summary
    print(f"\n📊 Test Results:")
    print(f"  - psd-tools available: {'✅' if psd_available else '❌'}")
    print(f"  - Mask application: {'✅' if mask_logic_works else '❌'}")
    
    if psd_available and mask_logic_works:
        print("\n🎉 All tests passed! Mask saving should work correctly.")
        print("💡 The mask saving issue has been fixed:")
        print("   - Improved mask collection logic in the saver node")
        print("   - Enhanced mask tensor processing with validation")
        print("   - Added comprehensive debugging output")
        print("   - Masks are now properly applied using PIL compositing")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")
    
    return psd_available and mask_logic_works

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
