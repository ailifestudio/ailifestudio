#!/usr/bin/env python3
"""
Step 4: Save to data.json & Markdown (Fixed Edition)
- 누락되었던 본문(Paragraph), 팁 박스, 코드 블록 등 모든 요소를 복구
- 한글 번역 기능 유지 및 디버깅 로그 추가
"""

import json
import os
from datetime import datetime
from pathlib import Path
import google.generativeai as genai
import time

class DataSaver:
    def __init__(self, config_path="config_ai.json"):
        self.output_dir = Path(__file__).parent.parent
        self.data_file = self.output_dir / 'data.json'
        self.contents_dir = self.output_dir / 'contents'
        self.contents_dir.mkdir(exist_ok=True)
        
        # 번역을 위한 Gemini 초기화
        self.config = {}
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        
        # 환경변수 우선 확인
        self.api_key = os.getenv('GEMINI_API_KEY', self.config.get('gemini_api_key', ''))
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            print("   ✅ 번역용 Gemini API 키 로드 성공")
        else:
            print("   ⚠️ GEMINI_API_KEY 없음: 번역 기능이 비활성화됩니다. (영어 원문 사용)")
            self.model = None

    def load_validated_content(self, input_path="automation/intermediate_outputs/step3_validated_content.json"):
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Step 3 결과 파일이 없습니다.")
            return None

    def translate_descriptions(self, descriptions):
        """영어 설명 리스트를 한글로 일괄 번역"""
        if not self.model or not descriptions:
            return descriptions 

        print(f"   🌐 이미지 설명 {len(descriptions)}개 한글로 번역 시도...")
        
        prompt = "Translate the following image descriptions into natural Korean captions for a blog post. Return ONLY the translated lines in order, one per line.\n\n"
        for desc in descriptions:
            prompt += f"- {desc}\n"
            
        try:
            response = self.model.generate_content(prompt)
            translated_lines = [line.strip().replace('- ', '') for line in response.text.strip().split('\n') if line.strip()]
            
            if len(translated_lines) == len(descriptions):
                print("   ✅ 번역 성공!")
                return translated_lines
            else:
                print(f"   ⚠️ 번역 개수 불일치 ({len(translated_lines)} vs {len(descriptions)}). 원본 사용.")
                return descriptions
        except Exception as e:
            print(f"   ⚠️ 번역 중 에러 발생: {e}")
            return descriptions

    def create_markdown_content(self, data):
        """JSON -> Markdown 변환 (모든 섹션 타입 처리 추가)"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today_date = datetime.now().strftime('%Y-%m-%d')
        
        # Front Matter
        md_content = "---\n"
        md_content += f"title: \"{data['title']}\"\n"
        md_content += f"date: {current_time}\n"
        md_content += f"layout: post\n"
        md_content += f"author: AI Editor\n"
        md_content += "category: ai\n" # 소문자로 통일
        md_content += "---\n\n"

        sections = data.get('sections', [])
        
        # 1. 이미지 번역 준비
        image_sections = [s for s in sections if s['type'] == 'image']
        english_descs = [s['description'] for s in image_sections]
        korean_descs = self.translate_descriptions(english_descs)
        desc_map = {eng: kor for eng, kor in zip(english_descs, korean_descs)}

        # 2. 본문 작성 Loop (누락된 타입 복구!)
        for section in sections:
            sType = section['type']
            content = section.get('content', '')

            # [복구됨] 문단 (Paragraph) & 단순 텍스트
            if sType == 'paragraph' or sType == 'text':
                md_content += f"{content}\n\n"
            
            # 헤딩
            elif sType == 'heading':
                md_content += f"{'#' * section['level']} {content}\n\n"

            # 리스트
            elif sType == 'list':
                for item in section['items']:
                    md_content += f"- {item}\n"
                md_content += "\n"
            
            # [복구됨] 코드 블록
            elif sType == 'code_block' or sType == 'code':
                lang = section.get('language', '')
                md_content += f"```{lang}\n{content}\n```\n\n"

            # [복구됨] 팁 박스 (HTML 스타일)
            elif sType == 'tip_box':
                md_content += f'<div style="background-color: #f0f9ff; border-left: 4px solid #3b82f6; padding: 15px; margin: 20px 0; border-radius: 4px;"><strong>💡 TIP:</strong> {content}</div>\n\n'

            # [복구됨] 경고 박스 (HTML 스타일)
            elif sType == 'warning_box':
                md_content += f'<div style="background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; margin: 20px 0; border-radius: 4px;"><strong>⚠️ 주의:</strong> {content}</div>\n\n'

            # 이미지
            elif sType == 'image':
                image_url = f"/{section['url']}"
                eng_desc = section['description'].replace('"', "'")
                kor_desc = desc_map.get(section['description'], eng_desc)
                
                img_tag = f"""
<figure style="text-align:center; margin: 30px 0;">
  <img src="{image_url}" alt="{kor_desc}" style="max-width:100%; height:auto; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
  <figcaption style="margin-top:10px; text-align: center;">
    <div style="color:#555; font-size:0.95em; font-weight:bold; margin-bottom:5px;">{kor_desc}</div>
    <div style="color:#aaa; font-size:0.8em; font-family:monospace; background:#f5f5f5; padding:4px 8px; border-radius:4px; display:inline-block;">Prompt: {eng_desc}</div>
  </figcaption>
</figure>
"""
                md_content += img_tag + "\n\n"
        
        # 3. 요약
        if 'summary' in data:
            md_content += "---\n## 📝 요약\n"
            md_content += f"{data['summary']}\n"

        return md_content, today_date

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

        print("\n💾 Step 4: Markdown 변환 (Fix: 본문 복구 + 번역)")
        md_content, date_str = self.create_markdown_content(data)
        
        timestamp = datetime.now().strftime('%H%M%S')
        filename = f"{date_str}-{timestamp}-ai-article.md"
        file_path = self.contents_dir / filename

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Markdown 생성 완료: contents/{filename}")

        # 썸네일 및 data.json 업데이트
        images = [s['url'] for s in data['sections'] if s['type'] == 'image']
        thumbnail = f"/{images[0]}" if images else "https://picsum.photos/800/400"
        
        article_entry = {
            "title": data['title'],
            "summary": data.get('summary', '')[:120] + "...",
            "date": date_str,
            "category": "ai", # 소문자 통일
            "image": thumbnail,
            "link": f"/contents/{filename.replace('.md', '.html')}",
            "tags": data.get('tags', []),
            "file_path": str(filename)
        }
        
        self.update_data_json(article_entry)

if __name__ == "__main__":
    saver = DataSaver()
    saver.run()
