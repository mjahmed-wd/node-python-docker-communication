const express = require('express');
const path = require('path');
const axios = require('axios');
const pdfRoutes = require('./routes/pdf-routes');

const app = express();
const port = 3000;

// Middleware to parse JSON bodies
app.use(express.json());

// Root endpoint
app.get('/', (req, res) => {
  res.send('Hello from Node.js!');
});

// Custom proxy middleware for Python static files
app.get('/python-static/*', async (req, res) => {
  try {
    // Extract the path after /python-static/
    const pythonPath = req.path.replace('/python-static', '/static');
    
    // Create the full URL to the Python service
    const pythonUrl = `http://python-app:5000${pythonPath}`;
    
    console.log(`Proxying request to: ${pythonUrl}`);
    
    // Make a request to the Python service
    const response = await axios({
      method: 'get',
      url: pythonUrl,
      responseType: 'stream'
    });
    
    // Set the content type header
    res.set('Content-Type', response.headers['content-type']);
    
    // Pipe the response
    response.data.pipe(res);
  } catch (error) {
    console.error(`Error proxying static file: ${error.message}`);
    res.status(404).send('File not found');
  }
});

// Register PDF routes
app.use('/api', pdfRoutes);

// Start the server
app.listen(port, () => {
  console.log(`Node.js server listening at http://localhost:${port}`);
}); 