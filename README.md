# 📄 인플루언서 계약서 자동 분석 시스템

AI 기반 계약서 자동 검토 및 위험 분석 시스템

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## ✨ 주요 기능

- 🔍 **AI 기반 자동 분석**: GPT-4를 활용한 계약서 자동 검토
- 📊 **위험도 분류**: 치명적 위험(🔴), 불리한 조항(🟡), 확인 필요(🔵)
- 🎯 **협상 전략 제공**: 구체적인 수정안 및 역제안 문구 제시
- 📥 **리포트 다운로드**: Markdown 형식의 상세 분석 리포트

## 🚀 온라인 사용 (권장)

웹 브라우저에서 바로 사용하세요:
**[→ 앱 실행하기](https://your-app-url.streamlit.app)**

## 💻 로컬 실행

### 1. 저장소 클론
```bash
git clone https://github.com/mgmtvybe-a11y/vybemgmt-con.git
cd vybemgmt-con
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
cp .env.example .env
```

`.env` 파일을 열어서 OpenAI API 키 입력:
```env
OPENAI_API_KEY=sk-your-api-key-here
LLM_MODEL=gpt-4o
```

### 4. 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 자동 실행

## 📋 필수 요구사항

- Python 3.9 이상
- OpenAI API 키 (필수)

## 💰 비용 안내

- **Streamlit**: 완전 무료
- **OpenAI API**: 사용량 기반 과금
  - 계약서 1건당 약 $0.50~$1.00

## 📚 사용 방법

1. 웹 앱 접속
2. PDF 계약서 업로드
3. 분석 시작 버튼 클릭
4. 결과 확인 및 다운로드

## 🎨 화면 구성

- **사이드바**: API 설정 및 상태 확인
- **메인 영역**: PDF 업로드 및 분석
- **결과 탭**: 분석 리포트 / 다운로드

## ⚠️ 주의사항

- 본 분석 결과는 AI 기반 자동 분석으로, 법적 자문을 대체하지 않습니다
- 중요한 계약의 경우 전문 변호사의 검토를 받으시기 바랍니다
- API 키는 절대 공개하지 마세요

## 🔧 기술 스택

- **프론트엔드**: Streamlit
- **백엔드**: Python 3.12
- **AI**: OpenAI GPT-4
- **PDF 처리**: pdfplumber, PyPDF2

## 📝 라이선스

MIT License

## 🤝 기여

이슈 및 풀 리퀘스트를 환영합니다!

---

**Made with ❤️ using Streamlit & OpenAI GPT-4**
