-- AgriAI Database Schema
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone TEXT UNIQUE NOT NULL,
    name TEXT DEFAULT 'Farmer',
    location TEXT,
    primary_crop TEXT,
    referral_code TEXT UNIQUE,
    referrals INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Diagnoses table
CREATE TABLE IF NOT EXISTS diagnoses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    crop TEXT,
    issue TEXT,
    confidence INTEGER,
    recommendation TEXT,
    risk TEXT,
    method TEXT, -- 'ai' or 'rule-based'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Feedback table (for RLHF)
CREATE TABLE IF NOT EXISTS feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    diagnosis_id UUID REFERENCES diagnoses(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    feedback_type TEXT, -- 'correct', 'incorrect', 'partial'
    actual_issue TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Earnings table (for data marketplace)
CREATE TABLE IF NOT EXISTS earnings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2),
    data_type TEXT,
    buyer TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Buyers table (for data marketplace)
CREATE TABLE IF NOT EXISTS buyers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    organization TEXT,
    api_key TEXT UNIQUE,
    credits DECIMAL(10, 2) DEFAULT 10.00,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);
CREATE INDEX IF NOT EXISTS idx_users_referral_code ON users(referral_code);
CREATE INDEX IF NOT EXISTS idx_diagnoses_user_id ON diagnoses(user_id);
CREATE INDEX IF NOT EXISTS idx_diagnoses_created_at ON diagnoses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_feedback_diagnosis_id ON feedback(diagnosis_id);
CREATE INDEX IF NOT EXISTS idx_earnings_user_id ON earnings(user_id);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE diagnoses ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE earnings ENABLE ROW LEVEL SECURITY;
ALTER TABLE buyers ENABLE ROW LEVEL SECURITY;

-- Create policies (allow all for service role, restrict for anon)
-- For development, we'll allow all. In production, refine these policies.

CREATE POLICY "Allow all for service role - users" ON users
    FOR ALL USING (true);

CREATE POLICY "Allow all for service role - diagnoses" ON diagnoses
    FOR ALL USING (true);

CREATE POLICY "Allow all for service role - feedback" ON feedback
    FOR ALL USING (true);

CREATE POLICY "Allow all for service role - earnings" ON earnings
    FOR ALL USING (true);

CREATE POLICY "Allow all for service role - buyers" ON buyers
    FOR ALL USING (true);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add trigger to users table
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing (optional)
-- Uncomment to add test data

-- INSERT INTO users (phone, name, location, primary_crop, referral_code) VALUES
--     ('+1234567890', 'Test Farmer', 'Nairobi', 'tomato', 'TEST1234');

COMMENT ON TABLE users IS 'Farmers using the platform';
COMMENT ON TABLE diagnoses IS 'AI diagnoses for crop issues';
COMMENT ON TABLE feedback IS 'User feedback for improving AI accuracy (RLHF)';
COMMENT ON TABLE earnings IS 'Farmer earnings from data contributions';
COMMENT ON TABLE buyers IS 'Organizations buying agricultural data insights';
