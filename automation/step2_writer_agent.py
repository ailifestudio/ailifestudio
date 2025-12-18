#!/usr/bin/env python3
"""
Step 2: Writer & Art Director Agent (Content Booster)
- 모델: gemini-2.5-flash (JSON 모드)
- 핵심 수정: '짧은 글 금지' 프롬프트 강화 -> 본문 내용 대폭 늘리기
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
        
        # [모델 설정] 2.5-flash
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
                
                # JSON 강제 모드
                response = self.model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return response.text
                
            except Exception as e:
                error_str = str(e)
                print(f"   ⚠️ 오류: {error_str.split('message')[0][:80]}...")
                
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
        print("📝 Step 2: Writer Agent (Rich Content Mode)")
        print(f"   ⚙️  모델: {self.model_name}")
        print("   ⚙️  설정: '본문 길게 쓰기' 강제 적용")
        print("="*60)
        
        writer_prompt = f"""# Role Definition
당신은 IT 비전공자도 쉽게 이해할 수 있는 콘텐츠를 만드는 '친절한 IT 에디터'입니다.

# Topic: {topic}

# Task
위 주제에 대해 **구조화된 JSON 형식**으로 블로그 콘텐츠를 작성하십시오.

# Target Audience
- 코딩을 모르는 일반 직장인
- AI 툴을 업무에 활용하고 싶은 비개발자

# ★ Writing Rules (반드시 준수)
1. **풍부한 내용 (Rich Content):**
   - 각 `paragraph`(문단)은 **최소 3~5문장 이상**으로 길고 자세하게 작성하세요.
   - 단순한 나열이 아니라, "왜(Why)", "어떻게(How)", "예시(Example)"를 포함하여 독자를 설득하세요.
   - 너무 짧은 글은 독자에게 도움이 되지 않습니다. 수다쟁이처럼 친절하게 설명하세요.

2. **코딩 금지:** Python 코드 대신 **'한글 명령어(Prompt)' 예시**를 보여주세요.

3. **이미지 묘사 (Flux Optimized):**
   - `description`: 50단어 이상의 영어. 조명, 구도, 인물, 8k 등 포함.
   - `description_ko`: 한글 요약.

# JSON Output Format
{{
  "title": "매력적인 제목",
  "sections": [
    {{ "type": "heading", "level": 2, "content": "서론" }},
    {{ "type": "paragraph", "content": "여기에는 독자의 공감을 이끌어내는 긴 서론을 작성합니다. 요즘 업무 트렌드가 어떻게 변하고 있는지, 왜 우리가 이 도구를 써야 하는지 최소 3문장 이상 서술하세요." }},
    {{ 
      "type": "image_placeholder", 
      "id": "img_1", 
      "description": "Long English prompt...", 
      "description_ko": "한글 설명", 
      "position": "after_intro" 
    }},
    {{ "type": "heading", "level": 3, "content": "섹션 1: 구체적인 방법" }},
    {{ "type": "paragraph", "content": "여기에는 구체적인 사용법이나 원리를 아주 상세하게 설명합니다. 단순히 '좋다'고 하지 말고, 어떤 상황에서 어떻게 쓰면 좋은지 구체적인 시나리오를 들어 설명하세요. 내용이 충분히 길어야 합니다." }},
    {{ "type": "tip_box", "content": "실무에서 바로 쓸 수 있는 꿀팁" }},
    {{ "type": "paragraph", "content": "팁을 준 뒤에 추가적인 부연 설명을 덧붙이는 문단입니다." }},
    {{ "type": "code_block", "language": "text", "content": "AI에게 질문할 한글 프롬프트 예시" }},
    {{ "type": "warning_box", "content": "주의사항" }},
    {{ "type": "paragraph", "content": "결론 및 마무리 인사" }}
  ],
  "summary": "요약문",
  "tags": ["태그1", "태그2"]
}}
"""
        
        try:
            print("\n✍️ 콘텐츠 생성 중 (길게 쓰는 중)...")
            response_text = self._generate_with_retry(writer_prompt)
            
            clean_text = response_text.strip()
            if clean_text.startswith('```json'): clean_text = clean_text[7:]
            if clean_text.startswith('```'): clean_text = clean_text[3:]
            if clean_text.endswith('```'): clean_text = clean_text[:-3]
            
            content_data = json.loads(clean_text.strip())
            
            # 섹션 개수 체크 (너무 짧으면 경고)
            if len(content_data.get('sections', [])) < 5:
                print("⚠️ 경고: 생성된 섹션 수가 너무 적습니다.")
            
            return {
                "title": topic,
                "sections": content_data.get('sections', []),
                "summary": content_data.get('summary', ''),
                "tags": content_data.get('tags', []),
                "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
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
        print("\n✅ Step 2 완료! (Rich Content Mode)")
    except Exception as e:
        print(f"\n❌ Step 2 실패: {e}")
        exit(1)

if __name__ == "__main__":
    main()
