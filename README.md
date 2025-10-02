# 📄 인플루언서 계약서 자동 분석 시스템

AI 기반 계약서 자동 검토 및 위험 분석 시스템

## ✨ 주요 기능

- 🔍 **AI 기반 자동 분석**: GPT-4를 활용한 계약서 자동 검토
- 📊 **위험도 분류**: 치명적 위험(🔴), 불리한 조항(🟡), 확인 필요(🔵)
- 🎯 **협상 전략 제공**: 구체적인 수정안 및 역제안 문구 제시
- 📥 **리포트 다운로드**: Markdown 형식의 상세 분석 리포트

## 🚀 빠른 시작

### 온라인 버전 (권장)
배포 후 여기에 URL이 표시됩니다

### 로컬 실행

1. **저장소 클론**
```bash
git clone https://github.com/yourusername/vybemgmt.git
cd vybemgmt
```

2. **패키지 설치**
```bash
pip install -r requirements.txt
```

3. **환경 변수 설정**
```bash
cp .env.example .env
# .env 파일에 OpenAI API 키 입력
```

4. **실행**
```bash
streamlit run app.py
```

## 📋 필수 요구사항

- Python 3.9 이상
- OpenAI API 키 (필수)
- 또는 Anthropic Claude API 키 (선택)

## 🔑 API 키 설정

`.env` 파일 생성 후:

```env
OPENAI_API_KEY=sk-your-api-key-here
LLM_MODEL=gpt-4o
```

## 📚 사용 방법

1. PDF 계약서 업로드
2. 분석 시작 버튼 클릭
3. 결과 확인 및 다운로드

## ⚠️ 주의사항

- 본 분석 결과는 AI 기반 자동 분석으로, 법적 자문을 대체하지 않습니다
- 중요한 계약의 경우 전문 변호사의 검토를 받으시기 바랍니다

## 📄 라이선스

MIT License
