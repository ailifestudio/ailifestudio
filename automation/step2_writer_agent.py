#!/usr/bin/env python3
"""
Step 2: Writer & Art Director Agent (JSON Enforcement Mode)
- 모델: gemini-2.5-flash (작동 확인됨!)
- 핵심 수정: 'response_mime_type: application/json' 설정 추가
  -> AI가 문법 오류 없는 완벽한 JSON만 출력하도록 강제함 (문법 에러 해결)
"""

import google.generativeai as genai
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import time

class WriterAgent:
    def __init__(self, config_path="config_ai.json"):
        """Gemini API 초기화"""
        self.config = {}
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        
        if not self.api_keys:
            raise ValueError("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
        
        genai.configure(api_key=self.api_keys[0])
        
        # [모델 설정] 2.5-flash 사용
        self.model_name = "gemini-2.5-flash"
        self.model = genai.GenerativeModel(self.model_name)
    
    def _load_api_keys(self) -> List[str]:
        keys_json = os.getenv('GEMINI_API_KEYS', '')
        if keys_json:
            try:
                keys = json.loads(keys_json)
                return keys if isinstance(keys, list) else []
            except:
                pass
        single_key = os.getenv('GEMINI_API_KEY', self.config.get('gemini_api_key', ''))
        return [single_key] if single_key else []
    
    def _generate_with_retry(self, prompt: str, max_key_rotations: int = None) -> str:
        if max_key_rotations is None:
            max_key_rotations = len(self.api_keys)
        
        for attempt in range(max_key_rotations):
            try:
                print(f"   🤖 시도: {self.model_name} (Key #{self.current_key_index + 1})")
                
                # [핵심 수정] JSON 강제 모드 설정 (문법 에러 방지)
                response = self.model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return response.text
                
            except Exception as e:
                error_str = str(e)
                print(f"   ⚠️ 오류: {error_str.split('message')[0][:80]}...")
                
                # 429 (쿼터 초과) 발생 시 키 교체
                if '429' in error_str or 'quota' in error_str.lower():
                    if self.current_key_index < len(self.api_keys) - 1:
                        self.current_key_index += 1
                        print(f"   🔄 쿼터 초과! Key #{self.current_key_index + 1}로 교체")
                        genai.configure(api_key=self.api_keys[self.current_key_index])
                        self.model = genai.GenerativeModel(self.model_name)
                        time.sleep(2)
                        continue
                    else:
                        print("❌ 모든 키의 쿼터가 소진되었습니다.")
                        raise e
                
                time.sleep(5)
                if attempt == max_key_rotations - 1:
                    raise e
    
    def load_topic(self, input_path: str = "automation/intermediate_outputs/step1_topic.json") -> dict:
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_structured_content(self, topic: str) -> dict:
        print("\n" + "="*60)
        print("📝 Step 2: Writer Agent (JSON Enforcement Mode)")
        print(f"   ⚙️  모델: {self.model_name}")
        print("   ⚙️  설정: JSON 출력 강제 (Syntax Error 방지)")
        print("="*60)
        
        writer_prompt = f"""# Role Definition
당신은 IT 비전공자도 쉽게 이해할 수 있는 콘텐츠를 만드는 '친절한 IT 에디터'이자 '아트 디렉터'입니다.

# Topic: {topic}

# Task
위 주제에 대해 **구조화된 JSON 형식**으로 블로그 콘텐츠를 작성하십시오.

# Target Audience & Tone
- 코딩을 모르는 일반 직장인 대상
- 친절하고, 쉽고, 바로 써먹을 수 있는 실용적인 톤

# Writing Rules
1. **코딩 금지:** Python, API 코드 대신 **'한글 명령어(Prompt)' 예시**를 보여주세요.
2. **이미지 묘사(중요):**
   - `description` (영어): 50단어 이상. 조명, 구도, 인물, 8k, photorealistic 등 구체적 묘사.
   - `description_ko` (한글): 관리자가 알아볼 수 있는 간단한 요약.

# JSON Output Format
반드시 아래 JSON 스키마를 따르세요:

{{
  "title": "매력적인 제목",
  "sections": [
    {{ "type": "heading", "level": 2, "content": "서론 제목" }},
    {{ "type": "paragraph", "content": "본문 내용..." }},
    {{ 
      "type": "image_placeholder", 
      "id": "img_1", 
      "description": "Long detailed English prompt for Flux generation...", 
      "description_ko": "한글 설명", 
      "position": "after_intro" 
    }},
    {{ "type": "tip_box", "content": "꿀팁 내용" }},
    {{ "type": "code_block", "language": "text", "content": "AI에게 질문할 한글 프롬프트 예시" }},
    {{ "type": "warning_box", "content": "주의사항" }}
  ],
  "summary": "요약문",
  "tags": ["태그1", "태그2"]
}}
"""
        
        try:
            print("\n✍️ 콘텐츠 생성 중...")
            response_text = self._generate_with_retry(writer_prompt)
            
            # JSON 파싱
            # (JSON 강제 모드를 썼으므로 마크다운 제거 로직이 굳이 필요 없지만, 안전을 위해 유지)
            clean_text = response_text.strip()
            if clean_text.startswith('```json'): clean_text = clean_text[7:]
            if clean_text.startswith('```'): clean_text = clean_text[3:]
            if clean_text.endswith('```'): clean_text = clean_text[:-3]
            
            content_data = json.loads(clean_text.strip())
            
            return {
                "title": topic,
                "sections": content_data.get('sections', []),
                "summary": content_data.get('summary', ''),
                "tags": content_data.get('tags', []),
                "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except json.JSONDecodeError as e:
            print(f"\n❌ JSON 파싱 실패: {e}")
            print(f"▼ 원본 응답:\n{response_text[:500]}...") # 디버깅용 출력
            raise
        except Exception as e:
            print(f"\n❌ 실패: {e}")
            raise

    def save_output(self, data: dict, output_path: str = "automation/intermediate_outputs/step2_structured_content.json"):
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 저장 완료: {output_path}")

def main():
    try:
        agent = WriterAgent()
        topic = agent.load_topic()
        result = agent.generate_structured_content(topic['title'])
        agent.save_output(result)
        print("\n✅ Step 2 완료! (JSON Mode)")
    except Exception as e:
        print(f"\n❌ Step 2 실패: {e}")
        exit(1)

if __name__ == "__main__":
    main()
