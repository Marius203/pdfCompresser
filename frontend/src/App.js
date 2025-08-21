import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { Upload, FileText, Download, RotateCcw, CheckCircle, XCircle } from 'lucide-react';

const PDFCompressor = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [quality, setQuality] = useState('medium');
    const [isCompressing, setIsCompressing] = useState(false);
    const [progress, setProgress] = useState(0);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const qualityOptions = [
        {
            value: 'low',
            name: 'Low',
            description: '72 DPI - Smallest size',
            color: 'bg-red-500'
        },
        {
            value: 'medium',
            name: 'Medium',
            description: '150 DPI - Balanced',
            color: 'bg-yellow-500'
        },
        {
            value: 'high',
            name: 'High',
            description: '300 DPI - Good quality',
            color: 'bg-green-500'
        },
        {
            value: 'max',
            name: 'Maximum',
            description: '300 DPI - Best quality',
            color: 'bg-blue-500'
        }
    ];

    const onDrop = useCallback((acceptedFiles) => {
        const file = acceptedFiles[0];
        if (file && file.type === 'application/pdf') {
            setSelectedFile(file);
            setResult(null);
            setError(null);
        } else {
            setError('Please select a valid PDF file');
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf']
        },
        multiple: false
    });

    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const compressFile = async () => {
        if (!selectedFile) return;

        setIsCompressing(true);
        setProgress(0);
        setError(null);
        setResult(null);

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('quality', quality);

        try {
            // Simulate progress
            const progressInterval = setInterval(() => {
                setProgress(prev => {
                    if (prev >= 90) {
                        clearInterval(progressInterval);
                        return 90;
                    }
                    return prev + 10;
                });
            }, 200);

            const response = await axios.post('pdfcompresser-production.up.railway.app/compress', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                responseType: 'blob'
            });

            clearInterval(progressInterval);
            setProgress(100);

            // Get compression stats from response headers
            const originalSize = parseInt(response.headers['x-original-size'] || selectedFile.size);
            const compressedSize = response.data.size;
            const compressionRatio = ((originalSize - compressedSize) / originalSize * 100).toFixed(1);

            setResult({
                blob: response.data,
                originalSize,
                compressedSize,
                compressionRatio,
                filename: selectedFile.name.replace('.pdf', '_compressed.pdf')
            });

        } catch (err) {
            setError(err.response?.data?.error || 'Compression failed. Please try again.');
        } finally {
            setIsCompressing(false);
        }
    };

    const downloadFile = () => {
        if (!result) return;

        const url = window.URL.createObjectURL(result.blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = result.filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    };

    const resetAll = () => {
        setSelectedFile(null);
        setResult(null);
        setError(null);
        setProgress(0);
        setIsCompressing(false);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-2xl w-full">
                {/* Header */}
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold text-gray-800 mb-2">PDF Compressor</h1>
                    <p className="text-gray-600 text-lg">Compress PDF files with various quality settings</p>
                </div>

                {/* File Upload Area */}
                <div
                    {...getRootProps()}
                    className={`border-3 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-300 mb-6 ${isDragActive
                        ? 'border-blue-500 bg-blue-50'
                        : selectedFile
                            ? 'border-green-500 bg-green-50'
                            : 'border-gray-300 bg-gray-50 hover:border-blue-400 hover:bg-blue-50'
                        }`}
                >
                    <input {...getInputProps()} />
                    <div className="flex flex-col items-center">
                        <Upload className={`w-12 h-12 mb-4 ${isDragActive ? 'text-blue-500' : selectedFile ? 'text-green-500' : 'text-gray-400'}`} />
                        {selectedFile ? (
                            <div className="text-center">
                                <p className="text-lg font-semibold text-gray-700 mb-2">Selected File:</p>
                                <p className="text-blue-600 font-medium">{selectedFile.name}</p>
                                <p className="text-gray-500 text-sm">{formatFileSize(selectedFile.size)}</p>
                            </div>
                        ) : (
                            <div>
                                <p className="text-lg text-gray-600 mb-2">
                                    {isDragActive ? 'Drop the PDF file here' : 'Drag & drop a PDF file here'}
                                </p>
                                <p className="text-gray-500">or click to select a file</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Quality Selection */}
                <div className="mb-6">
                    <h3 className="text-xl font-semibold text-gray-700 mb-4">Compression Quality</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {qualityOptions.map((option) => (
                            <button
                                key={option.value}
                                onClick={() => setQuality(option.value)}
                                className={`p-4 rounded-xl border-2 transition-all duration-200 ${quality === option.value
                                    ? 'border-blue-500 bg-blue-500 text-white shadow-lg'
                                    : 'border-gray-200 bg-white text-gray-700 hover:border-blue-300'
                                    }`}
                            >
                                <div className={`w-3 h-3 rounded-full ${option.color} mx-auto mb-2`}></div>
                                <div className="font-semibold text-sm">{option.name}</div>
                                <div className="text-xs opacity-80">{option.description}</div>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Progress Bar */}
                {isCompressing && (
                    <div className="mb-6">
                        <div className="flex justify-between items-center mb-2">
                            <span className="text-gray-600">Compressing...</span>
                            <span className="text-gray-600">{progress}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3">
                            <div
                                className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-300"
                                style={{ width: `${progress}%` }}
                            ></div>
                        </div>
                    </div>
                )}

                {/* Compress Button */}
                <button
                    onClick={compressFile}
                    disabled={!selectedFile || isCompressing}
                    className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-200 hover:from-blue-600 hover:to-purple-700 hover:shadow-lg disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed mb-6"
                >
                    {isCompressing ? 'Compressing...' : 'Compress PDF'}
                </button>

                {/* Error Message */}
                {error && (
                    <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4 mb-6">
                        <div className="flex items-center">
                            <XCircle className="w-5 h-5 text-red-500 mr-2" />
                            <span className="text-red-700 font-medium">Error</span>
                        </div>
                        <p className="text-red-600 mt-1">{error}</p>
                    </div>
                )}

                {/* Success Result */}
                {result && (
                    <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6 mb-6">
                        <div className="flex items-center mb-3">
                            <CheckCircle className="w-6 h-6 text-green-500 mr-2" />
                            <span className="text-green-700 font-semibold text-lg">Compression Successful!</span>
                        </div>
                        <div className="space-y-2 text-green-700">
                            <div className="flex justify-between">
                                <span>Original size:</span>
                                <span className="font-medium">{formatFileSize(result.originalSize)}</span>
                            </div>
                            <div className="flex justify-between">
                                <span>Compressed size:</span>
                                <span className="font-medium">{formatFileSize(result.compressedSize)}</span>
                            </div>
                            <div className="flex justify-between">
                                <span>Compression ratio:</span>
                                <span className="font-medium">{result.compressionRatio}%</span>
                            </div>
                        </div>
                        <div className="flex gap-3 mt-4">
                            <button
                                onClick={downloadFile}
                                className="flex items-center bg-green-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-700 transition-colors"
                            >
                                <Download className="w-4 h-4 mr-2" />
                                Download
                            </button>
                            <button
                                onClick={resetAll}
                                className="flex items-center bg-gray-200 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-300 transition-colors"
                            >
                                <RotateCcw className="w-4 h-4 mr-2" />
                                Reset
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PDFCompressor;
