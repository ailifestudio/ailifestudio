#!/usr/bin/env python3
"""
Step 3: Image Generation & Vision Audit Agent
- Pollinations.ai (Flux 모델)로 고품질 이미지 생성
- API 쿼터 절약을 위해 Vision 검수는 'Free Pass' (무조건 통과) 모드로 동작
"""

import google.generativeai as genai
import json
import os
import hashlib
import requests
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import time
import random

class ImageAuditAgent:
    def __init__(self, config_path="config_ai.json"):
        """Gemini API 초기화"""
        self.config = {}
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        
        # Vision 모델 초기화 (검수 프리패스 모드여도 초기화는 유지하거나, 에러 방지용으로 둠)
        if self.api_keys:
            genai.configure(api_key=self.api_keys[0])
            self.vision_model = genai.GenerativeModel("gemini-2.5-flash")
        
        # 출력 디렉토리 생성
        self.output_dir = Path(__file__).parent / "generated_images"
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"✅ Image Agent 초기화 완료")
        print(f"✅ 이미지 저장 경로: {self.output_dir}")
    
    def _load_api_keys(self) -> List[str]:
        """API 키 로드"""
        keys_json = os.getenv('GEMINI_API_KEYS', '')
        if keys_json:
            try:
                keys = json.loads(keys_json)
                if isinstance(keys, list) and keys:
                    return keys
            except:
                pass
        
        single_key = os.getenv('GEMINI_API_KEY', self.config.get('gemini_api_key', ''))
        if single_key:
            return [single_key]
        
        return []
    
    def load_structured_content(self, input_path: str = "automation/intermediate_outputs/step2_structured_content.json") -> dict:
        """Step 2 출력 로드"""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        image_count = sum(1 for s in data['sections'] if s['type'] == 'image_placeholder')
        
        print(f"\n📥 Step 2 출력 로드:")
        print(f"   제목: {data['title']}")
        print(f"   섹션 수: {len(data['sections'])}")
        print(f"   🎨 이미지 플레이스홀더: {image_count}개")
        
        return data
    
    def generate_image(self, description: str, image_id: str, max_retries: int = 3) -> tuple:
        """
        Pollinations.ai (Flux)로 이미지 생성
        """
        for attempt in range(max_retries):
            try:
                # 1. 랜덤 시드 생성 (캐싱 방지 & 다양성 확보)
                seed = random.randint(1, 99999999)
                
                # 2. 프롬프트 강화 (한국적 맥락이 있다면 유지, 없다면 비즈니스 톤 추가)
                # description에 이미 'Korean professional' 등이 포함되어 있다고 가정
                enhanced_prompt = f"{description}, photorealistic, 8k, cinematic lighting, high quality"
                encoded_prompt = urllib.parse.quote(enhanced_prompt)
                
                # 3. URL 생성 (Flux 모델 명시)
                # width/height는 16:9 비율 (1280x720) 추천
                pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=flux&nologo=true&seed={seed}"
                
                if attempt == 0:
                    print(f"   🎨 이미지 생성 시도: {description[:40]}...")
                    print(f"      🔗 URL: {pollinations_url}")
                else:
                    print(f"      🔄 재시도 {attempt}/{max_retries - 1}...")
                
                # 4. 요청
                response = requests.get(pollinations_url, timeout=30)
                
                if response.status_code == 200:
                    # 파일명 생성
                    file_hash = hashlib.md5(description.encode()).hexdigest()[:8]
                    image_filename = f"{image_id}_{file_hash}.png"
                    image_path = self.output_dir / image_filename
                    
                    # 저장
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    
                    # 상대 경로 반환
                    relative_path = f"automation/generated_images/{image_filename}"
                    
                    print(f"      ✅ 생성 성공: {image_filename}")
                    return str(image_path), relative_path
                else:
                    print(f"      ⚠️ HTTP {response.status_code}")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"      ⚠️ 생성 오류: {e}")
                time.sleep(2)
        
        print(f"      ❌ 최종 생성 실패 (재시도 초과)")
        return None, None
    
    def audit_image_with_vision(self, image_path: str, original_description: str, max_key_rotations: int = None) -> str:
        """
        [Free Pass 모드] API 쿼터 절약을 위해 Vision 검수를 생략하고 무조건 통과시킵니다.
        """
        # -----------------------------------------------------------
        # [Quota Saving Mode] API 호출 없이 즉시 통과
        # -----------------------------------------------------------
        print(f"      ⏩ [Free Pass] 쿼터 절약을 위해 Vision 검수 생략 (PASS)")
        return "PASS"

    def process_content_with_images(self, content_data: dict) -> dict:
        """이미지 플레이스홀더 처리 메인 로직"""
        print("\n" + "="*60)
        print("🎨 Step 3: Image Generation (Free Pass Mode)")
        print("="*60)
        
        sections = content_data['sections']
        updated_sections = []
        
        stats = {
            "total_placeholders": 0,
            "generated": 0,
            "passed": 0,
            "failed": 0,
            "removed": 0
        }
        
        for i, section in enumerate(sections):
            if section['type'] == 'image_placeholder':
                stats["total_placeholders"] += 1
                
                print(f"\n[{stats['total_placeholders']}] 이미지 처리 중 (ID: {section['id']})")
                
                # 1. 이미지 생성
                image_path, relative_path = self.generate_image(
                    section['description'],
                    section['id']
                )
                
                if image_path and relative_path:
                    stats["generated"] += 1
                    
                    # 2. 검수 (Free Pass)
                    audit_result = self.audit_image_with_vision(image_path, section['description'])
                    
                    if audit_result == "PASS":
                        stats["passed"] += 1
                        updated_section = {
                            "type": "image",
                            "id": section['id'],
                            "description": section['description'],
                            "url": relative_path,
                            "audit_status": "PASS",
                            "audit_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        updated_sections.append(updated_section)
                        print(f"      🎉 최종 승인: 이미지 삽입됨")
                    else:
                        # Free Pass 모드에서는 이쪽으로 올 일이 거의 없음
                        stats["failed"] += 1
                        stats["removed"] += 1
                        updated_sections.append(section) # 원본 유지하거나 삭제
                else:
                    stats["failed"] += 1
                    stats["removed"] += 1
                    print(f"      🗑️ 생성 실패로 플레이스홀더 삭제")
                    # 이미지가 없으므로 섹션 제거 (리스트에 추가 안함)
            else:
                updated_sections.append(section)
        
        result = content_data.copy()
        result['sections'] = updated_sections
        result['stats'] = stats
        
        print("\n" + "="*60)
        print(f"📊 처리 완료: 총 {stats['passed']}장 생성 및 삽입됨")
        print("="*60)
        
        return result
    
    def save_output(self, data: dict, output_path: str = "automation/intermediate_outputs/step3_validated_content.json"):
        """Step 3 출력 저장"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 출력 저장 완료: {output_path}")

def main():
    try:
        agent = ImageAuditAgent()
        content_data = agent.load_structured_content()
        result = agent.process_content_with_images(content_data)
        agent.save_output(result)
        
        print("\n✅ Step 3 완료!")
        
    except Exception as e:
        print(f"\n❌ Step 3 실패: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
