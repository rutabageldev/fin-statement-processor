-- Ledgerly Database Initialization Script
-- PostgreSQL 15+ required

-- Create database if not exists (handled by Docker compose)
-- This file contains initial database setup

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For full-text search

-- Set timezone
SET timezone = 'UTC';

-- Create application user (if not exists)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ledgerly_app') THEN
        CREATE ROLE ledgerly_app WITH LOGIN PASSWORD 'dev_password'; -- pragma: allowlist secret
    END IF;
END
$$;

-- Grant necessary permissions
GRANT CONNECT ON DATABASE ledgerly TO ledgerly_app;
GRANT USAGE ON SCHEMA public TO ledgerly_app;
GRANT CREATE ON SCHEMA public TO ledgerly_app;

-- Create audit function for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create logging function for development
CREATE OR REPLACE FUNCTION log_statement(message text)
RETURNS void AS $$
BEGIN
    RAISE NOTICE '%', message;
END;
$$ LANGUAGE plpgsql;

SELECT log_statement('Ledgerly database initialization completed successfully');
