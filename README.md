# ComfyUI-APZmedia-PSDtools

**ComfyUI-APZmedia-PSDtools** is a collection of custom nodes designed for use with ComfyUI. These nodes provide functionality for saving images as layers in PSD files with mask support, enabling seamless integration between ComfyUI workflows and Adobe Photoshop.

## Overview

ComfyUI-APZmedia-PSDtools includes custom nodes for:

- **APZmedia PSD Layer Saver**: A node for saving multiple images as layers in a PSD file with optional masks
- **APZmedia PSD Layer Saver Advanced**: An enhanced version with background layer support and advanced layer options
- **APZmedia PSD Layer Saver (8 Layers)**: A specialized node for exactly 8 layers with individual inputs for each layer
- **APZmedia PSD Layer Saver (8 Layers Advanced)**: Advanced version of the 8-layer node with offset support

## Features

### Core Functionality
- **Multi-Layer PSD Creation**: Save multiple images as separate layers in a single PSD file
- **Mask Support**: Apply masks to individual layers for precise control
- **Layer Naming**: Custom names for each layer
- **Opacity Control**: Set individual opacity for each layer (0-255)
- **Blend Modes**: Support for various blend modes (normal, multiply, screen, overlay, etc.)
- **Color Mode Support**: RGB, CMYK, and Grayscale color modes

### Advanced Features
- **Background Layer**: Optional background layer with custom color and opacity
- **Layer Offsets**: Position layers with custom X,Y offsets
- **Automatic Dimension Validation**: Ensures all layers have compatible dimensions
- **Error Handling**: Comprehensive error handling with detailed feedback
- **Batch Processing**: Process multiple images and masks in a single operation

## Installation

### Automatic Installation (Recommended)

1. **Install via pip** (dependencies will be installed automatically):
   ```bash
   pip install -e .
   ```

2. **Or use the installation script:**
   ```bash
   python install_dependencies.py
   ```

3. **Or copy to ComfyUI custom nodes directory:**
   - Copy this repository to `ComfyUI/custom_nodes/APZmedia-ComfyUI-PSDtools/`
   - Run `pip install -e .` from the extension directory to install dependencies
   - Restart ComfyUI

### Manual Installation (if automatic fails)

If the automatic dependency installation doesn't work, you can install dependencies manually:

**Standard installation:**
```bash
pip install pytoshop>=0.1.0 Pillow>=8.0.0 torch>=1.7.0 numpy>=1.19.0
```

**If you encounter permission issues, use the --user flag:**
```bash
pip install --user pytoshop>=0.1.0 Pillow>=8.0.0 torch>=1.7.0 numpy>=1.19.0
```

### Verify Installation

After installation, you should see the PSD nodes in the `image/psd` category:
- APZmedia PSD Layer Saver
- APZmedia PSD Layer Saver Advanced  
- APZmedia PSD Layer Saver (8 Layers)
- APZmedia PSD Layer Saver (8 Layers Advanced)

### Troubleshooting

If nodes don't appear, check the ComfyUI console for error messages. See [INSTALL.md](INSTALL.md) for detailed troubleshooting.

## Node Reference

### APZmedia PSD Layer Saver

**Category**: `image/psd`

**Inputs**:
- **images** (IMAGE): Batch of images to save as layers
- **layer_names** (STRING): Newline-separated list of layer names
- **output_path** (STRING): Path where to save the PSD file
- **color_mode** (COMBO): Color mode for the PSD file (rgb, cmyk, grayscale)
- **masks** (MASK, optional): Batch of masks to apply to layers
- **opacities** (STRING, optional): Newline-separated list of opacity values (0-255)
- **blend_modes** (STRING, optional): Newline-separated list of blend mode names
- **background_color** (STRING, optional): Hex color for background (default: #FFFFFF)

**Outputs**:
- **output_path** (STRING): Path where the PSD file was saved
- **success** (BOOLEAN): Whether the operation was successful

### APZmedia PSD Layer Saver Advanced

**Category**: `image/psd`

**Inputs**:
- **images** (IMAGE): Batch of images to save as layers
- **layer_names** (STRING): Newline-separated list of layer names
- **output_path** (STRING): Path where to save the PSD file
- **color_mode** (COMBO): Color mode for the PSD file (rgb, cmyk, grayscale)
- **create_background_layer** (COMBO): Whether to create a background layer (true/false)
- **masks** (MASK, optional): Batch of masks to apply to layers
- **opacities** (STRING, optional): Newline-separated list of opacity values (0-255)
- **blend_modes** (STRING, optional): Newline-separated list of blend mode names
- **background_color** (STRING, optional): Hex color for background (default: #FFFFFF)
- **background_opacity** (INT, optional): Opacity for background layer (0-255)
- **layer_offsets** (STRING, optional): Newline-separated list of "x,y" offsets

**Outputs**:
- **output_path** (STRING): Path where the PSD file was saved
- **success** (BOOLEAN): Whether the operation was successful
- **layer_count** (INT): Number of layers created in the PSD file

### APZmedia PSD Layer Saver (8 Layers)

**Category**: `image/psd`

**Inputs**:
- **image_1** through **image_8** (IMAGE): Individual images for each layer
- **layer_name_1** through **layer_name_8** (STRING): Individual layer names
- **psd_filename** (STRING): Name of the PSD file to create
- **color_mode** (COMBO): Color mode for the PSD file (rgb, cmyk, grayscale)
- **mask_1** through **mask_8** (MASK, optional): Individual masks for each layer
- **opacity_1** through **opacity_8** (INT, optional): Individual opacity values (0-255)
- **blend_mode_1** through **blend_mode_8** (COMBO, optional): Individual blend modes
- **create_background_layer** (COMBO, optional): Whether to create a background layer (true/false)
- **background_color** (STRING, optional): Hex color for background (default: #FFFFFF)
- **background_opacity** (INT, optional): Opacity for background layer (0-255)

**Outputs**:
- **output_path** (STRING): Path where the PSD file was saved
- **success** (BOOLEAN): Whether the operation was successful
- **layer_count** (INT): Number of layers created in the PSD file

### APZmedia PSD Layer Saver (8 Layers Advanced)

**Category**: `image/psd`

**Inputs**:
- **image_1** through **image_8** (IMAGE): Individual images for each layer
- **layer_name_1** through **layer_name_8** (STRING): Individual layer names
- **psd_filename** (STRING): Name of the PSD file to create
- **color_mode** (COMBO): Color mode for the PSD file (rgb, cmyk, grayscale)
- **create_background_layer** (COMBO): Whether to create a background layer (true/false)
- **mask_1** through **mask_8** (MASK, optional): Individual masks for each layer
- **opacity_1** through **opacity_8** (INT, optional): Individual opacity values (0-255)
- **blend_mode_1** through **blend_mode_8** (COMBO, optional): Individual blend modes
- **background_color** (STRING, optional): Hex color for background (default: #FFFFFF)
- **background_opacity** (INT, optional): Opacity for background layer (0-255)
- **offset_x_1** through **offset_x_8** (INT, optional): Individual X offsets for layers
- **offset_y_1** through **offset_y_8** (INT, optional): Individual Y offsets for layers

**Outputs**:
- **output_path** (STRING): Path where the PSD file was saved
- **success** (BOOLEAN): Whether the operation was successful
- **layer_count** (INT): Number of layers created in the PSD file

## Usage Examples

### Basic Usage

1. **Load Images**: Use ComfyUI's image loading nodes to load your images
2. **Connect to PSD Layer Saver**: Connect the images to the `images` input
3. **Set Layer Names**: Enter layer names, one per line:
   ```
   Background
   Foreground
   Overlay
   ```
4. **Set Output Path**: Specify where to save the PSD file (e.g., `./output.psd`)
5. **Run**: Execute the workflow to create the PSD file

### Advanced Usage with Masks

1. **Load Images and Masks**: Load both images and corresponding masks
2. **Connect to Advanced Saver**: Use the Advanced node for more control
3. **Configure Layer Properties**:
   - Layer names: `Background\nCharacter\nEffects`
   - Opacities: `255\n200\n150`
   - Blend modes: `normal\nmultiply\noverlay`
4. **Enable Background**: Set `create_background_layer` to `true`
5. **Set Background Color**: Use hex color like `#FF0000` for red background

### 8-Layer Node Usage

The 8-layer nodes are perfect when you have exactly 8 images to save as layers:

1. **Load 8 Images**: Use ComfyUI's image loading nodes to load your 8 images
2. **Connect to 8-Layer Saver**: Connect each image to the corresponding `image_1` through `image_8` inputs
3. **Set Layer Names**: Enter individual layer names:
   - `layer_name_1`: "Background"
   - `layer_name_2`: "Character"
   - `layer_name_3`: "Hair"
   - `layer_name_4`: "Clothing"
   - `layer_name_5`: "Accessories"
   - `layer_name_6`: "Effects"
   - `layer_name_7`: "Lighting"
   - `layer_name_8`: "Overlay"
4. **Set PSD Filename**: Enter the desired filename (e.g., `character_composition.psd`)
5. **Add Masks (Optional)**: Connect masks to `mask_1` through `mask_8` if needed
6. **Configure Properties**: Set individual opacities and blend modes for each layer
7. **Run**: Execute the workflow to create the PSD file

### Layer Names Format

Enter layer names separated by newlines:
```
Background Layer
Character
Hair
Clothing
Accessories
```

### Opacity Values Format

Enter opacity values (0-255) separated by newlines:
```
255
200
150
100
50
```

### Blend Modes Format

Enter blend mode names separated by newlines:
```
normal
multiply
screen
overlay
soft_light
```

### Layer Offsets Format

Enter X,Y coordinates separated by newlines:
```
0,0
10,20
-5,15
0,0
```

## Supported Blend Modes

- `normal` - Normal blending
- `multiply` - Multiply blending
- `screen` - Screen blending
- `overlay` - Overlay blending
- `soft_light` - Soft light blending
- `hard_light` - Hard light blending
- `color_dodge` - Color dodge blending
- `color_burn` - Color burn blending
- `darken` - Darken blending
- `lighten` - Lighten blending
- `difference` - Difference blending
- `exclusion` - Exclusion blending

## Color Modes

- **RGB**: Standard RGB color mode (recommended for most use cases)
- **CMYK**: CMYK color mode for print workflows
- **Grayscale**: Grayscale color mode for monochrome images

## Mask Handling

The nodes automatically handle various mask formats:
- **Tensor Masks**: ComfyUI MASK input type
- **Grayscale Images**: Automatically converted to masks
- **Alpha Channels**: Extracted from RGBA images
- **Normalization**: Masks are automatically normalized to 0-255 range

## Error Handling

The nodes include comprehensive error handling:
- **Dimension Validation**: Ensures all layers have compatible dimensions
- **File Path Validation**: Checks output directory and creates if needed
- **Mask Processing**: Handles various mask formats gracefully
- **Fallback Values**: Uses sensible defaults when optional inputs are missing

## Troubleshooting

### Common Issues

#### "Failed to save PSD file"
- **Check Output Path**: Ensure the output directory exists and is writable
- **Check Permissions**: Verify write permissions for the output location
- **Check Disk Space**: Ensure sufficient disk space for the PSD file

#### "Layer dimensions don't match"
- **Resize Images**: Use ComfyUI's resize nodes to make all images the same size
- **Check Image Formats**: Ensure all images have the same dimensions

#### "Mask processing error"
- **Check Mask Format**: Ensure masks are in the correct format (grayscale)
- **Check Mask Dimensions**: Masks should match image dimensions

### Console Output

The nodes provide detailed console output for debugging:
```
APZmediaPSDLayerSaver initialized
Successfully saved PSD file with 3 layers to: ./output.psd
```

## Technical Details

### Dependencies
- **pytoshop**: Core PSD file creation library
- **Pillow**: Image processing and format support
- **torch**: Tensor operations and ComfyUI integration
- **numpy**: Numerical operations and array handling

### File Format Support
- **Input**: ComfyUI IMAGE and MASK tensors
- **Output**: Adobe Photoshop PSD files
- **Compatibility**: Compatible with Photoshop CS6 and later

### Performance Considerations
- **Memory Usage**: Large images may require significant memory
- **Processing Time**: Complex PSD files with many layers may take time to create
- **File Size**: PSD files can be large, especially with high-resolution images

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 0.2.0
- Complete refactor from text overlay functionality to PSD layer saving
- Added support for masks and layer properties
- Implemented advanced layer options
- Added comprehensive error handling
- Updated dependencies to include pytoshop

### Version 0.1.0
- Initial release with text overlay functionality (deprecated)

## Support

For support, please open an issue on the GitHub repository or contact the maintainer.

## Acknowledgments

- **pytoshop**: For providing the PSD file creation capabilities
- **ComfyUI Community**: For the excellent framework and ecosystem
- **Adobe**: For the PSD file format specification

