#!/usr/bin/env python3
"""
인플루언서 계약서 자동 검토 시스템 메인 실행 파일

사용법:
    python main.py --contract "계약서.pdf" --output "./output"
    python main.py --contract "계약서.pdf"  # 기본 출력 디렉토리 사용
    python main.py --help  # 도움말 출력
"""

import os
import sys
import json
import logging
import click
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from modules.pdf_reader import PDFReader
from modules.llm_analyzer import LLMAnalyzer
from modules.report_generator import ReportGenerator


def setup_logging(verbose: bool = False) -> None:
    """로깅 설정"""
    level = logging.DEBUG if verbose else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def load_guideline_files() -> tuple[str, str, str, dict]:
    """가이드라인 파일들 로드"""
    data_dir = project_root / "data"
    
    try:
        # 협상 전략 가이드라인 로드
        negotiation_file = data_dir / "guideline_negotiation.txt"
        with open(negotiation_file, 'r', encoding='utf-8') as f:
            guideline_negotiation = f.read()
        
        # 위험 관리 가이드라인 로드
        risk_file = data_dir / "guideline_risk.txt"
        with open(risk_file, 'r', encoding='utf-8') as f:
            guideline_risk = f.read()
        
        # GPTs 심화 지식베이스 로드
        gpts_file = data_dir / "gpts_advanced_knowledge.txt"
        try:
            with open(gpts_file, 'r', encoding='utf-8') as f:
                gpts_advanced_knowledge = f.read()
        except FileNotFoundError:
            gpts_advanced_knowledge = ""  # 파일이 없으면 빈 문자열
        
        # 레드플래그 데이터 로드
        redflags_file = data_dir / "redflags.json"
        with open(redflags_file, 'r', encoding='utf-8') as f:
            redflags_data = json.load(f)
        
        return guideline_negotiation, guideline_risk, gpts_advanced_knowledge, redflags_data
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f"가이드라인 파일을 찾을 수 없습니다: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"레드플래그 JSON 파일 형식이 잘못되었습니다: {e}")


def validate_inputs(contract_path: str, output_dir: str) -> tuple[bool, str]:
    """입력값 유효성 검증"""
    # 계약서 파일 검증
    if not os.path.exists(contract_path):
        return False, f"계약서 파일을 찾을 수 없습니다: {contract_path}"
    
    if not contract_path.lower().endswith('.pdf'):
        return False, "PDF 파일만 지원됩니다."
    
    # 출력 디렉토리 생성 시도
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        return False, f"출력 디렉토리를 생성할 수 없습니다: {e}"
    
    # API 키 검증
    is_valid, message = settings.validate_api_keys()
    if not is_valid:
        return False, message
    
    return True, "모든 입력값이 유효합니다."


@click.command()
@click.option(
    '--contract', '-c',
    required=True,
    type=click.Path(exists=True),
    help='분석할 계약서 PDF 파일 경로'
)
@click.option(
    '--output', '-o',
    default='./output',
    type=click.Path(),
    help='리포트 출력 디렉토리 (기본값: ./output)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='상세한 로그 출력'
)
@click.option(
    '--estimate-cost',
    is_flag=True,
    help='분석 비용 추정만 수행 (실제 분석 안함)'
)
def main(contract: str, output: str, verbose: bool, estimate_cost: bool):
    """
    인플루언서 계약서 자동 검토 시스템
    
    PDF 계약서를 분석하여 위험 요소를 분류하고 협상 전략을 제시합니다.
    """
    # 로깅 설정
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # 환영 메시지
        click.echo("=" * 60)
        click.echo("🔍 인플루언서 계약서 자동 검토 시스템")
        click.echo("=" * 60)
        
        # 입력값 검증
        logger.info("입력값 유효성 검증 중...")
        is_valid, message = validate_inputs(contract, output)
        if not is_valid:
            click.echo(f"❌ 오류: {message}", err=True)
            sys.exit(1)
        
        click.echo(f"📄 분석 대상: {contract}")
        click.echo(f"📁 출력 디렉토리: {output}")
        
        # 가이드라인 파일 로드
        logger.info("가이드라인 파일 로드 중...")
        try:
            guideline_negotiation, guideline_risk, gpts_advanced_knowledge, redflags_data = load_guideline_files()
            click.echo("✅ 가이드라인 파일 로드 완료")
            if gpts_advanced_knowledge:
                click.echo("✅ GPTs 심화 지식베이스 로드 완료")
        except Exception as e:
            click.echo(f"❌ 가이드라인 파일 로드 실패: {e}", err=True)
            sys.exit(1)
        
        # PDF 텍스트 추출
        logger.info("PDF 텍스트 추출 중...")
        click.echo("📖 PDF 텍스트 추출 중...")
        
        pdf_reader = PDFReader()
        
        # PDF 정보 조회
        pdf_info = pdf_reader.get_pdf_info(contract)
        if not pdf_info['is_valid']:
            click.echo(f"❌ PDF 파일이 유효하지 않습니다: {pdf_info.get('error', '알 수 없는 오류')}", err=True)
            sys.exit(1)
        
        click.echo(f"   페이지 수: {pdf_info['page_count']}")
        click.echo(f"   파일 크기: {pdf_info['file_size'] / 1024 / 1024:.1f} MB")
        
        # 텍스트 추출
        try:
            contract_text = pdf_reader.extract_text_from_pdf(contract)
            if not contract_text or len(contract_text.strip()) < 100:
                click.echo("❌ PDF에서 충분한 텍스트를 추출할 수 없습니다.", err=True)
                sys.exit(1)
            
            click.echo(f"✅ 텍스트 추출 완료 ({len(contract_text):,} 문자)")
            
        except Exception as e:
            click.echo(f"❌ PDF 텍스트 추출 실패: {e}", err=True)
            sys.exit(1)
        
        # LLM 분석기 초기화
        try:
            analyzer = LLMAnalyzer()
            click.echo(f"🤖 LLM 분석기 초기화 완료 (Model: Claude Sonnet 4.5)")
        except Exception as e:
            click.echo(f"❌ LLM 분석기 초기화 실패: {e}", err=True)
            sys.exit(1)
        
        # 비용 추정
        logger.info("분석 비용 추정 중...")
        cost_info = analyzer.estimate_cost(contract_text, guideline_negotiation + guideline_risk + gpts_advanced_knowledge)
        
        click.echo("\n💰 예상 분석 비용:")
        click.echo(f"   토큰 수: {cost_info['total_tokens']:,}")
        click.echo(f"   예상 비용: ${cost_info['estimated_cost_usd']:.4f} (약 {cost_info['estimated_cost_krw']:.0f}원)")
        
        if estimate_cost:
            click.echo("\n✅ 비용 추정 완료. 실제 분석은 수행하지 않았습니다.")
            return
        
        # 사용자 확인
        if cost_info['estimated_cost_usd'] > 1.0:  # $1 이상인 경우 경고
            if not click.confirm(f"\n⚠️  예상 비용이 ${cost_info['estimated_cost_usd']:.4f}입니다. 계속하시겠습니까?"):
                click.echo("분석을 취소했습니다.")
                return
        
        # LLM 분석 수행
        logger.info("LLM 분석 시작...")
        click.echo("\n🔍 AI 분석 수행 중... (이 작업은 수 분이 소요될 수 있습니다)")
        
        with click.progressbar(length=100, label="분석 진행") as bar:
            # 진행률 표시를 위한 더미 업데이트
            for i in range(10):
                bar.update(10)
                
            success, result = analyzer.analyze_contract(
                contract_text, guideline_negotiation, guideline_risk, gpts_advanced_knowledge, redflags_data
            )
        
        if not success:
            click.echo(f"\n❌ 분석 실패: {result}", err=True)
            sys.exit(1)
        
        # 응답 유효성 검증
        is_valid_response, validation_message = analyzer.validate_response(result)
        if not is_valid_response:
            click.echo(f"\n⚠️  경고: {validation_message}")
            if not click.confirm("계속해서 리포트를 생성하시겠습니까?"):
                click.echo("리포트 생성을 취소했습니다.")
                return
        
        click.echo("✅ AI 분석 완료")
        
        # 리포트 생성
        logger.info("리포트 생성 중...")
        click.echo("📝 리포트 생성 중...")
        
        try:
            report_generator = ReportGenerator()
            contract_name = os.path.basename(contract)
            
            # 메타데이터 구성
            metadata = {
                'pdf_info': pdf_info,
                'cost_info': cost_info,
                'analysis_info': {
                    'api_provider': analyzer.api_provider,
                    'model': settings.llm_model,
                    'text_length': len(contract_text)
                }
            }
            
            report_path = report_generator.generate_report(
                result, output, contract_name, metadata
            )
            
            click.echo(f"✅ 리포트 생성 완료!")
            click.echo(f"📄 리포트 파일: {report_path}")
            
        except Exception as e:
            click.echo(f"❌ 리포트 생성 실패: {e}", err=True)
            sys.exit(1)
        
        # 완료 메시지
        click.echo("\n" + "=" * 60)
        click.echo("🎉 계약서 분석이 성공적으로 완료되었습니다!")
        click.echo("=" * 60)
        click.echo("\n📋 다음 단계:")
        click.echo("1. 생성된 리포트를 검토하세요")
        click.echo("2. 치명적 위험(🔴) 항목을 우선적으로 확인하세요")
        click.echo("3. 협상 전략에 따라 브랜드와 재협상을 진행하세요")
        
        # 리포트 파일 열기 옵션 (macOS에서만)
        if sys.platform == 'darwin':
            if click.confirm("\n리포트 파일을 바로 열어보시겠습니까?"):
                os.system(f"open '{report_path}'")
        
    except KeyboardInterrupt:
        click.echo("\n\n사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"예상치 못한 오류: {e}")
        click.echo(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()