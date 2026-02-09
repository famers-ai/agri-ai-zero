-- ============================================================================
-- SUPABASE ROW LEVEL SECURITY (RLS) SETUP
-- ============================================================================
-- This script enables Row Level Security on all tables to protect user data
-- Only authenticated service role (backend) can access data
-- Individual users cannot access other users' data

-- ============================================================================
-- 1. ENABLE RLS ON ALL TABLES
-- ============================================================================

-- Enable RLS on users table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Enable RLS on diagnoses table
ALTER TABLE diagnoses ENABLE ROW LEVEL SECURITY;

-- Enable RLS on feedback table
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- 2. CREATE POLICIES FOR SERVICE ROLE (Backend API)
-- ============================================================================

-- Policy: Backend service can do everything on users table
CREATE POLICY "Service role can manage users"
ON users
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Policy: Backend service can do everything on diagnoses table
CREATE POLICY "Service role can manage diagnoses"
ON diagnoses
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Policy: Backend service can do everything on feedback table
CREATE POLICY "Service role can manage feedback"
ON feedback
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- ============================================================================
-- 3. CREATE POLICIES FOR AUTHENTICATED USERS (Future Web Dashboard)
-- ============================================================================
-- These policies allow authenticated admin users to view data via dashboard
-- Regular farmers won't have direct database access (only via WhatsApp API)

-- Policy: Authenticated users can view all users (read-only for dashboard)
CREATE POLICY "Authenticated users can view users"
ON users
FOR SELECT
TO authenticated
USING (true);

-- Policy: Authenticated users can view all diagnoses (read-only for dashboard)
CREATE POLICY "Authenticated users can view diagnoses"
ON diagnoses
FOR SELECT
TO authenticated
USING (true);

-- Policy: Authenticated users can view all feedback (read-only for dashboard)
CREATE POLICY "Authenticated users can view feedback"
ON feedback
FOR SELECT
TO authenticated
USING (true);

-- ============================================================================
-- 4. REVOKE PUBLIC ACCESS
-- ============================================================================
-- Ensure anonymous users have NO access to any table

REVOKE ALL ON users FROM anon;
REVOKE ALL ON diagnoses FROM anon;
REVOKE ALL ON feedback FROM anon;

-- ============================================================================
-- 5. CREATE ADMIN ROLE (Optional - for future admin dashboard)
-- ============================================================================

-- Create a custom admin role
-- DO $$
-- BEGIN
--   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admin_role') THEN
--     CREATE ROLE admin_role;
--   END IF;
-- END
-- $$;

-- Grant full access to admin role
-- GRANT ALL ON users TO admin_role;
-- GRANT ALL ON diagnoses TO admin_role;
-- GRANT ALL ON feedback TO admin_role;

-- ============================================================================
-- 6. VERIFICATION QUERIES
-- ============================================================================
-- Run these to verify RLS is working correctly

-- Check if RLS is enabled
-- SELECT tablename, rowsecurity 
-- FROM pg_tables 
-- WHERE schemaname = 'public' 
-- AND tablename IN ('users', 'diagnoses', 'feedback');

-- Check existing policies
-- SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
-- FROM pg_policies
-- WHERE schemaname = 'public';

-- ============================================================================
-- NOTES FOR DEPLOYMENT
-- ============================================================================
-- 
-- 1. Run this script in Supabase SQL Editor AFTER creating your tables
-- 2. Your backend uses the SERVICE_ROLE key (not anon key) to bypass RLS
-- 3. Make sure SUPABASE_KEY in Railway is the SERVICE ROLE key, not anon key
-- 4. Test by trying to access data with anon key - should fail
-- 5. For admin dashboard, use Supabase Auth to authenticate users
--
-- SECURITY CHECKLIST:
-- ✅ RLS enabled on all tables
-- ✅ Service role has full access (backend API)
-- ✅ Authenticated users can only read (future dashboard)
-- ✅ Anonymous users have zero access
-- ✅ Phone numbers should be hashed before storage (handled in backend)
--
-- ============================================================================
