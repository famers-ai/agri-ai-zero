# 🤖 Groq AI 설정 가이드

**우선순위: 높음** - 5분 소요

---

## 🎯 목표

무료 Groq AI API를 설정하여 AgriAI가 고급 AI 진단을 제공할 수 있도록 합니다.

**Groq 장점:**
- ✅ 완전 무료 (일일 14,400 요청)
- ✅ 초고속 응답 (LPU 기반)
- ✅ Llama 3.1 70B 모델 사용
- ✅ 신용카드 불필요

---

## 📋 1단계: Groq 계정 생성

### 1. Groq Console 접속

1. https://console.groq.com 방문
2. **Sign Up** 또는 **Get Started** 클릭

### 2. 로그인 방법 선택

다음 중 하나로 가입:
- **GitHub** (추천 - 가장 빠름)
- **Google**
- 이메일

### 3. 계정 인증

- GitHub/Google: 자동 인증
- 이메일: 인증 링크 클릭

---

## 🔑 2단계: API 키 생성

### 1. API Keys 페이지 이동

1. 로그인 후 왼쪽 메뉴에서 **API Keys** 클릭
2. 또는 https://console.groq.com/keys 직접 접속

### 2. 새 API 키 생성

1. **Create API Key** 버튼 클릭
2. API Key 정보 입력:

```
Name: agri-ai-zero
Description: AI farming assistant for AgriAI platform
```

3. **Submit** 또는 **Create** 클릭

### 3. API 키 복사

**⚠️ 매우 중요!**

- API 키가 **한 번만** 표시됩니다
- 즉시 복사하여 안전한 곳에 저장
- 형식: `gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**복사 방법:**
1. 전체 키 선택 (클릭하면 자동 복사되기도 함)
2. 메모장이나 비밀번호 관리자에 저장
3. 창을 닫기 전에 반드시 저장 확인!

---

## 🚀 3단계: Railway에 환경 변수 추가

### 1. Railway 대시보드 열기

1. https://railway.app 접속
2. `agri-ai-zero` 프로젝트 선택
3. **Variables** 탭 클릭

### 2. Groq API 키 추가

**Raw Editor** 사용:

기존 변수에 다음 줄 추가:

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**⚠️ 중요**: `gsk_your_actual_api_key_here`를 실제 키로 교체!

**전체 예시:**
```env
PORT=8000
WEBHOOK_VERIFY_TOKEN=agri_ai_webhook_secret_2026
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. 저장 및 재배포

1. **Update Variables** 클릭
2. 자동 재배포 시작 (1-2분)
3. Deployments → Latest → View Logs 확인

---

## ✅ 4단계: AI 연결 테스트

### Railway 로그 확인

Deployments → Latest → View Logs:

**성공 시:**
```
🤖 AI Engine: Groq (Free)
============================================================
✅ Server ready and listening for requests!
```

**실패 시:**
```
🤖 AI Engine: Rule-based only
⚠️ Groq AI not configured. Using rule-based diagnosis only.
```

### 헬스 체크

```bash
curl https://your-railway-url.up.railway.app/health
```

**예상 응답:**
```json
{
  "status": "healthy",
  "database": "connected",
  "whatsapp": "not configured",
  "version": "2.0.0-stable"
}
```

---

## 🧪 5단계: AI 진단 테스트 (선택)

### 로컬 테스트 스크립트

프로젝트 루트에서:

```bash
cd "/Users/ijeong-u/Desktop/change the world/agri-ai-zero"
source venv/bin/activate
cd backend
python -c "
import asyncio
from main import FreeAIEngine

async def test():
    ai = FreeAIEngine()
    result = await ai.diagnose_crop(
        crop='tomato',
        observations='leaves are turning yellow',
        location='Nairobi'
    )
    print('AI Diagnosis:', result)

asyncio.run(test())
"
```

**예상 출력:**
```python
AI Diagnosis: {
    'crop': 'tomato',
    'issue': 'Nitrogen deficiency',
    'confidence': 85,
    'recommendation': 'Apply nitrogen-rich fertilizer...',
    'risk': 'medium',
    'method': 'ai'
}
```

---

## 📊 Groq AI 사양

### 사용 가능한 모델

AgriAI는 **Llama 3.1 70B Versatile** 사용:

| 모델 | 파라미터 | 속도 | 품질 |
|------|----------|------|------|
| Llama 3.1 70B | 70B | 초고속 | 최고 |
| Llama 3.1 8B | 8B | 극초고속 | 우수 |
| Mixtral 8x7B | 47B | 고속 | 우수 |

**선택 이유:**
- 농업 지식이 풍부한 대형 모델
- LPU 가속으로 빠른 응답 (1-2초)
- 정확한 진단 및 권장사항

### 무료 한도

| 항목 | 무료 한도 | 예상 사용량 |
|------|-----------|-------------|
| 분당 요청 | 30 | ~5 |
| 일일 요청 | 14,400 | ~500 |
| 토큰/요청 | 6,000 | ~500 |
| 월간 요청 | ~432,000 | ~15,000 |

**결론**: 500명 농부에게 충분! 🎉

---

## 🔄 AI vs Rule-based 비교

### AI 모드 (Groq 사용)

**장점:**
- ✅ 정확한 진단 (85-95% 신뢰도)
- ✅ 맥락 이해 (날씨, 위치 고려)
- ✅ 자연어 처리 (다양한 표현 이해)
- ✅ 구체적인 권장사항

**예시:**
```
입력: "토마토 잎이 노랗고 가장자리가 말라요"
AI 진단: "질소 결핍과 수분 스트레스 복합 증상. 
         요소 비료 50kg/ha 시비 후 충분한 관수 필요."
```

### Rule-based 모드 (Groq 없이)

**장점:**
- ✅ 항상 작동 (API 불필요)
- ✅ 즉각 응답
- ✅ 비용 $0

**단점:**
- ⚠️ 제한된 패턴 인식
- ⚠️ 낮은 신뢰도 (60-70%)
- ⚠️ 단순한 권장사항

**예시:**
```
입력: "토마토 잎이 노랗고 가장자리가 말라요"
Rule 진단: "질소 결핍 (노란 잎). 
           요소 비료 또는 퇴비 시비."
```

---

## 🎯 AI 진단 프롬프트 구조

AgriAI가 Groq에 보내는 프롬프트:

```
You are an expert agricultural advisor. Analyze this farmer's situation.

Crop: tomato
Location: Nairobi
Farmer's observation: leaves are turning yellow
Current weather: 25°C, Wind: 10 km/h

Provide a diagnosis in this exact JSON format:
{
    "crop": "tomato",
    "issue": "brief description",
    "confidence": 75,
    "recommendation": "specific action",
    "risk": "low/medium/high",
    "method": "ai"
}

Be specific and practical. Focus on low-cost solutions.
```

**최적화 설정:**
- Temperature: 0.3 (일관된 응답)
- Max tokens: 500 (간결한 답변)
- Model: llama-3.1-70b-versatile

---

## 🐛 문제 해결

### "Invalid API key" 오류

**원인**: 잘못된 키 또는 만료된 키

**해결**:
1. Groq Console에서 키 재확인
2. `gsk_`로 시작하는지 확인
3. 새 키 생성 후 Railway 업데이트

### "Rate limit exceeded" 오류

**원인**: 분당 30 요청 초과

**해결**:
- 자동으로 rule-based로 fallback
- 1분 후 자동 복구
- 대량 트래픽 시 유료 플랜 고려

### AI 응답 느림

**원인**: 네트워크 또는 Groq 서버

**해결**:
- 30초 타임아웃 설정됨
- 타임아웃 시 자동 rule-based fallback
- 사용자에게 친절한 메시지 전송

### AI 진단 품질 낮음

**원인**: 프롬프트 또는 모델 문제

**해결**:
1. 사용자 피드백 수집 (feedback 테이블)
2. 프롬프트 개선
3. 다른 모델 시도 (Mixtral 등)

---

## 📈 성능 모니터링

### Groq Dashboard

https://console.groq.com/usage

**확인 사항:**
- 일일 요청 수
- 평균 응답 시간
- 에러율
- 토큰 사용량

**권장 모니터링:**
- 매일 확인
- 한도 80% 도달 시 알림 설정
- 피크 시간대 파악

---

## 🎯 다음 단계

Groq AI 설정 완료 후:

1. ✅ **AI 진단 테스트** (위 테스트 스크립트)
2. ⏳ **WhatsApp 설정** → `WHATSAPP_SETUP.md`
3. ⏳ **첫 농부 온보딩!**
4. ⏳ **피드백 수집 및 AI 개선**

---

## 💡 고급 기능 (미래)

### RLHF (Reinforcement Learning from Human Feedback)

```python
# 사용자 피드백 기반 AI 개선
1. 농부가 진단 결과에 피드백 제공
2. feedback 테이블에 저장
3. 주기적으로 프롬프트 개선
4. 정확도 향상
```

### 이미지 분석

```python
# Computer Vision 추가 (미래)
1. 농부가 작물 사진 전송
2. Groq Vision API 사용
3. 시각적 진단 제공
4. 텍스트 + 이미지 복합 분석
```

---

**⏱️ 예상 소요 시간**: 5분  
**💰 비용**: $0 (무료 API)  
**🔄 다음**: WhatsApp Business 설정
