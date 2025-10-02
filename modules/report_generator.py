"""
리포트 생성 모듈
LLM 분석 결과를 Markdown 형식의 리포트로 저장
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import json


class ReportGenerator:
    """분석 결과를 리포트로 생성하는 클래스"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_report(
        self,
        analysis_result: str,
        output_dir: str,
        contract_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        분석 결과를 Markdown 리포트로 저장
        
        Args:
            analysis_result: LLM 분석 결과 텍스트
            output_dir: 출력 디렉토리
            contract_name: 계약서 파일명 (확장자 제외)
            metadata: 추가 메타데이터 (파일 정보, 분석 정보 등)
            
        Returns:
            str: 생성된 리포트 파일 경로
        """
        try:
            # 출력 디렉토리 생성
            os.makedirs(output_dir, exist_ok=True)
            
            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_contract_name = self._sanitize_filename(contract_name)
            report_filename = f"계약서분석리포트_{safe_contract_name}_{timestamp}.md"
            report_path = os.path.join(output_dir, report_filename)
            
            # 리포트 내용 구성
            report_content = self._build_report_content(
                analysis_result, contract_name, metadata
            )
            
            # 파일 저장
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.logger.info(f"리포트 생성 완료: {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"리포트 생성 실패: {e}")
            raise
    
    def _build_report_content(
        self,
        analysis_result: str,
        contract_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        리포트 내용 구성
        
        Args:
            analysis_result: LLM 분석 결과
            contract_name: 계약서 이름
            metadata: 추가 메타데이터
            
        Returns:
            str: 완성된 리포트 내용
        """
        # 헤더 정보 구성
        header = self._generate_header(contract_name, metadata)
        
        # 분석 결과 정리
        cleaned_analysis = self._clean_analysis_result(analysis_result)
        
        # 푸터 정보 구성
        footer = self._generate_footer(metadata)
        
        # 전체 리포트 조합
        report_content = f"{header}\n\n{cleaned_analysis}\n\n{footer}"
        
        return report_content
    
    def _generate_header(
        self,
        contract_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        리포트 헤더 생성
        
        Args:
            contract_name: 계약서 이름
            metadata: 메타데이터
            
        Returns:
            str: 헤더 텍스트
        """
        current_time = datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
        
        header = f"""# 인플루언서 계약서 자동 분석 리포트

## 📄 분석 대상 계약서
**파일명**: {contract_name}
**분석 일시**: {current_time}
**분석 시스템**: 인플루언서 계약서 자동 검토 시스템 v1.0

---"""
        
        # 메타데이터가 있으면 추가 정보 포함
        if metadata:
            if 'pdf_info' in metadata:
                pdf_info = metadata['pdf_info']
                header += f"""

## 📊 계약서 정보
- **파일 크기**: {pdf_info.get('file_size', 0) / 1024 / 1024:.1f} MB
- **페이지 수**: {pdf_info.get('page_count', 0)} 페이지"""
            
            if 'cost_info' in metadata:
                cost_info = metadata['cost_info']
                header += f"""

## 💰 분석 비용 정보
- **사용 토큰**: {cost_info.get('total_tokens', 0):,} 토큰
- **예상 비용**: ${cost_info.get('estimated_cost_usd', 0):.4f} (약 {cost_info.get('estimated_cost_krw', 0):.0f}원)
- **API 제공자**: {cost_info.get('api_provider', 'Unknown')}"""
        
        header += "\n\n---"
        return header
    
    def _clean_analysis_result(self, analysis_result: str) -> str:
        """
        LLM 분석 결과 정리 및 포맷팅
        
        Args:
            analysis_result: 원본 분석 결과
            
        Returns:
            str: 정리된 분석 결과
        """
        # 기본적인 텍스트 정리
        cleaned = analysis_result.strip()
        
        # 중복된 구분선 제거
        cleaned = cleaned.replace("---\n---", "---")
        
        # 불필요한 공백 줄 정리
        lines = cleaned.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            is_empty = line.strip() == ""
            if is_empty and prev_empty:
                continue  # 연속된 빈 줄 제거
            cleaned_lines.append(line)
            prev_empty = is_empty
        
        return '\n'.join(cleaned_lines)
    
    def _generate_footer(self, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        리포트 푸터 생성
        
        Args:
            metadata: 메타데이터
            
        Returns:
            str: 푸터 텍스트
        """
        footer = """---

## 📋 리포트 사용 안내

### ⚠️ 주의사항
1. 본 분석 결과는 AI 기반 자동 분석으로, 법적 자문을 대체하지 않습니다.
2. 중요한 계약의 경우 전문 변호사의 검토를 받으시기 바랍니다.
3. 분석 결과는 제공된 가이드라인 기준으로 작성되었으며, 실제 상황에 따라 해석이 달라질 수 있습니다.

### 📞 추가 문의
- 시스템 관련 문의: 개발팀
- 법적 자문 문의: 법무팀
- 협상 전략 문의: 비즈니스 팀

### 📝 다음 단계
1. **치명적 위험 (🔴)** 항목들을 우선 검토하고 대응 방안 수립
2. **불리한 조항 (🟡)** 에 대한 협상 전략 준비
3. **확인 필요 (🔵)** 항목들의 명확화 요청
4. 전체적인 협상 우선순위에 따라 브랜드와 재협상 진행

---

*Report generated by 인플루언서 계약서 자동 검토 시스템*"""
        
        return footer
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        파일명에서 사용할 수 없는 문자 제거
        
        Args:
            filename: 원본 파일명
            
        Returns:
            str: 정리된 파일명
        """
        # 확장자 제거
        if filename.endswith('.pdf'):
            filename = filename[:-4]
        
        # 파일시스템에서 사용할 수 없는 문자 제거
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # 길이 제한 (너무 긴 파일명 방지)
        if len(filename) > 50:
            filename = filename[:50]
        
        return filename
    
    def generate_summary_report(
        self,
        reports_dir: str,
        output_path: Optional[str] = None
    ) -> str:
        """
        여러 리포트의 요약 리포트 생성
        
        Args:
            reports_dir: 리포트들이 있는 디렉토리
            output_path: 출력 파일 경로 (없으면 자동 생성)
            
        Returns:
            str: 생성된 요약 리포트 경로
        """
        try:
            # 리포트 파일들 찾기
            report_files = [
                f for f in os.listdir(reports_dir)
                if f.startswith('계약서분석리포트_') and f.endswith('.md')
            ]
            
            if not report_files:
                raise ValueError("분석 리포트를 찾을 수 없습니다.")
            
            # 출력 경로 설정
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(reports_dir, f"종합분석요약_{timestamp}.md")
            
            # 요약 리포트 내용 생성
            summary_content = self._build_summary_content(reports_dir, report_files)
            
            # 파일 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            self.logger.info(f"요약 리포트 생성 완료: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"요약 리포트 생성 실패: {e}")
            raise
    
    def _build_summary_content(self, reports_dir: str, report_files: list) -> str:
        """
        요약 리포트 내용 생성
        
        Args:
            reports_dir: 리포트 디렉토리
            report_files: 리포트 파일 목록
            
        Returns:
            str: 요약 리포트 내용
        """
        current_time = datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
        
        summary = f"""# 📊 계약서 분석 종합 요약 리포트

**생성 일시**: {current_time}
**분석 계약서 수**: {len(report_files)}개

---

## 📋 분석 대상 계약서 목록

"""
        
        # 각 리포트의 기본 정보 추출
        for i, report_file in enumerate(report_files, 1):
            report_path = os.path.join(reports_dir, report_file)
            contract_name = self._extract_contract_name_from_report(report_path)
            file_size = os.path.getsize(report_path) / 1024  # KB
            
            summary += f"{i}. **{contract_name}**\n"
            summary += f"   - 리포트 파일: `{report_file}`\n"
            summary += f"   - 파일 크기: {file_size:.1f} KB\n\n"
        
        summary += """---

## 🎯 주요 권장사항

1. **모든 계약서의 치명적 위험 (🔴) 항목 우선 검토**
2. **공통적으로 발견되는 불리한 조항들에 대한 표준 대응 방안 수립**
3. **업계별 특수 위험 요소에 대한 전문가 자문 고려**

---

## 📞 후속 조치

- [ ] 각 계약서별 상세 리포트 검토
- [ ] 법무팀과 위험 항목 검토 미팅 예약
- [ ] 브랜드별 협상 전략 수립
- [ ] 표준 계약서 템플릿 개선 검토

---

*본 요약 리포트는 개별 분석 리포트를 기반으로 자동 생성되었습니다.*
*상세한 분석 내용은 각 개별 리포트를 참고하시기 바랍니다.*"""
        
        return summary
    
    def _extract_contract_name_from_report(self, report_path: str) -> str:
        """
        리포트 파일에서 계약서 이름 추출
        
        Args:
            report_path: 리포트 파일 경로
            
        Returns:
            str: 계약서 이름
        """
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # "파일명:" 라인에서 계약서 이름 추출
            lines = content.split('\n')
            for line in lines:
                if '**파일명**:' in line:
                    return line.split('**파일명**:')[1].strip()
            
            # 파일명에서 추출 (백업)
            filename = os.path.basename(report_path)
            parts = filename.split('_')
            if len(parts) >= 2:
                return parts[1]
            
            return "Unknown"
            
        except Exception:
            return "Unknown"


# 편의를 위한 함수
def generate_analysis_report(
    analysis_result: str,
    output_dir: str,
    contract_name: str,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    분석 결과 리포트를 생성하는 편의 함수
    
    Args:
        analysis_result: LLM 분석 결과
        output_dir: 출력 디렉토리
        contract_name: 계약서 이름
        metadata: 메타데이터
        
    Returns:
        str: 생성된 리포트 파일 경로
    """
    generator = ReportGenerator()
    return generator.generate_report(analysis_result, output_dir, contract_name, metadata)