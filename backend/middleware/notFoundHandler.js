/**
 * NOT FOUND MIDDLEWARE
 * Handles 404 responses for unmatched routes
 */

import logger from '../config/logger.js';

const notFoundHandler = (req, res, next) => {
    const message = `Route ${req.originalUrl} not found`;

    // Log the 404 attempt
    logger.warn('Route Not Found', {
        method: req.method,
        url: req.originalUrl,
        ip: req.ip,
        userAgent: req.get('User-Agent')
    });

    res.status(404).json({
        success: false,
        error: message,
        availableRoutes: [
            'GET /',
            'GET /health',
            'GET /api/docs',
            'POST /api/auth/login',
            'POST /api/auth/register',
            'GET /api/users',
            'GET /api/products',
            'GET /api/orders',
            'GET /api/stores',
            'GET /api/distributors',
            'POST /api/ai/chat',
            'GET /api/analytics',
            'GET /api/dashboard/stats',
            'POST /api/bot/chat'
        ]
    });
};

export default notFoundHandler; 