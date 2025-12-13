#!/usr/bin/env python3
"""
Nano Banana Pro를 사용한 AI 이미지 생성 스크립트

이 스크립트는 이미지 키워드를 받아서 Nano Banana Pro로 이미지를 생성하고
AI Drive에 저장한 후 공개 URL을 반환합니다.

사용법:
    python generate_ai_images.py "digital assistant interface on smartphone"
    python generate_ai_images.py --batch keywords.txt
"""

import sys
import json
import subprocess
import os
from pathlib import Path


def generate_single_image(prompt: str, output_dir: str = "/mnt/aidrive/blog_images") -> dict:
    """
    단일 이미지 생성
    
    Args:
        prompt: 이미지 생성 프롬프트 (영어)
        output_dir: 출력 디렉토리
    
    Returns:
        {"success": bool, "url": str, "aidrive_path": str, "prompt": str}
    """
    try:
        # 출력 디렉토리 생성
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 프롬프트 개선
        enhanced_prompt = f"{prompt}, high quality, professional photography, detailed, vibrant colors, clean composition, 16:9 aspect ratio"
        
        # 파일명 생성 (프롬프트 해시 기반)
        import hashlib
        from datetime import datetime
        
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blog_img_{timestamp}_{prompt_hash}.png"
        output_path = os.path.join(output_dir, filename)
        
        print(f"🎨 이미지 생성 중: {prompt[:50]}...")
        print(f"📁 저장 경로: {output_path}")
        
        # TODO: 실제 Nano Banana Pro API 호출
        # 현재는 GenSpark image_generation 도구를 외부에서 호출해야 함
        # 예시 명령어:
        # genspark generate-image --model nano-banana-pro \
        #   --prompt "{enhanced_prompt}" \
        #   --aspect-ratio 16:9 \
        #   --output {output_path}
        
        # 임시: 생성 실패 (API 미구현)
        return {
            "success": False,
            "url": None,
            "aidrive_path": None,
            "prompt": prompt,
            "error": "Nano Banana API not yet implemented in Python script"
        }
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        return {
            "success": False,
            "url": None,
            "aidrive_path": None,
            "prompt": prompt,
            "error": str(e)
        }


def generate_batch_images(keywords_file: str) -> list:
    """
    배치 이미지 생성
    
    Args:
        keywords_file: 키워드 파일 경로 (1줄에 1개 키워드)
    
    Returns:
        생성 결과 리스트
    """
    results = []
    
    try:
        with open(keywords_file, 'r', encoding='utf-8') as f:
            keywords = [line.strip() for line in f if line.strip()]
        
        print(f"📋 총 {len(keywords)}개 이미지 생성 예정")
        
        for i, keyword in enumerate(keywords, 1):
            print(f"\n[{i}/{len(keywords)}] {keyword}")
            result = generate_single_image(keyword)
            results.append(result)
            
            # 성공 시 결과 출력
            if result['success']:
                print(f"✅ 성공: {result['url']}")
            else:
                print(f"❌ 실패: {result.get('error', 'Unknown error')}")
        
        # 결과 요약
        success_count = sum(1 for r in results if r['success'])
        print(f"\n" + "="*50)
        print(f"✅ 성공: {success_count}/{len(results)}")
        print(f"❌ 실패: {len(results) - success_count}/{len(results)}")
        print("="*50)
        
    except Exception as e:
        print(f"❌ 배치 처리 오류: {e}")
    
    return results


def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법:")
        print("  단일 이미지: python generate_ai_images.py \"prompt\"")
        print("  배치 이미지: python generate_ai_images.py --batch keywords.txt")
        sys.exit(1)
    
    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("❌ 키워드 파일 경로를 지정하세요")
            sys.exit(1)
        
        results = generate_batch_images(sys.argv[2])
        
        # JSON 출력
        print("\n" + json.dumps(results, indent=2, ensure_ascii=False))
    else:
        prompt = sys.argv[1]
        result = generate_single_image(prompt)
        
        # JSON 출력
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
