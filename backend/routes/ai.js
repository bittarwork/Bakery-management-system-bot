/**
 * AI ROUTES - Modern AI endpoints for MERN dashboard
 * Enhanced AI integration for the new dashboard interface
 */

import express from 'express';
import { GeminiService } from '../services/ai/gemini.js';
import logger from '../config/logger.js';

const router = express.Router();
const geminiService = new GeminiService();

/**
 * Chat with AI - Enhanced for dashboard integration
 * POST /api/ai/chat
 */
router.post('/chat', async (req, res) => {
    try {
        const { message, language = 'ar', context = 'dashboard' } = req.body;

        if (!message?.trim()) {
            return res.status(400).json({
                success: false,
                error: 'Message is required'
            });
        }

        const response = await geminiService.processQuestion(message, language);

        res.json({
            success: true,
            data: {
                message: response.response,
                sql_query: response.sql_query,
                results: response.results,
                processing_time: response.processing_time,
                language: language,
                context: context
            }
        });

    } catch (error) {
        logger.error('AI chat error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

/**
 * Get analytics insights
 * GET /api/ai/analytics
 */
router.get('/analytics', async (req, res) => {
    try {
        const { type = 'comprehensive' } = req.query;

        const report = await geminiService.getAnalyticsReport(type);

        res.json({
            success: true,
            data: report
        });

    } catch (error) {
        logger.error('AI analytics error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

export default router; 