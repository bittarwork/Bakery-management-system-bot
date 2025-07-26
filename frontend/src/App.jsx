/**
 * MAIN APP COMPONENT
 * Root application component with routing and layout
 */

import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

// Components (to be created)
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import BotPage from './pages/BotPage';
import Products from './pages/Products';
import Orders from './pages/Orders';
import Stores from './pages/Stores';
import Analytics from './pages/Analytics';

// Error boundary for route-specific errors
import ErrorBoundary from './components/Common/ErrorBoundary';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 font-arabic rtl">
      <ErrorBoundary>
        <Layout>
          <Routes>
            {/* Dashboard - Main landing page */}
            <Route path="/" element={<Dashboard />} />
            
            {/* Bot Integration - Original bot as a page */}
            <Route path="/bot" element={<BotPage />} />
            
            {/* Management pages */}
            <Route path="/products" element={<Products />} />
            <Route path="/orders" element={<Orders />} />
            <Route path="/stores" element={<Stores />} />
            <Route path="/analytics" element={<Analytics />} />
            
            {/* Redirect any unknown routes to dashboard */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      </ErrorBoundary>
    </div>
  );
}

export default App; 