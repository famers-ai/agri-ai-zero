# 🚀 Railway 배포 가이드

**목표**: AgriAI를 Railway에 배포하여 전 세계에서 접근 가능하게 만들기

**소요 시간**: 15분

---

## 📋 사전 준비

✅ 로컬 서버 실행 성공  
✅ GitHub 계정 (https://github.com)  
✅ Railway 계정 (https://railway.app)  
⏳ 무료 API 키 (선택사항 - 나중에 추가 가능)

---

## 1️⃣ GitHub 저장소 생성 (5분)

### 방법 1: GitHub 웹사이트에서

1. https://github.com/new 방문
2. Repository name: `agri-ai-zero`
3. Description: "Zero-cost AI farming assistant via WhatsApp"
4. **Public** 선택 (무료 배포를 위해)
5. **Create repository** 클릭

### 방법 2: 터미널에서 (GitHub CLI 필요)

```bash
# GitHub CLI 설치 확인
gh --version

# 저장소 생성
gh repo create agri-ai-zero --public --source=. --remote=origin
```

### 로컬 저장소 연결

```bash
cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero"

# Git 사용자 설정 (처음 한 번만)
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# 원격 저장소 연결 (GitHub에서 제공하는 URL 사용)
git remote add origin https://github.com/yourusername/agri-ai-zero.git

# 브랜치 이름 확인/변경
git branch -M main

# 푸시
git push -u origin main
```

**중요**: `.env` 파일은 `.gitignore`에 포함되어 있어 푸시되지 않습니다!

---

## 2️⃣ Railway 프로젝트 생성 (5분)

### 계정 생성

1. https://railway.app 방문
2. **Login** 클릭
3. **Login with GitHub** 선택
4. GitHub 인증 승인

### 프로젝트 생성

1. **New Project** 클릭
2. **Deploy from GitHub repo** 선택
3. **Configure GitHub App** 클릭 (처음 한 번만)
4. 저장소 접근 권한 부여
5. `agri-ai-zero` 저장소 선택
6. **Deploy Now** 클릭

**배포 시작!** (2-3분 소요)

---

## 3️⃣ 환경 변수 설정 (5분)

### Railway 대시보드에서

1. 배포된 프로젝트 클릭
2. **Variables** 탭 클릭
3. **New Variable** 클릭

### 필수 환경 변수

```bash
# 서버 설정
PORT=8000

# Webhook 토큰 (임의의 문자열)
WEBHOOK_VERIFY_TOKEN=my_secret_verify_token_12345

# Supabase (나중에 추가 가능)
SUPABASE_URL=
SUPABASE_KEY=

# WhatsApp (나중에 추가 가능)
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_ID=

# Groq AI (나중에 추가 가능)
GROQ_API_KEY=
```

**중요**: 빈 값으로 두어도 서버는 작동합니다 (규칙 기반 모드)

### 변수 추가 방법

**옵션 1: 하나씩 추가**
1. Variable name: `PORT`
2. Variable value: `8000`
3. **Add** 클릭
4. 다른 변수들도 반복

**옵션 2: Raw Editor 사용**
1. **Raw Editor** 클릭
2. 다음 내용 붙여넣기:
```
PORT=8000
WEBHOOK_VERIFY_TOKEN=my_secret_verify_token_12345
SUPABASE_URL=
SUPABASE_KEY=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_ID=
GROQ_API_KEY=
```
3. **Update Variables** 클릭

### 재배포

환경 변수 추가 후 자동으로 재배포됩니다.

---

## 4️⃣ 도메인 생성 (1분)

### Railway에서 도메인 받기

1. **Settings** 탭 클릭
2. **Domains** 섹션 찾기
3. **Generate Domain** 클릭
4. URL 복사 (예: `agri-ai-zero-production.up.railway.app`)

---

## 5️⃣ 배포 확인 (2분)

### 배포 로그 확인

1. **Deployments** 탭 클릭
2. 최신 배포 클릭
3. **View Logs** 클릭

**성공 메시지 확인:**
```
🚀 AgriAI - Zero Capital Edition Starting...
============================================================
✅ Server ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 브라우저에서 테스트

```bash
# 브라우저에서 열기
https://your-app.up.railway.app

# 또는 curl로 테스트
curl https://your-app.up.railway.app/health
```

**예상 응답:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-09T...",
  "database": "not configured",
  "whatsapp": "not configured"
}
```

---

## 🎉 배포 완료!

**당신의 AgriAI 플랫폼이 이제 라이브입니다!**

- ✅ 전 세계에서 접근 가능
- ✅ 자동 HTTPS
- ✅ 무료 호스팅 ($5 크레딧/월)
- ✅ 자동 배포 (git push 시)

---

## 📊 비용 확인

### Railway 무료 티어
- **월 $5 크레딧** (자동 충전)
- **500GB 대역폭**
- **충분한 CPU/메모리**

### 현재 사용량
- **$0/월** (크레딧 내)
- **~500명 농부까지 무료**

---

## 🔄 코드 업데이트 방법

### 로컬에서 수정 후

```bash
cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero"

# 변경사항 커밋
git add .
git commit -m "Update: Your changes"

# 푸시 (자동 배포됨!)
git push origin main
```

**Railway가 자동으로 감지하고 재배포합니다!**

---

## 🐛 문제 해결

### 배포 실패 시

**로그 확인:**
1. Railway → Deployments → 실패한 배포 클릭
2. View Logs
3. 에러 메시지 확인

**일반적인 문제:**

1. **"Module not found"**
   - `requirements.txt` 확인
   - 모든 의존성 포함되었는지 확인

2. **"Port binding failed"**
   - `PORT` 환경 변수 확인
   - `main.py`에서 `PORT` 사용하는지 확인

3. **"Build failed"**
   - `runtime.txt` 확인 (Python 버전)
   - `Procfile` 확인

### 서버 응답 없음

```bash
# Railway 로그 확인
# Deployments → Latest → View Logs

# 재배포
# Deployments → Latest → Redeploy
```

### 환경 변수 변경 안 됨

```bash
# Variables 탭에서 변경 후
# 자동 재배포 대기 (1-2분)

# 또는 수동 재배포
# Deployments → Redeploy
```

---

## 🎯 다음 단계

### 1. API 키 추가 (선택사항)

**Groq AI 추가:**
```bash
# Railway → Variables
GROQ_API_KEY=gsk_your_actual_key
```

**Supabase 추가:**
```bash
# Railway → Variables
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
```

### 2. WhatsApp 연결

**Meta Business Manager에서:**
1. Webhook URL: `https://your-app.up.railway.app/webhook/whatsapp`
2. Verify Token: `my_secret_verify_token_12345`
3. Subscribe to messages

### 3. 첫 농부 온보딩

**WhatsApp으로 메시지 전송:**
```
Hello
```

**AgriAI 응답:**
```
👋 Welcome to AgriAI!

I'm your free AI farming assistant.

Send me:
📸 Photo of your crop for diagnosis
💬 Description of any issues
❓ Any farming questions

Let's start: What crop are you growing?
```

---

## 📝 체크리스트

- [ ] GitHub 저장소 생성
- [ ] 코드 푸시
- [ ] Railway 프로젝트 생성
- [ ] 환경 변수 설정
- [ ] 도메인 생성
- [ ] 배포 확인
- [ ] 헬스 체크 통과
- [ ] 대시보드 접속 가능

---

## 🎊 축하합니다!

**당신은 방금:**
✅ GitHub에 코드 업로드  
✅ Railway에 배포  
✅ 전 세계에서 접근 가능한 서비스 런칭  
✅ $0 비용으로 프로덕션 환경 구축  

**다음:**
WhatsApp을 연결하고 첫 농부를 온보딩하세요!

---

**Built with ❤️ by a 19-year-old student**  
**Deployed in 15 minutes**  
**Running on $0/month**  

**Let's go! 🚀**
