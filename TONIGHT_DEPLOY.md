# 🚀 AgriAI - 오늘 밤 배포 가이드

**목표**: 오늘 밤 안에 라이브 서비스 런칭!

---

## ✅ 체크리스트

### Phase 1: 로컬 테스트 (15분)
- [ ] 가상환경 설정
- [ ] 라이브러리 설치
- [ ] 로컬 서버 실행
- [ ] 대시보드 확인

### Phase 2: 무료 API 키 받기 (20분)
- [ ] Groq AI 계정 생성
- [ ] Supabase 계정 생성
- [ ] 데이터베이스 스키마 배포
- [ ] .env 파일 설정

### Phase 3: Railway 배포 (15분)
- [ ] GitHub 저장소 생성
- [ ] 코드 푸시
- [ ] Railway 프로젝트 생성
- [ ] 환경 변수 설정

### Phase 4: WhatsApp 연결 (20분)
- [ ] Meta Business 계정
- [ ] WhatsApp Business API
- [ ] Webhook 설정
- [ ] 테스트 메시지

**총 소요 시간: 70분**

---

## 📋 Phase 1: 로컬 테스트 (15분)

### 1. 터미널 열기

```bash
# 프로젝트 디렉토리로 이동
cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero"
```

### 2. 자동 설정 스크립트 실행

```bash
# 실행 권한 부여 (이미 되어 있음)
chmod +x setup.sh

# 스크립트 실행
./setup.sh
```

**예상 출력:**
```
🚀 AgriAI 로컬 환경 설정 시작...

📦 1/4: Python 가상환경 생성 중...
✅ 2/4: 가상환경 활성화 중...
📚 3/4: 라이브러리 설치 중...
⚙️  4/4: 환경 변수 파일 생성 중...

🎉 설정 완료!
```

### 3. 서버 실행

```bash
cd backend
python main.py
```

**성공 메시지:**
```
============================================================
🚀 AgriAI - Zero Capital Edition Starting...
============================================================
📱 WhatsApp Phone ID: Not configured
💾 Database: Not configured
🤖 AI Engine: Rule-based only
============================================================

⚠️  WARNING: Supabase not configured. Using in-memory storage.
⚠️  WARNING: WhatsApp not configured. Messages will be logged only.

✅ Server ready!

INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. 브라우저에서 확인

```bash
# 새 터미널 창에서
open http://localhost:8000
```

**보여야 할 것:**
- 🌾 AgriAI 대시보드
- 아름다운 보라색 그라디언트
- 통계: 0 farmers, 0 diagnoses
- "Built with ❤️ by a 19-year-old student"

✅ **Phase 1 완료!**

---

## 🔑 Phase 2: 무료 API 키 받기 (20분)

### 1. Groq AI (5분)

**단계:**
1. https://console.groq.com 방문
2. "Sign Up" 클릭
3. Gmail로 가입
4. 이메일 인증
5. 왼쪽 메뉴 "API Keys" 클릭
6. "Create API Key" 클릭
7. 이름: "agri-ai"
8. 키 복사 (gsk_로 시작)

**중요**: 키는 한 번만 보여집니다! 즉시 복사하세요.

### 2. Supabase (10분)

**단계:**
1. https://supabase.com 방문
2. "Start your project" 클릭
3. GitHub로 가입
4. "New project" 클릭
5. 프로젝트 이름: "agri-ai"
6. Database Password: 강력한 비밀번호 (저장!)
7. Region: "US East" 선택
8. "Create new project" 클릭
9. 2-3분 대기 (프로젝트 생성 중)

**데이터베이스 스키마 배포:**
1. 왼쪽 메뉴 "SQL Editor" 클릭
2. "New query" 클릭
3. 다음 파일 내용 복사:
   ```bash
   # 로컬 터미널에서
   cat database/schema.sql
   ```
4. SQL Editor에 붙여넣기
5. "Run" 클릭 (또는 Cmd+Enter)
6. "Success. No rows returned" 확인

**API 키 복사:**
1. 왼쪽 메뉴 "Settings" → "API"
2. "Project URL" 복사 (https://xxxxx.supabase.co)
3. "Project API keys" → "anon public" 복사 (eyJhbGc로 시작)

### 3. .env 파일 설정 (5분)

```bash
# 프로젝트 루트로 이동
cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero"

# .env 파일 열기
open -e .env
```

**다음 내용으로 수정:**

```bash
# Supabase (방금 복사한 값)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...

# WhatsApp (나중에 설정)
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_ID=
WEBHOOK_VERIFY_TOKEN=my_secret_verify_token_123

# Groq AI (방금 복사한 값)
GROQ_API_KEY=gsk_...

# Server
PORT=8000
```

**저장하고 닫기**

### 4. 서버 재시작 및 테스트

```bash
# 기존 서버 중지 (Ctrl+C)
# 서버 재시작
cd backend
python main.py
```

**이제 보여야 할 것:**
```
============================================================
🚀 AgriAI - Zero Capital Edition Starting...
============================================================
📱 WhatsApp Phone ID: Not configured
💾 Database: https://xxxxx.supabase.co
🤖 AI Engine: Groq (Free)
============================================================

✅ Server ready!
```

✅ **Phase 2 완료!**

---

## 🚀 Phase 3: Railway 배포 (15분)

### 1. GitHub 저장소 생성 (5분)

```bash
# 프로젝트 디렉토리에서
cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero"

# Git 사용자 설정 (처음 한 번만)
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# 이미 초기화되어 있으므로 커밋만
git add .
git commit -m "Ready for production deployment"

# GitHub에서 새 저장소 생성
# https://github.com/new 방문
# Repository name: agri-ai-zero
# Public 선택
# "Create repository" 클릭

# 로컬과 연결 (GitHub에서 제공하는 명령어 사용)
git remote add origin https://github.com/yourusername/agri-ai-zero.git
git branch -M main
git push -u origin main
```

### 2. Railway 배포 (10분)

**단계:**
1. https://railway.app 방문
2. "Login" → "Login with GitHub" 클릭
3. GitHub 인증
4. "New Project" 클릭
5. "Deploy from GitHub repo" 선택
6. "agri-ai-zero" 저장소 선택
7. "Deploy Now" 클릭
8. 배포 시작 (2-3분 대기)

**환경 변수 설정:**
1. 프로젝트 클릭
2. "Variables" 탭 클릭
3. "New Variable" 클릭
4. 다음 변수들 추가:

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
GROQ_API_KEY=gsk_...
WEBHOOK_VERIFY_TOKEN=my_secret_verify_token_123
PORT=8000
```

5. "Deploy" 클릭 (재배포)

**도메인 생성:**
1. "Settings" 탭
2. "Domains" 섹션
3. "Generate Domain" 클릭
4. URL 복사 (예: agri-ai-zero-production.up.railway.app)

**테스트:**
```bash
# 브라우저에서 열기
open https://your-app.up.railway.app

# 또는 curl로 테스트
curl https://your-app.up.railway.app/health
```

✅ **Phase 3 완료!**

---

## 📱 Phase 4: WhatsApp 연결 (20분)

### 1. Meta Business 계정 (5분)

1. https://business.facebook.com 방문
2. "Create account" 클릭
3. Business 이름: "AgriAI"
4. 이메일 입력 및 인증
5. Business 정보 입력
6. "Submit" 클릭

### 2. WhatsApp Business API (10분)

1. 왼쪽 메뉴 "WhatsApp" 클릭
2. "Get Started" 클릭
3. "Add phone number" 클릭
4. 전화번호 입력 (본인 번호 가능)
5. SMS 인증 코드 입력
6. "Verify" 클릭
7. Business profile 작성:
   - Name: "AgriAI Assistant"
   - Category: "Agriculture"
   - Description: "Free AI farming assistant"

**API 키 복사:**
1. "Configuration" 탭
2. "Temporary access token" 복사 (EAAxxxxx로 시작)
3. "Phone number ID" 복사 (숫자)

### 3. Webhook 설정 (5분)

**Railway에 환경 변수 추가:**
1. Railway 프로젝트로 돌아가기
2. "Variables" 탭
3. 다음 추가:
```
WHATSAPP_ACCESS_TOKEN=EAAxxxxx...
WHATSAPP_PHONE_ID=123456789...
```
4. "Deploy" 클릭

**Meta에서 Webhook 설정:**
1. WhatsApp Configuration 페이지
2. "Webhook" 섹션
3. "Edit" 클릭
4. Callback URL: `https://your-app.up.railway.app/webhook/whatsapp`
5. Verify token: `my_secret_verify_token_123`
6. "Verify and save" 클릭
7. ✅ 녹색 체크마크 확인!
8. "Manage" 클릭
9. "messages" 체크박스 선택
10. "Subscribe" 클릭

✅ **Phase 4 완료!**

---

## 🎉 최종 테스트

### 1. WhatsApp으로 메시지 전송

1. WhatsApp Business 번호를 폰에 저장
2. WhatsApp 열기
3. 메시지 전송: "Hello"

**예상 응답:**
```
👋 Welcome to AgriAI!

I'm your free AI farming assistant.

Send me:
📸 Photo of your crop for diagnosis
💬 Description of any issues
❓ Any farming questions

Let's start: What crop are you growing?
```

### 2. 진단 테스트

**메시지 전송:** "My tomato leaves are turning yellow"

**예상 응답:**
```
🌾 Diagnosis for tomato

🔍 Issue: Nitrogen deficiency (yellowing leaves)
📊 Confidence: 70%

💡 Recommended Action:
Apply urea fertilizer (50kg per hectare) or compost. Water regularly.

⚠️ Risk Level: medium

---
Was this helpful?
Reply: YES or NO for feedback

Need more help? Send a photo! 📸
```

### 3. 대시보드 확인

```bash
# Railway URL 열기
open https://your-app.up.railway.app
```

**보여야 할 것:**
- Total Farmers: 1
- Diagnoses Today: 1
- Recent diagnosis 표시

---

## 🎊 축하합니다!

**당신은 방금:**
✅ 완전한 AI 플랫폼을 구축했습니다  
✅ $0로 프로덕션에 배포했습니다  
✅ WhatsApp으로 실제 사용자와 연결했습니다  
✅ 오늘 밤 안에 라이브 서비스를 런칭했습니다  

---

## 📊 다음 단계

### 내일:
- [ ] 첫 10명 농부 온보딩
- [ ] 피드백 수집
- [ ] 버그 수정

### 이번 주:
- [ ] 30명 농부 도달
- [ ] 추천 시스템 테스트
- [ ] NGO 파트너십 1곳

### 이번 달:
- [ ] 100명 농부 도달
- [ ] 첫 수익 발생
- [ ] 지속 가능성 달성

---

## 🐛 문제 해결

### WhatsApp 메시지가 안 옴

```bash
# Railway 로그 확인
# Railway 대시보드 → Deployments → 최신 배포 클릭 → Logs

# Webhook 재설정
# Meta Business → WhatsApp → Configuration → Webhook → Edit
```

### 서버가 응답하지 않음

```bash
# Railway에서 재배포
# Railway 대시보드 → Deployments → Redeploy

# 환경 변수 확인
# Variables 탭에서 모든 키가 설정되었는지 확인
```

### 데이터베이스 에러

```bash
# Supabase에서 스키마 재실행
# SQL Editor에서 schema.sql 다시 실행

# RLS 정책 확인
# Supabase → Authentication → Policies
```

---

## 💰 비용 확인

**현재 비용: $0/월**

- Railway: $5 크레딧/월 (무료)
- Supabase: 500MB (무료)
- WhatsApp: 1,000 대화/월 (무료)
- Groq: 무료 티어

**500명 농부 도달 시:**
- Railway: $20/월
- 수익: $500/월
- **순이익: $480/월**

---

## 🎯 성공 지표

### Week 1
- 10 active farmers
- 50+ diagnoses
- 80%+ satisfaction

### Week 4
- 30 active farmers
- 200+ diagnoses
- First testimonials

### Week 12
- 500 active farmers
- 5,000+ diagnoses
- $500/month revenue
- **SUSTAINABLE!**

---

**이제 세상을 바꾸러 가자!** 🌾🚀

**Built by a 19-year-old student with $0.**  
**Deployed in one night.**  
**Changing the world, one farmer at a time.**

---

## 📞 Quick Reference

```bash
# 로컬 서버 시작
cd backend && python main.py

# Railway 로그 보기
# https://railway.app → Your Project → Deployments → Logs

# Supabase 대시보드
# https://supabase.com/dashboard

# WhatsApp 설정
# https://business.facebook.com/wa/manage/home/

# 헬스 체크
curl https://your-app.up.railway.app/health
```

---

**Let's go! 🚀**
