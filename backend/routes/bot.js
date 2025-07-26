/**
 * BOT ROUTES - Integration with existing Python bot system
 * These routes provide the same functionality as the current Flask app
 * Maintains compatibility while adding new MERN stack features
 */

import express from 'express';
import { executeRawQuery, getDatabaseStats, getTableInfo } from '../config/database.js';
import { GeminiService } from '../services/ai/gemini.js';
import logger from '../config/logger.js';
import NodeCache from 'node-cache';

const router = express.Router();

// Initialize AI service and cache (same as Python system)
const geminiService = new GeminiService();
const responseCache = new NodeCache({ stdTTL: 3600 }); // 1 hour cache

/**
 * Health check endpoint - compatible with current system
 * GET /api/bot/health
 */
router.get('/health', async (req, res) => {
    try {
        // Test database connection
        const tables = await getTableInfo();

        const healthStatus = {
            status: 'healthy',
            database: 'connected',
            tables_count: tables.length,
            ai_provider: process.env.AI_PROVIDER || 'gemini',
            timestamp: new Date().toISOString(),
            version: '2.0.0-mern',
            migration_status: 'integrated'
        };

        logger.info('Bot health check requested', healthStatus);
        res.json(healthStatus);

    } catch (error) {
        logger.error('Bot health check failed:', error);
        res.status(500).json({
            status: 'unhealthy',
            error: error.message,
            timestamp: new Date().toISOString()
        });
    }
});

/**
 * Chat endpoint - main bot functionality (same as Flask /api/chat)
 * POST /api/bot/chat
 */
router.post('/chat', async (req, res) => {
    try {
        const { message, language = 'ar' } = req.body;

        if (!message || !message.trim()) {
            return res.status(400).json({
                success: false,
                error: 'Message is required'
            });
        }

        const userMessage = message.trim();
        logger.info(`Bot chat request: ${userMessage.substring(0, 100)}...`);

        // Check cache first
        const cacheKey = `chat_${userMessage}_${language}`;
        const cachedResponse = responseCache.get(cacheKey);

        if (cachedResponse) {
            logger.info('Returning cached response');
            return res.json({
                ...cachedResponse,
                cached: true
            });
        }

        // Get AI response using Gemini service
        const startTime = Date.now();
        const aiResponse = await geminiService.processQuestion(userMessage, language);
        const processingTime = (Date.now() - startTime) / 1000;

        const response = {
            success: true,
            response: aiResponse.analysis || aiResponse.response,
            cached: false,
            processing_time: processingTime,
            model_used: process.env.GEMINI_MODEL || 'gemini-1.5-pro',
            tokens_used: aiResponse.tokens_used || 0,
            language: language,
            sql_query: aiResponse.sql_query,
            results_count: aiResponse.results ? aiResponse.results.length : 0
        };

        // Cache the response
        if (process.env.CACHE_ENABLED === 'true') {
            responseCache.set(cacheKey, response);
        }

        logger.logAIRequest(
            'gemini',
            process.env.GEMINI_MODEL,
            response.tokens_used,
            processingTime * 1000,
            true
        );

        res.json(response);

    } catch (error) {
        logger.error('Bot chat error:', error);
        res.status(500).json({
            success: false,
            error: error.message || 'Internal server error',
            cached: false
        });
    }
});

/**
 * Analytics endpoint - same as Flask /api/analytics
 * GET /api/bot/analytics
 */
router.get('/analytics', async (req, res) => {
    try {
        const reportType = req.query.type || 'comprehensive';

        logger.info(`Analytics request: ${reportType}`);

        // Get analytics report using AI
        const analyticsReport = await geminiService.getAnalyticsReport(reportType);

        res.json({
            success: true,
            report: analyticsReport,
            report_type: reportType,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        logger.error('Bot analytics error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

/**
 * Stats endpoint - same as Flask /api/stats  
 * GET /api/bot/stats
 */
router.get('/stats', async (req, res) => {
    try {
        const stats = await getDatabaseStats();

        res.json({
            success: true,
            stats: stats,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        logger.error('Bot stats error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

/**
 * Database query endpoint - same as Flask /api/query
 * POST /api/bot/query  
 */
router.post('/query', async (req, res) => {
    try {
        const { query } = req.body;

        if (!query || !query.trim()) {
            return res.status(400).json({
                success: false,
                error: 'Query is required'
            });
        }

        // Security: Only allow SELECT queries
        if (!query.trim().toUpperCase().startsWith('SELECT')) {
            return res.status(400).json({
                success: false,
                error: 'Only SELECT queries are allowed'
            });
        }

        logger.info(`Database query request: ${query.substring(0, 100)}...`);

        const result = await executeRawQuery(query);

        res.json({
            success: result.success,
            results: result.results,
            count: result.count,
            error: result.error
        });

    } catch (error) {
        logger.error('Bot query error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

/**
 * Tables information endpoint - same as Flask /api/tables
 * GET /api/bot/tables
 */
router.get('/tables', async (req, res) => {
    try {
        const tables = await getTableInfo();

        const tablesInfo = [];
        for (const table of tables) {
            const schema = await getTableInfo(table.table_name);
            tablesInfo.push({
                name: table.table_name,
                rows: table.table_rows,
                columns: schema.columns
            });
        }

        res.json({
            success: true,
            tables: tablesInfo,
            count: tables.length
        });

    } catch (error) {
        logger.error('Bot tables error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

/**
 * Cache management endpoint - same as Flask /api/cache
 * GET /api/bot/cache - get cache status
 * DELETE /api/bot/cache - clear cache
 */
router.route('/cache')
    .get((req, res) => {
        try {
            const keys = responseCache.keys();

            res.json({
                success: true,
                cache_enabled: process.env.CACHE_ENABLED === 'true',
                cached_items: keys.length,
                cache_keys: keys.slice(0, 10), // Show first 10 keys
                status: 'active'
            });

        } catch (error) {
            logger.error('Bot cache status error:', error);
            res.status(500).json({
                success: false,
                error: error.message
            });
        }
    })
    .delete((req, res) => {
        try {
            const deletedCount = responseCache.keys().length;
            responseCache.flushAll();

            res.json({
                success: true,
                message: 'Cache cleared successfully',
                deleted_items: deletedCount
            });

            logger.info(`Cache cleared: ${deletedCount} items deleted`);

        } catch (error) {
            logger.error('Bot cache clear error:', error);
            res.status(500).json({
                success: false,
                error: error.message
            });
        }
    });

/**
 * System info endpoint - enhanced version of current system
 * GET /api/bot/info
 */
router.get('/info', async (req, res) => {
    try {
        const tables = await getTableInfo();
        const stats = await getDatabaseStats();

        const systemInfo = {
            bot_name: 'BakeryBot Pro - MERN Integration',
            version: '2.0.0-mern',
            ai_provider: process.env.AI_PROVIDER,
            ai_model: process.env.GEMINI_MODEL,
            database_type: 'MySQL',
            environment: process.env.NODE_ENV,
            features: [
                'Natural Language Database Queries',
                'Advanced Analytics with AI',
                'Real-time Dashboard Integration',
                'Multi-language Support (AR/EN)',
                'Smart Caching System',
                'Product & Inventory Management',
                'Order Processing & Tracking',
                'Distributor Performance Analytics',
                'Store Management',
                'Financial Reporting'
            ],
            database_stats: stats,
            tables_count: tables.length,
            cache_enabled: process.env.CACHE_ENABLED === 'true',
            capabilities: [
                'متابعة المنتجات والمخزون',
                'تحليل المبيعات والإيرادات',
                'إدارة الطلبات والتوزيع',
                'تقارير الأداء التفصيلية',
                'استعلامات ذكية بالذكاء الاصطناعي'
            ]
        };

        res.json({
            success: true,
            info: systemInfo
        });

    } catch (error) {
        logger.error('Bot info error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

export default router; 