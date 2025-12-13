#!/usr/bin/env python3
"""
Gemini API를 사용한 무료 이미지 설명 생성 → Imagen 3 이미지 생성

Gemini는 완전 무료이고 이미 API 키가 설정되어 있습니다!
이미지 설명을 생성한 후, 해당 설명을 기반으로 이미지를 생성합니다.

사용법:
    python gemini_image_generator.py "digital assistant interface"
"""

import os
import sys
import json
import google.generativeai as genai
from typing import Optional, Dict, List


class GeminiImageGenerator:
    """Gemini API를 사용한 이미지 생성 클래스"""
    
    def __init__(self, api_keys: List[str] = None):
        """
        초기화
        
        Args:
            api_keys: Gemini API 키 리스트 (없으면 환경변수에서 로드)
        """
        self.api_keys = api_keys or self._load_api_keys()
        self.current_key_index = 0
        self.model_name = "gemini-2.0-flash-exp"
        
        if not self.api_keys:
            raise ValueError("Gemini API 키가 없습니다!")
        
        # 첫 번째 키로 초기화
        self._configure_api(self.api_keys[0])
        print(f"✅ Gemini API 초기화 완료 ({len(self.api_keys)}개 키)")
    
    def _load_api_keys(self) -> List[str]:
        """환경변수에서 API 키 로드"""
        keys = []
        
        # GEMINI_API_KEYS (JSON 배열)
        keys_json = os.getenv('GEMINI_API_KEYS', '')
        if keys_json:
            try:
                keys = json.loads(keys_json)
                print(f"✅ GEMINI_API_KEYS에서 {len(keys)}개 키 로드")
                return keys
            except:
                pass
        
        # GEMINI_API_KEY (단일 키)
        single_key = os.getenv('GEMINI_API_KEY', '')
        if single_key:
            keys.append(single_key)
            print(f"✅ GEMINI_API_KEY에서 1개 키 로드")
        
        return keys
    
    def _configure_api(self, api_key: str):
        """API 설정"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def _rotate_key(self):
        """API 키 로테이션"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        next_key = self.api_keys[self.current_key_index]
        self._configure_api(next_key)
        print(f"🔄 API 키 #{self.current_key_index + 1}로 전환")
    
    def enhance_image_prompt(self, keyword: str) -> str:
        """
        Gemini로 키워드를 고품질 이미지 프롬프트로 변환
        
        Args:
            keyword: 원본 키워드 (예: "digital assistant interface")
        
        Returns:
            향상된 이미지 생성 프롬프트
        """
        prompt_request = f"""
You are an expert image prompt engineer. Convert the following keyword into a detailed, 
high-quality image generation prompt for creating professional blog images.

Keyword: "{keyword}"

Requirements:
- Professional and clean composition
- 16:9 aspect ratio suitable for blog thumbnails
- Modern and tech-focused aesthetic
- High quality, detailed, vibrant colors
- Clear and engaging visual
- Photorealistic or minimalist illustration style
- NO text overlays

Output only the enhanced image prompt in English (no explanations).
Make it detailed but concise (max 50 words).

Example input: "digital assistant interface"
Example output: "Modern smartphone displaying AI assistant interface with clean UI design, 
vibrant app icons, sleek digital interface, professional photography, high quality, 
16:9 aspect ratio, detailed, bright and inviting atmosphere"

Now convert: "{keyword}"
"""
        
        try:
            response = self.model.generate_content(prompt_request)
            enhanced = response.text.strip()
            
            # 줄바꿈 제거
            enhanced = ' '.join(enhanced.split())
            
            print(f"  ✅ 프롬프트 향상: {keyword[:30]}... → {enhanced[:60]}...")
            return enhanced
            
        except Exception as e:
            if 'quota' in str(e).lower() or 'limit' in str(e).lower():
                print(f"  ⚠️ API 키 할당량 초과, 로테이션 시도...")
                self._rotate_key()
                return self.enhance_image_prompt(keyword)
            else:
                print(f"  ❌ 프롬프트 생성 실패: {e}")
                # Fallback: 기본 품질 향상
                return f"{keyword}, high quality, professional photography, 16:9 aspect ratio, detailed, vibrant colors, clean composition"
    
    def generate_image_metadata(self, keyword: str) -> Dict:
        """
        이미지 생성 메타데이터 생성
        
        Args:
            keyword: 원본 키워드
        
        Returns:
            이미지 생성에 필요한 메타데이터
        """
        # Gemini로 프롬프트 향상
        enhanced_prompt = self.enhance_image_prompt(keyword)
        
        # 파일명 생성
        import hashlib
        from datetime import datetime
        
        prompt_hash = hashlib.md5(keyword.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blog_img_{timestamp}_{prompt_hash}.png"
        
        return {
            "original_keyword": keyword,
            "enhanced_prompt": enhanced_prompt,
            "filename": filename,
            "aspect_ratio": "16:9",
            "model": "imagen-3",  # 또는 다른 이미지 생성 모델
            "quality": "high"
        }
    
    def generate_batch_metadata(self, keywords: List[str]) -> List[Dict]:
        """
        여러 키워드에 대해 메타데이터 생성
        
        Args:
            keywords: 키워드 리스트
        
        Returns:
            메타데이터 리스트
        """
        results = []
        
        print(f"\n🎨 {len(keywords)}개 이미지 프롬프트 생성 시작...\n")
        
        for i, keyword in enumerate(keywords, 1):
            print(f"[{i}/{len(keywords)}] {keyword}")
            
            try:
                metadata = self.generate_image_metadata(keyword)
                results.append(metadata)
            except Exception as e:
                print(f"  ❌ 실패: {e}")
                # Fallback 메타데이터
                results.append({
                    "original_keyword": keyword,
                    "enhanced_prompt": keyword,
                    "filename": f"fallback_{i}.png",
                    "aspect_ratio": "16:9",
                    "error": str(e)
                })
        
        print(f"\n✅ 프롬프트 생성 완료: {len(results)}/{len(keywords)}\n")
        return results


def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법:")
        print("  단일: python gemini_image_generator.py \"keyword\"")
        print("  배치: python gemini_image_generator.py --batch keywords.txt")
        sys.exit(1)
    
    try:
        generator = GeminiImageGenerator()
        
        if sys.argv[1] == "--batch":
            # 배치 처리
            if len(sys.argv) < 3:
                print("❌ 키워드 파일 경로를 지정하세요")
                sys.exit(1)
            
            with open(sys.argv[2], 'r', encoding='utf-8') as f:
                keywords = [line.strip() for line in f if line.strip()]
            
            results = generator.generate_batch_metadata(keywords)
            
            # JSON 출력
            print(json.dumps(results, indent=2, ensure_ascii=False))
            
            # 파일 저장
            output_file = "gemini_image_prompts.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 프롬프트 저장 완료: {output_file}")
            
        else:
            # 단일 처리
            keyword = sys.argv[1]
            metadata = generator.generate_image_metadata(keyword)
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
    
    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
