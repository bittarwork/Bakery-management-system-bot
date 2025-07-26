/**
 * BAKERY MERN STACK BACKEND SERVER
 * Main entry point for the Express.js backend server
 * Integrates with existing bakery management system and AI bot
 */

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import morgan from 'morgan';
import rateLimit from 'express-rate-limit';
import cookieParser from 'cookie-parser';
import session from 'express-session';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import 'express-async-errors';

// Import custom modules
import { connectDB, sequelize } from './config/database.js';
import logger from './config/logger.js';
import errorHandler from './middleware/errorHandler.js';
import notFoundHandler from './middleware/notFoundHandler.js';

// Import routes
import authRoutes from './routes/auth.js';
import userRoutes from './routes/users.js';
import productRoutes from './routes/products.js';
import orderRoutes from './routes/orders.js';
import storeRoutes from './routes/stores.js';
import distributorRoutes from './routes/distributors.js';
import aiRoutes from './routes/ai.js';
import analyticsRoutes from './routes/analytics.js';
import dashboardRoutes from './routes/dashboard.js';
import botRoutes from './routes/bot.js';

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Create Express app
const app = express();
const PORT = process.env.PORT || 5000;
const HOST = process.env.HOST || 'localhost';

// Trust proxy for production deployment
app.set('trust proxy', 1);

// Security middleware
app.use(helmet({
    crossOriginResourcePolicy: { policy: "cross-origin" },
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            scriptSrc: ["'self'"],
            imgSrc: ["'self'", "data:", "https:"],
        }
    }
}));

// CORS configuration
const corsOptions = {
    origin: process.env.CORS_ORIGIN ? process.env.CORS_ORIGIN.split(',') : [
        'http://localhost:3000',
        'http://localhost:3001',
        'http://localhost:5173'
    ],
    credentials: process.env.CORS_CREDENTIALS === 'true',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'x-api-key'],
    exposedHeaders: ['x-total-count', 'x-page-count']
};

app.use(cors(corsOptions));

// Rate limiting
const limiter = rateLimit({
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW) || 15 * 60 * 1000, // 15 minutes
    max: parseInt(process.env.RATE_LIMIT_REQUESTS) || 100, // requests per window
    message: {
        error: 'Too many requests from this IP, please try again later.',
        retryAfter: Math.ceil((parseInt(process.env.RATE_LIMIT_WINDOW) || 900000) / 1000)
    },
    standardHeaders: true,
    legacyHeaders: false,
});

app.use('/api/', limiter);

// General middleware
app.use(compression());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(cookieParser());

// Session configuration for dashboard authentication
app.use(session({
    secret: process.env.SESSION_SECRET || 'bakery-session-secret',
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: process.env.NODE_ENV === 'production',
        httpOnly: true,
        maxAge: 24 * 60 * 60 * 1000 // 24 hours
    }
}));

// Logging middleware
if (process.env.NODE_ENV !== 'test') {
    app.use(morgan('combined', {
        stream: { write: message => logger.info(message.trim()) }
    }));
}

// Static file serving for uploads
app.use('/uploads', express.static(join(__dirname, 'uploads')));
app.use('/assets', express.static(join(__dirname, 'public')));

// Health check endpoint
app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        environment: process.env.NODE_ENV,
        version: '1.0.0'
    });
});

// API routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/products', productRoutes);
app.use('/api/orders', orderRoutes);
app.use('/api/stores', storeRoutes);
app.use('/api/distributors', distributorRoutes);
app.use('/api/ai', aiRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/bot', botRoutes); // Original bot integration

// Root endpoint
app.get('/', (req, res) => {
    res.json({
        message: 'Bakery MERN Stack Backend API',
        version: '1.0.0',
        environment: process.env.NODE_ENV,
        documentation: '/api/docs',
        health: '/health',
        features: [
            'User Authentication & Authorization',
            'Product Management',
            'Order Processing',
            'Store Management',
            'Distributor Tracking',
            'AI-Powered Analytics',
            'Integrated Chat Bot',
            'Real-time Dashboard'
        ]
    });
});

// API documentation endpoint (Swagger will be added later)
app.get('/api/docs', (req, res) => {
    res.json({
        message: 'API Documentation',
        endpoints: {
            auth: '/api/auth/*',
            users: '/api/users/*',
            products: '/api/products/*',
            orders: '/api/orders/*',
            stores: '/api/stores/*',
            distributors: '/api/distributors/*',
            ai: '/api/ai/*',
            analytics: '/api/analytics/*',
            dashboard: '/api/dashboard/*',
            bot: '/api/bot/*'
        }
    });
});

// Error handling middleware (must be last)
app.use(notFoundHandler);
app.use(errorHandler);

// Database connection and server startup
const startServer = async () => {
    try {
        // Test database connection
        await connectDB();
        logger.info('Database connected successfully');

        // Sync database models (don't force in production)
        if (process.env.NODE_ENV !== 'production') {
            await sequelize.sync({ alter: false });
            logger.info('Database models synchronized');
        }

        // Start server
        const server = app.listen(PORT, HOST, () => {
            logger.info(`🚀 Bakery MERN Backend Server running on http://${HOST}:${PORT}`);
            logger.info(`📊 Environment: ${process.env.NODE_ENV}`);
            logger.info(`🗄️  Database: ${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_NAME}`);
            logger.info(`🤖 AI Provider: ${process.env.AI_PROVIDER}`);
            logger.info(`📈 Features: Analytics, Bot Integration, Real-time Dashboard`);
        });

        // Graceful shutdown handling
        const gracefulShutdown = (signal) => {
            logger.info(`Received ${signal}, shutting down gracefully...`);
            server.close(async () => {
                try {
                    await sequelize.close();
                    logger.info('Database connections closed');
                    process.exit(0);
                } catch (error) {
                    logger.error('Error during shutdown:', error);
                    process.exit(1);
                }
            });
        };

        process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
        process.on('SIGINT', () => gracefulShutdown('SIGINT'));

    } catch (error) {
        logger.error('Failed to start server:', error);
        process.exit(1);
    }
};

// Start the server
startServer();

export default app; 