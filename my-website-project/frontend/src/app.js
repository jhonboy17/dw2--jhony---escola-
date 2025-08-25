const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON requests
app.use(express.json());

// Example of a simple route
app.get('/', (req, res) => {
    res.send('Welcome to the frontend of the website!');
});

// Function to initialize the app
const init = () => {
    app.listen(PORT, () => {
        console.log(`Frontend is running on http://localhost:${PORT}`);
    });
};

init();