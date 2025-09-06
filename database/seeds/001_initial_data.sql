-- Initial seed data for Ledgerly
-- Run after tables are created

-- Insert default institutions
INSERT INTO institutions (id, name, slug, website) VALUES
    ('550e8400-e29b-41d4-a716-446655440000', 'Citibank', 'citi', 'https://www.citi.com'),
    ('550e8400-e29b-41d4-a716-446655440001', 'Chase', 'chase', 'https://www.chase.com'),
    ('550e8400-e29b-41d4-a716-446655440002', 'Bank of America', 'boa', 'https://www.bankofamerica.com'),
    ('550e8400-e29b-41d4-a716-446655440003', 'Wells Fargo', 'wells_fargo', 'https://www.wellsfargo.com'),
    ('550e8400-e29b-41d4-a716-446655440004', 'Capital One', 'capital_one', 'https://www.capitalone.com')
ON CONFLICT (id) DO NOTHING;

-- Insert default account types
INSERT INTO account_types (id, name, slug, description, parser_config) VALUES
    ('660e8400-e29b-41d4-a716-446655440000', 'Credit Card', 'credit_card', 'Standard credit card account', '{"supports_pdf": true, "supports_csv": true, "default_currency": "USD"}'),
    ('660e8400-e29b-41d4-a716-446655440001', 'Checking Account', 'checking', 'Standard checking account', '{"supports_pdf": true, "supports_csv": true, "default_currency": "USD"}'),
    ('660e8400-e29b-41d4-a716-446655440002', 'Savings Account', 'savings', 'Standard savings account', '{"supports_pdf": true, "supports_csv": true, "default_currency": "USD"}'),
    ('660e8400-e29b-41d4-a716-446655440003', 'Investment Account', 'investment', 'Investment/brokerage account', '{"supports_pdf": true, "supports_csv": true, "default_currency": "USD"}')
ON CONFLICT (id) DO NOTHING;

-- Create default categories for transactions
INSERT INTO transaction_categories (name, slug, color, icon) VALUES
    ('Groceries', 'groceries', '#10b981', 'shopping-cart'),
    ('Restaurants', 'restaurants', '#f59e0b', 'utensils'),
    ('Gas & Fuel', 'gas', '#ef4444', 'gas-pump'),
    ('Shopping', 'shopping', '#8b5cf6', 'shopping-bag'),
    ('Bills & Utilities', 'bills', '#6b7280', 'receipt'),
    ('Healthcare', 'healthcare', '#06b6d4', 'heart'),
    ('Transportation', 'transportation', '#84cc16', 'car'),
    ('Entertainment', 'entertainment', '#f97316', 'film'),
    ('Travel', 'travel', '#3b82f6', 'airplane'),
    ('Income', 'income', '#22c55e', 'plus-circle'),
    ('Refunds', 'refunds', '#22c55e', 'arrow-uturn-left'),
    ('Fees', 'fees', '#dc2626', 'minus-circle'),
    ('Other', 'other', '#9ca3af', 'question-mark-circle')
ON CONFLICT (slug) DO NOTHING;

-- Insert a demo user for development (password is 'demo_password' hashed)
INSERT INTO users (id, email, password_hash, is_active) VALUES
    ('demo-user-uuid-000000000000000', 'demo@ledgerly.local', '$2b$12$dummy.hash.for.development.only', true)
ON CONFLICT (email) DO NOTHING;

SELECT log_statement('Initial seed data inserted successfully');
