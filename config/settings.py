"""
설정 관리 모듈
.env 파일에서 API 키와 설정값을 로드하고 관리
"""
import os
from typing import Optional
from dotenv import load_dotenv


class Settings:
    """애플리케이션 설정을 관리하는 클래스"""
    
    def __init__(self):
        # .env 파일 로드
        load_dotenv()
        
        # API 키 설정
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # 모델 설정
        self.llm_model = os.getenv('LLM_MODEL', 'gpt-4o')
        
        # API 요청 설정
        self.api_timeout = int(os.getenv('API_TIMEOUT', '60'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))

        # 환율 설정 (원화 환산용)
        self.usd_to_krw_rate = float(os.getenv('USD_TO_KRW_RATE', '1300'))
        
    def validate_api_keys(self) -> tuple[bool, str]:
        """
        API 키 유효성 검증
        
        Returns:
            tuple[bool, str]: (유효성 여부, 에러 메시지)
        """
        if not self.openai_api_key and not self.anthropic_api_key:
            return False, "API 키가 설정되지 않았습니다. .env 파일에서 OPENAI_API_KEY 또는 ANTHROPIC_API_KEY를 설정하세요."
        
        if self.openai_api_key and not self.openai_api_key.startswith('sk-'):
            return False, "유효하지 않은 OpenAI API 키입니다. 'sk-'로 시작해야 합니다."
            
        return True, ""
    
    def get_api_provider(self) -> str:
        """
        사용 가능한 API 제공자 반환
        
        Returns:
            str: 'openai' 또는 'anthropic'
        """
        if self.openai_api_key:
            return 'openai'
        elif self.anthropic_api_key:
            return 'anthropic'
        else:
            raise ValueError("사용 가능한 API 키가 없습니다.")
    
    def get_api_key(self, provider: Optional[str] = None) -> str:
        """
        지정된 제공자의 API 키 반환
        
        Args:
            provider: API 제공자 ('openai' 또는 'anthropic')
            
        Returns:
            str: API 키
        """
        if provider is None:
            provider = self.get_api_provider()
            
        if provider == 'openai':
            if not self.openai_api_key:
                raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
            return self.openai_api_key
        elif provider == 'anthropic':
            if not self.anthropic_api_key:
                raise ValueError("Anthropic API 키가 설정되지 않았습니다.")
            return self.anthropic_api_key
        else:
            raise ValueError(f"지원하지 않는 API 제공자: {provider}")


# 전역 설정 인스턴스
settings = Settings()