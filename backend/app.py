#!/usr/bin/env python3
"""
Flask API server for PDF compression
Provides REST API endpoints and serves React frontend
"""

import os
import sys
import tempfile
import uuid
from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Add the current directory to Python path to import pdf_compressor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pdf_compressor import PDFCompressor

# Set static folder to point to React build
app = Flask(__name__, static_folder='../frontend/build', static_url_path='')

# Configure CORS to allow requests from your frontend
CORS(app)

# Configuration
class Config:
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_FILE_SIZE', 100 * 1024 * 1024))  # 100MB max file size
    WORKER_TIMEOUT = int(os.environ.get('WORKER_TIMEOUT', 120))

app.config.from_object(Config)

UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}

# Serve React App
@app.route('/')
def serve_react_app():
    """Serve the React app index.html"""
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        return f"Error serving React app: {str(e)}", 500

# Serve static files (CSS, JS, images, etc.)
@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from React build"""
    try:
        return send_from_directory(os.path.join(app.static_folder, 'static'), filename)
    except Exception as e:
        return f"Static file not found: {filename}", 404

# Handle favicon
@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    try:
        return send_from_directory(app.static_folder, 'favicon.ico')
    except Exception as e:
        return "", 404

# Catch-all route for React Router
@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files or React app for client-side routing"""
    try:
        # Check if the requested file exists in the static folder
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        return f"Error serving file: {str(e)}", 404

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
            'max_file_size': '100MB'
        })
    except Exception as e:
        return jsonify({'error': f'Failed to initialize compressor: {str(e)}'}), 500

# Add this route after your existing routes for debugging
@app.route('/api/debug', methods=['GET'])
def debug_files():
    """Debug endpoint to check if build files exist"""
    try:
        build_path = app.static_folder
        if os.path.exists(build_path):
            files = os.listdir(build_path)
            return jsonify({
                'build_path': build_path,
                'files': files,
                'static_exists': os.path.exists(os.path.join(build_path, 'static'))
            })
        else:
            return jsonify({'error': 'Build folder does not exist', 'path': build_path})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 100MB.'}), 413

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
