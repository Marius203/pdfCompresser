# PDF Compressor

A Python console application that compresses PDF files using Ghostscript with various quality settings.

## Features

- **Multiple compression quality levels**: Low, Medium, High, and Maximum quality settings
- **Interactive console interface**: User-friendly menu-driven interface
- **Command-line interface**: Batch processing and automation support
- **File size reporting**: Shows original size, compressed size, and compression ratio
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Error handling**: Comprehensive error checking and user feedback

## Prerequisites

### 1. Python 3.6 or higher
Make sure Python is installed on your system.

### 2. Ghostscript
Ghostscript must be installed on your system:

**Windows:**
1. Download Ghostscript from: https://www.ghostscript.com/download/gsdnld.html
2. Install the appropriate version (32-bit or 64-bit)
3. The installer should add Ghostscript to your PATH automatically

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ghostscript
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install ghostscript
```

**macOS:**
```bash
brew install ghostscript
```

## Installation

1. Clone or download this repository
2. Navigate to the backend directory:
   ```bash
   cd pdfCompresser/backend
   ```
3. (Optional) Install any additional requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Interactive Mode

Run the script without arguments to start the interactive mode:

```bash
python pdf_compressor.py
```

This will launch a user-friendly console interface where you can:
- Browse and select PDF files
- Choose compression quality
- Specify output locations
- See compression results

### Command Line Mode

For automation and batch processing:

```bash
# Basic usage with default settings
python pdf_compressor.py input.pdf

# Specify output file and quality
python pdf_compressor.py input.pdf -o compressed.pdf -q low

# Use high quality compression
python pdf_compressor.py input.pdf --quality high
```

### Command Line Options

```
usage: pdf_compressor.py [-h] [-o OUTPUT] [-q {low,medium,high,max}] [-i] input

positional arguments:
  input                 Input PDF file path

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output PDF file path (default: input_compressed.pdf)
  -q {low,medium,high,max}, --quality {low,medium,high,max}
                        Compression quality (default: medium)
  -i, --interactive     Run in interactive mode
```

## Quality Settings

| Quality | Description | DPI | Use Case |
|---------|-------------|-----|----------|
| **low** | Smallest file size | 72 | Web viewing, email attachments |
| **medium** | Balanced quality/size | 150 | General purpose (default) |
| **high** | High quality | 300 | Printing, professional documents |
| **max** | Maximum quality | 300 | Archival, color preservation |

## Examples

### Interactive Mode Examples

```bash
# Start interactive mode
python pdf_compressor.py

# Example session:
Enter path to PDF file: "C:\Documents\large_document.pdf"
Enter output file path [large_document_compressed.pdf]: 
Choose quality (1-4 or name) [2]: 1
Proceed with compression? (y/n) [y]: y
```

### Command Line Examples

```bash
# Compress with default medium quality
python pdf_compressor.py document.pdf

# Compress with low quality for smallest file size
python pdf_compressor.py document.pdf -q low -o small_document.pdf

# High quality compression for printing
python pdf_compressor.py presentation.pdf --quality high --output print_ready.pdf

# Batch processing with PowerShell (Windows)
Get-ChildItem *.pdf | ForEach-Object { python pdf_compressor.py $_.Name -q medium }
```

## Features in Detail

### File Size Reporting
The application provides detailed information about compression results:
- Original file size
- Compressed file size
- Compression ratio percentage

### Error Handling
- Validates Ghostscript installation
- Checks file existence and permissions
- Provides clear error messages
- Handles interruption gracefully

### Cross-Platform Support
- Automatically detects Ghostscript installation
- Works with different Ghostscript executable names
- Handles path differences between operating systems

## Troubleshooting

### "Ghostscript not found" Error
1. Ensure Ghostscript is installed
2. Check if Ghostscript is in your system PATH
3. On Windows, try reinstalling Ghostscript with "Add to PATH" option

### Permission Errors
- Ensure you have read permissions for input files
- Ensure you have write permissions for output directory
- Run as administrator if necessary (Windows)

### Large File Processing
- For very large PDF files, the compression may take time
- Ensure sufficient disk space for both input and output files
- Consider using lower quality settings for faster processing

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
