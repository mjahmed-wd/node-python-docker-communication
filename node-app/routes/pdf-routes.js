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

/**
 * Endpoint to import and process a PDF - combines text extraction and image extraction
 * Expects a JSON body with { "pdfPath": "path/to/pdf" }
 * Returns both extracted text data and image URLs
 */
router.post('/import-test', async (req, res) => {
  try {
    const { pdfPath } = req.body;
    
    if (!pdfPath) {
      return res.status(400).json({ error: 'PDF path is required' });
    }
    
    // Initialize results with default values in case any request fails
    let textData = { data: { text: {} }, message: 'Text extraction failed' };
    let imagesData = { data: { images: [] }, message: 'Image extraction failed' };
    let textError = null;
    let imagesError = null;
    
    try {
      // Call text extraction API
      const textResponse = await axios.post('http://python-app:5000/api/extract-text', { pdf_path: pdfPath });
      textData = textResponse.data;
      // Ensure we're handling the text data correctly
      if (!textData.data || !textData.data.text) {
        console.warn('Text extraction returned unexpected format:', textData);
        // Try to normalize the response if possible
        if (textData.data && typeof textData.data === 'object') {
          textData = { 
            data: { text: textData.data },
            message: textData.message || 'Text extracted with unexpected format'
          };
        }
      }
    } catch (error) {
      console.error('Error in text extraction:', error.message);
      textError = error.response?.data?.detail || error.message;
    }
    
    try {
      // Call image extraction API
      const imagesResponse = await axios.post('http://python-app:5000/api/extract-images', { pdf_path: pdfPath });
      imagesData = imagesResponse.data;
      
      // Transform the Python static URLs to be accessible through the Node.js app
      if (imagesData.data && imagesData.data.images) {
        imagesData.data.images = imagesData.data.images.map(image => {
          // Replace /static/ with /python-static/ to match our proxy setup
          const nodeUrl = image.url.replace('/static/', '/python-static/');
          return {
            ...image,
            url: nodeUrl
          };
        });
      }
    } catch (error) {
      console.error('Error in image extraction:', error.message);
      imagesError = error.response?.data?.detail || error.message;
    }
    
    // Check if both requests failed completely
    if (textError && imagesError) {
      return res.status(500).json({
        success: false,
        error: `Text extraction: ${textError}. Image extraction: ${imagesError}`,
        message: 'Failed to process PDF'
      });
    }
    
    // Determine the overall success status
    const textSuccess = !textError && textData.data && textData.data.text;
    const imageSuccess = !imagesError && imagesData.data && imagesData.data.images && imagesData.data.images.length > 0;
    
    // Create combined status message
    let statusMessage = '';
    if (textSuccess && imageSuccess) {
      statusMessage = 'PDF successfully processed with text and images';
    } else if (textSuccess) {
      statusMessage = 'PDF text extracted successfully, but image extraction failed or returned no images';
    } else if (imageSuccess) {
      statusMessage = 'PDF images extracted successfully, but text extraction failed or returned no data';
    } else {
      statusMessage = 'PDF processing partially successful, some data may be missing';
    }
    
    // Combine the results - Ensure success is a boolean
    return res.json({
      success: Boolean(textSuccess || imageSuccess),
      data: {
        text: textData.data?.text || {},
        images: imagesData.data?.images || []
      },
      pdf_path: pdfPath,
      textMessage: textData.message || (textError ? `Error: ${textError}` : 'No text data available'),
      imageMessage: imagesData.message || (imagesError ? `Error: ${imagesError}` : 'No image data available'),
      message: statusMessage
    });
  } catch (error) {
    console.error('Error processing PDF:', error.message);
    
    return res.status(500).json({ 
      success: false, 
      error: 'Failed to process PDF: ' + error.message,
      message: 'Failed to process PDF'
    });
  }
});

module.exports = router; 