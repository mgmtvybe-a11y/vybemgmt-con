# 🚀 Streamlit Cloud 배포 가이드

## 📋 배포 전 체크리스트

- [x] Python 코드 문법 검증 완료
- [x] requirements.txt 준비 완료
- [x] .env.example 준비 완료
- [x] .gitignore 설정 완료
- [x] README.md 작성 완료

## 🌐 Streamlit Cloud 배포 단계

### 1️⃣ GitHub 저장소 준비

이미 저장소가 있습니다:
```
https://github.com/mgmtvybe-a11y/vybemgmt-con
```

### 2️⃣ Streamlit Cloud 접속

1. **https://share.streamlit.io** 방문
2. **Sign in with GitHub** 클릭
3. GitHub 계정으로 로그인

### 3️⃣ 앱 배포

1. **New app** 버튼 클릭

2. **배포 설정 입력:**
   - **Repository**: `mgmtvybe-a11y/vybemgmt-con`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: 원하는 이름 (예: `contract-analyzer`)

3. **Advanced settings** 클릭

4. **Secrets** 탭에서 다음 입력 (실제 API 키로 교체):
```toml
OPENAI_API_KEY = "your-actual-openai-api-key-here"
LLM_MODEL = "gpt-4o"
API_TIMEOUT = "60"
MAX_RETRIES = "3"
USD_TO_KRW_RATE = "1300"
```

5. **Python version** (선택사항):
   - `3.12` 선택

6. **Deploy!** 버튼 클릭

### 4️⃣ 배포 완료 대기

- 약 2-3분 소요
- 로그에서 진행 상황 확인
- 빌드 성공 시 URL 생성됨

### 5️⃣ 접속

생성된 URL로 접속:
```
https://contract-analyzer.streamlit.app
```

## 🔄 업데이트 방법

코드 수정 후 GitHub에 push하면 자동 재배포:

```bash
git add .
git commit -m "업데이트 내용"
git push
```

약 1-2분 후 자동으로 반영됩니다.

## 🔧 트러블슈팅

### 문제 1: "ModuleNotFoundError"
**원인**: requirements.txt에 패키지 누락
**해결**: requirements.txt 확인 후 push

### 문제 2: "API 키 오류"
**원인**: Secrets 미설정
**해결**: Streamlit Cloud → Settings → Secrets 확인

### 문제 3: "앱이 슬립 모드"
**원인**: 7일간 미사용
**해결**: URL 접속하면 자동으로 깨어남 (10초 소요)

### 문제 4: "배포 실패"
**원인**: Python 버전 불일치
**해결**: Settings → Python version 3.12 선택

## 📊 배포 후 확인사항

- [ ] 메인 페이지 로딩 확인
- [ ] 사이드바 API 키 상태 확인
- [ ] PDF 업로드 테스트
- [ ] 분석 기능 동작 확인
- [ ] 리포트 다운로드 확인

## 💡 최적화 팁

### 캐싱 활용
```python
@st.cache_data
def load_guideline_files():
    # 가이드라인 파일 로드
    pass
```

### 세션 스테이트 활용
```python
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
```

## 🎯 배포 완료 후

1. **README.md 업데이트**
   - 앱 URL 추가
   - 배지 추가

2. **사용자 테스트**
   - 실제 PDF로 분석 테스트
   - 다양한 케이스 확인

3. **모니터링**
   - Streamlit Cloud 대시보드에서 로그 확인
   - OpenAI API 사용량 모니터링

## 📞 지원

- **Streamlit 문서**: https://docs.streamlit.io
- **커뮤니티 포럼**: https://discuss.streamlit.io
- **GitHub Issues**: 프로젝트 저장소

---

**배포 성공을 기원합니다! 🎉**
