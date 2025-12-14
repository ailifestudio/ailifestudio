#!/usr/bin/env python3
"""
Step 3: Image Generation & Vision Audit Agent
- Pollinations.ai로 이미지 생성
- Gemini Vision으로 품질 검수 (PASS/FAIL)
- 검증된 이미지만 최종 콘텐츠에 포함
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


class ImageAuditAgent:
    def __init__(self, config_path="config_ai.json"):
        """Gemini API 초기화"""
        # config 파일은 선택사항 (환경변수 우선)
        self.config = {}
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        
        if not self.api_keys:
            raise ValueError("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
        
        genai.configure(api_key=self.api_keys[0])
        # Vision 모델 사용
        self.vision_model = genai.GenerativeModel("gemini-2.5-flash")
        
        # 출력 디렉토리 생성
        self.output_dir = Path(__file__).parent / "generated_images"
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"✅ Gemini Vision API 초기화 완료")
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
        
        # 이미지 플레이스홀더 개수 카운트
        image_count = sum(1 for s in data['sections'] if s['type'] == 'image_placeholder')
        
        print(f"\n📥 Step 2 출력 로드:")
        print(f"   제목: {data['title']}")
        print(f"   섹션 수: {len(data['sections'])}")
        print(f"   🎨 이미지 플레이스홀더: {image_count}개")
        
        return data
    
    def generate_image(description, img_type, img_id, output_dir):
    """FLUX.1-schnell 모델로 이미지 생성 (Hugging Face Inference API)"""
    import os
    import requests
    import time
    
    # Hugging Face API 설정
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"}
    
    # 프롬프트 최적화 (네거티브 프롬프트 추가)
    positive_prompt = description
    negative_prompt = "low quality, blurry, distorted text, deformed, ugly, bad anatomy"
    
    # API 요청 페이로드
    payload = {
        "inputs": positive_prompt,
        "parameters": {
            "negative_prompt": negative_prompt,
            "width": 1024,
            "height": 576,  # 블로그 썸네일에 최적화된 비율
            "num_inference_steps": 4,  # FLUX.1-schnell은 4스텝 최적
        }
    }
    
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                # 이미지 저장
                filename = f"img_{img_id}_{secrets.token_hex(4)}.png"
                image_path = output_dir / filename
                
                with open(image_path, "wb") as f:
                    f.write(response.content)
                
                print(f"✅ 생성 완료: {image_path.name} (시도 {attempt}/{max_retries})")
                return str(image_path)
            else:
                print(f"⚠️  생성 실패 (HTTP {response.status_code}): {response.text[:100]}")
                if attempt < max_retries:
                    time.sleep(2)
        except Exception as e:
            print(f"❌ 생성 오류 (시도 {attempt}/{max_retries}): {str(e)[:50]}")
            if attempt < max_retries:
                time.sleep(2)
    
    print(f"❌ 최종 실패: {description[:50]}...")
    return None

    
    def audit_image_with_vision(self, image_path: str, original_description: str) -> str:
        """
        Gemini Vision으로 이미지 품질 검수
        
        Returns:
            "PASS" or "FAIL"
        """
        try:
            # 이미지 파일 로드
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Gemini Vision 검수 프롬프트 (완화된 기준)
            audit_prompt = f"""# Role Definition
당신은 실용적인 AI 이미지 품질 관리자(QA Auditor)입니다.

# Input Data
1. Original Description (요청사항): "{original_description}"
2. Generated Image (결과물): (첨부된 이미지)

# Audit Tasks
이미지를 보고 아래 **핵심 기준**만 평가하십시오.

1. ✅ 주제 일치성: 이미지가 Description의 "핵심 주제"를 표현하고 있는가?
   - 예: "office worker"가 있으면 사무실 환경 + 사람만 있으면 OK
   - 세부사항(Namsan Tower, cinematic shot 등)은 무시 가능

2. ✅ 치명적 결함 없음: 명백히 사용 불가능한 이미지인가?
   - 심각한 왜곡, 기형, 깨진 이미지 (약간의 부자연스러움은 OK)
   - 완전히 관계없는 주제 (예: 자동차를 요청했는데 나무)

# Decision Rules (완화됨)
- 핵심 주제만 맞으면 "PASS" 
- 치명적 결함이 없으면 "PASS"
- 두 가지 모두 실패한 경우에만 "FAIL: 이유"

# Important
- 세부 요구사항(배경, 각도, 텍스트 정확성)은 **무시**하십시오
- 반드시 "PASS" 또는 "FAIL"로 시작하는 한 줄만 출력하십시오
"""
            
            print(f"      🔍 Gemini Vision 검수 중...")
            
            # Gemini Vision API 호출
            # 이미지를 PIL Image로 변환
            from PIL import Image
            import io
            
            image_obj = Image.open(io.BytesIO(image_data))
            
            response = self.vision_model.generate_content([audit_prompt, image_obj])
            result = response.text.strip()
            
            # 결과 파싱
            if result.startswith("PASS"):
                print(f"      ✅ 검수 통과: PASS")
                return "PASS"
            else:
                print(f"      ❌ 검수 실패: {result[:60]}")
                return result  # "FAIL: ..." 반환
                
        except Exception as e:
            print(f"      ⚠️ 검수 오류: {e}")
            # 검수 실패 시 FAIL 처리 (안전한 선택)
            return f"FAIL: Audit error - {str(e)}"
    
    def process_content_with_images(self, content_data: dict) -> dict:
        """
        이미지 플레이스홀더를 처리하여 검증된 이미지로 교체
        """
        print("\n" + "="*60)
        print("🎨 Step 3: Image Generation & Vision Audit")
        print("   📁 automation/step3_image_audit_agent.py")
        print("   ⚙️  검수 조건: 라인 145-186 (Vision 검수 프롬프트)")
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
                
                print(f"\n[{stats['total_placeholders']}/{sum(1 for s in sections if s['type'] == 'image_placeholder')}] 이미지 처리 중:")
                print(f"   ID: {section['id']}")
                print(f"   Description: {section['description'][:80]}...")
                
                # 1. 이미지 생성
                image_path, relative_path = self.generate_image(
                    section['description'],
                    section['id']
                )
                
                if image_path and relative_path:
                    stats["generated"] += 1
                    
                    # 생성된 이미지 정보 출력
                    image_filename = Path(image_path).name
                    print(f"      📷 생성 파일: {image_filename}")
                    print(f"      🔗 경로: {relative_path}")
                    
                    # 2. Gemini Vision 검수
                    audit_result = self.audit_image_with_vision(
                        image_path,
                        section['description']
                    )
                    
                    if audit_result == "PASS":
                        # 검수 통과 → image 타입으로 변경
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
                        print(f"      ✅ 저장됨: {relative_path}")
                    else:
                        # 검수 실패 → 삭제 전 정보 출력
                        stats["failed"] += 1
                        stats["removed"] += 1
                        
                        print(f"      ⚠️  삭제 예정: {image_filename}")
                        print(f"      📋 실패 사유: {audit_result[:100]}...")
                        
                        # 실패한 이미지 파일 삭제
                        if Path(image_path).exists():
                            Path(image_path).unlink()
                        
                        print(f"      🗑️  검수 실패로 삭제 완료")
                        # 섹션 자체를 제거 (updated_sections에 추가하지 않음)
                else:
                    # 이미지 생성 실패 → 삭제
                    stats["failed"] += 1
                    stats["removed"] += 1
                    print(f"      🗑️ 생성 실패로 삭제됨")
                    # 섹션 자체를 제거
                
                # API 레이트 리밋 방지
                time.sleep(2)
                
            else:
                # 일반 섹션은 그대로 유지
                updated_sections.append(section)
        
        # 결과 업데이트
        result = {
            "title": content_data['title'],
            "sections": updated_sections,
            "summary": content_data.get('summary', ''),
            "tags": content_data.get('tags', []),
            "generated_at": content_data.get('generated_at', ''),
            "validated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "agent": "step3_image_audit_agent",
            "stats": stats
        }
        
        print("\n" + "="*60)
        print("📊 이미지 처리 통계:")
        print(f"   • 총 플레이스홀더: {stats['total_placeholders']}개")
        print(f"   • 생성 성공: {stats['generated']}개")
        print(f"   • 검수 통과 (PASS): {stats['passed']}개")
        print(f"   • 검수 실패 (FAIL): {stats['failed']}개")
        print(f"   • 삭제됨: {stats['removed']}개")
        print(f"   • 최종 이미지 수: {stats['passed']}개")
        print("="*60)
        
        return result
    
    def save_output(self, data: dict, output_path: str = "automation/intermediate_outputs/step3_validated_content.json"):
        """Step 3 출력 저장"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 출력 저장: {output_path}")
        print(f"   크기: {output_file.stat().st_size} bytes")


def main():
    """메인 실행 함수"""
    try:
        agent = ImageAuditAgent()
        
        # Step 2 출력 로드
        content_data = agent.load_structured_content()
        
        # 이미지 생성 및 검수
        result = agent.process_content_with_images(content_data)
        
        # 출력 저장
        agent.save_output(result)
        
        print("\n" + "="*60)
        print("✅ Step 3 완료!")
        print("="*60)
        print(f"\n다음 단계: python automation/step4_save_to_data_json.py")
        
    except Exception as e:
        print(f"\n❌ Step 3 실패: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
