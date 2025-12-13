#!/usr/bin/env python3
"""
일괄 이미지 생성 스크립트
- image_generation_requests.json에 저장된 키워드 확인
- 각 키워드에 대해 외부 이미지 API 호출
- generated_images.json 업데이트
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, Optional


def load_image_requests() -> Dict[str, str]:
    """이미지 생성 요청 로드"""
    json_path = Path(__file__).parent / "image_generation_requests.json"
    
    if not json_path.exists():
        return {}
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_generated_images() -> Dict[str, str]:
    """기존 생성된 이미지 로드"""
    json_path = Path(__file__).parent / "generated_images.json"
    
    if not json_path.exists():
        return {}
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_generated_images(images: Dict[str, str]):
    """생성된 이미지 저장"""
    json_path = Path(__file__).parent / "generated_images.json"
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(images, f, ensure_ascii=False, indent=2)


def generate_image_with_unsplash(keyword: str) -> Optional[str]:
    """
    Unsplash API로 이미지 생성 (무료)
    
    Args:
        keyword: 이미지 키워드
    
    Returns:
        이미지 URL 또는 None
    """
    # Unsplash 무료 API (access key 불필요)
    base_url = "https://source.unsplash.com/1280x720/?"
    
    # 키워드 정리
    query = keyword.replace(" ", ",")
    
    # 이미지 URL 생성
    image_url = f"{base_url}{query}"
    
    try:
        # URL 유효성 검사
        response = requests.head(image_url, timeout=5)
        if response.status_code == 200:
            return image_url
    except:
        pass
    
    return None


def generate_image_with_picsum(keyword: str) -> str:
    """
    Picsum API로 이미지 생성 (fallback)
    
    Args:
        keyword: 이미지 키워드
    
    Returns:
        이미지 URL
    """
    import hashlib
    
    # 키워드 해시로 시드 생성
    seed = hashlib.md5(keyword.encode()).hexdigest()[:8]
    
    return f"https://picsum.photos/seed/{seed}/1280/720"


def process_image_requests():
    """이미지 생성 요청 처리"""
    print("🎨 일괄 이미지 생성 시작\n")
    
    # 요청 로드
    requests_data = load_image_requests()
    
    if not requests_data:
        print("ℹ️ 처리할 이미지 요청이 없습니다")
        return
    
    # 기존 이미지 로드
    generated_images = load_generated_images()
    print(f"📊 기존 이미지: {len(generated_images)}개")
    print(f"📝 새 요청: {len(requests_data)}개\n")
    
    # 각 요청 처리
    success_count = 0
    
    for i, (keyword, prompt) in enumerate(requests_data.items(), 1):
        print(f"[{i}/{len(requests_data)}] '{keyword}'")
        
        # 이미 생성된 경우 스킵
        if keyword in generated_images:
            print(f"  ⏭️ 이미 생성됨")
            continue
        
        # 이미지 생성 시도
        # 1. Unsplash 시도
        image_url = generate_image_with_unsplash(keyword)
        
        if image_url:
            print(f"  ✅ Unsplash 이미지 생성 완료")
            generated_images[keyword] = image_url
            success_count += 1
        else:
            # 2. Picsum fallback
            image_url = generate_image_with_picsum(keyword)
            print(f"  ⚠️ Picsum fallback 사용")
            generated_images[keyword] = image_url
            success_count += 1
        
        print(f"     → {image_url[:80]}...")
    
    # 저장
    if success_count > 0:
        save_generated_images(generated_images)
        print(f"\n✅ {success_count}개 이미지 생성 완료!")
        print(f"📊 총 이미지: {len(generated_images)}개")
        
        # 요청 파일 삭제
        json_path = Path(__file__).parent / "image_generation_requests.json"
        if json_path.exists():
            json_path.unlink()
            print("🗑️ image_generation_requests.json 삭제")
    else:
        print("\nℹ️ 새로 생성된 이미지가 없습니다")


if __name__ == "__main__":
    process_image_requests()
