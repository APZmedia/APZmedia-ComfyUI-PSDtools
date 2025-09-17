#!/usr/bin/env python3
"""
Create a template PSD with 8 empty layers for use with psd-tools
"""

import os
from PIL import Image
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer

def create_template_psd():
    """Create a template PSD with 8 empty layers"""
    
    # Create a 512x512 transparent image for each layer
    transparent_image = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    
    # Create a new PSD
    psd = PSDImage.new((512, 512), color_mode='RGB')
    
    # Add 8 empty layers with default names
    layer_names = [
        "Layer_1",
        "Layer_2", 
        "Layer_3",
        "Layer_4",
        "Layer_5",
        "Layer_6",
        "Layer_7",
        "Layer_8"
    ]
    
    for i, name in enumerate(layer_names):
        # Create a pixel layer from the transparent image
        layer = PixelLayer.frompil(transparent_image, name=name)
        
        # Add the layer to the PSD
        psd.append(layer)
        print(f"Added layer {i+1}: {name}")
    
    # Save the template
    template_path = os.path.join("templates", "8layer_template.psd")
    psd.save(template_path)
    print(f"Template PSD created: {template_path}")
    
    return template_path

if __name__ == "__main__":
    create_template_psd()
