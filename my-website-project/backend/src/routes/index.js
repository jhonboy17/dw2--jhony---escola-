const express = require('express');
const router = express.Router();

// Define your API routes here
router.get('/', (req, res) => {
    res.send('Welcome to the API!');
});

// Add more routes as needed
// router.get('/example', (req, res) => {
//     res.json({ message: 'This is an example route.' });
// });

module.exports = router;