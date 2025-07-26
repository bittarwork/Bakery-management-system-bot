import express from 'express';
import { getDatabaseStats } from '../config/database.js';

const router = express.Router();

router.get('/', async (req, res) => {
    try {
        const stats = await getDatabaseStats();
        res.json({
            success: true,
            data: {
                overview: stats,
                timestamp: new Date().toISOString()
            }
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

export default router; 