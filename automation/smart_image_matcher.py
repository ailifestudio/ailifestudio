#!/usr/bin/env python3
"""
스마트 이미지 매칭 시스템
- 새 키워드를 기존 생성된 이미지와 지능적으로 매칭
- 유사도 기반 매칭 (의미론적 유사성)
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
import re


class SmartImageMatcher:
    """지능형 이미지 매칭"""
    
    def __init__(self):
        self.generated_images = self.load_generated_images()
        self.keywords_map = self.build_keywords_map()
    
    def load_generated_images(self) -> Dict[str, str]:
        """생성된 이미지 로드"""
        json_path = Path(__file__).parent / "generated_images.json"
        
        if not json_path.exists():
            return {}
        
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def build_keywords_map(self) -> Dict[str, List[str]]:
        """
        각 이미지 키워드를 개별 단어로 분리하여 검색 가능하게 만듦
        
        Returns:
            {original_keyword: [word1, word2, ...]}
        """
        keywords_map = {}
        
        for keyword in self.generated_images.keys():
            # 소문자로 변환, 특수문자 제거
            words = re.findall(r'\b\w+\b', keyword.lower())
            keywords_map[keyword] = words
        
        return keywords_map
    
    def calculate_similarity(self, query: str, target_keywords: List[str]) -> float:
        """
        쿼리와 타겟 키워드 간의 유사도 계산
        
        Args:
            query: 검색할 키워드
            target_keywords: 비교 대상 키워드 리스트
        
        Returns:
            유사도 (0.0 ~ 1.0)
        """
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        target_words = set(target_keywords)
        
        if not query_words or not target_words:
            return 0.0
        
        # Jaccard 유사도
        intersection = len(query_words & target_words)
        union = len(query_words | target_words)
        
        return intersection / union if union > 0 else 0.0
    
    def find_best_match(self, query: str, threshold: float = 0.2) -> Tuple[str, float]:
        """
        쿼리와 가장 유사한 이미지 키워드 찾기
        
        Args:
            query: 검색할 키워드
            threshold: 최소 유사도 임계값
        
        Returns:
            (매칭된_키워드, 유사도) 또는 (None, 0.0)
        """
        best_match = None
        best_score = 0.0
        
        for keyword, words in self.keywords_map.items():
            score = self.calculate_similarity(query, words)
            
            if score > best_score:
                best_score = score
                best_match = keyword
        
        if best_score >= threshold:
            return best_match, best_score
        
        return None, 0.0
    
    def get_image_url(self, query: str) -> str:
        """
        쿼리에 대한 이미지 URL 반환
        
        Args:
            query: 검색할 키워드
        
        Returns:
            이미지 URL
        """
        # 1. 정확한 매칭 확인
        if query in self.generated_images:
            return self.generated_images[query]
        
        # 2. 유사도 기반 매칭
        best_match, score = self.find_best_match(query)
        
        if best_match:
            url = self.generated_images[best_match]
            print(f"  🔍 '{query}' → '{best_match}' (유사도: {score:.2f})")
            return url
        
        # 3. 기본 AI 관련 이미지 반환
        default_keywords = [
            "futuristic AI assistant interface with personalized data",
            "professional working on computer with AI assistant dashboard",
            "creative thought process with AI integration"
        ]
        
        for default_key in default_keywords:
            if default_key in self.generated_images:
                print(f"  ⚠️ '{query}' → 기본 AI 이미지 사용")
                return self.generated_images[default_key]
        
        # 4. Fallback: 첫 번째 이미지
        if self.generated_images:
            first_key = list(self.generated_images.keys())[0]
            return self.generated_images[first_key]
        
        # 5. 최종 fallback
        return "https://via.placeholder.com/1280x720/1e293b/60a5fa?text=AI+Image"


# 전역 매처 인스턴스
_matcher = None


def get_matcher() -> SmartImageMatcher:
    """매처 싱글톤 인스턴스 반환"""
    global _matcher
    if _matcher is None:
        _matcher = SmartImageMatcher()
    return _matcher


def search_image_smart(keyword: str) -> str:
    """
    스마트 이미지 검색 (외부에서 호출 가능)
    
    Args:
        keyword: 검색할 키워드
    
    Returns:
        이미지 URL
    """
    matcher = get_matcher()
    return matcher.get_image_url(keyword)


if __name__ == "__main__":
    # 테스트
    import sys
    
    matcher = SmartImageMatcher()
    
    print(f"📊 생성된 이미지: {len(matcher.generated_images)}개\n")
    
    # 테스트 쿼리
    test_queries = [
        "digital knowledge base with various data types",
        "AI brain generating creative ideas",
        "modern workspace with laptop",
        "team collaboration with AI tools",
        "data visualization dashboard"
    ]
    
    if len(sys.argv) > 1:
        test_queries = sys.argv[1:]
    
    print("🔍 매칭 테스트:\n")
    
    for query in test_queries:
        print(f"🔎 '{query}'")
        url = matcher.get_image_url(query)
        print(f"   → {url[:80]}...")
        print()
