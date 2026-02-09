# 🚀 Railway 환경 변수 설정 가이드

**즉시 실행 필요** - 5분 소요

---

## 📋 Railway 대시보드 접속

1. 브라우저에서 https://railway.app 열기
2. GitHub 계정으로 로그인
3. `agri-ai-zero` 프로젝트 선택

---

## ⚙️ 환경 변수 설정 (필수)

### 방법 1: Raw Editor 사용 (추천)

1. **Variables** 탭 클릭
2. **Raw Editor** 버튼 클릭
3. 아래 내용 **전체 복사** 후 붙여넣기:

```env
PORT=8000
WEBHOOK_VERIFY_TOKEN=agri_ai_webhook_secret_2026
ALLOWED_ORIGINS=https://web-production-17eb9.up.railway.app,http://localhost:8000,http://localhost:3000
```

4. **Update Variables** 클릭
5. 자동 재배포 시작 (1-2분 대기)

### 방법 2: 하나씩 추가

| Variable Name | Value |
|---------------|-------|
| `PORT` | `8000` |
| `WEBHOOK_VERIFY_TOKEN` | `agri_ai_webhook_secret_2026` |
| `ALLOWED_ORIGINS` | `https://web-production-17eb9.up.railway.app,http://localhost:8000,http://localhost:3000` |

---

## ✅ 배포 확인

### 1. 배포 로그 확인

1. **Deployments** 탭 클릭
2. 최신 배포 선택
3. **View Logs** 클릭
4. 다음 메시지 확인:

```
🚀 AgriAI - Zero Capital Edition Starting...
============================================================
✅ Server ready and listening for requests!
```

### 2. 도메인 확인

1. **Settings** 탭 클릭
2. **Domains** 섹션에서 URL 확인
3. URL 복사 (예: `agri-ai-zero-production.up.railway.app`)

### 3. 헬스 체크 테스트

브라우저 또는 터미널에서:

```bash
# 브라우저에서
https://your-railway-url.up.railway.app/health

# 또는 터미널에서
curl https://your-railway-url.up.railway.app/health
```

**예상 응답:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-09T...",
  "database": "not configured",
  "whatsapp": "not configured",
  "version": "2.0.0-stable"
}
```

---

## 🎯 다음 단계

환경 변수 설정이 완료되면:

1. ✅ **기본 서버 작동 확인** (위 헬스 체크)
2. ⏳ **Supabase 설정** → `SUPABASE_SETUP.md` 참고
3. ⏳ **Groq AI 설정** → `GROQ_SETUP.md` 참고
4. ⏳ **WhatsApp 설정** → `WHATSAPP_SETUP.md` 참고

---

## 🐛 문제 해결

### 배포 실패 시

**증상**: 배포가 "Failed" 상태

**해결**:
1. Deployments → 실패한 배포 → View Logs
2. 에러 메시지 확인
3. 일반적인 문제:
   - `requirements.txt` 누락 → 루트에 있는지 확인
   - `Procfile` 오류 → 내용 확인
   - Python 버전 → `runtime.txt` 확인

### 서버 응답 없음

**증상**: URL 접속 시 "Application Error"

**해결**:
1. Deployments → Latest → View Logs
2. "Server ready" 메시지 확인
3. Variables에서 `PORT=8000` 확인
4. 수동 재배포: Deployments → Redeploy

### 환경 변수 적용 안 됨

**증상**: 변수 변경했는데 반영 안 됨

**해결**:
1. Variables 탭에서 값 재확인
2. 자동 재배포 대기 (1-2분)
3. 또는 수동 재배포

---

**⏱️ 예상 소요 시간**: 5분  
**💰 비용**: $0 (무료 크레딧 사용)  
**🔄 다음**: Supabase 설정
