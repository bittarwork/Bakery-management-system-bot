/**
 * DASHBOARD ROUTES
 * API endpoints for dashboard statistics and overview data
 */

import express from 'express';
import { getDatabaseStats, executeRawQuery } from '../config/database.js';
import logger from '../config/logger.js';

const router = express.Router();

/**
 * Get dashboard overview statistics
 * GET /api/dashboard/stats
 */
router.get('/stats', async (req, res) => {
    try {
        const stats = await getDatabaseStats();

        // Get additional dashboard metrics
        const additionalStats = await Promise.allSettled([
            executeRawQuery("SELECT COUNT(*) as active_stores FROM stores WHERE status = 'active'"),
            executeRawQuery("SELECT COUNT(*) as pending_orders FROM orders WHERE status = 'pending'"),
            executeRawQuery("SELECT COUNT(*) as active_distributors FROM distributors WHERE status = 'active'"),
            executeRawQuery(`
                SELECT 
                    SUM(final_amount_eur) as today_revenue_eur,
                    COUNT(*) as today_orders
                FROM orders 
                WHERE DATE(order_date) = CURDATE() AND payment_status = 'paid'
            `)
        ]);

        // Extract results safely
        const activeStores = additionalStats[0].status === 'fulfilled' ? additionalStats[0].value.results[0]?.active_stores || 0 : 0;
        const pendingOrders = additionalStats[1].status === 'fulfilled' ? additionalStats[1].value.results[0]?.pending_orders || 0 : 0;
        const activeDistributors = additionalStats[2].status === 'fulfilled' ? additionalStats[2].value.results[0]?.active_distributors || 0 : 0;
        const todayData = additionalStats[3].status === 'fulfilled' ? additionalStats[3].value.results[0] || {} : {};

        const dashboardStats = {
            ...stats,
            active_stores: activeStores,
            pending_orders: pendingOrders,
            active_distributors: activeDistributors,
            today_revenue_eur: todayData.today_revenue_eur || 0,
            today_orders: todayData.today_orders || 0,
            last_updated: new Date().toISOString()
        };

        res.json({
            success: true,
            stats: dashboardStats
        });

    } catch (error) {
        logger.error('Dashboard stats error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

export default router; 