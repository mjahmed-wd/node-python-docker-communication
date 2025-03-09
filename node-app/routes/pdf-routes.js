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

/**
 * Endpoint to extract visualization images from PDF
 * Expects a JSON body with { "pdfPath": "path/to/pdf" }
 * Returns URLs to access the extracted images
 */
router.post('/extract-images', async (req, res) => {
  try {
    const { pdfPath } = req.body;
    
    if (!pdfPath) {
      return res.status(400).json({ error: 'PDF path is required' });
    }
    
    // Make a request to the Python FastAPI service
    const pythonResponse = await axios.post('http://python-app:5000/api/extract-images', {
      pdf_path: pdfPath
    });
    
    const responseData = pythonResponse.data;
    
    // Check if the Python service encountered an error
    if (responseData.error) {
      return res.status(422).json({
        success: false,
        error: responseData.error,
        message: 'Error extracting images from PDF'
      });
    }
    
    // Transform the Python static URLs to be accessible through the Node.js app
    if (responseData.data && responseData.data.images) {
      responseData.data.images = responseData.data.images.map(image => {
        // Replace /static/ with /python-static/ to match our proxy setup
        const nodeUrl = image.url.replace('/static/', '/python-static/');
        return {
          ...image,
          url: nodeUrl
        };
      });
    }
    
    // Return the image data from the Python service with updated URLs
    return res.json({
      success: true,
      data: responseData.data,
      message: responseData.message
    });
  } catch (error) {
    console.error('Error extracting images from PDF:', error.message);
    
    // If the error comes from the Python service, forward its response
    if (error.response && error.response.data) {
      return res.status(error.response.status || 500).json({
        success: false,
        error: error.response.data.detail || 'Error extracting images from PDF'
      });
    }
    
    return res.status(500).json({ 
      success: false, 
      error: 'Failed to extract images from PDF'
    });
  }
});

module.exports = router; 