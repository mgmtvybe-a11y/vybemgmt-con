"""
PDF 텍스트 추출 모듈
pdfplumber와 PyPDF2를 사용하여 PDF에서 텍스트를 추출
"""
import os
import logging
from typing import Optional
import pdfplumber
import PyPDF2


class PDFReader:
    """PDF 파일에서 텍스트를 추출하는 클래스"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        PDF 파일에서 텍스트 추출
        
        Args:
            pdf_path (str): PDF 파일 경로
            
        Returns:
            str: 추출된 텍스트
            
        Raises:
            FileNotFoundError: PDF 파일이 존재하지 않는 경우
            Exception: PDF 읽기 실패 시
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        
        # 1차 시도: pdfplumber 사용 (더 정확한 텍스트 추출)
        try:
            text = self._extract_with_pdfplumber(pdf_path)
            if text and len(text.strip()) > 0:
                self.logger.info(f"pdfplumber로 텍스트 추출 성공: {len(text)} 문자")
                return text
        except Exception as e:
            self.logger.warning(f"pdfplumber 추출 실패: {e}")
        
        # 2차 시도: PyPDF2 사용 (백업)
        try:
            text = self._extract_with_pypdf2(pdf_path)
            if text and len(text.strip()) > 0:
                self.logger.info(f"PyPDF2로 텍스트 추출 성공: {len(text)} 문자")
                return text
        except Exception as e:
            self.logger.error(f"PyPDF2 추출도 실패: {e}")
        
        raise Exception("PDF에서 텍스트를 추출할 수 없습니다. 파일이 손상되었거나 텍스트가 포함되지 않은 이미지 전용 PDF일 수 있습니다.")
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """
        pdfplumber를 사용한 텍스트 추출
        
        Args:
            pdf_path (str): PDF 파일 경로
            
        Returns:
            str: 추출된 텍스트
        """
        text_parts = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"--- 페이지 {page_num} ---\n{page_text}")
                        self.logger.debug(f"페이지 {page_num}: {len(page_text)} 문자 추출")
                    else:
                        self.logger.warning(f"페이지 {page_num}: 텍스트가 없음")
                except Exception as e:
                    self.logger.warning(f"페이지 {page_num} 처리 중 오류: {e}")
                    continue
        
        return "\n\n".join(text_parts)
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """
        PyPDF2를 사용한 텍스트 추출
        
        Args:
            pdf_path (str): PDF 파일 경로
            
        Returns:
            str: 추출된 텍스트
        """
        text_parts = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"--- 페이지 {page_num} ---\n{page_text}")
                        self.logger.debug(f"페이지 {page_num}: {len(page_text)} 문자 추출")
                    else:
                        self.logger.warning(f"페이지 {page_num}: 텍스트가 없음")
                except Exception as e:
                    self.logger.warning(f"페이지 {page_num} 처리 중 오류: {e}")
                    continue
        
        return "\n\n".join(text_parts)
    
    def validate_pdf(self, pdf_path: str) -> tuple[bool, str]:
        """
        PDF 파일 유효성 검증
        
        Args:
            pdf_path (str): PDF 파일 경로
            
        Returns:
            tuple[bool, str]: (유효성 여부, 메시지)
        """
        if not os.path.exists(pdf_path):
            return False, f"파일이 존재하지 않습니다: {pdf_path}"
        
        if not pdf_path.lower().endswith('.pdf'):
            return False, "PDF 파일만 지원됩니다."
        
        file_size = os.path.getsize(pdf_path)
        if file_size == 0:
            return False, "빈 파일입니다."
        
        # 파일 크기 체크 (100MB 제한)
        max_size = 100 * 1024 * 1024  # 100MB
        if file_size > max_size:
            return False, f"파일이 너무 큽니다. 최대 100MB까지 지원됩니다. (현재: {file_size / 1024 / 1024:.1f}MB)"
        
        return True, "유효한 PDF 파일입니다."
    
    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        PDF 파일 정보 조회
        
        Args:
            pdf_path (str): PDF 파일 경로
            
        Returns:
            dict: PDF 정보 (페이지 수, 파일 크기 등)
        """
        info = {
            'file_path': pdf_path,
            'file_size': 0,
            'page_count': 0,
            'is_valid': False
        }
        
        try:
            info['file_size'] = os.path.getsize(pdf_path)
            
            with pdfplumber.open(pdf_path) as pdf:
                info['page_count'] = len(pdf.pages)
                info['is_valid'] = True
                
        except Exception as e:
            self.logger.error(f"PDF 정보 조회 실패: {e}")
            info['error'] = str(e)
        
        return info


# 편의를 위한 함수
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    PDF에서 텍스트를 추출하는 편의 함수
    
    Args:
        pdf_path (str): PDF 파일 경로
        
    Returns:
        str: 추출된 텍스트
    """
    reader = PDFReader()
    return reader.extract_text_from_pdf(pdf_path)