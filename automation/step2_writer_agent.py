#!/usr/bin/env python3
"""
Step 4: Save to data.json & Markdown (Mobile Scroll Fix)
- 핵심 수정: '가로 스크롤'을 유발하는 Code Block(```)을 원천 봉쇄
- 모든 프롬프트 예시를 '인용구(Blockquote)'로 변환하여 모바일에서 자동 줄바꿈 되도록 함
"""

import json
import os
from datetime import datetime
from pathlib import Path
import re  # 정규표현식 추가

class DataSaver:
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent
        self.data_file = self.output_dir / 'data.json'
        self.contents_dir = self.output_dir / 'contents'
        self.contents_dir.mkdir(exist_ok=True)

    def load_validated_content(self, input_path="automation/intermediate_outputs/step3_validated_content.json"):
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Step 3 결과 파일이 없습니다.")
            return None

    def clean_markdown_syntax(self, text):
        """본문 내에 숨어있는 코드블록 문법(```) 제거"""
        if not text: return ""
        # ```text, ```json 등 제거하고 그냥 내용만 남김
        text = re.sub(r'```\w*\n', '', text) 
        text = text.replace('```', '')
        return text

    def create_markdown_content(self, data):
        """Markdown 변환 로직"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today_date = datetime.now().strftime('%Y-%m-%d')
        
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

            # [1] 문단 처리 (안전장치: 혹시 모를 코드블록 제거)
            if sType in ['paragraph', 'text']:
                cleaned_content = self.clean_markdown_syntax(content)
                md += f"{cleaned_content}\n\n"
            
            # [2] 헤딩
            elif sType == 'heading':
                md += f"{'#' * s['level']} {content}\n\n"
            
            # [3] 리스트
            elif sType == 'list':
                for item in s['items']:
                    md += f"- {item}\n"
                md += "\n"
            
            # [🔥 핵심 수정] 코드 블록 -> '인용구 박스'로 스타일 강제 변경
            # 스크롤바가 생기는 ``` 대신 > (Blockquote) 사용
            elif sType in ['code_block', 'code']:
                md += f"> 💬 **AI 프롬프트 예시:**\n>\n"
                # 내용에 줄바꿈이 있으면 인용구(>)를 줄마다 붙여줌 (끊기지 않게)
                clean_code = self.clean_markdown_syntax(content).strip()
                formatted_content = clean_code.replace("\n", "\n> ")
                md += f"> {formatted_content}\n\n"

            # 팁 박스
            elif sType == 'tip_box':
                md += f"> 💡 **TIP:** {content}\n\n"

            # 경고 박스
            elif sType == 'warning_box':
                md += f"> ⚠️ **주의:** {content}\n\n"

            # 이미지 처리
            elif sType == 'image':
                url = f"/{s['url']}"
                eng = s.get('description', '')
                kor = s.get('description_ko', eng)
                
                md += f"![{kor}]({url})\n"
                md += f"\n\n"
        
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

        articles = [a for a in articles if a['title'] != new_article['title']]
        articles.insert(0, new_article)
        articles = articles[:50]

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump({"articles": articles}, f, ensure_ascii=False, indent=2)
        print(f"✅ data.json 업데이트 완료 ({len(articles)}개 글)")

    def run(self):
        data = self.load_validated_content()
        if not data: return

        print("\n💾 Step 4: Markdown 변환 (Scroll Fix Applied)")
        md_content, date_str = self.create_markdown_content(data)
        
        timestamp = datetime.now().strftime('%H%M%S')
        filename = f"{date_str}-{timestamp}-ai-article.md"
        file_path = self.contents_dir / filename

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Markdown 생성 완료: contents/{filename}")

        images = [s['url'] for s in data['sections'] if s['type'] == 'image']
        thumbnail = f"/{images[0]}" if images else "[https://picsum.photos/800/400](https://picsum.photos/800/400)"
        
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
