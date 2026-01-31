![Alt text](main/GUI.png)

# PENPLOTTER PAINT SPLITTER

A Python GUI tool to split multi-color pen plotter drawings into segments with automatic paint reload paths. Perfect for creating paintings with pen plotters.

## What does it do?

This tool takes a multi-color SVG drawing and automatically inserts "bucket paths" (paint reload points) at regular intervals. Each color layer gets its own reload path, making it easy to create pen plotter paintings with real paint.

## Features

- ✅ Simple step-by-step interface
- ✅ Automatic splitting of long paths into paintable segments
- ✅ Supports multi-layer SVG files (one layer per color)
- ✅ Custom bucket path positioning
- ✅ Adjustable split distance

## Requirements

- **Python 3.7+** (Python 3.11 recommended)
- **vpype** (vector graphics pipeline tool)
- **tkinter** (usually included with Python)

## Installation

### 1. Install Python

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- OR install from Microsoft Store (search "Python 3.11")
- ✅ Check "Add Python to PATH" during installation

**Mac:**
```bash
brew install python
```

**Linux:**
```bash
sudo apt install python3 python3-pip
```

### 2. Install vpype

Open a terminal/command prompt and run:

```bash
pip install vpype
```

For detailed installation instructions, see the [vpype documentation](https://vpype.readthedocs.io/en/latest/install.html).

### 3. Download this tool

Clone or download this repository:
```bash
git clone https://github.com/yourusername/penplotter-paint-splitter.git
cd penplotter-paint-splitter
```

Or download the ZIP file and extract it.

## Configuration

### Finding your vpype path

Before running the tool, you need to configure the path to your vpype installation.

**Windows:**
1. Open Command Prompt (cmd) or PowerShell
2. Type: `where vpype`
3. Copy the full path shown (e.g., `C:\Users\YourName\AppData\Local\...\vpype.exe`)

**Mac/Linux:**
1. Open Terminal
2. Type: `which vpype`
3. Copy the full path shown (e.g., `/usr/local/bin/vpype`)

### Editing the configuration

1. Open `PENPLOTTER_PAINT_SPLITTER.py` in any text editor (Notepad, VS Code, etc.)
2. Find this line near the top:
   ```python
   VPYPE_CMD = r"C:\Users\PC\AppData\...\vpype.exe"
   ```
3. Replace it with your vpype path:
   ```python
   VPYPE_CMD = r"YOUR_VPYPE_PATH_HERE"
   ```
4. Save the file

**Example paths:**
- Windows (Microsoft Store Python): `C:\Users\YourName\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_xxxxx\LocalCache\local-packages\Python311\Scripts\vpype.exe`
- Windows (standard Python): `C:\Python311\Scripts\vpype.exe`
- Mac (Homebrew): `/opt/homebrew/bin/vpype`
- Linux: `/usr/local/bin/vpype`

## Usage

### 1. Launch the program

**Windows:**
- Double-click `PENPLOTTER_PAINT_SPLITTER.py`

**Mac/Linux:**
```bash
python3 PENPLOTTER_PAINT_SPLITTER.py
```

### 2. Prepare your files

You need two SVG files:

**Bucket Path SVG:**
- Same paper size and units (mm) as your drawing
- Contains a **single line/path** where your first paint color is located
- Example: a 30mm horizontal line at coordinates (25, 25)
- vpype will automatically duplicate this for each color layer

**Drawing SVG:**
- Same paper size and units (mm) as the bucket path
- Multi-color drawing with **each color on a separate layer**
- Layers should be named (e.g., "Layer 1", "Layer 2", etc.)

### 3. Follow the steps in the GUI

1. **STEP 1:** Make sure vpype is installed (link provided)
2. **STEP 2:** Load your bucket path SVG
3. **STEP 3:** Load your multi-color drawing SVG
4. **STEP 4:** Set the split distance (distance in mm between paint reloads)
5. **STEP 5:** Click SPLIT and choose where to save the output
6. **STEP 6:** Open the result in Inkscape and manually adjust each bucket path position to match your actual paint palette layout

### 4. Example workflow

1. Create a bucket path with a single 30mm line at (25, 25)
2. Load your 4-color drawing (4 layers)
3. Set split distance to 100mm
4. Click SPLIT → save as `my_drawing_PAINT.svg`
5. Open in Inkscape:
   - Move layer 1 bucket paths to paint position 1
   - Move layer 2 bucket paths to paint position 2 (e.g., 50mm below)
   - Move layer 3 bucket paths to paint position 3 (e.g., 100mm below)
   - Move layer 4 bucket paths to paint position 4 (e.g., 150mm below)
6. Plot!

## Troubleshooting

### "vpype command failed" error

- Make sure vpype is installed: `pip install vpype`
- Check that the VPYPE_CMD path in the code is correct
- Try running vpype manually in terminal to verify installation

### "File not found" error

- Make sure your SVG files exist
- Check that file paths don't contain special characters

### Window too small / content hidden

- The window is set to 700x900 pixels
- If your screen is smaller, you can scroll or maximize the window
- Or edit the code to change the window size in the `__init__` method

### Antivirus blocking (if using .exe version)

- This tool should be distributed as .py file, not .exe
- If someone creates an .exe, Windows Defender may flag it as suspicious
- Solution: use the .py file instead

## How it works

The tool uses vpype commands to:
1. Read your multi-color drawing and preserve all layers
2. Split each layer's paths into segments based on the split distance
3. Insert the bucket path before each segment
4. Output a new SVG with all the paint reload points included

The vpype command generated is:
```bash
vpype read -a stroke "drawing.svg" \
  forlayer \
    splitdist 100mm \
    forlayer \
      lmove %_lid% "%_lid*2%" \
      read -l "%_lid*2-1%" "bucket.svg" \
    end \
    lmove all %_lid% \
  end \
  write "output.svg"
```

## Tips

- **Split distance:** Shorter = more paint reloads = more consistent color, but slower
- **Bucket path:** Keep it simple - a single straight line works best
- **Units:** Always use millimeters (mm) for consistency
- **Paper size:** Bucket path and drawing must match exactly (e.g., both A3 or both A4)

## Credits

- Created for pen plotter painting workflows
- Uses [vpype](https://github.com/abey79/vpype) by @abey79
- Built with Python and tkinter

## License

MIT License - feel free to use, modify, and share!

## Contributing

Issues and pull requests welcome! This is a community tool for pen plotter artists.

## Support

If you have questions or issues:
1. Check the Troubleshooting section above
2. Open an issue on GitHub
3. Include your vpype version: `vpype --version`
4. Include your Python version: `python --version`

---

Happy plotting! 🎨🖌️
