#!/usr/bin/env python3
"""
Nano Banana Pro 이미지 생성을 위한 wrapper 모듈

이 모듈은 blog_automation.py에서 호출되어
Nano Banana Pro로 이미지를 생성합니다.

실제 image_generation 도구는 별도로 호출해야 하므로,
이 스크립트는 프롬프트를 준비하고 이미지 URL을 관리하는 역할을 합니다.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Optional, Dict, List


class NanoBananaImageGenerator:
    """Nano Banana Pro 이미지 생성 클래스"""
    
    def __init__(self, output_dir: str = "/mnt/aidrive/blog_images"):
        """
        초기화
        
        Args:
            output_dir: AI Drive 출력 디렉토리
        """
        self.output_dir = output_dir
        self.model = "nano-banana-pro"
        self.aspect_ratio = "16:9"
        self.image_size = "auto"
    
    def enhance_prompt(self, keyword: str) -> str:
        """
        키워드를 고품질 이미지 생성 프롬프트로 변환
        
        Args:
            keyword: 원본 키워드 (예: "digital assistant interface on smartphone")
        
        Returns:
            향상된 프롬프트
        """
        # 기본 품질 향상 키워드
        quality_keywords = [
            "high quality",
            "professional photography",
            "detailed",
            "vibrant colors",
            "clean composition",
            "well-lit",
            "sharp focus"
        ]
        
        # 16:9 비율 명시
        aspect_hint = "16:9 aspect ratio, wide angle"
        
        # 기술/AI 관련 키워드 추가
        if any(word in keyword.lower() for word in ['ai', 'artificial', 'digital', 'tech', 'computer']):
            tech_keywords = "modern technology, futuristic, sleek design"
            enhanced = f"{keyword}, {tech_keywords}, {aspect_hint}, {', '.join(quality_keywords)}"
        else:
            enhanced = f"{keyword}, {aspect_hint}, {', '.join(quality_keywords)}"
        
        return enhanced
    
    def generate_filename(self, keyword: str) -> str:
        """
        키워드 기반 파일명 생성
        
        Args:
            keyword: 이미지 키워드
        
        Returns:
            파일명 (예: blog_img_20251213_abc123.png)
        """
        # 프롬프트 해시
        prompt_hash = hashlib.md5(keyword.encode()).hexdigest()[:12]
        
        # 타임스탬프
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return f"blog_img_{timestamp}_{prompt_hash}.png"
    
    def should_generate_image(self, keyword: str) -> bool:
        """
        이미지 생성 여부 결정
        
        Args:
            keyword: 이미지 키워드
        
        Returns:
            True: 생성 필요, False: 스킵
        """
        # 한글 키워드는 스킵
        if any('\uac00' <= char <= '\ud7a3' for char in keyword):
            print(f"    ⚠️ 한글 키워드 감지, 스킵: {keyword}")
            return False
        
        # 너무 짧은 키워드는 스킵
        if len(keyword.split()) < 3:
            print(f"    ⚠️ 키워드가 너무 짧음, 스킵: {keyword}")
            return False
        
        return True
    
    def prepare_image_generation_request(self, keyword: str) -> Optional[Dict]:
        """
        이미지 생성 요청 준비
        
        Args:
            keyword: 원본 키워드
        
        Returns:
            생성 요청 딕셔너리 또는 None
        """
        if not self.should_generate_image(keyword):
            return None
        
        enhanced_prompt = self.enhance_prompt(keyword)
        filename = self.generate_filename(keyword)
        output_path = os.path.join(self.output_dir, filename)
        
        return {
            "model": self.model,
            "prompt": enhanced_prompt,
            "original_keyword": keyword,
            "aspect_ratio": self.aspect_ratio,
            "image_size": self.image_size,
            "output_path": output_path,
            "filename": filename
        }
    
    def generate_image_url(self, keyword: str) -> str:
        """
        이미지 URL 생성 (실제 생성 또는 fallback)
        
        Args:
            keyword: 이미지 키워드
        
        Returns:
            이미지 URL
        """
        # 현재는 Nano Banana API를 Python 스크립트에서 직접 호출할 수 없으므로
        # Picsum fallback 사용
        
        import hashlib
        keyword_hash = hashlib.md5(keyword.lower().encode()).hexdigest()
        fallback_url = f"https://picsum.photos/seed/{keyword_hash[:16]}/1280/720"
        
        print(f"    ⚠️ Nano Banana 미구현, Fallback 사용: {keyword}")
        return fallback_url


def generate_images_for_keywords(keywords: List[str], use_nano_banana: bool = True) -> Dict[str, str]:
    """
    여러 키워드에 대해 이미지 생성
    
    Args:
        keywords: 이미지 키워드 리스트
        use_nano_banana: Nano Banana 사용 여부
    
    Returns:
        {keyword: image_url} 딕셔너리
    """
    generator = NanoBananaImageGenerator()
    results = {}
    
    for keyword in keywords:
        if use_nano_banana:
            # Nano Banana로 이미지 생성 시도
            url = generator.generate_image_url(keyword)
        else:
            # Picsum fallback
            import hashlib
            keyword_hash = hashlib.md5(keyword.lower().encode()).hexdigest()
            url = f"https://picsum.photos/seed/{keyword_hash[:16]}/1280/720"
        
        results[keyword] = url
    
    return results


# 사용 예시
if __name__ == "__main__":
    generator = NanoBananaImageGenerator()
    
    test_keywords = [
        "digital assistant interface on smartphone",
        "person managing calendar with AI",
        "student researching with AI on laptop"
    ]
    
    print("🎨 Nano Banana Pro 이미지 생성 테스트\n")
    
    for keyword in test_keywords:
        print(f"키워드: {keyword}")
        
        # 프롬프트 향상
        enhanced = generator.enhance_prompt(keyword)
        print(f"  향상된 프롬프트: {enhanced[:80]}...")
        
        # 생성 요청 준비
        request = generator.prepare_image_generation_request(keyword)
        if request:
            print(f"  ✅ 생성 요청 준비 완료")
            print(f"  모델: {request['model']}")
            print(f"  출력: {request['filename']}")
        else:
            print(f"  ❌ 생성 불가")
        
        print()
