"""
테스트 스크립트 - 기본 기능 검증
"""
import os
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """모든 모듈 import 테스트"""
    print("🔍 모듈 import 테스트 중...")
    
    try:
        from config.settings import settings
        print("✅ settings 모듈 import 성공")
        
        from modules.pdf_reader import PDFReader
        print("✅ pdf_reader 모듈 import 성공")
        
        from modules.llm_analyzer import LLMAnalyzer
        print("✅ llm_analyzer 모듈 import 성공")
        
        from modules.report_generator import ReportGenerator
        print("✅ report_generator 모듈 import 성공")
        
        from config.prompts import PromptTemplate
        print("✅ prompts 모듈 import 성공")
        
        return True
        
    except ImportError as e:
        print(f"❌ import 실패: {e}")
        return False

def test_settings():
    """설정 모듈 테스트"""
    print("\n🔧 설정 모듈 테스트 중...")
    
    try:
        from config.settings import settings
        
        # API 키 검증 테스트 (키가 없어도 정상 동작해야 함)
        is_valid, message = settings.validate_api_keys()
        print(f"API 키 검증 결과: {message}")
        
        # 모델 설정 확인
        print(f"설정된 모델: {settings.llm_model}")
        print(f"API 타임아웃: {settings.api_timeout}초")
        print(f"최대 재시도: {settings.max_retries}회")
        
        return True
        
    except Exception as e:
        print(f"❌ 설정 모듈 테스트 실패: {e}")
        return False

def test_data_files():
    """데이터 파일 존재 확인"""
    print("\n📄 데이터 파일 테스트 중...")
    
    data_dir = project_root / "data"
    required_files = [
        "guideline_negotiation.txt",
        "guideline_risk.txt", 
        "redflags.json"
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = data_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✅ {filename} 존재 ({size:,} bytes)")
        else:
            print(f"❌ {filename} 없음")
            all_exist = False
    
    return all_exist

def test_prompt_generation():
    """프롬프트 생성 테스트"""
    print("\n📝 프롬프트 생성 테스트 중...")
    
    try:
        from config.prompts import PromptTemplate
        import json
        
        # 샘플 데이터
        sample_guideline = "샘플 협상 가이드라인"
        sample_risk = "샘플 위험 관리 지침"
        sample_redflags = {"red_flags": [{"keyword": "테스트", "severity": "high", "reason": "테스트용"}]}
        
        # 시스템 프롬프트 생성
        system_prompt = PromptTemplate.create_system_prompt(
            sample_guideline, sample_risk, json.dumps(sample_redflags, ensure_ascii=False)
        )
        
        if len(system_prompt) > 100:
            print("✅ 시스템 프롬프트 생성 성공")
            print(f"   길이: {len(system_prompt):,} 문자")
        else:
            print("❌ 시스템 프롬프트가 너무 짧음")
            return False
        
        # 사용자 프롬프트 생성
        user_prompt = PromptTemplate.create_user_prompt("샘플 계약서 텍스트")
        
        if "샘플 계약서 텍스트" in user_prompt:
            print("✅ 사용자 프롬프트 생성 성공")
        else:
            print("❌ 사용자 프롬프트 생성 실패")
            return False
        
        # 토큰 추정 테스트
        estimated_tokens = PromptTemplate.get_token_estimate("안녕하세요 테스트입니다")
        print(f"✅ 토큰 추정 기능 동작 (예상: {estimated_tokens} 토큰)")
        
        return True
        
    except Exception as e:
        print(f"❌ 프롬프트 생성 테스트 실패: {e}")
        return False

def test_report_generator():
    """리포트 생성기 테스트"""
    print("\n📊 리포트 생성기 테스트 중...")
    
    try:
        from modules.report_generator import ReportGenerator
        
        generator = ReportGenerator()
        
        # 샘플 분석 결과
        sample_analysis = """
# 계약서 분석 리포트

## 총평
테스트 분석 결과입니다.

## 🔴 치명적 위험
특별한 위험이 발견되지 않았습니다.

## 협상 전략
기본적인 협상 전략을 수립하세요.
"""
        
        # 임시 출력 디렉토리
        test_output_dir = project_root / "test_output"
        test_output_dir.mkdir(exist_ok=True)
        
        # 리포트 생성 테스트
        report_path = generator.generate_report(
            sample_analysis,
            str(test_output_dir),
            "테스트계약서.pdf"
        )
        
        if Path(report_path).exists():
            print(f"✅ 리포트 생성 성공: {report_path}")
            
            # 파일 내용 확인
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "테스트계약서.pdf" in content and "분석 리포트" in content:
                    print("✅ 리포트 내용 검증 성공")
                else:
                    print("❌ 리포트 내용 검증 실패")
                    return False
        else:
            print("❌ 리포트 파일이 생성되지 않음")
            return False
        
        # 정리
        if Path(report_path).exists():
            Path(report_path).unlink()
        
        return True
        
    except Exception as e:
        print(f"❌ 리포트 생성기 테스트 실패: {e}")
        return False

def main():
    """전체 테스트 실행"""
    print("=" * 60)
    print("🧪 인플루언서 계약서 시스템 테스트")
    print("=" * 60)
    
    tests = [
        ("모듈 Import", test_imports),
        ("설정 모듈", test_settings),
        ("데이터 파일", test_data_files),
        ("프롬프트 생성", test_prompt_generation),
        ("리포트 생성기", test_report_generator)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"⚠️  {test_name} 테스트 실패")
        except Exception as e:
            print(f"❌ {test_name} 테스트 중 예외 발생: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 테스트 결과: {passed}/{total} 통과")
    print("=" * 60)
    
    if passed == total:
        print("🎉 모든 테스트 통과! 시스템이 정상적으로 구동됩니다.")
        return True
    else:
        print("⚠️  일부 테스트 실패. 문제를 해결해주세요.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)