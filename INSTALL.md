# Installation Guide for ComfyUI-APZmedia-PSDtools

## Automatic Installation (Recommended)

The extension includes a complete setup script that handles everything automatically.

### Complete Setup (Recommended)

1. **Copy the extension to ComfyUI:**
   ```
   ComfyUI/custom_nodes/APZmedia-ComfyUI-PSDtools/
   ```

2. **Run the complete setup script:**
   ```bash
   cd ComfyUI/custom_nodes/APZmedia-ComfyUI-PSDtools/
   python setup_extension.py
   ```

3. **Restart ComfyUI**

The setup script will:
- ✅ Install all required dependencies (pytoshop, Pillow, torch, numpy)
- ✅ Validate that all packages are properly installed
- ✅ Test the PSD functionality
- ✅ Provide clear feedback on success/failure
- ✅ Handle permission issues automatically

### Alternative Methods

If the complete setup script doesn't work, you can try:

**Method 1: Direct pip installation**
```bash
cd ComfyUI/custom_nodes/APZmedia-ComfyUI-PSDtools/
pip install -e .
```

**Method 2: Individual dependency installation**
```bash
cd ComfyUI/custom_nodes/APZmedia-ComfyUI-PSDtools/
python install_dependencies.py
```

## Manual Installation (if automatic fails)

If the automatic installation doesn't work, you can install dependencies manually:

### Install Dependencies

**For ComfyUI with pip:**
```bash
pip install pytoshop>=0.1.0 Pillow>=8.0.0 torch>=1.7.0 numpy>=1.19.0
```

**If you encounter permission issues, use the --user flag:**
```bash
pip install --user pytoshop>=0.1.0 Pillow>=8.0.0 torch>=1.7.0 numpy>=1.19.0
```

**For ComfyUI with conda:**
```bash
conda install pytoshop pillow torch numpy
```

**For ComfyUI portable (Windows):**
```bash
# Navigate to your ComfyUI directory
cd C:\AI\ComfyUI_windows_portable\ComfyUI_windows_portable\ComfyUI

# Install using the Python executable in the ComfyUI directory
python -m pip install pytoshop>=0.1.0 Pillow>=8.0.0 torch>=1.7.0 numpy>=1.19.0
```

### 3. Verify Installation

After restarting ComfyUI, you should see the PSD nodes in the `image/psd` category:

- APZmedia PSD Layer Saver
- APZmedia PSD Layer Saver Advanced  
- APZmedia PSD Layer Saver (8 Layers)
- APZmedia PSD Layer Saver (8 Layers Advanced)

## Troubleshooting

### "ModuleNotFoundError: No module named 'pytoshop'"

This error means pytoshop is not installed. Follow the installation steps above.

### "Failed to import" errors

If you see import errors, make sure:
1. All dependencies are installed
2. The extension is in the correct directory
3. ComfyUI has been restarted after installation

### Nodes not appearing in ComfyUI

If the nodes don't appear:
1. Check the ComfyUI console for error messages
2. Verify the installation path is correct
3. Make sure all dependencies are installed
4. Restart ComfyUI completely

## Dependencies

- **pytoshop**: Core PSD file creation library
- **Pillow**: Image processing and format support  
- **torch**: Tensor operations and ComfyUI integration
- **numpy**: Numerical operations and array handling

## Support

If you continue to have issues, please check:
1. ComfyUI console output for detailed error messages
2. Python version compatibility (requires Python 3.7+)
3. All dependencies are properly installed
