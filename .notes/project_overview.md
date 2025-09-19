# ComfyUI APZmedia PSD Tools - Project Overview

## Project Description
ComfyUI APZmedia PSD Tools is a streamlined collection of custom nodes for ComfyUI that provides functionality for saving and loading images as layers in PSD files with mask support. This enables seamless integration between ComfyUI workflows and Adobe Photoshop.

## Core Functionality
- **PSD Layer Saving**: Save 1-10 images as separate layers in a single PSD file
- **PSD Layer Loading**: Load existing PSD files and extract specific layers with masks
- **Mask Support**: Apply masks to individual layers for precise control
- **Automatic Dependency Management**: Dependencies are installed automatically when needed

## Architecture

### Nodes
1. **APZmedia PSD Multilayer Saver** (`apzPSDLayerSaverMultilayer.py`)
   - Saves up to 10 images as layers in a PSD file
   - Optional masks for each layer
   - Flexible input system (all layers are optional)
   - Custom layer naming

2. **APZmedia PSD Layer Loader** (`apzPSDLayerLoader.py`)
   - Loads PSD files and extracts specific layers
   - Returns image, mask, layer name, and layer count
   - Supports layer selection by index

### Utilities
- **apz_psd_tools_utility.py**: Core PSD creation and manipulation using psd-tools
- **apz_psd_loader_utility.py**: PSD loading and layer extraction utilities
- **auto_installer.py**: Automatic dependency installation system

### Dependencies
- **psd-tools**: Primary library for PSD file operations (reading and writing)
- **Pillow**: Image processing and format conversion
- **torch**: ComfyUI tensor operations
- **numpy**: Numerical operations

## Recent Changes (v0.2.1)
- **Removed pytoshop dependency**: Simplified to use only psd-tools for all operations
- **Simplified PSD creation**: Replaced complex manual PSD structure creation with PIL compositing
- **Improved mask handling**: Uses PIL to composite masks into images before PSD creation
- **Cleaner dependency management**: Removed unnecessary pytoshop references
- **Better error handling**: More consistent error reporting and fallback mechanisms

## Key Design Decisions
1. **psd-tools only**: Eliminated pytoshop dependency for simpler, more reliable operation
2. **PIL compositing for masks**: Instead of complex PSD mask structures, masks are applied using PIL
3. **Flexible layer inputs**: All layer inputs are optional to maximize usability
4. **Automatic dependency installation**: Reduces setup complexity for users
5. **Robust import system**: Multiple fallback methods ensure compatibility across environments

## File Structure
```
APZmedia-ComfyUI-PSDtools/
├── __init__.py                 # Extension initialization and node registration
├── auto_installer.py           # Automatic dependency installation
├── requirements.txt            # Dependency specifications
├── nodes/
│   ├── apzPSDLayerSaverMultilayer.py    # PSD saving node
│   └── apzPSDLayerLoader.py             # PSD loading node
├── utils/
│   ├── apz_psd_tools_utility.py         # PSD creation utilities
│   └── apz_psd_loader_utility.py        # PSD loading utilities
└── .notes/                     # Project documentation
```

## Integration Points
- **ComfyUI**: Integrates as custom nodes in the `image/psd` category
- **Adobe Photoshop**: Creates PSD files compatible with Photoshop CS6+
- **PIL/Pillow**: Uses for image processing and mask compositing
- **psd-tools**: Primary library for PSD file operations
