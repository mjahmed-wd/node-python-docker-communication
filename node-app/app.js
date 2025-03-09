const express = require('express');
const path = require('path');
const pdfRoutes = require('./routes/pdf-routes');

const app = express();
const port = 3000;

// Middleware to parse JSON bodies
app.use(express.json());

// Root endpoint
app.get('/', (req, res) => {
  res.send('Hello from Node.js!');
});

// Register PDF routes
app.use('/api', pdfRoutes);

// Start the server
app.listen(port, () => {
  console.log(`Node.js server listening at http://localhost:${port}`);
}); 