# 🔒 AgriAI 보안 설정 가이드

## 📋 목차
1. [환경 변수 보안](#1-환경-변수-보안)
2. [데이터베이스 보안 (RLS)](#2-데이터베이스-보안-rls)
3. [CORS 보안](#3-cors-보안)
4. [API 키 관리](#4-api-키-관리)
5. [전화번호 암호화](#5-전화번호-암호화)

---

## 1. 환경 변수 보안

### ✅ 현재 상태
모든 민감한 정보는 이미 `os.getenv()`를 통해 환경 변수로 관리되고 있습니다.

### 🔧 Railway 설정 방법

1. **Railway Dashboard** → 프로젝트 → **Variables** 탭
2. 다음 환경 변수들을 추가:

```bash
# 필수 환경 변수
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key  # ⚠️ SERVICE ROLE KEY 사용 (anon key 아님!)
WHATSAPP_ACCESS_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_ID=your-phone-id
WEBHOOK_VERIFY_TOKEN=your-random-secure-token
GROQ_API_KEY=your-groq-api-key

# 보안 환경 변수 (새로 추가)
PHONE_HASH_SALT=your-random-salt-string-here  # 32자 이상 랜덤 문자열
ALLOWED_ORIGINS=https://web-production-17eb9.up.railway.app,https://your-custom-domain.com
```

### 🔐 Salt 생성 방법
터미널에서 실행:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 2. 데이터베이스 보안 (RLS)

### 📌 Row Level Security란?
Supabase의 RLS는 데이터베이스 레벨에서 접근 제어를 설정하는 기능입니다.
- **Service Role**: 백엔드 API만 모든 데이터 접근 가능
- **Authenticated**: 인증된 관리자만 읽기 가능
- **Anonymous**: 일반 사용자는 접근 불가

### 🚀 설정 방법

1. **Supabase Dashboard** → SQL Editor
2. `database/security_setup.sql` 파일 내용 복사
3. SQL Editor에 붙여넣기
4. **Run** 클릭

### ✅ 확인 방법

SQL Editor에서 실행:
```sql
-- RLS가 활성화되었는지 확인
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('users', 'diagnoses', 'feedback');

-- 결과: rowsecurity 컬럼이 모두 't' (true)여야 함
```

### ⚠️ 중요 주의사항

**Railway 환경 변수에서 반드시 SERVICE ROLE KEY를 사용하세요!**

```bash
# ❌ 잘못된 예 (anon key)
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InByb2plY3QiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY...

# ✅ 올바른 예 (service_role key)
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InByb2plY3QiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNj...
```

**Service Role Key 찾는 방법:**
1. Supabase Dashboard → Project Settings → API
2. **Project API keys** 섹션
3. `service_role` 키 복사 (⚠️ secret 표시됨)

---

## 3. CORS 보안

### ✅ 현재 설정
코드가 업데이트되어 이제 특정 도메인만 허용합니다:

```python
# ❌ 이전 (모든 출처 허용 - 위험!)
allow_origins=["*"]

# ✅ 현재 (특정 도메인만 허용 - 안전!)
allow_origins=ALLOWED_ORIGINS  # 환경 변수에서 관리
```

### 🔧 커스텀 도메인 추가 방법

Railway Variables에서 `ALLOWED_ORIGINS` 수정:
```bash
ALLOWED_ORIGINS=https://web-production-17eb9.up.railway.app,https://your-domain.com,http://localhost:8000
```

**주의**: 쉼표로 구분, 공백 없이!

---

## 4. API 키 관리

### 🔐 보안 원칙

1. **절대 코드에 직접 작성 금지**
   ```python
   # ❌ 절대 이렇게 하지 마세요!
   GROQ_API_KEY = "gsk_abc123..."
   
   # ✅ 항상 환경 변수 사용
   GROQ_API_KEY = os.getenv("GROQ_API_KEY")
   ```

2. **Git에 업로드 금지**
   - `.env` 파일은 `.gitignore`에 포함됨
   - `.env.example`만 공유 (실제 값 없이)

3. **정기적으로 키 교체**
   - 3개월마다 API 키 재발급 권장
   - 의심스러운 활동 발견 시 즉시 교체

### 📝 API 키 저장 위치

| 환경 | 저장 위치 |
|------|----------|
| 로컬 개발 | `.env` 파일 (Git 제외) |
| Railway 배포 | Railway Variables 탭 |
| 백업 | 비밀번호 관리자 (1Password, Bitwarden 등) |

---

## 5. 전화번호 암호화

### 🔒 현재 구현
전화번호를 SHA-256으로 해싱하여 저장합니다.

```python
def hash_phone_number(phone: str) -> str:
    """전화번호를 해시로 변환 (복호화 불가능)"""
    salt = os.getenv("PHONE_HASH_SALT", "default-salt")
    salted_phone = f"{salt}:{phone}"
    return hashlib.sha256(salted_phone.encode()).hexdigest()
```

### ⚠️ 중요 사항

**현재는 평문 전화번호를 저장하고 있습니다!**

전화번호 해싱을 활성화하려면:

1. **데이터베이스 스키마 수정** (`database/schema.sql`):
   ```sql
   -- users 테이블에 phone_hash 컬럼 추가
   ALTER TABLE users ADD COLUMN phone_hash TEXT UNIQUE;
   ```

2. **백엔드 코드 수정** (`backend/main.py`):
   ```python
   # create_user 함수에서
   result = supabase.table("users").insert({
       "phone_hash": hash_phone_number(phone),  # 해시 저장
       "name": name,
       # phone 필드는 제거하거나 마스킹 처리
   }).execute()
   ```

3. **조회 로직 수정**:
   ```python
   # get_user_by_phone 함수에서
   phone_hash = hash_phone_number(phone)
   result = supabase.table("users").select("*").eq("phone_hash", phone_hash).execute()
   ```

### 🤔 해싱 vs 암호화

| 방식 | 장점 | 단점 | 사용 시기 |
|------|------|------|----------|
| **해싱** (현재) | 복호화 불가능, 최고 보안 | 원본 복구 불가 | 인증만 필요할 때 |
| **암호화** | 원본 복구 가능 | 키 관리 필요 | WhatsApp 메시지 전송 필요 |

**AgriAI의 경우**: WhatsApp으로 메시지를 보내야 하므로 **암호화**가 더 적합할 수 있습니다.

---

## 🎯 보안 체크리스트

배포 전 반드시 확인:

- [ ] Railway Variables에 모든 환경 변수 설정됨
- [ ] `SUPABASE_KEY`가 SERVICE ROLE KEY임 (anon key 아님)
- [ ] `PHONE_HASH_SALT`가 32자 이상 랜덤 문자열
- [ ] Supabase에서 RLS 활성화됨 (`security_setup.sql` 실행)
- [ ] CORS가 특정 도메인만 허용하도록 설정됨
- [ ] `.env` 파일이 Git에 업로드되지 않음 (`.gitignore` 확인)
- [ ] API 키가 코드에 직접 작성되지 않음
- [ ] Railway 배포 로그에 민감한 정보가 출력되지 않음

---

## 🚨 보안 사고 발생 시

1. **즉시 모든 API 키 교체**
   - Groq API Key
   - Supabase Keys
   - WhatsApp Access Token

2. **Railway Variables 업데이트**
   - 새 키로 모두 교체

3. **데이터베이스 점검**
   - 비정상적인 접근 로그 확인
   - Supabase Dashboard → Logs

4. **코드 검토**
   - Git 히스토리에 키가 노출되었는지 확인
   - 노출되었다면 즉시 키 교체

---

## 📚 추가 보안 권장사항

### 1. HTTPS 강제
Railway는 기본적으로 HTTPS를 제공하지만, 커스텀 도메인 사용 시 확인 필요.

### 2. Rate Limiting
향후 추가 권장:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/webhook/whatsapp")
@limiter.limit("100/minute")  # 분당 100회 제한
async def whatsapp_webhook(...):
    ...
```

### 3. 로그 관리
민감한 정보를 로그에 출력하지 않기:
```python
# ❌ 위험
print(f"User phone: {phone}")

# ✅ 안전
print(f"User registered: {phone[:3]}***{phone[-2:]}")
```

### 4. 정기 보안 감사
- 월 1회: API 키 사용량 확인
- 분기 1회: 데이터베이스 접근 로그 검토
- 반기 1회: 전체 보안 설정 재검토

---

## 🆘 도움이 필요하신가요?

- **Supabase 보안**: https://supabase.com/docs/guides/auth/row-level-security
- **Railway 환경 변수**: https://docs.railway.app/develop/variables
- **OWASP 보안 가이드**: https://owasp.org/www-project-top-ten/

---

**마지막 업데이트**: 2026-02-09  
**보안 레벨**: 🟢 Production Ready
