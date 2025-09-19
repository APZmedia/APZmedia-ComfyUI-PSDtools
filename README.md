# ComfyUI-APZmedia-PSDtools

**ComfyUI-APZmedia-PSDtools** is a streamlined collection of custom nodes designed for use with ComfyUI. These nodes provide functionality for saving and loading images as layers in PSD files with mask support, enabling seamless integration between ComfyUI workflows and Adobe Photoshop.

## Overview

ComfyUI-APZmedia-PSDtools includes two essential nodes:

- **APZmedia PSD Multilayer Saver**: A flexible node for saving 1-10 images as layers in a PSD file with optional masks
- **APZmedia PSD Layer Loader**: A node for loading PSD files and extracting specific layers with their masks

## Features

### Core Functionality
- **Flexible Multi-Layer PSD Creation**: Save 1-10 images as separate layers in a single PSD file
- **Optional Layer Inputs**: All layers are optional - connect only what you need
- **Mask Support**: Apply masks to individual layers for precise control
- **Layer Naming**: Custom names for each layer
- **PSD Loading**: Load existing PSD files and extract specific layers
- **Layer Information**: Get layer names, counts, and metadata from PSD files

### Advanced Features
- **Smart Error Handling**: Clear error messages when no layers are provided
- **Automatic Dependency Management**: Dependencies are installed automatically when needed
- **Robust Import System**: Fallback import methods ensure nodes work in all environments
- **Smart Installation**: Detects missing packages and installs them without user intervention
- **Installation Feedback**: Clear console output showing installation progress and status
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux

## Installation

### Automatic Dependency Installation (Recommended)

**🎉 NEW: Dependencies are now installed automatically!**

The extension now includes automatic dependency installation that runs when ComfyUI loads the extension. No manual installation required!

1. **Copy to ComfyUI custom nodes directory:**
   ```
   ComfyUI/custom_nodes/APZmedia-ComfyUI-PSDtools/
   ```

2. **Restart ComfyUI**

The extension will automatically:
- ✅ Check for missing dependencies
- ✅ Install psd-tools for PSD file operations
- ✅ Install other required packages (Pillow, torch, numpy)
- ✅ Provide clear feedback on installation progress
- ✅ Verify all dependencies are working

--- Automatic Dependency Installation ---
[INFO] Checking and installing dependencies automatically...
[INFO] Installing pytoshop>=0.1.0...
[SUCCESS] Successfully installed pytoshop>=0.1.0
[SUCCESS] 🎉 All dependencies are ready!
✅ Automatic dependency installation is enabled
```
**What you'll see in the console:**
```
APZmedia PSD Tools Extension - Starting Load Process
--- Automatic Dependency Installation ---
[INFO] Checking and installing dependencies automatically...
[INFO] Installing psd-tools>=1.9.0...
[SUCCESS] Successfully installed psd-tools>=1.9.0
[SUCCESS] 🎉 All dependencies are ready!
✅ Automatic dependency installation is enabled
```
============================================================
--- Automatic Dependency Installation ---
[INFO] Checking and installing dependencies automatically...
[INFO] Installing pytoshop>=0.1.0...
[SUCCESS] Successfully installed pytoshop>=0.1.0
[SUCCESS] 🎉 All dependencies are ready!
✅ Automatic dependency installation is enabled
```

### Manual Installation (Fallback)

If automatic installation fails, you can still install dependencies manually:

1. **Install dependencies in ComfyUI environment:**
   ```bash
   cd ComfyUI/custom_nodes/APZmedia-ComfyUI-PSDtools/
   python install_for_comfyui.py
   ```

2. **Restart ComfyUI**

The manual installation script will:
- Install psd-tools for PSD file operations
- Install other required packages (Pillow, torch, numpy)
- Provide clear feedback on success/failure

**Note:** This approach is based on the proven method from [ComfyUI-Layers](https://github.com/alessandrozonta/ComfyUI-Layers).

### Alternative: Install from ComfyUI Directory

If the above doesn't work, try installing from the ComfyUI root directory:

1. **Navigate to ComfyUI root:**
   ```bash
   cd ComfyUI/
   ```

2. **Run the ComfyUI-specific installer:**
   ```bash
   python custom_nodes/APZmedia-ComfyUI-PSDtools/install_for_comfyui.py
   ```

3. **Restart ComfyUI**

### Manual Installation (if automatic fails)

If the automatic dependency installation doesn't work, you can install dependencies manually:

**Standard installation:**
```bash
pip install psd-tools>=1.9.0
pip install Pillow>=8.0.0 torch>=1.7.0 numpy>=1.19.0
```

**If you encounter permission issues, use the --user flag:**
```bash
pip install --user psd-tools>=1.9.0
pip install --user Pillow>=8.0.0 torch>=1.7.0 numpy>=1.19.0
```

### Verify Installation

After installation, you should see the PSD nodes in the `image/psd` category:
- **APZmedia PSD Multilayer Saver**: For saving multiple images as PSD layers
- **APZmedia PSD Layer Loader**: For loading PSD files and extracting layers

### Troubleshooting

#### Automatic Installation Issues

If automatic dependency installation fails:

1. **Check Console Output**: Look for error messages in the ComfyUI console
2. **Try Manual Installation**: Use the manual installation scripts as fallback
3. **Check Permissions**: Ensure ComfyUI has permission to install packages
4. **Check Internet Connection**: Automatic installation requires internet access
5. **Restart ComfyUI**: Sometimes a restart helps with dependency loading

#### Common Issues

**"Auto-installer not available"**
- This is normal if the auto_installer.py file is missing
- Use manual installation scripts instead

**"Dependencies not available for node"**
- Automatic installation may have failed
- Check console for specific error messages
- Try manual installation

**"Failed to install [package]"**
- Check internet connection
- Try manual installation with different flags
- Check ComfyUI Python environment

If nodes don't appear, check the ComfyUI console for error messages. See [INSTALL.md](INSTALL.md) for detailed troubleshooting.

## Node Reference

### APZmedia PSD Multilayer Saver

**Category**: `image/psd`

**Inputs** (All Optional):
- **output_dir** (STRING, optional): Directory to save the PSD file (default: "./output")
- **filename_prefix** (STRING, optional): Prefix for the filename (default: "output")
- **layer1** through **layer10** (IMAGE, optional): Individual images for each layer
- **mask1** through **mask10** (MASK, optional): Individual masks for each layer
- **layer_name1** through **layer_name10** (STRING, optional): Individual layer names

**Outputs**:
- **None** (OUTPUT_NODE): This is an output node that writes to disk

**Features**:
- **Flexible Input**: Connect 1-10 layers as needed
- **Optional Masks**: Each layer can have an optional mask
- **Custom Names**: Each layer can have a custom name
- **Error Handling**: Clear error message if no layers are provided
- **Automatic File Naming**: Generates unique filenames to avoid overwrites

### APZmedia PSD Layer Loader

**Category**: `image/psd`

**Inputs**:
- **psd_file** (STRING): Path to the PSD file to load
- **layer_index** (INT): Index of the layer to extract (0-based)
- **load_mask** (COMBO, optional): Whether to load the mask ("true" or "false", default: "true")
- **overwrite_mode** (COMBO, optional): Placeholder for consistency (default: "false")

**Outputs**:
- **image** (IMAGE): The extracted layer as a tensor
- **mask** (MASK): The layer's mask as a tensor
- **layer_name** (STRING): Name of the extracted layer
- **layer_count** (INT): Total number of layers in the PSD file

**Features**:
- **Layer Selection**: Extract specific layers by index
- **Mask Support**: Load layer masks when available
- **Layer Information**: Get layer names and total count
- **Error Handling**: Graceful handling of missing layers or files

## Usage Examples

### Basic Multilayer Saving

1. **Load Images**: Use ComfyUI's image loading nodes to load your images
2. **Connect to Multilayer Saver**: Connect images to `layer1`, `layer2`, etc.
3. **Set Layer Names**: Enter custom names for each layer:
   - `layer_name1`: "Background"
   - `layer_name2`: "Character"
   - `layer_name3`: "Effects"
4. **Add Masks (Optional)**: Connect masks to `mask1`, `mask2`, etc.
5. **Set Output Directory**: Specify where to save (default: "./output")
6. **Set Filename Prefix**: Enter a prefix for the filename (default: "output")
7. **Run**: Execute the workflow to create the PSD file

### Loading PSD Files

1. **Set PSD File Path**: Enter the path to your PSD file
2. **Select Layer Index**: Choose which layer to extract (0-based index)
3. **Load Mask**: Choose whether to load the layer's mask
4. **Connect Outputs**: Use the extracted image and mask in your workflow
5. **Get Layer Info**: Use the layer name and count for further processing

### Flexible Layer Usage

The multilayer saver is designed to be flexible:

- **1 Layer**: Connect only `layer1` and `layer_name1`
- **3 Layers**: Connect `layer1`, `layer2`, `layer3` with their names
- **5 Layers**: Connect `layer1` through `layer5` as needed
- **10 Layers**: Use all available layer inputs

**Error Handling**: If no layers are connected, you'll see: "No layers or masks are being saved"

### Layer Names

Enter custom names for each layer:
- `layer_name1`: "Background"
- `layer_name2`: "Character" 
- `layer_name3`: "Effects"
- `layer_name4`: "Lighting"
- etc.

### Mask Handling

The nodes automatically handle various mask formats:
- **Tensor Masks**: ComfyUI MASK input type
- **Grayscale Images**: Automatically converted to masks
- **Alpha Channels**: Extracted from RGBA images
- **Normalization**: Masks are automatically normalized to 0-255 range

## Error Handling

The nodes include comprehensive error handling:
- **No Layers Error**: Clear message "No layers or masks are being saved" when no layers are provided
- **File Path Validation**: Checks output directory and creates if needed
- **Mask Processing**: Handles various mask formats gracefully
- **Layer Index Validation**: Ensures layer index is within valid range
- **Import Fallbacks**: Robust import system with multiple fallback methods

## Troubleshooting

### Common Issues

#### "No layers or masks are being saved"
- **Connect Layers**: Make sure at least one layer input is connected
- **Check Connections**: Verify that images are properly connected to layer inputs

#### "Failed to save PSD file"
- **Check Output Path**: Ensure the output directory exists and is writable
- **Check Permissions**: Verify write permissions for the output location
- **Check Disk Space**: Ensure sufficient disk space for the PSD file

#### "Layer index out of range"
- **Check Layer Count**: Verify the layer index is within the valid range (0 to layer_count-1)
- **Use Layer Count Output**: The loader provides the total layer count for reference

#### "PSD loader utilities not available"
- **Check Dependencies**: Ensure psd-tools is properly installed
- **Restart ComfyUI**: Sometimes a restart helps with dependency loading

### Console Output

The nodes provide detailed console output for debugging:
```
APZmediaPSDLayerSaverMultilayer initialized
✅ Successfully imported PSD tools utility functions
Processing 3 layers for PSD creation
Successfully saved PSD file with 3 layers to: ./output/output_001.psd
```

## Technical Details

### Dependencies
- **psd-tools**: Primary library for PSD file operations (reading and writing)
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

### Version 0.2.1
- **NEW: Simplified Extension**: Streamlined to only include essential nodes
- **APZmedia PSD Multilayer Saver**: Flexible node for saving 1-10 layers with optional inputs
- **APZmedia PSD Layer Loader**: Node for loading PSD files and extracting layers
- **Optional Layer Inputs**: All layer inputs are optional for maximum flexibility
- **Smart Error Handling**: Clear error message when no layers are provided
- **Robust Import System**: Fallback import methods ensure nodes work in all environments
- **Automatic Dependency Installation**: Dependencies are installed automatically when the extension loads
- **Enhanced Error Handling**: Better error messages and troubleshooting guidance

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

- **psd-tools**: For providing the PSD file creation and reading capabilities
- **ComfyUI Community**: For the excellent framework and ecosystem
- **Adobe**: For the PSD file format specification
