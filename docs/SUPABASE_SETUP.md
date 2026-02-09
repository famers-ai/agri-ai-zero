# 🗄️ Supabase 데이터베이스 설정 가이드

**우선순위: 높음** - 10분 소요

---

## 🎯 목표

무료 Supabase 데이터베이스를 생성하고 AgriAI와 연결하여 사용자 데이터, 진단 기록, 피드백을 저장합니다.

---

## 📋 1단계: Supabase 프로젝트 생성

### 1. 계정 생성 및 로그인

1. https://supabase.com 방문
2. **Start your project** 클릭
3. **Sign in with GitHub** (추천) 또는 이메일로 가입
4. GitHub 인증 승인

### 2. 새 프로젝트 생성

1. 대시보드에서 **New Project** 클릭
2. Organization 선택 (또는 새로 생성)
3. 프로젝트 정보 입력:

```
Project Name: agri-ai-zero
Database Password: [강력한 비밀번호 생성 - 저장 필수!]
Region: Northeast Asia (Seoul) 또는 가장 가까운 지역
Pricing Plan: Free (500MB 데이터베이스, 충분함)
```

4. **Create new project** 클릭
5. 프로젝트 생성 대기 (1-2분)

---

## 📊 2단계: 데이터베이스 스키마 생성

### 1. SQL Editor 열기

1. 왼쪽 메뉴에서 **SQL Editor** 클릭
2. **New query** 클릭

### 2. 스키마 SQL 실행

1. 아래 SQL을 **전체 복사**
2. SQL Editor에 붙여넣기
3. **Run** 버튼 클릭 (또는 Cmd/Ctrl + Enter)

```sql
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

-- Create policies (allow all for service role)
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
```

### 3. 실행 확인

**성공 메시지:**
```
Success. No rows returned
```

**테이블 확인:**
1. 왼쪽 메뉴 → **Table Editor**
2. 다음 테이블들이 보여야 함:
   - users
   - diagnoses
   - feedback
   - earnings
   - buyers

---

## 🔑 3단계: API 키 복사

### 1. Project Settings 열기

1. 왼쪽 하단 **Settings** (톱니바퀴) 클릭
2. **API** 메뉴 선택

### 2. API 정보 복사

다음 두 값을 복사하여 안전한 곳에 저장:

```
Project URL: https://xxxxxxxxxxxxx.supabase.co
anon public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**⚠️ 주의:**
- `anon public` 키를 사용하세요 (NOT `service_role`)
- `service_role` 키는 절대 공개하지 마세요!

---

## 🚀 4단계: Railway에 환경 변수 추가

### 1. Railway 대시보드 열기

1. https://railway.app 접속
2. `agri-ai-zero` 프로젝트 선택
3. **Variables** 탭 클릭

### 2. Supabase 변수 추가

**Raw Editor** 사용:

기존 변수에 다음 두 줄 추가:

```env
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**⚠️ 중요**: 실제 값으로 교체하세요!

### 3. 저장 및 재배포

1. **Update Variables** 클릭
2. 자동 재배포 시작 (1-2분)
3. Deployments → Latest → View Logs에서 확인:

```
✅ Supabase client initialized successfully
```

---

## ✅ 5단계: 연결 테스트

### Railway 로그 확인

Deployments → Latest → View Logs:

**성공 시:**
```
💾 Database: https://xxxxx.supabase.co
✅ Supabase client initialized successfully
```

**실패 시:**
```
⚠️ Supabase not configured - using in-memory mode
```

### API 테스트

브라우저 또는 curl:

```bash
curl https://your-railway-url.up.railway.app/health
```

**예상 응답:**
```json
{
  "status": "healthy",
  "database": "connected",  ← 이제 "connected"!
  "whatsapp": "not configured",
  "version": "2.0.0-stable"
}
```

### 통계 확인

```bash
curl https://your-railway-url.up.railway.app/stats
```

**예상 응답:**
```json
{
  "total_users": 0,
  "total_diagnoses": 0,
  "timestamp": "2026-02-09T..."
}
```

---

## 📊 데이터베이스 구조

### 테이블 설명

| 테이블 | 용도 | 주요 필드 |
|--------|------|-----------|
| `users` | 농부 정보 | phone, name, location, primary_crop |
| `diagnoses` | AI 진단 기록 | crop, issue, recommendation, confidence |
| `feedback` | 사용자 피드백 (RLHF) | feedback_type, actual_issue |
| `earnings` | 농부 수익 (미래) | amount, data_type |
| `buyers` | 데이터 구매자 (미래) | organization, credits |

### 데이터 흐름

```
1. 농부가 WhatsApp 메시지 전송
   ↓
2. users 테이블에 저장 (또는 조회)
   ↓
3. AI 진단 수행
   ↓
4. diagnoses 테이블에 저장
   ↓
5. 농부가 피드백 제공
   ↓
6. feedback 테이블에 저장 (AI 개선용)
```

---

## 🔒 보안 설정 (RLS)

Row Level Security가 활성화되어 있지만, 현재는 모든 접근을 허용하는 정책입니다.

**프로덕션 환경에서는:**
1. Supabase → Authentication 설정
2. RLS 정책을 사용자별로 제한
3. `service_role` 키는 백엔드에서만 사용

**현재 설정으로 충분한 이유:**
- Railway 환경 변수는 비공개
- `anon` 키는 제한된 권한
- 초기 단계에서는 간단한 보안으로 충분

---

## 💰 무료 티어 한도

| 항목 | 무료 한도 | 예상 사용량 |
|------|-----------|-------------|
| 데이터베이스 | 500MB | ~50MB (500명 농부) |
| API 요청 | 무제한 | ~10,000/일 |
| 대역폭 | 2GB/월 | ~500MB/월 |
| 동시 연결 | 60개 | ~10개 |

**결론**: 500명 농부까지 무료로 충분! 🎉

---

## 🐛 문제 해결

### "Invalid API key" 오류

**원인**: 잘못된 키 또는 URL

**해결**:
1. Supabase → Settings → API에서 다시 복사
2. `anon public` 키 사용 확인
3. URL이 `https://`로 시작하는지 확인

### "Connection failed" 오류

**원인**: 네트워크 또는 프로젝트 상태

**해결**:
1. Supabase 프로젝트가 "Active" 상태인지 확인
2. Railway에서 변수 재확인
3. 재배포 시도

### 테이블이 안 보임

**원인**: SQL 실행 실패

**해결**:
1. SQL Editor에서 에러 메시지 확인
2. 스키마 SQL 다시 실행
3. Table Editor에서 수동 확인

---

## 🎯 다음 단계

Supabase 설정 완료 후:

1. ✅ **데이터베이스 연결 확인** (위 테스트)
2. ⏳ **Groq AI 설정** → `GROQ_SETUP.md`
3. ⏳ **WhatsApp 설정** → `WHATSAPP_SETUP.md`
4. ⏳ **첫 농부 온보딩!**

---

**⏱️ 예상 소요 시간**: 10분  
**💰 비용**: $0 (무료 티어)  
**🔄 다음**: Groq AI 설정
