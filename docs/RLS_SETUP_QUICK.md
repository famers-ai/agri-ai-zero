# 🔐 Supabase RLS 실행 가이드 (5분 완료)

## ⚠️ 실행 전 필수 확인사항

### 1. Railway 환경 변수 확인
**반드시 SERVICE ROLE KEY를 사용해야 합니다!**

```bash
# Railway Dashboard → Variables 탭에서 확인
SUPABASE_KEY=eyJhbGc...  # 이 키가 service_role인지 확인!
```

**확인 방법:**
1. Supabase Dashboard → Project Settings → API
2. `service_role` 키 복사 (⚠️ secret으로 표시됨)
3. Railway Variables의 `SUPABASE_KEY`와 일치하는지 확인

**❌ anon key 사용 시**: RLS 활성화 후 백엔드가 DB에 접근 불가!  
**✅ service_role key 사용 시**: 백엔드가 RLS를 우회하여 정상 작동

---

## 📝 실행 단계

### Step 1: Supabase SQL Editor 열기
1. [Supabase Dashboard](https://supabase.com/dashboard) 접속
2. 프로젝트 선택
3. 왼쪽 메뉴 → **SQL Editor** 클릭

### Step 2: 스크립트 복사 & 실행
1. 아래 **핵심 SQL 코드**를 복사
2. SQL Editor에 붙여넣기
3. **Run** 버튼 클릭 (Ctrl/Cmd + Enter)

### Step 3: 결과 확인
성공 시 다음과 같은 메시지가 표시됩니다:
```
Success. No rows returned
```

---

## 🔑 핵심 SQL 코드 (복사해서 실행)

```sql
-- ============================================================================
-- STEP 1: RLS 활성화
-- ============================================================================
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE diagnoses ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- STEP 2: Service Role 정책 (백엔드 API 전체 접근 허용)
-- ============================================================================
CREATE POLICY "Service role can manage users"
ON users FOR ALL TO service_role
USING (true) WITH CHECK (true);

CREATE POLICY "Service role can manage diagnoses"
ON diagnoses FOR ALL TO service_role
USING (true) WITH CHECK (true);

CREATE POLICY "Service role can manage feedback"
ON feedback FOR ALL TO service_role
USING (true) WITH CHECK (true);

-- ============================================================================
-- STEP 3: Anonymous 접근 차단
-- ============================================================================
REVOKE ALL ON users FROM anon;
REVOKE ALL ON diagnoses FROM anon;
REVOKE ALL ON feedback FROM anon;
```

---

## ✅ 검증 방법

### 1. RLS 활성화 확인
SQL Editor에서 실행:
```sql
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('users', 'diagnoses', 'feedback');
```

**예상 결과:**
```
tablename   | rowsecurity
------------|------------
users       | t
diagnoses   | t
feedback    | t
```

### 2. 정책 확인
```sql
SELECT tablename, policyname, roles
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename;
```

**예상 결과:** 각 테이블당 1개의 정책 (service_role)

### 3. 백엔드 작동 확인
Railway 앱 접속: https://web-production-17eb9.up.railway.app

- ✅ 대시보드가 정상 표시되면 성공!
- ❌ 500 에러 발생 시: Railway Variables의 `SUPABASE_KEY` 확인

---

## 🚨 문제 해결

### 문제 1: "permission denied for table users"
**원인:** Railway에서 anon key를 사용 중  
**해결:**
1. Supabase → Settings → API → `service_role` 키 복사
2. Railway → Variables → `SUPABASE_KEY` 업데이트
3. Railway 자동 재배포 대기 (1-2분)

### 문제 2: "policy already exists"
**원인:** 이미 실행했거나 중복 실행  
**해결:** 무시해도 됨. 검증 쿼리로 확인

### 문제 3: RLS 비활성화하고 싶을 때
```sql
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE diagnoses DISABLE ROW LEVEL SECURITY;
ALTER TABLE feedback DISABLE ROW LEVEL SECURITY;
```

---

## 📊 실행 체크리스트

- [ ] Railway Variables에서 `SUPABASE_KEY`가 service_role인지 확인
- [ ] Supabase SQL Editor에서 핵심 SQL 코드 실행
- [ ] 검증 쿼리로 RLS 활성화 확인
- [ ] Railway 앱 접속하여 정상 작동 확인
- [ ] 대시보드에서 통계가 정상 표시되는지 확인

---

## ⏱️ 예상 소요 시간
- SQL 실행: 10초
- 검증: 1분
- 백엔드 확인: 1분
- **총 3분 이내 완료**

---

**준비되셨나요? 위 핵심 SQL 코드를 복사해서 Supabase SQL Editor에서 실행하세요!** 🚀
