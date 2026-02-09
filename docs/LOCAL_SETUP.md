# 🚀 로컬 실행 가이드

**AgriAI를 로컬에서 테스트하는 방법**

---

## 1️⃣ 로컬 환경 설정 (5분)

### 가상환경 생성 및 활성화

```bash
# 프로젝트 디렉토리로 이동
cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero"

# Python 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

# 의존성 설치
pip install -r backend/requirements.txt
```

---

## 2️⃣ 환경 변수 설정 (10분)

### .env 파일 생성

```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집
nano .env
# 또는
open -e .env
```

### .env 파일 내용 (필수 항목만)

```bash
# Supabase (나중에 설정 - 지금은 비워둬도 됨)
SUPABASE_URL=
SUPABASE_KEY=

# WhatsApp (나중에 설정 - 지금은 비워둬도 됨)
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_ID=
WEBHOOK_VERIFY_TOKEN=test_verify_token_123

# Groq AI (나중에 설정 - 지금은 비워둬도 됨)
GROQ_API_KEY=

# 서버 설정
PORT=8000
```

**중요**: 지금은 모두 비워둬도 됩니다! 로컬 테스트는 규칙 기반 시스템으로 작동합니다.

---

## 3️⃣ 로컬 서버 실행 (1분)

```bash
# backend 디렉토리로 이동
cd backend

# 서버 실행
python main.py
```

**출력 예시:**
```
🚀 AgriAI - Zero Capital Edition Starting...
============================================================
📱 WhatsApp Phone ID: Not configured
💾 Database: Not configured
🤖 AI Engine: Rule-based only
============================================================

⚠️  WARNING: Supabase not configured. Using in-memory storage.
⚠️  WARNING: WhatsApp not configured. Messages will be logged only.

✅ Server ready!

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 4️⃣ 로컬 테스트 (2분)

### 브라우저에서 대시보드 확인

```bash
# 브라우저에서 열기
open http://localhost:8000
```

**보여야 할 것:**
- 🌾 AgriAI 대시보드
- 통계: 0 users, 0 diagnoses
- 아름다운 그라디언트 배경

### API 테스트

```bash
# 헬스 체크
curl http://localhost:8000/health

# 예상 출력:
{
  "status": "healthy",
  "timestamp": "2026-02-08T...",
  "database": "not configured",
  "whatsapp": "not configured"
}
```

---

## 5️⃣ 규칙 기반 진단 테스트

### Python으로 직접 테스트

```python
# test_diagnosis.py 파일 생성
import asyncio
from main import FreeAIEngine

async def test():
    engine = FreeAIEngine()
    
    # 테스트 1: 노란 잎
    result = await engine.diagnose_crop(
        crop="tomato",
        observations="leaves are turning yellow",
        location="test"
    )
    print("Test 1:", result)
    
    # 테스트 2: 반점
    result = await engine.diagnose_crop(
        crop="corn",
        observations="brown spots on leaves",
        location="test"
    )
    print("Test 2:", result)
    
    # 테스트 3: 시들음
    result = await engine.diagnose_crop(
        crop="rice",
        observations="plants are wilting",
        location="test"
    )
    print("Test 3:", result)

asyncio.run(test())
```

```bash
# 테스트 실행
python test_diagnosis.py
```

**예상 출력:**
```python
Test 1: {
    'crop': 'tomato',
    'issue': 'Nitrogen deficiency (yellowing leaves)',
    'confidence': 70,
    'recommendation': 'Apply urea fertilizer (50kg per hectare) or compost. Water regularly.',
    'risk': 'medium',
    'method': 'rule-based'
}

Test 2: {
    'crop': 'corn',
    'issue': 'Fungal infection (leaf spots)',
    'confidence': 65,
    'recommendation': 'Remove affected leaves. Apply fungicide or neem oil spray. Improve air circulation.',
    'risk': 'high',
    'method': 'rule-based'
}

Test 3: {
    'crop': 'rice',
    'issue': 'Water stress or root damage',
    'confidence': 75,
    'recommendation': 'Check soil moisture. Water deeply if dry. Check for root rot if soil is wet.',
    'risk': 'medium',
    'method': 'rule-based'
}
```

---

## 6️⃣ 무료 서비스 설정 (선택사항)

### Groq AI 설정 (5분)

1. https://console.groq.com 방문
2. 계정 생성 (Gmail)
3. API Keys → Create API Key
4. 키 복사 (gsk_로 시작)
5. .env 파일에 추가:
   ```bash
   GROQ_API_KEY=gsk_your_key_here
   ```
6. 서버 재시작

### Supabase 설정 (10분)

1. https://supabase.com 방문
2. 계정 생성 (GitHub)
3. New Project 생성
4. SQL Editor에서 `database/schema.sql` 실행
5. Settings → API에서 복사:
   ```bash
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbGc...
   ```
6. .env 파일에 추가
7. 서버 재시작

### WhatsApp Business 설정 (15분)

1. https://business.facebook.com 방문
2. Business 계정 생성
3. WhatsApp → Get Started
4. 전화번호 추가 및 인증
5. Configuration에서 복사:
   ```bash
   WHATSAPP_ACCESS_TOKEN=EAAxxxxx...
   WHATSAPP_PHONE_ID=123456789
   ```
6. .env 파일에 추가
7. 서버 재시작

---

## 7️⃣ 문제 해결

### "Module not found" 에러

```bash
# 가상환경이 활성화되었는지 확인
which python
# 출력: /Users/ijeong-u/Desktop/change the world/agri-ai-zero/venv/bin/python

# 의존성 재설치
pip install -r backend/requirements.txt
```

### "Port already in use" 에러

```bash
# 다른 포트 사용
PORT=8001 python main.py

# 또는 8000 포트 사용 중인 프로세스 종료
lsof -ti:8000 | xargs kill -9
```

### 서버가 시작되지 않음

```bash
# Python 버전 확인 (3.11+ 필요)
python --version

# 로그 확인
python main.py 2>&1 | tee server.log
```

---

## 8️⃣ 개발 워크플로우

### 코드 수정 후 재시작

```bash
# Ctrl+C로 서버 중지
# 코드 수정
# 서버 재시작
python main.py
```

### 자동 재시작 (개발 모드)

```bash
# uvicorn 직접 사용 (자동 재로드)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 로그 확인

```bash
# 실시간 로그 보기
tail -f server.log

# 에러만 보기
grep ERROR server.log
```

---

## 9️⃣ 배포 준비

### Railway 배포 전 체크리스트

- [ ] 로컬에서 모든 기능 테스트 완료
- [ ] .env 파일에 모든 키 설정
- [ ] 데이터베이스 스키마 배포 완료
- [ ] GitHub에 코드 푸시
- [ ] .env 파일은 .gitignore에 포함 (절대 푸시 안 됨!)

### GitHub에 푸시

```bash
# Git 설정 (처음 한 번만)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 변경사항 커밋
git add .
git commit -m "Ready for deployment"

# GitHub 저장소 생성 후
git remote add origin https://github.com/yourusername/agri-ai-zero.git
git push -u origin main
```

---

## 🎯 빠른 시작 요약

```bash
# 1. 프로젝트로 이동
cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero"

# 2. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 3. 의존성 설치
pip install -r backend/requirements.txt

# 4. .env 파일 생성 (일단 비워둬도 됨)
cp .env.example .env

# 5. 서버 실행
cd backend
python main.py

# 6. 브라우저에서 확인
open http://localhost:8000
```

**그게 전부다!** 🚀

---

## 📝 다음 단계

1. ✅ 로컬에서 작동 확인
2. 🔑 무료 API 키 받기 (Groq, Supabase)
3. 🚀 Railway에 배포
4. 📱 WhatsApp 연결
5. 🌾 첫 농부 온보딩

---

**로컬 테스트 완료되면 `docs/DEPLOYMENT_GUIDE.md`로 이동!**
