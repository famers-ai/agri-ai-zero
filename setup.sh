#!/bin/bash

# AgriAI 로컬 설정 스크립트
# 이 스크립트를 실행하면 자동으로 환경이 설정됩니다

echo "🚀 AgriAI 로컬 환경 설정 시작..."
echo ""

# 1. 가상환경 생성
echo "📦 1/4: Python 가상환경 생성 중..."
python3 -m venv venv

# 2. 가상환경 활성화
echo "✅ 2/4: 가상환경 활성화 중..."
source venv/bin/activate

# 3. 의존성 설치
echo "📚 3/4: 라이브러리 설치 중..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. .env 파일 생성
echo "⚙️  4/4: 환경 변수 파일 생성 중..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env 파일 생성 완료"
    echo ""
    echo "⚠️  중요: .env 파일을 편집하여 API 키를 추가하세요"
    echo "   (지금은 비워둬도 로컬 테스트 가능합니다)"
else
    echo "✅ .env 파일이 이미 존재합니다"
fi

echo ""
echo "🎉 설정 완료!"
echo ""
echo "다음 명령어로 서버를 실행하세요:"
echo ""
echo "  cd backend"
echo "  python main.py"
echo ""
echo "그 다음 브라우저에서 http://localhost:8000 을 여세요!"
echo ""
