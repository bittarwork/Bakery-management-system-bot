/**
 * GEMINI AI SERVICE
 * Enhanced Gemini AI service compatible with existing Python bot system
 * Provides natural language database queries and analytics
 */

import { GoogleGenerativeAI } from '@google/generative-ai';
import { executeRawQuery, getTableInfo, getDatabaseStats } from '../../config/database.js';
import logger from '../../config/logger.js';

export class GeminiService {
    constructor() {
        this.apiKey = process.env.GEMINI_API_KEY;
        this.model = process.env.GEMINI_MODEL || 'gemini-1.5-pro-latest';

        if (!this.apiKey) {
            throw new Error('GEMINI_API_KEY is required');
        }

        this.genAI = new GoogleGenerativeAI(this.apiKey);
        this.generativeModel = this.genAI.getGenerativeModel({
            model: this.model.includes('gemini') ? this.model : 'gemini-1.5-pro'
        });

        // Initialize system context
        this.systemContext = '';
        this.initializeContext();
    }

    async initializeContext() {
        try {
            const tables = await getTableInfo();
            const stats = await getDatabaseStats();

            this.systemContext = `
You are BakeryBot Pro, an advanced AI assistant for a bakery distribution management system. You help users analyze business data and answer questions about their bakery operations.

SYSTEM INFORMATION:
- Database: MySQL with ${tables.length} tables
- Language Support: Arabic (primary) and English  
- Currency: EUR (primary) and SYP (secondary)
- Current Stats: ${JSON.stringify(stats)}

DATABASE SCHEMA:
${await this.getSchemaContext()}

CAPABILITIES:
- Natural language database queries
- Sales analytics and reporting
- Product inventory management
- Order tracking and processing
- Distributor performance analysis
- Financial summaries and insights
- Multi-currency calculations (EUR/SYP)

RESPONSE GUIDELINES:
1. Always respond in Arabic unless specifically asked in English
2. Provide clear, actionable insights
3. Include relevant numbers and statistics
4. Generate appropriate SQL queries when needed
5. Explain complex data in simple terms
6. Focus on business value and recommendations

IMPORTANT: Only generate SELECT queries. Never modify data.
`;
        } catch (error) {
            logger.error('Failed to initialize Gemini context:', error);
        }
    }

    async getSchemaContext() {
        try {
            const tables = await getTableInfo();
            let schemaContext = '';

            for (const table of tables.slice(0, 10)) { // Limit to first 10 tables
                try {
                    const schema = await getTableInfo(table.table_name);
                    schemaContext += `\nTable: ${table.table_name} (${table.table_rows} rows)\n`;

                    if (schema.columns) {
                        const columns = schema.columns.slice(0, 8); // Limit columns
                        schemaContext += columns.map(col =>
                            `  - ${col.column_name}: ${col.data_type}`
                        ).join('\n') + '\n';
                    }
                } catch (err) {
                    logger.warn(`Failed to get schema for ${table.table_name}:`, err.message);
                }
            }

            return schemaContext;
        } catch (error) {
            logger.error('Error getting schema context:', error);
            return 'Schema information unavailable';
        }
    }

    async processQuestion(question, language = 'ar') {
        try {
            const startTime = Date.now();

            // Prepare the prompt
            const prompt = `
${this.systemContext}

USER QUESTION: ${question}
RESPONSE LANGUAGE: ${language}

Please analyze this question and provide:
1. A helpful response in ${language === 'ar' ? 'Arabic' : 'English'}
2. If data analysis is needed, generate an appropriate SQL query
3. Provide insights and recommendations

Remember: 
- Use currency symbols (€ for EUR, ل.س for SYP)  
- Format numbers properly
- Be conversational and helpful
- Focus on actionable business insights
`;

            // Get AI response
            const result = await this.generativeModel.generateContent(prompt);
            const response = await result.response;
            const text = response.text();

            // Extract SQL query if present
            const sqlMatch = text.match(/```sql\n([\s\S]*?)\n```/i);
            let sqlQuery = null;
            let queryResults = [];

            if (sqlMatch) {
                sqlQuery = sqlMatch[1].trim();

                // Execute the query if it's a SELECT statement
                if (sqlQuery.toUpperCase().startsWith('SELECT')) {
                    try {
                        const queryResult = await executeRawQuery(sqlQuery);
                        if (queryResult.success) {
                            queryResults = queryResult.results;
                        }
                    } catch (queryError) {
                        logger.warn('Query execution failed:', queryError.message);
                    }
                }
            }

            const processingTime = Date.now() - startTime;

            // Log the AI request
            logger.logAIRequest(
                'gemini',
                this.model,
                this.estimateTokens(prompt + text),
                processingTime,
                true
            );

            return {
                success: true,
                question: question,
                response: text,
                analysis: text,
                sql_query: sqlQuery,
                results: queryResults,
                tokens_used: this.estimateTokens(prompt + text),
                processing_time: processingTime / 1000,
                model_used: this.model,
                language: language
            };

        } catch (error) {
            logger.error('Gemini processing error:', error);

            return {
                success: false,
                error: error.message,
                question: question,
                response: language === 'ar' ?
                    'عذراً، حدث خطأ في معالجة استفسارك. يرجى المحاولة مرة أخرى.' :
                    'Sorry, there was an error processing your question. Please try again.',
                analysis: '',
                language: language
            };
        }
    }

    async getAnalyticsReport(reportType = 'comprehensive') {
        try {
            const stats = await getDatabaseStats();

            const analyticsPrompt = `
${this.systemContext}

Generate a ${reportType} analytics report for the bakery business based on current data:
${JSON.stringify(stats, null, 2)}

Please provide:
1. Executive summary in Arabic
2. Key performance indicators
3. Trends analysis  
4. Recommendations for improvement
5. Financial insights with EUR/SYP breakdown

Focus on actionable business insights and growth opportunities.
`;

            const result = await this.generativeModel.generateContent(analyticsPrompt);
            const response = await result.response;
            const reportText = response.text();

            // Structure the report
            return {
                type: reportType,
                generated_at: new Date().toISOString(),
                summary: reportText,
                data_points: stats,
                recommendations: this.extractRecommendations(reportText),
                key_metrics: {
                    total_users: stats.users || 0,
                    total_products: stats.products || 0,
                    total_orders: stats.orders || 0,
                    revenue_eur: stats.total_revenue_eur || 0,
                    revenue_syp: stats.total_revenue_syp || 0
                }
            };

        } catch (error) {
            logger.error('Analytics report generation error:', error);

            return {
                type: reportType,
                error: error.message,
                generated_at: new Date().toISOString(),
                summary: 'تعذر إنشاء التقرير التحليلي في الوقت الحالي'
            };
        }
    }

    extractRecommendations(reportText) {
        // Extract recommendation points from the report
        const lines = reportText.split('\n');
        const recommendations = [];

        let inRecommendations = false;

        for (const line of lines) {
            if (line.includes('توصيات') || line.includes('Recommendations')) {
                inRecommendations = true;
                continue;
            }

            if (inRecommendations && (line.startsWith('-') || line.startsWith('•') || line.startsWith('*'))) {
                recommendations.push(line.replace(/^[-•*]\s*/, '').trim());
            }
        }

        return recommendations.slice(0, 5); // Limit to top 5
    }

    estimateTokens(text) {
        // Rough token estimation (4 characters ≈ 1 token for Arabic/English)
        return Math.ceil(text.length / 4);
    }

    async clearCache() {
        // This would clear any internal caching if implemented
        return { success: true, message: 'Gemini service cache cleared' };
    }

    async getSystemInfo() {
        try {
            const tables = await getTableInfo();
            const stats = await getDatabaseStats();

            return `
أنا BakeryBot Pro، مساعدك الذكي لإدارة المخبز والتوزيع.

📊 معلومات النظام:
- قاعدة البيانات: ${tables.length} جدول
- المستخدمين: ${stats.users || 0}
- المنتجات: ${stats.products || 0}  
- الطلبات: ${stats.orders || 0}
- الإيرادات: €${stats.total_revenue_eur || 0}

🤖 قدراتي:
- تحليل البيانات بالذكاء الاصطناعي
- استعلامات باللغة الطبيعية
- تقارير المبيعات والأداء
- متابعة المخزون والطلبات
- تحليل أداء الموزعين

اسألني أي سؤال حول عملك!
`;
        } catch (error) {
            logger.error('Error getting Gemini system info:', error);
            return 'أنا BakeryBot Pro، مساعدك الذكي لإدارة المخبز. أواجه صعوبة في الوصول للبيانات حالياً.';
        }
    }
} 