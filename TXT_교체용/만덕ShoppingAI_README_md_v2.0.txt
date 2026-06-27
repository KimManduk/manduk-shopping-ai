# 만덕 Shopping AI Studio v2.0 Clean

새로 정리한 통합 프로젝트입니다.

## 목표
상품 URL/상품명 입력 → AI 팀이 상품 분석, 대본, 장면, 이미지 프롬프트, 영상 프롬프트, TTS, MP4 작업, 업로드 플랜까지 한 번에 준비합니다.

## 현재 포함
- React + Vite 프론트
- FastAPI 백엔드
- URL 분석
- AI 제작 패키지 생성
- AI 팀/직원 진행 화면
- 작업 큐
- 쇼츠 대본/장면/자막/해시태그
- 이미지/영상/TTS/MP4 작업 생성
- 업로드 플랜
- 데모 모드
- API 연결 자리

## 실행

### 백엔드
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 프론트
```bash
cd frontend
npm install
npm run dev
```

## 확인
- 백엔드: http://127.0.0.1:8000
- 프론트: 터미널에 뜨는 localhost 주소

## GitHub 업로드
```bash
git add .
git commit -m "Manduk Shopping AI Studio v2 clean"
git push
```
