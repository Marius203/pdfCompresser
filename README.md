# PDF Compressor

A modern web application for compressing PDF files with a React frontend and Python Flask backend.

## Features

- 🎯 **Modern React UI** - Clean, responsive interface built with Tailwind CSS
- 📁 **Drag & Drop** - Easy file upload with drag and drop support
- ⚡ **Multiple Quality Options** - Low, Medium, High, and Maximum quality settings
- 📊 **Real-time Progress** - Visual progress indicator during compression
- 📈 **Compression Stats** - See original size, compressed size, and compression ratio
- 💾 **Direct Download** - Download compressed files immediately
- 🔧 **Ghostscript Integration** - Uses industry-standard Ghostscript for reliable compression

## Project Structure

```
pdfCompresser/
├── backend/
│   ├── pdf_compressor.py      # Core compression logic
│   ├── app.py                 # Flask API server
│   ├── requirements.txt       # Python console app dependencies
│   └── requirements_api.txt   # Flask API dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   └── index.js          # React entry point
│   ├── public/
│   │   └── index.html        # HTML template with Tailwind CDN
│   └── package.json          # Node.js dependencies
└── gs10.05.1/                # Ghostscript installation
```

## Quick Start

### Prerequisites

- Node.js (for React frontend)
- Python 3.7+ (for backend)
- Ghostscript (included in gs10.05.1 folder)

### 1. Start the Backend API

```bash
cd backend
pip install -r requirements_api.txt
python app.py
```

The API will start on `http://localhost:5000`

### 2. Start the Frontend

```bash
cd frontend
npm install
npm start
```

The React app will start on `http://localhost:3000`

## Usage

### Web Interface

1. Open `http://localhost:3000` in your browser
2. Drag and drop a PDF file or click to select
3. Choose compression quality (Low, Medium, High, Maximum)
4. Click "Compress PDF"
5. Download the compressed file

### Console Interface

You can also use the original console interface:

```bash
cd backend
python pdf_compressor.py
```

For command-line usage:
```bash
python pdf_compressor.py input.pdf -q medium -o output.pdf
```

## Quality Settings

- **Low** (72 DPI) - Smallest file size, suitable for screen viewing
- **Medium** (150 DPI) - Balanced quality and size, good for most uses
- **High** (300 DPI) - High quality, suitable for printing
- **Maximum** (300 DPI) - Best quality with color preservation

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/info` - Get compressor information
- `POST /api/compress` - Compress PDF file

## Technologies Used

### Frontend
- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework (via CDN)
- **Axios** - HTTP client for API requests
- **React Dropzone** - File upload with drag & drop
- **Lucide React** - Beautiful icons

### Backend
- **Python 3** - Core language
- **Flask** - Lightweight web framework
- **Ghostscript** - PDF processing engine
- **Flask-CORS** - Cross-origin resource sharing

## Development

### Backend Development

The backend consists of two main components:

1. **pdf_compressor.py** - Core compression logic that can be used standalone
2. **app.py** - Flask API wrapper that provides REST endpoints for the frontend

### Frontend Development

The frontend is a single-page React application that communicates with the Flask API. It uses Tailwind CSS for styling without any custom CSS files.

## Troubleshooting

### Ghostscript Not Found
- Ensure the `gs10.05.1` folder is in the project root
- Check that `gswin64c.exe` exists in `gs10.05.1/bin/`

### CORS Issues
- The Flask backend includes CORS headers for development
- For production, configure CORS properly for your domain

### File Upload Issues
- Maximum file size is 50MB
- Only PDF files are accepted
- Ensure sufficient disk space for temporary files

## License

This project is for educational and personal use.
