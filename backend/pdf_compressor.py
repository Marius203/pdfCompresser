import os
import subprocess
import platform

class PDFCompressor:
    """PDF compression utility using Ghostscript"""
    
    QUALITY_SETTINGS = {
        'low': {
            'dPDFSETTINGS': '/screen',
            'dColorImageResolution': 72,
            'dGrayImageResolution': 72,
            'dMonoImageResolution': 72
        },
        'medium': {
            'dPDFSETTINGS': '/ebook',
            'dColorImageResolution': 150,
            'dGrayImageResolution': 150,
            'dMonoImageResolution': 150
        },
        'high': {
            'dPDFSETTINGS': '/printer',
            'dColorImageResolution': 300,
            'dGrayImageResolution': 300,
            'dMonoImageResolution': 300
        },
        'max': {
            'dPDFSETTINGS': '/prepress',
            'dColorImageResolution': 300,
            'dGrayImageResolution': 300,
            'dMonoImageResolution': 300
        }
    }
    
    def __init__(self):
        """Initialize the PDF compressor with Ghostscript path"""
        self.ghostscript_cmd = self._find_ghostscript()
        if not self.ghostscript_cmd:
            raise RuntimeError("Ghostscript not found. Please install Ghostscript.")
    
    def _find_ghostscript(self):
        """Find Ghostscript executable on the system"""
        # Common Ghostscript command names
        gs_commands = ['gs', 'ghostscript', 'gswin64c', 'gswin32c']
        
        for cmd in gs_commands:
            try:
                # Test if command exists and works
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                if result.returncode == 0:
                    return cmd
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
        
        return None
    
    def compress_pdf(self, input_path, output_path, quality='medium'):
        """
        Compress a PDF file using Ghostscript
        
        Args:
            input_path (str): Path to input PDF file
            output_path (str): Path to output compressed PDF file
            quality (str): Compression quality ('low', 'medium', 'high', 'max')
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Validate inputs
            if not os.path.exists(input_path):
                return False, f"Input file does not exist: {input_path}"
            
            if quality not in self.QUALITY_SETTINGS:
                return False, f"Invalid quality setting: {quality}"
            
            # Get quality settings
            settings = self.QUALITY_SETTINGS[quality]
            
            # Build Ghostscript command
            gs_command = [
                self.ghostscript_cmd,
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                '-dPDFSETTINGS=' + settings['dPDFSETTINGS'],
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                '-dSAFER',
                f'-dColorImageResolution={settings["dColorImageResolution"]}',
                f'-dGrayImageResolution={settings["dGrayImageResolution"]}',
                f'-dMonoImageResolution={settings["dMonoImageResolution"]}',
                '-dColorImageDownsampleType=/Bicubic',
                '-dGrayImageDownsampleType=/Bicubic',
                '-dMonoImageDownsampleType=/Bicubic',
                '-dColorImageFilter=/DCTEncode',
                '-dGrayImageFilter=/DCTEncode',
                '-dAutoFilterColorImages=false',
                '-dAutoFilterGrayImages=false',
                f'-sOutputFile={output_path}',
                input_path
            ]
            
            # Execute Ghostscript command
            result = subprocess.run(gs_command, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=300)  # 5 minute timeout
            
            if result.returncode != 0:
                error_msg = result.stderr if result.stderr else "Unknown Ghostscript error"
                return False, f"Ghostscript compression failed: {error_msg}"
            
            # Verify output file was created
            if not os.path.exists(output_path):
                return False, "Output file was not created"
            
            # Check if output file has reasonable size
            if os.path.getsize(output_path) == 0:
                return False, "Output file is empty"
            
            return True, "PDF compressed successfully"
            
        except subprocess.TimeoutExpired:
            return False, "Compression timed out"
        except Exception as e:
            return False, f"Compression error: {str(e)}"
    
    def get_file_size(self, file_path):
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except OSError:
            return 0
    
    def calculate_compression_ratio(self, original_size, compressed_size):
        """Calculate compression ratio as percentage"""
        if original_size == 0:
            return 0
        return round((1 - compressed_size / original_size) * 100, 1)