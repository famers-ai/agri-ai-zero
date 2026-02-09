# 🎯 빠른 완료 가이드 - API 키 설정

## ✅ 현재 상태
- Railway에 `GROQ_API_KEY` 변수 추가됨 (placeholder 값)
- 배포 성공 (2.0.0-stable 버전 실행 중)
- 시스템 안정성 강화 완료

## 🚀 지금 해야 할 일 (5분)

### 1단계: Groq API 키 획득 (2분)

1. **브라우저에서 Groq Console 열기**
   - URL: https://console.groq.com/keys
   - Google 계정으로 로그인

2. **API 키 생성**
   - "Create API Key" 버튼 클릭
   - 키 이름 입력 (예: "AgriAI Production")
   - 생성된 키 복사 (gsk_로 시작하는 긴 문자열)

### 2단계: Railway에 실제 키 추가 (2분)

**방법 A: Railway Dashboard (권장)**
1. https://railway.com/project/c6cdfacb-b0a1-42fe-9678-36f428957f47/service/9b6fa42f-60a0-43c8-899d-8b865225d19d/variables 접속
2. `GROQ_API_KEY` 찾기
3. 값 클릭하여 편집
4. `PLACEHOLDER_GROQ_KEY`를 실제 Groq 키로 교체
5. 저장 (Railway가 자동으로 재배포)

**방법 B: 터미널 (빠름)**
```bash
# Railway CLI 사용 (이미 설치되어 있다면)
railway variables set GROQ_API_KEY=gsk_여기에_실제_키_붙여넣기
```

### 3단계: 배포 확인 (1분)

배포 완료 후 (1-2분 소요):
```bash
curl https://web-production-17eb9.up.railway.app/health
```

**예상 결과**:
```json
{
  "status": "healthy",
  "database": "not configured",
  "whatsapp": "not configured",
  "version": "2.0.0-stable"
}
```

---

## 🎉 완료!

Groq API 키만 추가하면:
- ✅ AI 진단 엔진 활성화
- ✅ 실시간 날씨 정보 제공
- ✅ 지능형 작물 진단
- ✅ 대시보드 완전 작동

---

## 📋 선택사항: Supabase 추가 (나중에 해도 됨)

현재 시스템은 **메모리 모드**로 작동 중입니다:
- ✅ 모든 기능 작동
- ⚠️ 서버 재시작 시 데이터 삭제

**영구 저장이 필요하면**:
1. Supabase 프로젝트 생성
2. 데이터베이스 스키마 실행 (`database/schema.sql`)
3. Railway에 변수 추가:
   - `SUPABASE_URL`
   - `SUPABASE_KEY` (service_role key)

---

## 🔥 현재 우선순위

**1순위**: Groq API 키 추가 (위 1-2단계)  
**2순위**: 시스템 테스트  
**3순위**: Supabase 설정 (선택사항)

**Groq 키만 추가하면 바로 사용 가능합니다!** 🚀
