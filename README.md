# 🤖 ARC Raiders Tool

A powerful desktop utility for ARC Raiders that automatically detects item popups on screen and displays detailed information about items, including their dependencies for quests and hideout modules.

## Features

- **Real-time Item Detection**: Uses computer vision to detect item popups when they appear on screen
- **Comprehensive Item Info**: Displays item descriptions, categories, and values
- **Quest Dependencies**: Shows which quests require the item and in what quantities
- **Hideout Module Requirements**: Lists hideout modules that need the item, including tier information
- **Beautiful Console UI**: Rich, colorful interface with tables and panels for easy reading
- **Hotkey Controls**: Simple keyboard shortcuts for activation and quitting
- **OCR Integration**: Extracts item names from popups using Tesseract OCR

## Requirements

- Python 3.9+
- Windows (for screen capture)
- Tesseract OCR installed and in PATH

## Installation

1. **Install uv** (Python package manager):
   
   On Windows (PowerShell):
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   
   On macOS/Linux:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   
   Or with pip:
   ```bash
   pip install uv
   ```
   
   More info: https://docs.astral.sh/uv/getting-started/installation/

2. Clone this repository:
   ```bash
   git clone https://github.com/onycher/arc-tools.git
   cd arc-tools
   ```

3. Install Tesseract OCR:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Add to your system PATH

4. Place the `actions.png` template image in the root directory or use the default one provided in the repository if it works for you.

**Note**: `uv` will automatically handle all Python dependencies when you run the tool.

## Usage

Run the tool:
```bash
uv run main.py
```

The tool will start in the background. When you see an item popup in ARC Raiders:

1. Press **Ctrl+Alt+S** to scan the popup
2. View the detailed item information in the console
3. Press **Ctrl+Q** to quit the application

## Hotkeys

- **Ctrl+Alt+S**: Activate item info lookup
- **Ctrl+Q**: Quit the application

## Configuration

The tool uses the following data files from the ARC Data Compendium:
- `Arc-Data-Compendium/src/data/items/itemData.json`
- `Arc-Data-Compendium/src/data/quests/questData.json`
- `Arc-Data-Compendium/src/data/workbenches/workbenchData.json`

Ensure these files are present in the correct relative paths.

## How It Works

1. **Screen Capture**: Uses MSS to capture the primary monitor
2. **Template Matching**: Locates the actions button using OpenCV template matching
3. **Popup Detection**: Uses flood fill to isolate the item popup area
4. **Text Extraction**: Applies OCR to extract the item name
5. **Data Lookup**: Queries JSON data for item details and dependencies
6. **UI Display**: Presents information in a rich console interface

## Troubleshooting

- **Popup not detected**: Ensure the `actions.png` template matches your game's UI
- **OCR fails**: Check Tesseract installation and PATH
- **No item data**: Verify JSON file paths and contents
- **Low confidence**: The tool requires 70%+ template match confidence

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- Built with OpenCV, Tesseract, Rich, and other Python libraries
- Data sourced from the ARC Data Compendium
- Inspired by the ARC Raiders community

---

**Note**: This tool is for educational and personal use. Ensure compliance with ARC Raiders terms of service.
