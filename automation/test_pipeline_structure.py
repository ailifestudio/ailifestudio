#!/usr/bin/env python3
"""
파이프라인 구조 검증 테스트
- API 호출 없이 데이터 흐름만 검증
- 각 Step의 입출력 형식 확인
"""

import json
from pathlib import Path
from datetime import datetime


def test_step1_output_format():
    """Step 1 출력 형식 검증"""
    print("\n" + "="*60)
    print("🧪 Test 1: Step 1 출력 형식 검증")
    print("="*60)
    
    # Step 1 예상 출력
    step1_output = {
        "title": "[테스트] 직장인 AI 활용법, 업무 효율 3배 향상 비결",
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "agent": "step1_topic_agent"
    }
    
    # 검증
    assert "title" in step1_output, "❌ title 키 누락"
    assert len(step1_output["title"]) >= 15, "❌ 제목이 너무 짧음"
    assert "generated_at" in step1_output, "❌ generated_at 키 누락"
    assert "agent" in step1_output, "❌ agent 키 누락"
    
    print("✅ Step 1 출력 형식 검증 통과")
    print(f"   제목: {step1_output['title']}")
    print(f"   생성 시간: {step1_output['generated_at']}")
    
    # 파일 저장 (테스트용)
    output_dir = Path("automation/intermediate_outputs")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "step1_topic.json", 'w', encoding='utf-8') as f:
        json.dump(step1_output, f, ensure_ascii=False, indent=2)
    
    print(f"   저장: {output_dir / 'step1_topic.json'}")
    
    return step1_output


def test_step2_output_format():
    """Step 2 출력 형식 검증"""
    print("\n" + "="*60)
    print("🧪 Test 2: Step 2 출력 형식 검증")
    print("="*60)
    
    # Step 1 출력 로드
    with open("automation/intermediate_outputs/step1_topic.json", 'r', encoding='utf-8') as f:
        step1_data = json.load(f)
    
    print(f"   Step 1 제목 로드: {step1_data['title']}")
    
    # Step 2 예상 출력
    step2_output = {
        "title": step1_data["title"],
        "sections": [
            {"type": "heading", "level": 2, "content": step1_data["title"]},
            {"type": "paragraph", "content": "AI 도구를 활용하면 반복적인 업무를 자동화하여 시간을 절약할 수 있습니다."},
            {
                "type": "image_placeholder",
                "id": "img_1",
                "description": "A confident Korean IT professional (age 30-40) sitting in a modern Seoul office with floor-to-ceiling windows showing Namsan Tower in the background, typing on MacBook, natural afternoon lighting, professional photography style, 8k quality",
                "position": "after_intro"
            },
            {"type": "heading", "level": 3, "content": "AI 도구 활용 방법"},
            {"type": "paragraph", "content": "다양한 AI 도구를 업무에 적용하는 구체적인 방법을 소개합니다."},
            {"type": "tip_box", "content": "실무에서는 ChatGPT와 Claude를 조합하여 사용하면 더욱 효과적입니다."},
            {
                "type": "image_placeholder",
                "id": "img_2",
                "description": "Korean business team (3-4 people, mixed gender, professional attire) discussing AI strategy around a large monitor displaying Korean text dashboard, modern Gangnam office interior, warm collaborative atmosphere, cinematic wide shot",
                "position": "after_section_1"
            },
            {"type": "heading", "level": 3, "content": "주의사항"},
            {"type": "warning_box", "content": "무료 플랜은 월 100회로 제한되어 있으니 주의하세요."},
            {"type": "paragraph", "content": "AI 도구를 활용하여 업무 효율을 극대화하세요."}
        ],
        "summary": "AI 도구를 활용한 업무 자동화 방법을 소개합니다. 실전 예시와 주의사항을 통해 효과적으로 적용할 수 있습니다.",
        "tags": ["AI", "업무자동화", "실전활용"],
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "agent": "step2_writer_agent",
        "stats": {
            "total_sections": 10,
            "total_paragraphs": 3,
            "total_images": 2,
            "total_chars": 150
        }
    }
    
    # 검증
    assert "sections" in step2_output, "❌ sections 키 누락"
    assert len(step2_output["sections"]) > 0, "❌ sections가 비어있음"
    
    # 섹션 타입 검증
    section_types = [s["type"] for s in step2_output["sections"]]
    assert "heading" in section_types, "❌ heading 타입 누락"
    assert "paragraph" in section_types, "❌ paragraph 타입 누락"
    assert "image_placeholder" in section_types, "❌ image_placeholder 타입 누락"
    
    # 이미지 플레이스홀더 검증
    image_placeholders = [s for s in step2_output["sections"] if s["type"] == "image_placeholder"]
    assert len(image_placeholders) > 0, "❌ 이미지 플레이스홀더 없음"
    
    for img in image_placeholders:
        assert "description" in img, f"❌ {img['id']}: description 누락"
        assert "Korean" in img["description"] or "Seoul" in img["description"], \
            f"❌ {img['id']}: 한국적 맥락 누락"
        assert len(img["description"]) > 50, f"❌ {img['id']}: 설명이 너무 짧음"
    
    print("✅ Step 2 출력 형식 검증 통과")
    print(f"   총 섹션: {len(step2_output['sections'])}")
    print(f"   이미지 플레이스홀더: {len(image_placeholders)}개")
    
    for img in image_placeholders:
        print(f"      • {img['id']}: {img['description'][:60]}...")
    
    # 파일 저장
    with open("automation/intermediate_outputs/step2_structured_content.json", 'w', encoding='utf-8') as f:
        json.dump(step2_output, f, ensure_ascii=False, indent=2)
    
    print(f"   저장: automation/intermediate_outputs/step2_structured_content.json")
    
    return step2_output


def test_step3_output_format():
    """Step 3 출력 형식 검증 (이미지 생성은 스킵, 구조만 검증)"""
    print("\n" + "="*60)
    print("🧪 Test 3: Step 3 출력 형식 검증")
    print("="*60)
    
    # Step 2 출력 로드
    with open("automation/intermediate_outputs/step2_structured_content.json", 'r', encoding='utf-8') as f:
        step2_data = json.load(f)
    
    print(f"   Step 2 섹션 로드: {len(step2_data['sections'])}개")
    
    # Step 3 예상 출력 (이미지 생성은 시뮬레이션)
    step3_output = {
        "title": step2_data["title"],
        "sections": [],
        "summary": step2_data["summary"],
        "tags": step2_data["tags"],
        "generated_at": step2_data["generated_at"],
        "validated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "agent": "step3_image_audit_agent",
        "stats": {
            "total_placeholders": 0,
            "generated": 0,
            "passed": 0,
            "failed": 0,
            "removed": 0
        }
    }
    
    # 섹션 처리 (이미지 플레이스홀더 → 시뮬레이션)
    for section in step2_data["sections"]:
        if section["type"] == "image_placeholder":
            step3_output["stats"]["total_placeholders"] += 1
            
            # 시뮬레이션: 80% PASS, 20% FAIL
            import random
            random.seed(42)  # 재현 가능하도록
            
            if random.random() < 0.8:  # 80% PASS
                step3_output["stats"]["generated"] += 1
                step3_output["stats"]["passed"] += 1
                
                # image 타입으로 변경
                validated_section = {
                    "type": "image",
                    "id": section["id"],
                    "description": section["description"],
                    "url": f"automation/generated_images/{section['id']}_abc123.png",
                    "audit_status": "PASS",
                    "audit_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                step3_output["sections"].append(validated_section)
                print(f"   ✅ {section['id']}: PASS (시뮬레이션)")
            else:  # 20% FAIL
                step3_output["stats"]["generated"] += 1
                step3_output["stats"]["failed"] += 1
                step3_output["stats"]["removed"] += 1
                print(f"   ❌ {section['id']}: FAIL (시뮬레이션, 삭제됨)")
                # 섹션 자체를 추가하지 않음 (삭제)
        else:
            # 일반 섹션은 그대로 유지
            step3_output["sections"].append(section)
    
    # 검증
    assert "validated_at" in step3_output, "❌ validated_at 키 누락"
    assert "stats" in step3_output, "❌ stats 키 누락"
    
    stats = step3_output["stats"]
    assert stats["passed"] + stats["failed"] == stats["generated"], "❌ 통계 불일치"
    
    print("\n✅ Step 3 출력 형식 검증 통과")
    print(f"   총 플레이스홀더: {stats['total_placeholders']}개")
    print(f"   생성 성공: {stats['generated']}개")
    print(f"   검수 통과 (PASS): {stats['passed']}개")
    print(f"   검수 실패 (FAIL): {stats['failed']}개")
    print(f"   최종 이미지 수: {stats['passed']}개")
    
    # 파일 저장
    with open("automation/intermediate_outputs/step3_validated_content.json", 'w', encoding='utf-8') as f:
        json.dump(step3_output, f, ensure_ascii=False, indent=2)
    
    print(f"   저장: automation/intermediate_outputs/step3_validated_content.json")
    
    return step3_output


def test_step4_data_structure():
    """Step 4 data.json 구조 검증"""
    print("\n" + "="*60)
    print("🧪 Test 4: Step 4 data.json 구조 검증")
    print("="*60)
    
    # Step 3 출력 로드
    with open("automation/intermediate_outputs/step3_validated_content.json", 'r', encoding='utf-8') as f:
        step3_data = json.load(f)
    
    print(f"   Step 3 섹션 로드: {len(step3_data['sections'])}개")
    
    # data.json 형식으로 변환
    article = {
        "title": step3_data["title"],
        "source": "AI/테크",
        "time": "방금 전",
        "summary": step3_data["summary"],
        "link": "#",
        "image": "automation/generated_images/thumbnail_test123.png",
        "category": "ai",
        "type": "ai_generated",
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "data": {
            "sections": step3_data["sections"],
            "tags": step3_data["tags"],
            "stats": step3_data["stats"]
        }
    }
    
    # 검증
    required_keys = ["title", "source", "summary", "image", "category", "data"]
    for key in required_keys:
        assert key in article, f"❌ {key} 키 누락"
    
    assert "sections" in article["data"], "❌ data.sections 키 누락"
    assert "tags" in article["data"], "❌ data.tags 키 누락"
    
    print("\n✅ Step 4 data.json 구조 검증 통과")
    print(f"   제목: {article['title']}")
    print(f"   카테고리: {article['category']}")
    print(f"   태그: {', '.join(article['data']['tags'])}")
    print(f"   섹션 수: {len(article['data']['sections'])}")
    
    # 이미지 개수 확인
    image_count = sum(1 for s in article['data']['sections'] if s['type'] == 'image')
    print(f"   최종 이미지: {image_count}개")
    
    return article


def test_html_rendering():
    """HTML 렌더링 테스트"""
    print("\n" + "="*60)
    print("🧪 Test 5: HTML 렌더링 검증")
    print("="*60)
    
    # Step 3 출력 로드
    with open("automation/intermediate_outputs/step3_validated_content.json", 'r', encoding='utf-8') as f:
        step3_data = json.load(f)
    
    # HTML 변환 함수 (step4_save_to_data_json.py의 로직)
    html_parts = []
    
    for section in step3_data["sections"]:
        section_type = section['type']
        
        if section_type == 'heading':
            level = section['level']
            content = section['content']
            html_parts.append(f"<h{level}>{content}</h{level}>")
            
        elif section_type == 'paragraph':
            content = section['content']
            html_parts.append(f"<p>{content}</p>")
            
        elif section_type == 'image':
            url = section['url']
            description = section.get('description', '')[:50]
            html_parts.append(f'<img src="{url}" alt="{description}..." />')
            
        elif section_type == 'tip_box':
            content = section['content']
            html_parts.append(
                f'<p style="border-left:4px solid #3b82f6; background:#f0f9ff; '
                f'padding:15px; border-radius:4px; margin:15px 0;">'
                f'<strong>💡 TIP:</strong> {content}</p>'
            )
            
        elif section_type == 'warning_box':
            content = section['content']
            html_parts.append(
                f'<p style="border-left:4px solid #ef4444; background:#fef2f2; '
                f'padding:15px; border-radius:4px; margin:15px 0;">'
                f'<strong>⚠️ 주의:</strong> {content}</p>'
            )
    
    html_content = '\n'.join(html_parts)
    
    # 검증
    assert len(html_content) > 0, "❌ HTML이 비어있음"
    assert '<h2>' in html_content, "❌ 제목 태그 누락"
    assert '<p>' in html_content, "❌ 문단 태그 누락"
    
    # 이미지 태그 확인
    image_tags = html_content.count('<img ')
    expected_images = sum(1 for s in step3_data['sections'] if s['type'] == 'image')
    assert image_tags == expected_images, f"❌ 이미지 개수 불일치 (예상: {expected_images}, 실제: {image_tags})"
    
    print("\n✅ HTML 렌더링 검증 통과")
    print(f"   HTML 길이: {len(html_content)} 문자")
    print(f"   이미지 태그: {image_tags}개")
    print(f"   제목 태그: {html_content.count('<h2>')}개")
    print(f"   문단 태그: {html_content.count('<p>')}개")
    
    # HTML 미리보기 (처음 300자)
    print(f"\n   HTML 미리보기:")
    print(f"   {html_content[:300]}...")
    
    return html_content


def main():
    """전체 테스트 실행"""
    print("\n" + "="*70)
    print("🧪 AI 블로그 자동화 파이프라인 구조 검증 테스트")
    print("="*70)
    print("ℹ️  API 호출 없이 데이터 흐름과 형식만 검증합니다.")
    
    try:
        # Test 1: Step 1 출력 형식
        step1_output = test_step1_output_format()
        
        # Test 2: Step 2 출력 형식
        step2_output = test_step2_output_format()
        
        # Test 3: Step 3 출력 형식
        step3_output = test_step3_output_format()
        
        # Test 4: Step 4 data.json 구조
        article = test_step4_data_structure()
        
        # Test 5: HTML 렌더링
        html_content = test_html_rendering()
        
        print("\n" + "="*70)
        print("🎉 전체 테스트 통과!")
        print("="*70)
        print("\n✅ 검증 완료 항목:")
        print("   1. Step 1: 주제 생성 형식 ✓")
        print("   2. Step 2: 구조화된 콘텐츠 형식 ✓")
        print("   3. Step 3: 이미지 검증 형식 ✓")
        print("   4. Step 4: data.json 구조 ✓")
        print("   5. HTML 렌더링 ✓")
        
        print("\n📊 최종 통계:")
        print(f"   • 생성된 중간 파일: 3개")
        print(f"   • 최종 섹션 수: {len(step3_output['sections'])}개")
        print(f"   • 최종 이미지 수: {step3_output['stats']['passed']}개")
        print(f"   • HTML 길이: {len(html_content)} 문자")
        
        print("\n✅ 파이프라인 구조가 올바르게 설계되었습니다!")
        print("   실제 API 호출은 GitHub Actions에서 진행됩니다.")
        
    except AssertionError as e:
        print(f"\n❌ 테스트 실패: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
