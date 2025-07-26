import express from 'express';

const router = express.Router();

// Basic auth routes - to be implemented later
router.post('/login', (req, res) => {
    res.json({ success: true, message: 'Login endpoint - to be implemented' });
});

router.post('/register', (req, res) => {
    res.json({ success: true, message: 'Register endpoint - to be implemented' });
});

export default router; 