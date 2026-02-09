# 💬 WhatsApp Business API 설정 가이드

**우선순위: 중간** - 15분 소요

---

## 🎯 목표

WhatsApp Business API를 설정하여 농부들이 WhatsApp으로 AgriAI와 대화할 수 있도록 합니다.

**WhatsApp 장점:**
- ✅ 전 세계 20억 사용자
- ✅ 무료 메시지 (월 1,000 대화)
- ✅ 농부들이 이미 사용 중
- ✅ 이미지, 음성 지원

---

## 📋 1단계: Meta Business 계정 생성

### 1. Meta Business Suite 접속

1. https://business.facebook.com 방문
2. **Create Account** 클릭 (또는 기존 계정 로그인)

### 2. Business 계정 정보 입력

```
Business Name: AgriAI
Your Name: [실명]
Business Email: [이메일]
```

3. **Next** 클릭
4. 비즈니스 세부정보 입력
5. **Submit** 클릭

---

## 📱 2단계: WhatsApp Business 앱 추가

### 1. WhatsApp 제품 추가

1. Meta Business Suite 대시보드
2. 왼쪽 메뉴 → **All tools**
3. **WhatsApp** 찾아서 클릭
4. **Get Started** 클릭

### 2. WhatsApp Business 계정 생성

**옵션 A: 새 번호 사용 (추천)**
1. **Create a WhatsApp Business Account** 선택
2. Display name: `AgriAI`
3. Category: `Business Services` 또는 `Agriculture`
4. Description: `Free AI farming assistant`
5. **Next** 클릭

**옵션 B: 기존 번호 사용**
1. **Use existing WhatsApp Business Account**
2. 전화번호 입력 및 인증

### 3. 전화번호 추가 및 인증

1. **Add phone number** 클릭
2. 국가 선택 및 번호 입력
3. SMS 또는 전화로 인증 코드 수신
4. 인증 코드 입력
5. **Verify** 클릭

**⚠️ 중요:**
- 개인 WhatsApp에서 사용 중인 번호는 사용 불가
- 새 SIM 카드 또는 가상 번호 사용
- 한 번 등록하면 변경 어려움

---

## 🔑 3단계: API 자격 증명 받기

### 1. API Setup 페이지 이동

1. WhatsApp → **API Setup** 또는 **Getting Started**
2. 또는 https://business.facebook.com/wa/manage/home/

### 2. Temporary Access Token 복사

**⚠️ 임시 토큰 (24시간 유효):**

1. **Temporary access token** 섹션 찾기
2. **Copy** 버튼 클릭
3. 안전한 곳에 저장

**형식:**
```
EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Phone Number ID 복사

1. **Phone number ID** 섹션 찾기
2. 숫자 ID 복사 (예: `123456789012345`)
3. 안전한 곳에 저장

### 4. WhatsApp Business Account ID 복사 (선택)

1. **WhatsApp Business Account ID** 찾기
2. 복사 (나중에 필요할 수 있음)

---

## 🔗 4단계: Webhook 설정

### 1. Railway URL 확인

1. https://railway.app 접속
2. `agri-ai-zero` 프로젝트
3. **Settings** → **Domains**
4. URL 복사 (예: `agri-ai-zero-production.up.railway.app`)

### 2. Webhook URL 구성

**Callback URL:**
```
https://your-railway-url.up.railway.app/webhook/whatsapp
```

**Verify Token:**
```
agri_ai_webhook_secret_2026
```

(Railway Variables에 설정한 `WEBHOOK_VERIFY_TOKEN`과 동일)

### 3. Meta에서 Webhook 설정

1. WhatsApp → **Configuration** → **Webhooks**
2. **Edit** 버튼 클릭
3. 정보 입력:

```
Callback URL: https://your-railway-url.up.railway.app/webhook/whatsapp
Verify Token: agri_ai_webhook_secret_2026
```

4. **Verify and Save** 클릭

**성공 시:**
- ✅ 녹색 체크 표시
- "Webhook verified successfully"

**실패 시:**
- ❌ 빨간 X 표시
- Verify Token 확인
- Railway 배포 상태 확인

### 4. Webhook Fields 구독

**Subscribe to:**
- ✅ `messages` (필수)
- ✅ `message_status` (선택)

**저장:**
1. **Subscribe** 버튼 클릭
2. Status가 **Active** (녹색)인지 확인

---

## 🚀 5단계: Railway에 환경 변수 추가

### 1. Railway Variables 업데이트

https://railway.app → `agri-ai-zero` → **Variables**

**Raw Editor**에 추가:

```env
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WHATSAPP_PHONE_ID=123456789012345
```

**⚠️ 중요**: 실제 값으로 교체!

**전체 예시:**
```env
PORT=8000
WEBHOOK_VERIFY_TOKEN=agri_ai_webhook_secret_2026
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
GROQ_API_KEY=gsk_xxx...
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WHATSAPP_PHONE_ID=123456789012345
```

### 2. 저장 및 재배포

1. **Update Variables** 클릭
2. 자동 재배포 (1-2분)
3. Deployments → Latest → View Logs 확인

---

## ✅ 6단계: 연결 테스트

### Railway 로그 확인

Deployments → Latest → View Logs:

**성공 시:**
```
📱 WhatsApp Phone ID: 123456789012345
============================================================
✅ Server ready and listening for requests!
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
  "whatsapp": "configured",  ← 이제 "configured"!
  "version": "2.0.0-stable"
}
```

### 첫 메시지 테스트

**방법 1: Meta Test Message (추천)**

1. WhatsApp → **API Setup**
2. **Send test message** 섹션
3. 본인 전화번호 입력
4. **Send Message** 클릭
5. WhatsApp에서 메시지 수신 확인

**방법 2: 직접 메시지**

1. 등록한 WhatsApp Business 번호로 메시지 전송
2. 메시지 내용: `Hello`
3. AgriAI 환영 메시지 수신 대기

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

---

## 🧪 7단계: 전체 시나리오 테스트

### 시나리오 1: 새 사용자 온보딩

```
농부: Hello
AgriAI: 👋 Welcome to AgriAI! ...

농부: I grow tomatoes
AgriAI: 🌾 Diagnosis for tomatoes ...
```

### 시나리오 2: 진단 요청

```
농부: My tomato leaves are turning yellow
AgriAI: 🔬 진단 중입니다... (5-10초)
AgriAI: 🌾 Diagnosis for tomato
      🔍 Issue: Nitrogen deficiency
      📊 Confidence: 85%
      💡 Recommended Action: Apply urea fertilizer...
```

### 시나리오 3: 이미지 전송

```
농부: [사진 전송 + "What's wrong?"]
AgriAI: 📸 Photo received! Analyzing...
      (Note: Visual analysis coming soon...)
      🌾 Diagnosis based on description...
```

### Railway 로그 확인

각 메시지마다 로그 확인:

```
Received text message from +1234567890
Processing text message from user xxx: My tomato leaves...
Diagnosis completed for user xxx: Nitrogen deficiency
Successfully sent diagnosis to user xxx
```

---

## 🔄 8단계: Permanent Access Token 생성 (중요!)

**⚠️ 임시 토큰은 24시간 후 만료됩니다!**

### 옵션 A: System User Token (추천)

1. Meta Business Settings → **Users** → **System Users**
2. **Add** 클릭
3. Name: `AgriAI System User`
4. Role: **Admin**
5. **Create System User**
6. **Generate New Token** 클릭
7. App 선택: WhatsApp Business 앱
8. Permissions:
   - ✅ `whatsapp_business_management`
   - ✅ `whatsapp_business_messaging`
9. Token expiration: **Never** (추천) 또는 60 days
10. **Generate Token** 클릭
11. 토큰 복사 및 안전하게 저장
12. Railway Variables에서 `WHATSAPP_ACCESS_TOKEN` 업데이트

### 옵션 B: App Access Token

1. Meta for Developers → https://developers.facebook.com
2. My Apps → WhatsApp 앱 선택
3. Settings → Basic
4. App Secret 복사
5. Access Token Tools 사용하여 장기 토큰 생성

**⚠️ 중요:**
- 영구 토큰을 안전하게 보관
- 절대 공개하지 말 것
- Railway 환경 변수에만 저장

---

## 💰 무료 티어 한도

### WhatsApp Business API 가격

| 항목 | 무료 한도 | 초과 시 |
|------|-----------|---------|
| 비즈니스 시작 대화 | 1,000/월 | $0.005/대화 |
| 사용자 시작 대화 | 무제한 | 무료 |
| 서비스 대화 | 무제한 | 무료 |

**대화 정의:**
- 24시간 세션 = 1 대화
- 농부가 먼저 메시지 → 무료
- AgriAI가 먼저 메시지 → 유료 (1,000 무료)

**예상 비용:**
- 500명 농부 × 월 2회 대화 = 1,000 대화
- **$0/월** (무료 한도 내)

---

## 🐛 문제 해결

### Webhook 인증 실패

**증상**: "Webhook verification failed"

**해결**:
1. Verify Token 확인 (대소문자 구분)
2. Railway Variables에서 `WEBHOOK_VERIFY_TOKEN` 확인
3. Railway 배포 상태 확인 (Active)
4. URL이 `https://`로 시작하는지 확인
5. Railway 로그에서 webhook 요청 확인

### 메시지 수신 안 됨

**증상**: 메시지 보냈는데 응답 없음

**해결**:
1. Webhook Status가 **Active**인지 확인
2. Railway 로그 확인:
   ```
   Received webhook data: 1 entries
   Received text message from +xxx
   ```
3. `WHATSAPP_ACCESS_TOKEN` 확인
4. `WHATSAPP_PHONE_ID` 확인
5. 전화번호가 올바른지 확인

### 메시지 전송 실패

**증상**: 수신은 되는데 응답 못 보냄

**해결**:
1. Access Token 만료 확인 (24시간)
2. Permanent Token으로 교체
3. Phone Number ID 확인
4. Railway 로그에서 에러 확인:
   ```
   Failed to send WhatsApp message: ...
   ```

### "Template required" 오류

**증상**: 비즈니스 시작 메시지 실패

**해결**:
- 24시간 내 농부가 먼저 메시지 보내야 함
- 또는 승인된 템플릿 사용
- 초기 단계에서는 농부가 먼저 연락하도록 안내

---

## 📊 메시지 모니터링

### Meta Business Manager

https://business.facebook.com/wa/manage/home/

**확인 사항:**
- 일일 메시지 수
- 대화 수 (무료 한도 추적)
- 응답 시간
- 에러율

### Railway 로그

실시간 메시지 추적:

```
Received text message from +1234567890
Processing text message: My tomato leaves...
Diagnosis completed: Nitrogen deficiency
Successfully sent diagnosis
```

---

## 🎯 다음 단계

WhatsApp 설정 완료 후:

1. ✅ **첫 농부 온보딩**
2. ⏳ **사용자 피드백 수집**
3. ⏳ **AI 진단 개선**
4. ⏳ **커뮤니티 구축**

---

## 💡 고급 기능 (미래)

### 메시지 템플릿

```
# 승인된 템플릿으로 프로모션 메시지 전송
- 날씨 알림
- 작물 관리 팁
- 시장 가격 정보
```

### 미디어 메시지

```python
# 이미지, 비디오, 문서 전송
- 진단 결과 이미지
- 교육 비디오
- PDF 가이드
```

### 인터랙티브 메시지

```python
# 버튼, 리스트, 빠른 답장
- 작물 선택 버튼
- 진단 결과 평가 (👍/👎)
- 메뉴 네비게이션
```

---

## 🔒 보안 및 규정 준수

### Meta 정책 준수

- ✅ 스팸 금지
- ✅ 24시간 응답 규칙
- ✅ 사용자 동의 필요
- ✅ 개인정보 보호

### 전화번호 보호

```python
# backend/main.py에 이미 구현됨
def hash_phone_number(phone: str) -> str:
    # SHA-256 해싱으로 전화번호 보호
    return hashlib.sha256(phone.encode()).hexdigest()
```

---

**⏱️ 예상 소요 시간**: 15분  
**💰 비용**: $0 (월 1,000 대화 무료)  
**🔄 다음**: 첫 농부 온보딩!
