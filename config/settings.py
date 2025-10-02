"""
설정 관리 모듈
.env 파일 또는 Streamlit secrets에서 API 키와 설정값을 로드하고 관리
"""
import os
from dotenv import load_dotenv

# Streamlit secrets 사용 여부 확인
try:
    import streamlit as st
    USE_STREAMLIT_SECRETS = hasattr(st, 'secrets')
except ImportError:
    USE_STREAMLIT_SECRETS = False


class Settings:
    """애플리케이션 설정을 관리하는 클래스"""

    def __init__(self):
        # .env 파일 로드 (로컬 실행용)
        load_dotenv()

        # Anthropic API 키 설정 - Streamlit secrets 우선, 없으면 환경 변수
        if USE_STREAMLIT_SECRETS:
            try:
                self.anthropic_api_key = st.secrets.get('ANTHROPIC_API_KEY')
            except:
                self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        else:
            self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

        # 모델 설정
        if USE_STREAMLIT_SECRETS:
            try:
                self.llm_model = st.secrets.get('LLM_MODEL', 'claude-sonnet-4-5-20250929')
                self.api_timeout = int(st.secrets.get('API_TIMEOUT', '60'))
                self.max_retries = int(st.secrets.get('MAX_RETRIES', '3'))
                self.usd_to_krw_rate = float(st.secrets.get('USD_TO_KRW_RATE', '1300'))
            except:
                self.llm_model = os.getenv('LLM_MODEL', 'claude-sonnet-4-5-20250929')
                self.api_timeout = int(os.getenv('API_TIMEOUT', '60'))
                self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
                self.usd_to_krw_rate = float(os.getenv('USD_TO_KRW_RATE', '1300'))
        else:
            self.llm_model = os.getenv('LLM_MODEL', 'claude-sonnet-4-5-20250929')
            self.api_timeout = int(os.getenv('API_TIMEOUT', '60'))
            self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
            self.usd_to_krw_rate = float(os.getenv('USD_TO_KRW_RATE', '1300'))

    def validate_api_keys(self) -> tuple[bool, str]:
        """
        API 키 유효성 검증

        Returns:
            tuple[bool, str]: (유효성 여부, 에러 메시지)
        """
        if not self.anthropic_api_key:
            return False, "Anthropic API 키가 설정되지 않았습니다. .env 파일에서 ANTHROPIC_API_KEY를 설정하세요."

        if not self.anthropic_api_key.startswith('sk-ant-'):
            return False, "유효하지 않은 Anthropic API 키입니다. 'sk-ant-'로 시작해야 합니다."

        return True, ""

    def get_api_key(self) -> str:
        """
        Anthropic API 키 반환

        Returns:
            str: API 키
        """
        if not self.anthropic_api_key:
            raise ValueError("Anthropic API 키가 설정되지 않았습니다.")
        return self.anthropic_api_key


# 전역 설정 인스턴스
settings = Settings()