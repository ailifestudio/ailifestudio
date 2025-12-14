#!/usr/bin/env python3
"""
API 키 로테이션 시스템
- 여러 API 키를 순환하며 사용
- 할당량 초과 시 자동으로 다음 키로 전환
"""

import google.generativeai as genai
import os
import json
from datetime import datetime

class APIKeyRotator:
    def __init__(self, keys_file="api_keys.json"):
        """여러 API 키 로드"""
        # 환경변수에서 키 목록 로드 (JSON 형식)
        keys_json = os.getenv('GEMINI_API_KEYS', '[]')
        self.api_keys = json.loads(keys_json)
        
        if not self.api_keys:
            # Fallback: 단일 키
            single_key = os.getenv('GEMINI_API_KEY', '')
            if single_key:
                self.api_keys = [single_key]
        
        self.current_key_index = 0
        self.max_retries = len(self.api_keys)
        
        print(f"✅ {len(self.api_keys)}개의 API 키 로드됨")
    
    def get_model(self, model_name="gemini-2.5-flash"):
        """현재 API 키로 모델 초기화"""
        if not self.api_keys:
            raise ValueError("❌ API 키가 없습니다.")
        
        current_key = self.api_keys[self.current_key_index]
        genai.configure(api_key=current_key)
        return genai.GenerativeModel(model_name)
    
    def generate_content(self, prompt, max_retries=None):
        """할당량 초과 시 자동으로 다음 키로 전환"""
        if max_retries is None:
            max_retries = self.max_retries
        
        for attempt in range(max_retries):
            try:
                model = self.get_model()
                response = model.generate_content(prompt)
                
                print(f"✅ API 키 #{self.current_key_index + 1} 사용 성공")
                return response.text
                
            except Exception as e:
                error_msg = str(e).lower()
                
                # 할당량 초과 에러 감지
                if 'quota' in error_msg or 'limit' in error_msg or '429' in error_msg:
                    print(f"⚠️ API 키 #{self.current_key_index + 1} 할당량 초과")
                    
                    # 다음 키로 전환
                    self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                    
                    if attempt < max_retries - 1:
                        print(f"🔄 API 키 #{self.current_key_index + 1}로 재시도...")
                        continue
                    else:
                        print("❌ 모든 API 키의 할당량이 초과되었습니다.")
                        raise Exception("모든 API 키 할당량 초과. 24시간 후 재시도하세요.")
                else:
                    # 할당량 외 다른 에러
                    print(f"❌ API 에러: {e}")
                    raise
        
        raise Exception("최대 재시도 횟수 초과")


# 사용 예시
if __name__ == "__main__":
    # 환경변수 설정 예시 (GitHub Actions에서):
    # GEMINI_API_KEYS='["key1", "key2", "key3"]'
    
    rotator = APIKeyRotator()
    
    try:
        result = rotator.generate_content("안녕하세요. 테스트 메시지입니다.")
        print(f"\n결과:\n{result}")
    except Exception as e:
        print(f"\n❌ 실패: {e}")
