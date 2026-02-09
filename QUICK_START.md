# 🎯 즉시 실행 가이드

**지금 바로 AgriAI를 실행하는 3가지 방법**

---

## 방법 1: 자동 설정 스크립트 (추천) ⚡

```bash
# 터미널을 열고 다음 명령어 실행:

cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero"
./setup.sh
```

**그 다음:**

```bash
cd backend
python main.py
```

**브라우저에서 열기:**
```
http://localhost:8000
```

---

## 방법 2: 수동 설정 (단계별)

### 1단계: 가상환경 생성

```bash
cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero"
python3 -m venv venv
source venv/bin/activate
```

### 2단계: 라이브러리 설치

```bash
pip install -r backend/requirements.txt
```

### 3단계: 환경 변수 설정

```bash
cp .env.example .env
```

### 4단계: 서버 실행

```bash
cd backend
python main.py
```

### 5단계: 브라우저에서 확인

```
http://localhost:8000
```

---

## 방법 3: 한 줄 명령어 🚀

```bash
cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero" && python3 -m venv venv && source venv/bin/activate && pip install -r backend/requirements.txt && cp .env.example .env && cd backend && python main.py
```

---

## ✅ 성공 확인

서버가 시작되면 다음과 같은 메시지가 보입니다:

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

INFO:     Uvicorn running on http://0.0.0.0:8000
```

**브라우저에서 http://localhost:8000 을 열면:**
- 🌾 아름다운 대시보드
- 통계: 0 users, 0 diagnoses
- "Built with ❤️ by a 19-year-old student"

---

## 🧪 테스트하기

### API 테스트

```bash
# 새 터미널 창에서:
curl http://localhost:8000/health
```

**예상 출력:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-08T...",
  "database": "not configured",
  "whatsapp": "not configured"
}
```

### 진단 엔진 테스트

```bash
# Python 인터프리터 열기
cd backend
python

# 다음 코드 실행:
```

```python
import asyncio
from main import FreeAIEngine

async def test():
    engine = FreeAIEngine()
    result = await engine.diagnose_crop(
        crop="tomato",
        observations="leaves are yellow",
        location="test"
    )
    print(result)

asyncio.run(test())
```

**예상 출력:**
```python
{
    'crop': 'tomato',
    'issue': 'Nitrogen deficiency (yellowing leaves)',
    'confidence': 70,
    'recommendation': 'Apply urea fertilizer (50kg per hectare) or compost. Water regularly.',
    'risk': 'medium',
    'method': 'rule-based'
}
```

---

## 🔑 API 키 추가 (선택사항)

로컬 테스트는 API 키 없이도 작동합니다 (규칙 기반).

하지만 AI 기능을 테스트하려면:

### Groq AI 키 받기 (5분)

1. https://console.groq.com 방문
2. 계정 생성 (무료)
3. API Keys → Create API Key
4. 키 복사

### .env 파일에 추가

```bash
# .env 파일 열기
nano .env

# 또는
open -e .env
```

```bash
# 이 줄 찾아서 키 추가:
GROQ_API_KEY=gsk_your_actual_key_here
```

### 서버 재시작

```bash
# Ctrl+C로 서버 중지
# 다시 시작
python main.py
```

이제 AI 진단이 작동합니다! 🤖

---

## 🐛 문제 해결

### "command not found: python3"

```bash
# Python 3 설치 확인
which python3

# 없으면 Homebrew로 설치
brew install python3
```

### "Permission denied: ./setup.sh"

```bash
chmod +x setup.sh
./setup.sh
```

### "Port 8000 already in use"

```bash
# 다른 포트 사용
PORT=8001 python main.py

# 또는 8000 포트 프로세스 종료
lsof -ti:8000 | xargs kill -9
```

### "No module named 'fastapi'"

```bash
# 가상환경 활성화 확인
source venv/bin/activate

# 의존성 재설치
pip install -r backend/requirements.txt
```

---

## 📝 다음 단계

로컬 테스트가 완료되면:

1. ✅ **무료 API 키 받기**
   - Groq: https://console.groq.com
   - Supabase: https://supabase.com

2. ✅ **Railway에 배포**
   - `docs/DEPLOYMENT_GUIDE.md` 참조

3. ✅ **WhatsApp 연결**
   - Meta Business Manager 설정

4. ✅ **첫 농부 온보딩**
   - 실제 사용자 테스트!

---

## 🎉 축하합니다!

로컬에서 AgriAI가 작동 중입니다!

**이제 배포만 하면 됩니다.** 🚀

---

## 빠른 참조

```bash
# 서버 시작
cd backend && python main.py

# 서버 중지
Ctrl + C

# 가상환경 활성화
source venv/bin/activate

# 가상환경 비활성화
deactivate

# 로그 보기
tail -f ../logs/server.log

# 테스트
curl http://localhost:8000/health
```

---

**준비됐으면 배포하러 가자!** 🌾
