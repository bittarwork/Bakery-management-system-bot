-- Sample Bakery Management Database Schema and Data
-- This file contains sample tables and data for testing the bot

-- Create tables for a typical bakery management system

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    total_orders INTEGER DEFAULT 0,
    total_spent DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(20),
    delivery_address TEXT
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL
);

-- Employees table
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE,
    email VARCHAR(100),
    phone VARCHAR(20)
);

-- Sales table (for tracking daily sales)
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    total_revenue DECIMAL(10,2) DEFAULT 0.00,
    total_orders INTEGER DEFAULT 0,
    total_items_sold INTEGER DEFAULT 0
);

-- Insert sample data

-- Sample products
INSERT INTO products (name, description, price, cost, stock_quantity, category) VALUES
('Chocolate Cake', 'Delicious chocolate cake with cream filling', 25.00, 12.00, 15, 'Cakes'),
('Bread Loaf', 'Fresh baked bread', 3.50, 1.50, 50, 'Bread'),
('Croissant', 'Buttery French croissant', 2.50, 1.00, 30, 'Pastries'),
('Muffin', 'Blueberry muffin', 2.00, 0.80, 40, 'Pastries'),
('Cheesecake', 'New York style cheesecake', 30.00, 15.00, 8, 'Cakes'),
('Donut', 'Glazed donut', 1.50, 0.60, 60, 'Pastries'),
('Pizza', 'Margherita pizza', 18.00, 8.00, 12, 'Savory'),
('Sandwich', 'Chicken sandwich', 8.50, 4.00, 25, 'Savory'),
('Cookie', 'Chocolate chip cookie', 1.00, 0.40, 100, 'Cookies'),
('Brownie', 'Fudge brownie', 2.50, 1.20, 35, 'Cookies');

-- Sample customers
INSERT INTO customers (name, email, phone, address, total_orders, total_spent) VALUES
('John Smith', 'john@email.com', '+1234567890', '123 Main St, City', 5, 150.00),
('Sarah Johnson', 'sarah@email.com', '+1234567891', '456 Oak Ave, Town', 3, 85.50),
('Mike Wilson', 'mike@email.com', '+1234567892', '789 Pine Rd, Village', 8, 220.00),
('Lisa Brown', 'lisa@email.com', '+1234567893', '321 Elm St, Borough', 2, 45.00),
('David Lee', 'david@email.com', '+1234567894', '654 Maple Dr, County', 6, 180.00),
('Emma Davis', 'emma@email.com', '+1234567895', '987 Cedar Ln, District', 4, 95.00),
('Alex Turner', 'alex@email.com', '+1234567896', '147 Birch Way, Area', 7, 160.00),
('Maria Garcia', 'maria@email.com', '+1234567897', '258 Spruce Ct, Zone', 1, 25.00);

-- Sample employees
INSERT INTO employees (name, position, salary, hire_date, email, phone) VALUES
('Robert Baker', 'Head Baker', 45000.00, '2020-01-15', 'robert@bakery.com', '+1234567900'),
('Jennifer Cook', 'Assistant Baker', 35000.00, '2020-03-20', 'jennifer@bakery.com', '+1234567901'),
('Michael Sales', 'Sales Manager', 40000.00, '2019-11-10', 'michael@bakery.com', '+1234567902'),
('Amanda Cashier', 'Cashier', 28000.00, '2021-02-01', 'amanda@bakery.com', '+1234567903'),
('Tom Delivery', 'Delivery Driver', 32000.00, '2020-06-15', 'tom@bakery.com', '+1234567904');

-- Sample orders
INSERT INTO orders (customer_id, order_date, total_amount, status, payment_method, delivery_address) VALUES
(1, '2024-01-15 10:30:00', 45.00, 'completed', 'credit_card', '123 Main St, City'),
(2, '2024-01-15 11:15:00', 28.50, 'completed', 'cash', '456 Oak Ave, Town'),
(3, '2024-01-15 12:00:00', 65.00, 'completed', 'credit_card', '789 Pine Rd, Village'),
(4, '2024-01-15 14:20:00', 25.00, 'completed', 'cash', '321 Elm St, Borough'),
(5, '2024-01-15 16:45:00', 52.00, 'completed', 'credit_card', '654 Maple Dr, County'),
(6, '2024-01-16 09:30:00', 35.00, 'completed', 'cash', '987 Cedar Ln, District'),
(7, '2024-01-16 10:15:00', 48.00, 'completed', 'credit_card', '147 Birch Way, Area'),
(8, '2024-01-16 11:00:00', 25.00, 'pending', 'cash', '258 Spruce Ct, Zone'),
(1, '2024-01-16 13:30:00', 38.00, 'completed', 'credit_card', '123 Main St, City'),
(3, '2024-01-16 15:45:00', 72.00, 'completed', 'credit_card', '789 Pine Rd, Village');

-- Sample order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(1, 1, 1, 25.00, 25.00),
(1, 3, 2, 2.50, 5.00),
(1, 6, 5, 1.50, 7.50),
(1, 9, 7, 1.00, 7.50),
(2, 2, 3, 3.50, 10.50),
(2, 4, 2, 2.00, 4.00),
(2, 5, 1, 30.00, 30.00),
(2, 8, 2, 8.50, 17.00),
(3, 1, 2, 25.00, 50.00),
(3, 7, 1, 18.00, 18.00),
(3, 10, 3, 2.50, 7.50),
(4, 3, 4, 2.50, 10.00),
(4, 6, 10, 1.50, 15.00),
(5, 5, 1, 30.00, 30.00),
(5, 8, 2, 8.50, 17.00),
(5, 9, 5, 1.00, 5.00),
(6, 2, 5, 3.50, 17.50),
(6, 4, 3, 2.00, 6.00),
(6, 10, 5, 2.50, 12.50),
(7, 1, 1, 25.00, 25.00),
(7, 3, 3, 2.50, 7.50),
(7, 6, 8, 1.50, 12.00),
(7, 9, 3, 1.00, 3.50),
(8, 5, 1, 25.00, 25.00),
(9, 2, 4, 3.50, 14.00),
(9, 4, 2, 2.00, 4.00),
(9, 7, 1, 18.00, 18.00),
(9, 9, 2, 1.00, 2.00),
(10, 1, 2, 25.00, 50.00),
(10, 3, 4, 2.50, 10.00),
(10, 6, 8, 1.50, 12.00);

-- Sample sales data
INSERT INTO sales (date, total_revenue, total_orders, total_items_sold) VALUES
('2024-01-15', 215.50, 5, 45),
('2024-01-16', 180.00, 5, 38),
('2024-01-17', 195.00, 6, 42),
('2024-01-18', 220.00, 7, 50),
('2024-01-19', 180.50, 5, 35),
('2024-01-20', 250.00, 8, 55),
('2024-01-21', 210.00, 6, 48);

-- Update customer totals based on orders
UPDATE customers SET 
    total_orders = (SELECT COUNT(*) FROM orders WHERE customer_id = customers.id),
    total_spent = (SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE customer_id = customers.id); 