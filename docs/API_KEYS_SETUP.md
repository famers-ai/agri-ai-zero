# 🔑 API 키 설정 가이드 (5분 완료)

## 📋 필요한 API 키 목록

### 1. Groq AI (무료, 필수) ⭐
**용도**: AI 진단 엔진  
**무료 한도**: 14,400 requests/day  
**획득 방법**:
1. https://console.groq.com/keys 접속
2. Google 계정으로 로그인
3. "Create API Key" 클릭
4. 키 복사 (gsk_로 시작)

**Railway 변수명**: `GROQ_API_KEY`

---

### 2. Supabase (무료, 선택) 
**용도**: 데이터베이스  
**무료 한도**: 500MB storage, 2GB transfer/month  
**획득 방법**:
1. https://supabase.com/dashboard 접속
2. 프로젝트 생성 또는 기존 프로젝트 선택
3. Settings → API 클릭
4. 다음 두 값 복사:
   - **Project URL** (https://xxx.supabase.co)
   - **service_role key** (⚠️ anon key 아님!)

**Railway 변수명**: 
- `SUPABASE_URL`
- `SUPABASE_KEY` (service_role key 사용!)

---

### 3. WhatsApp Business API (무료, 선택)
**용도**: 실제 WhatsApp 메시지 수신  
**무료 한도**: 1,000 conversations/month  
**획득 방법**:
1. https://business.facebook.com 접속
2. WhatsApp Business Platform 설정
3. 다음 값 복사:
   - **Access Token**
   - **Phone Number ID**
   - **Webhook Verify Token** (직접 생성)

**Railway 변수명**:
- `WHATSAPP_ACCESS_TOKEN`
- `WHATSAPP_PHONE_ID`
- `WEBHOOK_VERIFY_TOKEN`

---

## 🚀 Railway에 API 키 추가하기

### 방법 1: Railway Dashboard (권장)
1. https://railway.com/project/c6cdfacb-b0a1-42fe-9678-36f428957f47 접속
2. **web** 서비스 클릭
3. **Variables** 탭 클릭
4. **New Variable** 클릭
5. 다음 형식으로 추가:
   ```
   GROQ_API_KEY=gsk_xxxxxxxxxxxxx
   ```
6. 각 키마다 반복

### 방법 2: Railway CLI (빠름)
```bash
# Railway CLI 설치 (한 번만)
npm install -g @railway/cli

# 프로젝트 연결
railway link c6cdfacb-b0a1-42fe-9678-36f428957f47

# 변수 추가
railway variables set GROQ_API_KEY=gsk_xxxxxxxxxxxxx
railway variables set SUPABASE_URL=https://xxx.supabase.co
railway variables set SUPABASE_KEY=eyJhbGc...
```

---

## ✅ 최소 설정 (바로 시작 가능)

**Groq AI만 설정하면 AI 진단 작동!**

```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

이것만 추가하면:
- ✅ AI 진단 활성화
- ✅ 날씨 정보 제공
- ✅ 대시보드 작동
- ⚠️ 데이터는 메모리에만 저장 (재시작 시 삭제)

---

## 🎯 권장 설정 (프로덕션)

**Groq + Supabase 설정**

```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbGc... (service_role key)
```

이렇게 하면:
- ✅ AI 진단 활성화
- ✅ 데이터 영구 저장
- ✅ 사용자 관리
- ✅ 진단 이력 추적

---

## 🔒 보안 주의사항

### ⚠️ 절대 하지 말 것:
- ❌ GitHub에 API 키 커밋
- ❌ 코드에 직접 키 입력
- ❌ Supabase anon key를 service_role 대신 사용

### ✅ 올바른 방법:
- ✅ Railway Variables에만 저장
- ✅ .env 파일은 .gitignore에 포함
- ✅ service_role key 사용 (RLS 우회 가능)

---

## 📊 설정 후 확인

### 1. Health Check
```bash
curl https://web-production-17eb9.up.railway.app/health
```

**예상 결과**:
```json
{
  "status": "healthy",
  "database": "connected",  // Supabase 설정 시
  "whatsapp": "not configured",
  "version": "2.0.0-stable"
}
```

### 2. Railway Logs 확인
```
2026-02-09 06:19:30 | INFO | AgriAI | startup_event:1185 | 🤖 AI Engine: Groq (Free)
2026-02-09 06:19:30 | INFO | AgriAI | startup_event:1186 | 💾 Database: https://xxx.supabase.co
```

---

## 🎉 완료!

API 키 추가 후:
1. Railway가 자동으로 재배포 (1-2분)
2. Health check로 확인
3. 대시보드 접속하여 테스트

**다음 단계**: Supabase 데이터베이스 스키마 생성 (선택사항)
