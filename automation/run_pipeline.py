#!/usr/bin/env python3
"""
통합 실행 스크립트: 전체 파이프라인을 순차적으로 실행
"""

import subprocess
import sys
from pathlib import Path


def run_step(step_name: str, script_path: str) -> bool:
    """
    개별 Step 실행
    
    Returns:
        성공 여부
    """
    print("\n" + "="*70)
    print(f"🚀 {step_name} 실행 시작")
    print("="*70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=Path(__file__).parent.parent,
            check=True,
            capture_output=False,
            text=True
        )
        
        print(f"\n✅ {step_name} 성공")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {step_name} 실패 (Exit Code: {e.returncode})")
        return False
    except Exception as e:
        print(f"\n❌ {step_name} 오류: {e}")
        return False


def main():
    """메인 실행 함수"""
    print("\n" + "="*70)
    print("🎯 AI 블로그 자동화 파이프라인 시작")
    print("="*70)
    
    steps = [
        ("Step 1: Trend & Topic Agent", "automation/step1_topic_agent.py"),
        ("Step 2: Writer & Art Director Agent", "automation/step2_writer_agent.py"),
        ("Step 3: Image Generation & Vision Audit Agent", "automation/step3_image_audit_agent.py"),
        ("Step 4: Save to data.json", "automation/step4_save_to_data_json.py"),
    ]
    
    for i, (step_name, script_path) in enumerate(steps, 1):
        success = run_step(step_name, script_path)
        
        if not success:
            print("\n" + "="*70)
            print(f"❌ 파이프라인 실패: {step_name}에서 중단됨")
            print("="*70)
            print(f"\n재실행 방법:")
            print(f"   python {script_path}")
            sys.exit(1)
        
        print(f"\n✅ {i}/{len(steps)} 단계 완료")
    
    print("\n" + "="*70)
    print("🎉 전체 파이프라인 성공!")
    print("="*70)
    print("\n생성된 파일:")
    print("   • automation/intermediate_outputs/step1_topic.json")
    print("   • automation/intermediate_outputs/step2_structured_content.json")
    print("   • automation/intermediate_outputs/step3_validated_content.json")
    print("   • data.json (업데이트됨)")
    print("   • contents/*.md")
    print("   • automation/generated_images/*.png")
    
    print("\n다음 단계:")
    print("   git add .")
    print("   git commit -m \"🤖 자동 배포: 블로그 빌드 완료\"")
    print("   git push origin main")


if __name__ == "__main__":
    main()
