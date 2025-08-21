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
## License

This project is for educational and personal use.
