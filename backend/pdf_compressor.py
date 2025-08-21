#!/usr/bin/env python3
"""
PDF Compressor using Ghostscript
A console user interface for compressing PDF files with various quality settings.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Tuple
import shutil

class PDFCompressor:
    """PDF compression utility using Ghostscript."""
    
    # Compression quality settings
    QUALITY_SETTINGS = {
        'low': '/screen',      # Low quality, smallest file size (72 dpi)
        'medium': '/ebook',    # Medium quality (150 dpi)
        'high': '/printer',    # High quality (300 dpi)
        'max': '/prepress'     # Maximum quality (color preserving, 300 dpi)
    }
    
    def __init__(self):
        """Initialize the PDF compressor."""
        self.ghostscript_cmd = self._find_ghostscript()
        if not self.ghostscript_cmd:
            raise RuntimeError("Ghostscript not found. Please install Ghostscript.")
    
    def _find_ghostscript(self) -> Optional[str]:
        """Find Ghostscript executable on the system."""
        # Common Ghostscript executable names
        import glob
        script_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join(script_dir, "..", "gs10.05.1", "bin", "gswin64c.exe")
        relative_path = os.path.normpath(relative_path)  # Clean up the path

        if os.path.exists(relative_path):
            return relative_path
    
    
    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        return os.path.getsize(file_path)
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def compress_pdf(self, input_path: str, output_path: str, quality: str = 'medium') -> Tuple[bool, str]:
        """
        Compress a PDF file using Ghostscript.
        
        Args:
            input_path: Path to input PDF file
            output_path: Path to output compressed PDF file
            quality: Compression quality ('low', 'medium', 'high', 'max')
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if quality not in self.QUALITY_SETTINGS:
            return False, f"Invalid quality setting. Choose from: {list(self.QUALITY_SETTINGS.keys())}"
        
        if not os.path.exists(input_path):
            return False, f"Input file not found: {input_path}"
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Build Ghostscript command
        gs_command = [
            self.ghostscript_cmd,
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=' + self.QUALITY_SETTINGS[quality],
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_path}',
            input_path
        ]
        
        try:
            # Run Ghostscript
            result = subprocess.run(gs_command, capture_output=True, text=True, check=True)
            
            if os.path.exists(output_path):
                original_size = self.get_file_size(input_path)
                compressed_size = self.get_file_size(output_path)
                compression_ratio = (1 - compressed_size / original_size) * 100
                
                message = (f"Compression successful!\n"
                          f"Original size: {self.format_file_size(original_size)}\n"
                          f"Compressed size: {self.format_file_size(compressed_size)}\n"
                          f"Compression ratio: {compression_ratio:.1f}%")
                return True, message
            else:
                return False, "Compression failed: Output file not created"
                
        except subprocess.CalledProcessError as e:
            return False, f"Ghostscript error: {e.stderr}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"


def display_banner():
    """Display application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                      PDF COMPRESSOR                          ║
║                  Using Ghostscript Engine                    ║
║                                                              ║
║  Compress PDF files with various quality settings           ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def display_quality_options():
    """Display available quality options."""
    print("\nAvailable compression quality options:")
    print("  1. low    - Low quality, smallest file size (72 dpi)")
    print("  2. medium - Medium quality (150 dpi) [DEFAULT]")
    print("  3. high   - High quality (300 dpi)")
    print("  4. max    - Maximum quality, color preserving (300 dpi)")


def get_user_input(prompt: str, default: str = None) -> str:
    """Get user input with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()


def interactive_mode():
    """Run the PDF compressor in interactive mode."""
    compressor = PDFCompressor()
    
    display_banner()
    print(f"Ghostscript found: {compressor.ghostscript_cmd}")
    
    while True:
        print("\n" + "="*60)
        print("PDF COMPRESSION MENU")
        print("="*60)
        
        # Get input file
        input_file = get_user_input("Enter path to PDF file (or 'quit' to exit)")
        
        if input_file.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        # Remove quotes if present
        input_file = input_file.strip('"\'')
        
        if not os.path.exists(input_file):
            print(f"❌ Error: File not found - {input_file}")
            continue
        
        if not input_file.lower().endswith('.pdf'):
            print("❌ Error: Please provide a PDF file")
            continue
        
        # Get output file
        output_file = input_file.replace('.pdf', '_compressed.pdf')
        
        # Get quality setting
        display_quality_options()
        quality_input = get_user_input("Choose quality (1-4 or name)", "2")
        
        # Map quality input
        quality_map = {
            '1': 'low', '2': 'medium', '3': 'high', '4': 'max',
            'low': 'low', 'medium': 'medium', 'high': 'high', 'max': 'max'
        }
        
        quality = quality_map.get(quality_input.lower(), 'medium')
        
        # Show compression details
        print(f"\n📄 Input file: {input_file}")
        print(f"💾 Output file: {output_file}")
        print(f"⚙️  Quality: {quality}")
        print(f"📏 Original size: {compressor.format_file_size(compressor.get_file_size(input_file))}")
        
        # Confirm compression
        confirm = get_user_input("Proceed with compression? (y/n)", "y")
        
        if confirm.lower() not in ['y', 'yes']:
            print("Compression cancelled.")
            continue
        
        # Perform compression
        print("\n🔄 Compressing PDF...")
        success, message = compressor.compress_pdf(input_file, output_file, quality)
        
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")


def command_line_mode():
    """Run the PDF compressor in command-line mode."""
    parser = argparse.ArgumentParser(
        description="Compress PDF files using Ghostscript",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quality options:
  low     - Low quality, smallest file size (72 dpi)
  medium  - Medium quality (150 dpi) [DEFAULT]
  high    - High quality (300 dpi)
  max     - Maximum quality, color preserving (300 dpi)

Examples:
  python pdf_compressor.py input.pdf
  python pdf_compressor.py input.pdf -o compressed.pdf -q low
  python pdf_compressor.py input.pdf --quality high
        """
    )
    
    parser.add_argument('input', help='Input PDF file path')
    parser.add_argument('-o', '--output', help='Output PDF file path (default: input_compressed.pdf)')
    parser.add_argument('-q', '--quality', choices=['low', 'medium', 'high', 'max'], 
                       default='medium', help='Compression quality (default: medium)')
    parser.add_argument('-i', '--interactive', action='store_true', 
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    try:
        compressor = PDFCompressor()
        
        # Set default output if not provided
        if not args.output:
            input_path = Path(args.input)
            args.output = str(input_path.with_stem(input_path.stem + '_compressed'))
        
        print(f"Compressing: {args.input}")
        print(f"Output: {args.output}")
        print(f"Quality: {args.quality}")
        print(f"Original size: {compressor.format_file_size(compressor.get_file_size(args.input))}")
        
        success, message = compressor.compress_pdf(args.input, args.output, args.quality)
        
        if success:
            print(f"✅ {message}")
            sys.exit(0)
        else:
            print(f"❌ {message}")
            sys.exit(1)
            
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        # No arguments provided, run in interactive mode
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
        except RuntimeError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    else:
        # Arguments provided, run in command-line mode
        command_line_mode()


if __name__ == "__main__":
    main()
