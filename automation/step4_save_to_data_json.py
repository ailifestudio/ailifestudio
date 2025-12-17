#!/usr/bin/env python3
"""
Step 4: Save to data.json & Markdown (Optimization Version)
- 최적화: 불필요한 번역 API 호출 제거 (Step 2에서 만든 한글 설명 사용)
- 스타일: 박스 깨짐 방지 (>)
- 이미지: 화면엔 이미지만 표시 + 한글(Alt)/영어(주석) 숨김 처리
"""

import json
import os
from datetime import datetime
from pathlib import Path

class DataSaver:
    def __init__(self):
        """초기화 (API 설정 불필요)"""
        self.output_dir = Path(__file__).parent.parent
        self.data_file = self.output_dir / 'data.json'
        self.contents_dir = self.output_dir / 'contents'
        self.contents_dir.mkdir(exist_ok=True)

    def load_validated_content(self, input_path="automation/intermediate_outputs/step3_validated_content.json"):
        """Step 3 결과 로드"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Step 3 결과 파일이 없습니다.")
            return None

    def create_markdown_content(self, data):
        """Markdown 변환 로직 (번역 과정 없이 즉시 생성)"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today_date = datetime.now().strftime('%Y-%m-%d')
        
        # Front Matter
        md = "---\n"
        md += f"title: \"{data['title']}\"\n"
        md += f"date: {current_time}\n"
        md += f"layout: post\n"
        md += f"author: AI Editor\n"
        md += "category: ai\n"
        md += "---\n\n"

        sections = data.get('sections', [])

        for s in sections:
            sType = s['type']
            content = s.get('content', '')

            # [기본] 문단, 헤딩, 리스트
            if sType in ['paragraph', 'text']:
                md += f"{content}\n\n"
            elif sType == 'heading':
                md += f"{'#' * s['level']} {content}\n\n"
            elif sType == 'list':
                for item in s['items']:
                    md += f"- {item}\n"
                md += "\n"
            
            # [코드 블록] 영어/한글 상관없이 있는 그대로 출력
            elif sType in ['code_block', 'code']:
                lang = s.get('language', 'text')
                md += f"```{lang}\n{content}\n```\n\n"

            # [스타일 수정] 팁 박스 (인용구 스타일)
            elif sType == 'tip_box':
                md += f"> 💡 **TIP:** {content}\n\n"

            # [스타일 수정] 경고 박스 (인용구 스타일)
            elif sType == 'warning_box':
                md += f"> ⚠️ **주의:** {content}\n\n"

            # [핵심] 이미지 처리 (API 호출 없이 바로 사용)
            elif sType == 'image':
                url = f"/{s['url']}"
                eng = s.get('description', '')          # 영어 (Flux용)
                kor = s.get('description_ko', eng)      # 한글 (관리자용 - Step 2에서 가져옴)
                
                # 1. 화면 표시: 이미지만 깔끔하게 (Alt 태그는 SEO를 위해 한글 사용)
                md += f"![{kor}]({url})\n"
                
                # 2. 숨김 처리 (관리자용 주석): 영어와 한글 모두 기록
                md += f"\n\n"
        
        # 요약 추가
        if 'summary' in data:
            md += "---\n## 📝 요약\n"
            md += f"{data['summary']}\n"

        return md, today_date

    def update_data_json(self, new_article):
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    articles = data.get('articles', []) if isinstance(data, dict) else data
                except:
                    articles = []
        else:
            articles = []

        # 중복 방지 및 최신 글 추가
        articles = [a for a in articles if a['title'] != new_article['title']]
        articles.insert(0, new_article)
        articles = articles[:50]

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump({"articles": articles}, f, ensure_ascii=False, indent=2)
        print(f"✅ data.json 업데이트 완료 ({len(articles)}개 글)")

    def run(self):
        data = self.load_validated_content()
        if not data: return

        print("\n💾 Step 4: Markdown 변환 (Optimization Mode)")
        md_content, date_str = self.create_markdown_content(data)
        
        timestamp = datetime.now().strftime('%H%M%S')
        filename = f"{date_str}-{timestamp}-ai-article.md"
        file_path = self.contents_dir / filename

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Markdown 생성 완료: contents/{filename}")

        images = [s['url'] for s in data['sections'] if s['type'] == 'image']
        thumbnail = f"/{images[0]}" if images else "https://picsum.photos/800/400"
        
        article_entry = {
            "title": data['title'],
            "summary": data.get('summary', '')[:120] + "...",
            "date": date_str,
            "category": "ai",
            "image": thumbnail,
            "link": f"/contents/{filename.replace('.md', '.html')}",
            "tags": data.get('tags', []),
            "file_path": str(filename)
        }
        
        self.update_data_json(article_entry)

if __name__ == "__main__":
    DataSaver().run()
