const express = require('express');
const axios = require('axios');
const path = require('path');

const router = express.Router();

/**
 * Endpoint to convert PDF to image
 * Expects a JSON body with { "pdfPath": "path/to/pdf" }
 */
router.post('/convert-pdf', async (req, res) => {
  try {
    const { pdfPath } = req.body;
    
    if (!pdfPath) {
      return res.status(400).json({ error: 'PDF path is required' });
    }
    
    // Make a request to the Python FastAPI service
    const pythonResponse = await axios.post('http://python-app:5000/api/convert-pdf', {
      pdf_path: pdfPath
    });
    
    // Return the image path from the Python service
    return res.json({ 
      success: true, 
      imagePath: pythonResponse.data.image_path,
      message: 'PDF successfully converted to image'
    });
  } catch (error) {
    console.error('Error converting PDF:', error.message);
    
    // If the error comes from the Python service, forward its response
    if (error.response && error.response.data) {
      return res.status(error.response.status || 500).json({
        success: false,
        error: error.response.data.detail || 'Error processing PDF'
      });
    }
    
    return res.status(500).json({ 
      success: false, 
      error: 'Failed to convert PDF to image'
    });
  }
});

/**
 * Endpoint to extract text from PDF
 * Expects a JSON body with { "pdfPath": "path/to/pdf" }
 * Returns both structured data and raw text extracted from the PDF
 */
router.post('/extract-text', async (req, res) => {
  try {
    const { pdfPath } = req.body;
    
    if (!pdfPath) {
      return res.status(400).json({ error: 'PDF path is required' });
    }
    
    // Make a request to the Python FastAPI service
    const pythonResponse = await axios.post('http://python-app:5000/api/extract-text', {
      pdf_path: pdfPath
    });
    
    const responseData = pythonResponse.data;
    
    // Check if the Python service encountered an error
    if (responseData.error) {
      return res.status(422).json({
        success: false,
        error: responseData.error,
        message: 'Error extracting text from PDF'
      });
    }
    
    // Return the complete data from the Python service, including raw_text
    return res.json({ 
      success: responseData.status, 
      data: responseData.data,
      raw_text: responseData.raw_text,
      message: responseData.status 
        ? 'PDF text successfully extracted' 
        : 'PDF text extraction partially successful, some data may be missing'
    });
  } catch (error) {
    console.error('Error extracting text from PDF:', error.message);
    
    // If the error comes from the Python service, forward its response
    if (error.response && error.response.data) {
      return res.status(error.response.status || 500).json({
        success: false,
        error: error.response.data.detail || 'Error extracting text from PDF'
      });
    }
    
    return res.status(500).json({ 
      success: false, 
      error: 'Failed to extract text from PDF'
    });
  }
});

module.exports = router; 