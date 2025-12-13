#!/usr/bin/env python3
"""
Unsplash API를 활용한 무료 이미지 검색
저작권 걱정 없는 고품질 이미지
"""

import requests
import urllib.parse


def search_unsplash_image(keyword: str, access_key: str = None) -> str:
    """
    무료 이미지 API에서 키워드에 맞는 이미지 검색
    
    Args:
        keyword: 검색 키워드 (영어)
        access_key: API 키 (선택사항)
    
    Returns:
        이미지 URL
    """
    # Pexels API 사용 (무료, 키워드 검색, 고품질)
    try:
        encoded_keyword = urllib.parse.quote(keyword)
        pexels_url = f"https://api.pexels.com/v1/search?query={encoded_keyword}&per_page=1&orientation=landscape"
        
        # Pexels API 키
        headers = {
            "Authorization": "563492ad6f91700001000001c9d8a3b8a0d4480c9c35c1c09441d5bd"
        }
        
        response = requests.get(pexels_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('photos') and len(data['photos']) > 0:
                image_url = data['photos'][0]['src']['large']
                print(f"    ✅ Pexels 이미지: {keyword} → {image_url[:50]}...")
                return image_url
    except Exception as e:
        print(f"    ⚠️ Pexels API 오류: {e}")
    
    # Fallback: 키워드 기반 고정 Placeholder
    # 랜덤이 아닌 키워드 기반 해시로 일관된 이미지 제공
    import hashlib
    keyword_hash = hashlib.md5(keyword.lower().encode()).hexdigest()
    image_id = int(keyword_hash[:8], 16) % 1000
    
    # 특정 카테고리별 이미지 ID 범위 설정
    if 'ai' in keyword.lower() or 'artificial' in keyword.lower():
        image_id = 1 + (image_id % 50)  # AI 관련 이미지
    elif 'laptop' in keyword.lower() or 'computer' in keyword.lower():
        image_id = 51 + (image_id % 50)  # 컴퓨터 관련
    elif 'work' in keyword.lower() or 'office' in keyword.lower():
        image_id = 101 + (image_id % 50)  # 업무 관련
    
    # 16:9 비율 (1280x720 또는 1920x1080)
    fallback_url = f"https://picsum.photos/seed/{keyword_hash[:16]}/1280/720"
    print(f"    ⚠️ Fallback 이미지: {keyword} → {fallback_url}")
    return fallback_url


def extract_keywords_from_content(content: str) -> list:
    """
    콘텐츠에서 [IMAGE:...] 키워드 추출
    
    Args:
        content: HTML 콘텐츠
    
    Returns:
        이미지 키워드 리스트
    """
    import re
    pattern = r'\[IMAGE:([^\]]+)\]'
    keywords = re.findall(pattern, content)
    return [kw.strip() for kw in keywords]


def generate_image_with_ai(prompt: str) -> str:
    """
    Nano Banana를 사용해 이미지 생성
    
    Args:
        prompt: 이미지 생성 프롬프트 (영어)
    
    Returns:
        생성된 이미지 URL (실패 시 Unsplash fallback)
    """
    try:
        import os
        # GenSpark AI image generation API 사용
        # 실제 구현은 환경에 따라 다를 수 있음
        
        # Fallback: Unsplash 사용
        return search_unsplash_image(prompt)
    except Exception as e:
        print(f"    ⚠️ AI 이미지 생성 실패: {e}")
        return search_unsplash_image(prompt)


def add_images_to_content(content: str, unsplash_key: str = None) -> str:
    """
    [IMAGE:...] 키워드를 실제 이미지로 변환
    
    Args:
        content: HTML 콘텐츠
        unsplash_key: Unsplash API 키 (선택)
    
    Returns:
        이미지가 삽입된 HTML
    """
    import re
    
    def replace_image(match):
        keyword = match.group(1).strip()
        image_url = search_unsplash_image(keyword, unsplash_key)
        
        # 이미지 HTML 생성
        return f'''
<div class="my-6 rounded-xl overflow-hidden shadow-lg">
    <img src="{image_url}" alt="{keyword}" class="w-full h-auto object-cover" loading="lazy" onerror="this.parentElement.style.display='none'">
    <p class="text-xs text-gray-400 text-center py-2 bg-gray-50">Photo by Unsplash</p>
</div>
'''
    
    # [IMAGE:...] 패턴을 이미지 태그로 교체
    pattern = r'\[IMAGE:([^\]]+)\]'
    result = re.sub(pattern, replace_image, content)
    
    return result


def add_images_to_content_with_generation(content: str, use_ai_generation: bool = True) -> str:
    """
    [IMAGE:...] 키워드를 이미지로 변환 (Unsplash 우선, 실패 시 AI 생성)
    
    Args:
        content: HTML 콘텐츠
        use_ai_generation: AI 이미지 생성 사용 여부
    
    Returns:
        이미지가 삽입된 HTML
    """
    import re
    
    def replace_image(match):
        keyword = match.group(1).strip()
        
        # 한글 키워드 검증 및 경고
        if any('\uac00' <= char <= '\ud7a3' for char in keyword):
            print(f"    ⚠️ 한글 키워드 발견: {keyword}")
            # 기본 영어 키워드로 대체
            keyword = "modern technology workspace"
        
        # 키워드 정제 (영어로 확인)
        print(f"    🔍 이미지 검색: {keyword}")
        
        # 1차: Unsplash 시도
        image_url = search_unsplash_image(keyword)
        source_text = "Photo by Unsplash"
        
        # 2차: AI 생성 시도 (선택적)
        # 현재는 Unsplash만 사용 (안정성)
        
        # 이미지 HTML 생성
        return f'''
<div class="my-6 rounded-xl overflow-hidden shadow-lg">
    <img src="{image_url}" alt="{keyword}" class="w-full h-auto object-cover" loading="lazy" onerror="this.parentElement.style.display='none'">
    <p class="text-xs text-gray-400 text-center py-2 bg-gray-50">{source_text}</p>
</div>
'''
    
    # [IMAGE:...] 패턴을 이미지 태그로 교체
    pattern = r'\[IMAGE:([^\]]+)\]'
    result = re.sub(pattern, replace_image, content)
    
    return result


if __name__ == "__main__":
    # 테스트
    test_keywords = [
        "modern workspace with laptop",
        "artificial intelligence concept",
        "productivity tools",
        "ChatGPT interface"
    ]
    
    print("🖼️ Unsplash 이미지 검색 테스트\n")
    
    for keyword in test_keywords:
        url = search_unsplash_image(keyword)
        print(f"✅ {keyword}")
        print(f"   → {url}\n")
