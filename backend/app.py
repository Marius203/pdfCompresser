#!/usr/bin/env python3
"""
Flask API server for PDF compression
Provides REST API endpoints for the React frontend
"""

import os
import tempfile
import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sys

# Add the current directory to Python path to import pdf_compressor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pdf_compressor import PDFCompressor

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 50MB max file size
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'PDF Compressor API is running'})

@app.route('/api/compress', methods=['POST'])
def compress_pdf():
    """Compress PDF file endpoint."""
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        quality = request.form.get('quality', 'medium')
        
        # Validate file
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Validate quality parameter
        valid_qualities = ['low', 'medium', 'high', 'max']
        if quality not in valid_qualities:
            return jsonify({'error': f'Invalid quality. Must be one of: {valid_qualities}'}), 400
        
        # Generate unique filenames
        unique_id = str(uuid.uuid4())
        original_filename = secure_filename(file.filename)
        input_filename = f"{unique_id}_input_{original_filename}"
        output_filename = f"{unique_id}_output_{original_filename}"
        
        input_path = os.path.join(UPLOAD_FOLDER, input_filename)
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        # Save uploaded file
        file.save(input_path)
        
        try:
            # Initialize compressor and compress file
            compressor = PDFCompressor()
            success, message = compressor.compress_pdf(input_path, output_path, quality)
            
            if not success:
                return jsonify({'error': message}), 500
            
            # Get file sizes for response headers
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            
            # Send compressed file
            response = send_file(
                output_path,
                as_attachment=True,
                download_name=f"compressed_{original_filename}",
                mimetype='application/pdf'
            )
            
            # Add custom headers with compression info
            response.headers['X-Original-Size'] = str(original_size)
            response.headers['X-Compressed-Size'] = str(compressed_size)
            response.headers['X-Compression-Ratio'] = str(round((1 - compressed_size / original_size) * 100, 1))
            
            return response
            
        finally:
            # Clean up temporary files
            try:
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
            except Exception as e:
                print(f"Warning: Failed to clean up temporary files: {e}")
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get compressor information."""
    try:
        compressor = PDFCompressor()
        return jsonify({
            'ghostscript_path': compressor.ghostscript_cmd,
            'quality_options': compressor.QUALITY_SETTINGS,
            'max_file_size': '50MB'
        })
    except Exception as e:
        return jsonify({'error': f'Failed to initialize compressor: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 50MB.'}), 413

if __name__ == '__main__':
    print("Starting PDF Compressor API server...")
    print("Frontend should be accessible at: http://localhost:3000")
    print("API endpoints:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/info - Compressor information")
    print("  POST /api/compress - Compress PDF file")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
