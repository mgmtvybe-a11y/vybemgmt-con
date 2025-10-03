#!/usr/bin/env python3
"""
인플루언서 계약서 자동 검토 시스템 - Web UI
Streamlit 기반 웹 인터페이스
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Tuple
import streamlit as st

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from modules.pdf_reader import PDFReader
from modules.llm_analyzer import LLMAnalyzer
from modules.report_generator import ReportGenerator


def load_guideline_files() -> Tuple[str, str, str, Dict[str, Any]]:
    """
    가이드라인 파일들 로드

    Returns:
        Tuple[str, str, str, Dict[str, Any]]:
            (협상 가이드라인, 위험 가이드라인, GPTs 지식베이스, 레드플래그 데이터)

    Raises:
        FileNotFoundError: 필수 파일이 없는 경우
        json.JSONDecodeError: JSON 파싱 실패 시
    """
    data_dir = project_root / "data"

    try:
        with open(data_dir / "guideline_negotiation.txt", 'r', encoding='utf-8') as f:
            guideline_negotiation = f.read()

        with open(data_dir / "guideline_risk.txt", 'r', encoding='utf-8') as f:
            guideline_risk = f.read()

        try:
            with open(data_dir / "gpts_advanced_knowledge.txt", 'r', encoding='utf-8') as f:
                gpts_advanced_knowledge = f.read()
        except FileNotFoundError:
            gpts_advanced_knowledge = ""

        with open(data_dir / "redflags.json", 'r', encoding='utf-8') as f:
            redflags_data = json.load(f)

        return guideline_negotiation, guideline_risk, gpts_advanced_knowledge, redflags_data

    except FileNotFoundError as e:
        raise FileNotFoundError(f"가이드라인 파일을 찾을 수 없습니다: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 파일 형식이 잘못되었습니다: {e}")


def main():
    """Streamlit 앱 메인 함수"""

    # 페이지 설정
    st.set_page_config(
        page_title="인플루언서 계약서 분석 시스템",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 커스텀 CSS - 모던하고 깔끔한 디자인
    st.markdown("""
        <style>
        /* 메인 컨테이너 */
        .main .block-container {
            padding: 2rem 3rem;
            max-width: 1400px;
        }

        /* 헤더 스타일 */
        h1 {
            color: #1a1a1a;
            font-weight: 700;
            font-size: 2.5rem !important;
            margin-bottom: 0.5rem !important;
        }

        h2 {
            color: #2c3e50;
            font-weight: 600;
            font-size: 1.8rem !important;
            margin-top: 2.5rem !important;
            margin-bottom: 1.2rem !important;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #3498db;
        }

        /* 버튼 스타일 - 검은색 테마 */
        .stButton>button {
            width: 100%;
            background-color: #000000;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.8rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .stButton>button:hover {
            background-color: #333333;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }

        /* 메트릭 카드 - 깔끔한 회색 */
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700;
            color: #1a1a1a;
        }

        [data-testid="stMetric"] {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        /* 파일 업로더 */
        [data-testid="stFileUploader"] {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 2rem;
            border: 2px dashed #dee2e6;
            transition: all 0.3s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #000000;
            background-color: #f8f9fa;
        }

        /* 탭 스타일 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #f8f9fa;
            padding: 8px;
            border-radius: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 6px;
            padding: 12px 24px;
            background-color: white;
            border: 1px solid #dee2e6;
            color: #495057;
            font-weight: 500;
        }

        .stTabs [aria-selected="true"] {
            background-color: #000000;
            color: white !important;
            border-color: #000000;
        }

        /* 다운로드 버튼 */
        .stDownloadButton>button {
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            box-shadow: 0 4px 6px rgba(40, 167, 69, 0.3);
        }

        .stDownloadButton>button:hover {
            background-color: #218838;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(40, 167, 69, 0.4);
        }

        /* 성공/경고/에러 메시지 */
        .stSuccess {
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            border-radius: 8px;
            padding: 1rem;
        }

        .stWarning {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 8px;
            padding: 1rem;
        }

        .stError {
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            border-radius: 8px;
            padding: 1rem;
        }

        .stInfo {
            background-color: #d1ecf1;
            border-left: 4px solid #17a2b8;
            border-radius: 8px;
            padding: 1rem;
        }

        /* 사이드바 */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
            border-right: 1px solid #dee2e6;
        }

        [data-testid="stSidebar"] h2 {
            color: #1a1a1a;
            border-bottom: 2px solid #000000;
        }

        /* 프로그레스 바 */
        .stProgress > div > div > div > div {
            background-color: #000000;
        }

        /* 텍스트 영역 */
        .stTextArea textarea {
            border-radius: 8px;
            border: 2px solid #dee2e6;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }

        /* 구분선 */
        hr {
            margin: 2rem 0;
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #dee2e6, transparent);
        }

        /* 선택 박스 */
        .stSelectbox > div > div {
            border-radius: 8px;
            border-color: #dee2e6;
        }

        /* Expander */
        .streamlit-expanderHeader {
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }
        </style>
    """, unsafe_allow_html=True)

    # 타이틀 - 깔끔하고 심플한 디자인
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0 1rem 0;'>
            <h1 style='margin: 0; color: #000000; font-size: 3rem; font-weight: 800;'>
                📄 인플루언서 계약서 분석
            </h1>
            <p style='color: #6c757d; font-size: 1.2rem; margin-top: 0.5rem; font-weight: 400;'>
                AI 기반 계약서 자동 검토 및 위험 분석 시스템
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 사이드바 - 설정
    with st.sidebar:
        st.header("⚙️ 설정")

        # API 제공자 선택
        st.info("🤖 AI 모델: Claude Sonnet 4.5 (Anthropic)")
        st.markdown("---")

        # API 키 상태 확인
        st.subheader("🔑 API 키 상태")
        is_valid, message = settings.validate_api_keys()

        if is_valid:
            st.success("✅ API 키 설정 완료")
            st.info("사용 중인 제공자: Anthropic (Claude)")
        else:
            st.error("❌ API 키가 설정되지 않았습니다")
            st.warning(message)
            st.info("💡 .env 파일에 API 키를 설정해주세요")

        st.markdown("---")
        st.markdown("### 📖 사용 방법")
        st.markdown("""
        1. PDF 계약서 파일 업로드
        2. 분석 비용 확인
        3. 분석 시작 버튼 클릭
        4. 결과 확인 및 다운로드
        """)

    # 메인 영역
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📄 계약서 업로드")
        uploaded_file = st.file_uploader(
            "PDF 계약서를 업로드하세요",
            type=['pdf'],
            help="분석할 계약서 PDF 파일을 선택하세요"
        )

    with col2:
        st.header("📊 분석 정보")
        if uploaded_file:
            st.metric("파일명", uploaded_file.name)
            file_size_mb = len(uploaded_file.getvalue()) / 1024 / 1024
            st.metric("파일 크기", f"{file_size_mb:.2f} MB")

    # 파일이 업로드된 경우
    if uploaded_file is not None:

        # API 키 검증
        if not is_valid:
            st.error("⚠️ API 키를 먼저 설정해주세요 (.env 파일)")
            st.stop()

        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_pdf_path = tmp_file.name

        try:
            # PDF 정보 추출
            st.markdown("---")
            st.header("📖 PDF 정보")

            with st.spinner("PDF 정보 확인 중..."):
                pdf_reader = PDFReader()
                pdf_info = pdf_reader.get_pdf_info(tmp_pdf_path)

            if not pdf_info['is_valid']:
                st.error(f"❌ PDF 파일이 유효하지 않습니다: {pdf_info.get('error', '알 수 없는 오류')}")
                st.stop()

            info_col1, info_col2, info_col3 = st.columns(3)
            with info_col1:
                st.metric("페이지 수", f"{pdf_info['page_count']} 페이지")
            with info_col2:
                st.metric("파일 크기", f"{pdf_info['file_size'] / 1024 / 1024:.1f} MB")
            with info_col3:
                st.metric("상태", "✅ 유효함")

            # 텍스트 추출
            st.markdown("---")
            with st.spinner("PDF에서 텍스트 추출 중..."):
                contract_text = pdf_reader.extract_text_from_pdf(tmp_pdf_path)

            if not contract_text or len(contract_text.strip()) < 100:
                st.error("❌ PDF에서 충분한 텍스트를 추출할 수 없습니다.")
                st.stop()

            st.success(f"✅ 텍스트 추출 완료 ({len(contract_text):,} 문자)")

            # 추출된 텍스트 미리보기
            with st.expander("📝 추출된 텍스트 미리보기"):
                st.text_area(
                    "계약서 내용",
                    contract_text[:2000] + "..." if len(contract_text) > 2000 else contract_text,
                    height=300,
                    disabled=True
                )

            # 가이드라인 로드
            try:
                guideline_negotiation, guideline_risk, gpts_advanced_knowledge, redflags_data = load_guideline_files()
            except (FileNotFoundError, ValueError) as e:
                st.error(f"❌ 가이드라인 파일 로드 실패: {e}")
                st.stop()

            # LLM 분석기 초기화
            try:
                analyzer = LLMAnalyzer()
            except Exception as e:
                st.error(f"❌ LLM 분석기 초기화 실패: {e}")
                st.stop()

            st.info(f"🤖 사용 모델: Claude Sonnet 4.5")

            # 분석 시작 버튼
            st.markdown("---")
            st.header("🚀 분석 시작")

            analyze_button = st.button(
                "📊 계약서 분석 시작",
                type="primary",
                use_container_width=True
            )

            if analyze_button:
                # 분석 수행
                st.markdown("---")
                st.header("🔍 분석 진행 중...")

                progress_bar = st.progress(0, text="분석을 시작합니다...")
                status_text = st.empty()

                try:
                    # 분석 시작
                    progress_bar.progress(10, text="AI 모델에 요청 전송 중...")

                    success, result = analyzer.analyze_contract(
                        contract_text,
                        guideline_negotiation,
                        guideline_risk,
                        gpts_advanced_knowledge,
                        redflags_data
                    )

                    progress_bar.progress(80, text="분석 결과 수신 완료...")

                    if not success:
                        st.error(f"❌ 분석 실패: {result}")
                        st.stop()

                    # 응답 유효성 검증
                    is_valid_response, validation_message = analyzer.validate_response(result)
                    if not is_valid_response:
                        st.warning(f"⚠️ {validation_message}")

                    progress_bar.progress(90, text="리포트 생성 중...")

                    # 리포트 생성
                    report_generator = ReportGenerator()
                    output_dir = project_root / "output"
                    output_dir.mkdir(exist_ok=True)

                    metadata = {
                        'pdf_info': pdf_info,
                        'analysis_info': {
                            'api_provider': 'anthropic',
                            'model': settings.llm_model,
                            'text_length': len(contract_text)
                        }
                    }

                    report_path = report_generator.generate_report(
                        result,
                        str(output_dir),
                        uploaded_file.name,
                        metadata
                    )

                    progress_bar.progress(100, text="✅ 분석 완료!")

                    # 성공 메시지
                    st.success("🎉 계약서 분석이 성공적으로 완료되었습니다!")

                    # 분석 결과 표시
                    st.markdown("---")
                    st.header("📊 분석 결과")

                    # 결과 탭
                    tab1, tab2 = st.tabs(["📄 분석 리포트", "💾 다운로드"])

                    with tab1:
                        st.markdown(result)

                    with tab2:
                        # 리포트 파일 다운로드
                        with open(report_path, 'r', encoding='utf-8') as f:
                            report_content = f.read()

                        st.download_button(
                            label="📥 Markdown 리포트 다운로드",
                            data=report_content,
                            file_name=os.path.basename(report_path),
                            mime="text/markdown",
                            use_container_width=True
                        )

                        st.info(f"💾 리포트가 저장되었습니다: {report_path}")

                    # 다음 단계 안내
                    st.markdown("---")
                    st.header("📋 다음 단계")
                    st.markdown("""
                    1. **치명적 위험 (🔴)** 항목을 우선적으로 확인하세요
                    2. **불리한 조항 (🟡)** 에 대한 협상 전략을 준비하세요
                    3. **확인 필요 (🔵)** 항목들의 명확화를 요청하세요
                    4. 협상 전략에 따라 브랜드와 재협상을 진행하세요
                    """)

                except Exception as e:
                    progress_bar.empty()
                    st.error(f"❌ 분석 중 오류 발생: {e}")
                    st.exception(e)

        finally:
            # 임시 파일 정리
            if os.path.exists(tmp_pdf_path):
                os.unlink(tmp_pdf_path)

    else:
        # 파일이 업로드되지 않은 경우
        st.info("👆 PDF 계약서를 업로드하여 분석을 시작하세요")

        # 기능 소개
        st.markdown("---")
        st.header("✨ 주요 기능")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            ### 🔍 자동 분석
            - AI 기반 계약서 검토
            - 위험 요소 자동 탐지
            - 법적 근거 제시
            """)

        with col2:
            st.markdown("""
            ### 📊 위험도 분류
            - 🔴 치명적 위험
            - 🟡 불리한 조항
            - 🔵 확인 필요
            """)

        with col3:
            st.markdown("""
            ### 🎯 협상 전략
            - 구체적인 수정안
            - 역제안 문구 제공
            - 협상 우선순위
            """)

        # 주의사항
        st.markdown("---")
        st.warning("""
        ⚠️ **주의사항**
        - 본 분석 결과는 AI 기반 자동 분석으로, 법적 자문을 대체하지 않습니다
        - 중요한 계약의 경우 전문 변호사의 검토를 받으시기 바랍니다
        - .env 파일에 API 키가 설정되어 있어야 합니다
        """)


if __name__ == "__main__":
    main()
