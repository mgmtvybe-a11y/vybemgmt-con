"""
LLM 분석 엔진 모듈
Anthropic Claude API와 연동하여 계약서 분석을 수행
"""
import json
import logging
import time
from typing import Dict, Any, Tuple
import anthropic
from config.settings import settings
from config.prompts import PromptTemplate


class LLMAnalyzer:
    """Claude를 사용하여 계약서를 분석하는 클래스"""

    def __init__(self):
        """LLMAnalyzer 초기화"""
        self.logger = logging.getLogger(__name__)
        self.client = self._initialize_client()

    def _initialize_client(self):
        """Anthropic API 클라이언트 초기화"""
        try:
            api_key = settings.get_api_key()
            return anthropic.Anthropic(api_key=api_key)
        except Exception as e:
            self.logger.error(f"API 클라이언트 초기화 실패: {e}")
            raise
    
    def analyze_contract(
        self,
        contract_text: str,
        guideline_negotiation: str,
        guideline_risk: str,
        gpts_advanced_knowledge: str,
        redflags_data: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        계약서 분석 수행
        
        Args:
            contract_text: PDF에서 추출한 계약서 텍스트
            guideline_negotiation: 협상 전략 가이드라인
            guideline_risk: 위험 관리 가이드라인
            gpts_advanced_knowledge: GPTs 심화 지식베이스
            redflags_data: 레드플래그 데이터
            
        Returns:
            Tuple[bool, str]: (성공 여부, 분석 결과 또는 에러 메시지)
        """
        try:
            # 토큰 수 체크
            total_text = contract_text + guideline_negotiation + guideline_risk + gpts_advanced_knowledge
            estimated_tokens = PromptTemplate.get_token_estimate(total_text)
            
            if estimated_tokens > 100000:  # 대략적인 토큰 제한
                self.logger.warning(f"토큰 수가 많습니다: {estimated_tokens:,} 토큰")
                return False, f"계약서가 너무 깁니다. 예상 토큰 수: {estimated_tokens:,}. 문서를 나누어 처리해주세요."
            
            # 시스템 프롬프트 구성
            redflags_text = PromptTemplate.format_redflags_for_prompt(redflags_data)
            system_prompt = PromptTemplate.create_system_prompt(
                guideline_negotiation=guideline_negotiation,
                guideline_risk=guideline_risk,
                gpts_advanced_knowledge=gpts_advanced_knowledge,
                redflags=redflags_text
            )
            
            # 사용자 프롬프트 구성
            user_prompt = PromptTemplate.create_user_prompt(contract_text)
            
            # Claude API 호출
            analysis_result = self._call_claude_api(system_prompt, user_prompt)

            if analysis_result:
                self.logger.info("계약서 분석 완료")
                return True, analysis_result
            else:
                return False, "Claude 분석 중 오류가 발생했습니다."

        except Exception as e:
            self.logger.error(f"계약서 분석 실패: {e}")
            return False, f"분석 중 오류 발생: {str(e)}"

    def _call_claude_api(self, system_prompt: str, user_prompt: str) -> str:
        """
        Anthropic Claude API 호출 (재시도 로직 포함)

        Args:
            system_prompt: 시스템 프롬프트
            user_prompt: 사용자 프롬프트

        Returns:
            str: Claude 응답 텍스트
        """
        for attempt in range(settings.max_retries):
            try:
                message = self.client.messages.create(
                    model=settings.llm_model,
                    max_tokens=4000,
                    temperature=0.1,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ],
                    timeout=settings.api_timeout
                )

                return message.content[0].text

            except anthropic.RateLimitError as e:
                self.logger.error(f"Claude API 요금 한도 초과: {e}")
                raise Exception("API 요금 한도를 확인해주세요.")
            except anthropic.APIError as e:
                self.logger.warning(f"API 호출 실패 ({attempt + 1}/{settings.max_retries}): {e}")
                if attempt < settings.max_retries - 1:
                    time.sleep(2 ** attempt)  # 지수적 백오프
                else:
                    self.logger.error(f"모든 재시도 실패: {e}")
                    raise Exception(f"Claude API 오류: {str(e)}")
            except Exception as e:
                self.logger.error(f"Claude API 호출 중 예외 발생: {e}")
                raise
    
    def estimate_cost(self, contract_text: str, guideline_text: str) -> Dict[str, Any]:
        """
        분석 비용 추정 (Claude 기준)

        Args:
            contract_text: 계약서 텍스트
            guideline_text: 가이드라인 텍스트

        Returns:
            Dict[str, Any]: 비용 추정 정보
        """
        total_text = contract_text + guideline_text
        input_tokens = PromptTemplate.get_token_estimate(total_text)
        output_tokens = 4000  # 예상 출력 토큰

        # Claude Sonnet 4.5 가격 기준 (2025년 기준)
        input_cost_per_1m = 3.00  # $3.00 per 1M input tokens
        output_cost_per_1m = 15.00  # $15.00 per 1M output tokens

        input_cost = (input_tokens / 1000000) * input_cost_per_1m
        output_cost = (output_tokens / 1000000) * output_cost_per_1m
        total_cost = input_cost + output_cost

        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "estimated_cost_usd": round(total_cost, 4),
            "estimated_cost_krw": round(total_cost * settings.usd_to_krw_rate, 0),
            "api_provider": "anthropic"
        }
    
    def validate_response(self, response: str) -> Tuple[bool, str]:
        """
        LLM 응답의 유효성 검증
        
        Args:
            response: LLM 응답 텍스트
            
        Returns:
            Tuple[bool, str]: (유효성, 메시지)
        """
        if not response or len(response.strip()) < 100:
            return False, "응답이 너무 짧습니다."
        
        # 필수 섹션 존재 확인
        required_sections = [
            "총평",
            "치명적 위험",
            "협상 전략"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in response:
                missing_sections.append(section)
        
        if missing_sections:
            return False, f"필수 섹션이 누락되었습니다: {', '.join(missing_sections)}"
        
        return True, "유효한 응답입니다."


# 편의를 위한 함수
def analyze_contract_with_llm(
    contract_text: str,
    guideline_negotiation: str,
    guideline_risk: str,
    gpts_advanced_knowledge: str,
    redflags_data: Dict[str, Any]
) -> Tuple[bool, str]:
    """
    계약서를 Claude로 분석하는 편의 함수

    Args:
        contract_text: 계약서 텍스트
        guideline_negotiation: 협상 전략 가이드라인
        guideline_risk: 위험 관리 가이드라인
        gpts_advanced_knowledge: GPTs 심화 지식베이스
        redflags_data: 레드플래그 데이터

    Returns:
        Tuple[bool, str]: (성공 여부, 분석 결과)
    """
    analyzer = LLMAnalyzer()
    return analyzer.analyze_contract(
        contract_text, guideline_negotiation, guideline_risk, gpts_advanced_knowledge, redflags_data
    )