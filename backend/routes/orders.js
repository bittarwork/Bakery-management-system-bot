import express from 'express';
import { executeRawQuery } from '../config/database.js';

const router = express.Router();

router.get('/', async (req, res) => {
    try {
        const result = await executeRawQuery('SELECT * FROM orders ORDER BY order_date DESC LIMIT 50');
        res.json({ success: true, data: result.results });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

export default router; 