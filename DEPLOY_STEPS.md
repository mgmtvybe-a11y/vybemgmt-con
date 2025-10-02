# 🚀 Streamlit Cloud 배포 단계별 가이드

## 📝 사전 준비 체크리스트

- [x] GitHub 저장소 준비: `mgmtvybe-a11y/vybemgmt-con`
- [x] `app.py` 파일 확인
- [x] `requirements.txt` 확인
- [x] OpenAI API 키 준비

---

## 🌐 배포 시작!

### 1단계: Streamlit Cloud 접속

**https://share.streamlit.io** 접속

→ **Continue with GitHub** 클릭
→ GitHub 로그인
→ Streamlit 권한 승인

---

### 2단계: New app 클릭

우측 상단 **"New app"** 버튼 클릭

---

### 3단계: 배포 설정 입력

**Repository 섹션:**
```
Repository: mgmtvybe-a11y/vybemgmt-con
Branch: main
Main file path: app.py
```

**App URL (선택사항):**
```
App URL: contract-analyzer
```
(원하는 이름으로 변경 가능)

최종 URL: `https://contract-analyzer.streamlit.app`

---

### 4단계: Advanced settings 클릭 (중요!)

하단의 **"Advanced settings"** 클릭

---

### 5단계: Secrets 설정 (필수!)

**"Secrets"** 탭 선택

다음 내용을 **정확히** 복사해서 붙여넣기:

```toml
OPENAI_API_KEY = "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"
LLM_MODEL = "gpt-4o"
API_TIMEOUT = "60"
MAX_RETRIES = "3"
USD_TO_KRW_RATE = "1300"
```

⚠️ **주의사항:**
- 따옴표 `"` 필수
- `=` 양쪽 공백 필수
- 줄 끝에 세미콜론 없음
- 마지막 줄 이후 빈 줄 없음

---

### 6단계: Python 버전 설정 (선택)

**"Python version"** 섹션:
```
3.12
```

입력 후 Enter

---

### 7단계: 배포 시작!

우측 하단 **"Deploy!"** 버튼 클릭

---

## ⏳ 배포 진행 중...

### 로그 확인

배포가 시작되면 실시간 로그가 표시됩니다.

**정상 진행 시 로그:**
```
Cloning repository...
Installing Python 3.12...
Installing requirements from requirements.txt...
  - pdfplumber
  - PyPDF2
  - openai
  - anthropic
  - streamlit
  ...
Building...
Starting server...
✓ Your app is now deployed!
```

**예상 소요 시간:** 2-3분

---

## ✅ 배포 완료!

### 성공 메시지:
```
🎉 Your app is live!
You can now view your Streamlit app in your browser.

URL: https://contract-analyzer.streamlit.app
```

---

## 🧪 배포 후 테스트

### 1. 앱 접속
생성된 URL 클릭 또는 직접 입력

### 2. 기능 확인
- [ ] 페이지 정상 로딩
- [ ] 사이드바 표시
- [ ] "✅ API 키 설정 완료" 메시지 확인
- [ ] PDF 업로드 버튼 작동
- [ ] 테스트 PDF 업로드 (선택)
- [ ] 분석 기능 테스트 (선택)

---

## 🔧 문제 해결

### 문제 1: "ModuleNotFoundError"

**원인:** requirements.txt 누락
**해결:**
1. GitHub 저장소에서 requirements.txt 확인
2. 누락된 패키지 추가
3. Streamlit Cloud → Reboot app

### 문제 2: "API 키 오류"

**원인:** Secrets 미설정 또는 오타
**해결:**
1. Streamlit Cloud → 앱 선택
2. Settings → Secrets
3. API 키 재확인
4. Save 후 Reboot app

### 문제 3: "App is sleeping"

**원인:** 7일간 미사용
**해결:** URL 접속하면 자동으로 깨어남 (10초 소요)

### 문제 4: 배포 실패

**원인:** 코드 에러
**해결:**
1. Logs 탭에서 에러 확인
2. 로컬에서 테스트:
   ```bash
   streamlit run app.py
   ```
3. 에러 수정 후 GitHub push

---

## 🔄 코드 업데이트 방법

코드 수정 후:

```bash
git add .
git commit -m "업데이트 내용"
git push
```

→ Streamlit Cloud가 **자동으로 재배포** (1-2분 소요)

---

## 📊 Streamlit Cloud 대시보드

### 주요 메뉴:
- **Logs**: 실시간 로그 확인
- **Settings**: 설정 변경
- **Secrets**: 환경 변수 관리
- **Reboot app**: 앱 재시작
- **Delete app**: 앱 삭제

---

## 💡 추가 팁

### 1. 커스텀 도메인 (유료)
Streamlit Cloud 유료 플랜 가입 시 가능

### 2. 비공개 앱 (유료)
무료 플랜은 Public만 가능

### 3. 성능 최적화
```python
@st.cache_data
def load_data():
    # 캐싱으로 성능 향상
    pass
```

### 4. 모니터링
- Streamlit Cloud 대시보드에서 실시간 로그 확인
- OpenAI API 사용량은 OpenAI 대시보드에서 확인

---

## 🎉 배포 완료!

이제 전 세계 어디서나 접속 가능한 웹 앱이 되었습니다!

**앱 URL 공유:**
```
https://contract-analyzer.streamlit.app
```

**즐거운 사용 되세요!** 🚀
