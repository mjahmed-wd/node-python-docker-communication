const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const port = 3000;

// Middleware to parse JSON bodies
app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello from Node.js!');
});

/**
 * Endpoint to convert PDF to image
 * Expects a JSON body with { "pdfPath": "path/to/pdf" }
 */
app.post('/api/convert-pdf', async (req, res) => {
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

app.listen(port, () => {
  console.log(`Node.js server listening at http://localhost:${port}`);
}); 