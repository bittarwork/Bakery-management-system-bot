/**
 * DATABASE CONFIGURATION
 * Sequelize configuration for MySQL database connection
 * Uses the same database as the existing Python bot system
 */

import { Sequelize } from 'sequelize';
import dotenv from 'dotenv';
import logger from './logger.js';

dotenv.config();

// Database configuration
const config = {
    host: process.env.DB_HOST || 'shinkansen.proxy.rlwy.net',
    port: process.env.DB_PORT || 24785,
    database: process.env.DB_NAME || 'railway',
    username: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || 'ZEsGFfzwlnsvgvcUiNsvGraAKFnuVZRA',
    dialect: 'mysql',
    dialectOptions: {
        charset: 'utf8mb4',
        collate: 'utf8mb4_unicode_ci',
        connectTimeout: 60000,
        acquireTimeout: 60000,
        timeout: 60000,
        ssl: process.env.NODE_ENV === 'production' ? {
            rejectUnauthorized: false
        } : false
    },
    pool: {
        max: 10,
        min: 0,
        acquire: 30000,
        idle: 10000
    },
    logging: process.env.NODE_ENV === 'development' ?
        (msg) => logger.debug('DB Query:', msg) : false,
    timezone: '+01:00', // Brussels timezone
    define: {
        timestamps: true,
        underscored: false,
        freezeTableName: true,
        charset: 'utf8mb4',
        collate: 'utf8mb4_unicode_ci'
    }
};

// Create Sequelize instance
const sequelize = new Sequelize(
    config.database,
    config.username,
    config.password,
    config
);

// Test database connection
const connectDB = async () => {
    try {
        await sequelize.authenticate();
        logger.info(`✅ Database connected successfully to ${config.host}:${config.port}/${config.database}`);

        // Get database info
        const [results] = await sequelize.query('SELECT VERSION() as version, DATABASE() as database_name, USER() as user');
        const dbInfo = results[0];

        logger.info(`📊 MySQL Version: ${dbInfo.version}`);
        logger.info(`📋 Current Database: ${dbInfo.database_name}`);
        logger.info(`👤 Database User: ${dbInfo.user}`);

        return true;
    } catch (error) {
        logger.error('❌ Database connection failed:', {
            message: error.message,
            code: error.original?.code,
            sqlState: error.original?.sqlState,
            host: config.host,
            port: config.port,
            database: config.database
        });
        throw error;
    }
};

// Database health check
const checkDatabaseHealth = async () => {
    try {
        await sequelize.query('SELECT 1+1 as result');
        return {
            status: 'healthy',
            timestamp: new Date().toISOString(),
            connection: 'active'
        };
    } catch (error) {
        return {
            status: 'unhealthy',
            error: error.message,
            timestamp: new Date().toISOString(),
            connection: 'failed'
        };
    }
};

// Get table information (for compatibility with existing Python system)
const getTableInfo = async (tableName = null) => {
    try {
        if (tableName) {
            // Get specific table schema
            const [results] = await sequelize.query(`
                SELECT 
                    COLUMN_NAME as column_name,
                    DATA_TYPE as data_type,
                    IS_NULLABLE as is_nullable,
                    COLUMN_DEFAULT as column_default,
                    COLUMN_KEY as column_key,
                    EXTRA as extra
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = '${config.database}' 
                AND TABLE_NAME = '${tableName}'
                ORDER BY ORDINAL_POSITION
            `);

            return {
                table_name: tableName,
                columns: results
            };
        } else {
            // Get all tables
            const [results] = await sequelize.query(`
                SELECT TABLE_NAME as table_name, TABLE_ROWS as table_rows
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = '${config.database}' 
                AND TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            `);

            return results;
        }
    } catch (error) {
        logger.error('Error getting table info:', error);
        throw error;
    }
};

// Execute raw SQL queries (for compatibility with Python bot system)
const executeRawQuery = async (query, replacements = {}) => {
    try {
        const [results, metadata] = await sequelize.query(query, {
            replacements,
            type: Sequelize.QueryTypes.SELECT
        });

        return {
            success: true,
            results,
            count: results.length,
            metadata
        };
    } catch (error) {
        logger.error('Raw query execution failed:', error);
        return {
            success: false,
            error: error.message,
            results: [],
            count: 0
        };
    }
};

// Get database statistics
const getDatabaseStats = async () => {
    try {
        const queries = {
            users: "SELECT COUNT(*) as count FROM users",
            products: "SELECT COUNT(*) as count FROM products",
            orders: "SELECT COUNT(*) as count FROM orders",
            stores: "SELECT COUNT(*) as count FROM stores",
            distributors: "SELECT COUNT(*) as count FROM distributors",
            order_items: "SELECT COUNT(*) as count FROM order_items"
        };

        const stats = {};

        for (const [key, query] of Object.entries(queries)) {
            try {
                const [results] = await sequelize.query(query);
                stats[key] = results[0].count;
            } catch (error) {
                logger.warn(`Failed to get count for ${key}:`, error.message);
                stats[key] = 0;
            }
        }

        // Get total revenue
        try {
            const [revenueResults] = await sequelize.query(`
                SELECT 
                    SUM(final_amount_eur) as total_eur,
                    SUM(final_amount_syp) as total_syp
                FROM orders 
                WHERE payment_status = 'paid'
            `);

            stats.total_revenue_eur = revenueResults[0].total_eur || 0;
            stats.total_revenue_syp = revenueResults[0].total_syp || 0;
        } catch (error) {
            logger.warn('Failed to get revenue stats:', error.message);
            stats.total_revenue_eur = 0;
            stats.total_revenue_syp = 0;
        }

        return stats;
    } catch (error) {
        logger.error('Error getting database stats:', error);
        throw error;
    }
};

// Close database connection
const closeDB = async () => {
    try {
        await sequelize.close();
        logger.info('Database connection closed successfully');
    } catch (error) {
        logger.error('Error closing database connection:', error);
        throw error;
    }
};

export {
    sequelize,
    connectDB,
    closeDB,
    checkDatabaseHealth,
    getTableInfo,
    executeRawQuery,
    getDatabaseStats
}; 