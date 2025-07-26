/**
 * LOGGING CONFIGURATION
 * Advanced logging system using Winston with daily rotate files
 */

import winston from 'winston';
import DailyRotateFile from 'winston-daily-rotate-file';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { existsSync, mkdirSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Ensure logs directory exists
const logsDir = join(__dirname, '..', 'logs');
if (!existsSync(logsDir)) {
    mkdirSync(logsDir, { recursive: true });
}

// Define log levels and colors
const logLevels = {
    error: 0,
    warn: 1,
    info: 2,
    http: 3,
    debug: 4
};

winston.addColors({
    error: 'red',
    warn: 'yellow',
    info: 'green',
    http: 'magenta',
    debug: 'white'
});

// Create custom format for console output
const consoleFormat = winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.colorize({ all: true }),
    winston.format.printf(({ timestamp, level, message, ...meta }) => {
        let metaStr = '';
        if (Object.keys(meta).length > 0) {
            metaStr = '\n' + JSON.stringify(meta, null, 2);
        }
        return `${timestamp} [${level}]: ${message}${metaStr}`;
    })
);

// Create custom format for file output
const fileFormat = winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
);

// Create the logger
const logger = winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    levels: logLevels,
    format: fileFormat,
    defaultMeta: {
        service: 'bakery-mern-backend',
        version: '1.0.0',
        environment: process.env.NODE_ENV || 'development'
    },
    transports: [
        // Error log file (only errors)
        new DailyRotateFile({
            filename: join(logsDir, 'error-%DATE%.log'),
            datePattern: 'YYYY-MM-DD',
            level: 'error',
            handleExceptions: true,
            handleRejections: true,
            maxSize: '20m',
            maxFiles: '14d',
            zippedArchive: true
        }),

        // Combined log file (all levels)
        new DailyRotateFile({
            filename: join(logsDir, 'combined-%DATE%.log'),
            datePattern: 'YYYY-MM-DD',
            handleExceptions: true,
            handleRejections: true,
            maxSize: '20m',
            maxFiles: '14d',
            zippedArchive: true
        }),

        // HTTP access log
        new DailyRotateFile({
            filename: join(logsDir, 'http-%DATE%.log'),
            datePattern: 'YYYY-MM-DD',
            level: 'http',
            maxSize: '20m',
            maxFiles: '7d',
            zippedArchive: true
        })
    ]
});

// Add console transport for development
if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
        format: consoleFormat,
        handleExceptions: true,
        handleRejections: true
    }));
}

// Add console transport for production errors
if (process.env.NODE_ENV === 'production') {
    logger.add(new winston.transports.Console({
        level: 'error',
        format: consoleFormat,
        handleExceptions: true,
        handleRejections: true
    }));
}

// Create a stream object for Morgan HTTP logging
logger.stream = {
    write: function (message) {
        logger.http(message.trim());
    }
};

// Utility functions
logger.logError = (error, context = {}) => {
    const errorInfo = {
        message: error.message,
        stack: error.stack,
        code: error.code,
        ...context
    };

    logger.error('Application Error', errorInfo);
};

logger.logAPICall = (req, res, responseTime) => {
    const logData = {
        method: req.method,
        url: req.originalUrl,
        status: res.statusCode,
        responseTime: `${responseTime}ms`,
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        contentLength: res.get('Content-Length') || 0
    };

    if (res.statusCode >= 400) {
        logger.warn('HTTP Request Warning', logData);
    } else {
        logger.http('HTTP Request', logData);
    }
};

logger.logDatabaseQuery = (query, duration, success = true) => {
    const logData = {
        query: query.length > 500 ? query.substring(0, 500) + '...' : query,
        duration: `${duration}ms`,
        success
    };

    if (success) {
        logger.debug('Database Query', logData);
    } else {
        logger.error('Database Query Failed', logData);
    }
};

logger.logAIRequest = (provider, model, tokens, responseTime, success = true) => {
    const logData = {
        provider,
        model,
        tokens,
        responseTime: `${responseTime}ms`,
        success
    };

    if (success) {
        logger.info('AI Request', logData);
    } else {
        logger.error('AI Request Failed', logData);
    }
};

logger.logUserAction = (userId, action, resource, details = {}) => {
    const logData = {
        userId,
        action,
        resource,
        timestamp: new Date().toISOString(),
        ...details
    };

    logger.info('User Action', logData);
};

// Handle uncaught exceptions and unhandled rejections
process.on('uncaughtException', (error) => {
    logger.error('Uncaught Exception', {
        message: error.message,
        stack: error.stack
    });
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    logger.error('Unhandled Rejection', {
        reason: reason?.message || reason,
        promise: promise.toString()
    });
});

export default logger; 