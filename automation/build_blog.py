#!/usr/bin/env python3
"""
Blog Build System - Standard Directory Structure Compliant
==========================================================
Markdown (contents/) → data/ (UI JSON) + feed/ (WordPress)

Author: AI Life Studio
Date: 2025-12-12
License: MIT

Standard Directory Structure:
/ (Root)
├── index.html
├── data/                    # [Output] UI용 JSON
│   ├── dashboard_summary.json
│   └── {category}/page_*.json
├── feed/                    # [Output] WP용 피드
│   ├── rss.xml
│   └── full_export.json
├── contents/                # [Input] 원본 Markdown
│   └── post*.md
└── automation/
    └── build_blog.py
"""

import os
import json
import re
import base64
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys

# Required libraries: python-frontmatter, requests, markdown
try:
    import frontmatter
    import requests
    import markdown
except ImportError as e:
    print(f"⚠️ Missing required library: {e}")
    print("📦 Please install: pip install python-frontmatter requests markdown")
    sys.exit(1)


# ============================================================
# 표준 디렉토리 경로 상수 (Standard Directory Constants)
# ============================================================
# 절대 경로를 사용하여 어디서든 실행 가능하도록 설정
BASE_DIR = Path(__file__).parent.parent.resolve()  # /home/user/webapp
CONTENTS_DIR = BASE_DIR / "contents"                # 원본 Markdown 위치
DATA_DIR = BASE_DIR / "data"                        # UI용 JSON 출력
FEED_DIR = BASE_DIR / "feed"                        # WP용 피드 출력

# 설정 파일
CONFIG_FILE = BASE_DIR / "automation" / "config_blog.json"


class BlogBuilder:
    """표준 디렉토리 구조 기반 블로그 빌드 시스템"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize Blog Builder
        
        Args:
            config_path: 설정 파일 경로 (기본: automation/config_blog.json)
        """
        self.base_dir = BASE_DIR
        self.contents_dir = CONTENTS_DIR
        self.data_dir = DATA_DIR
        self.feed_dir = FEED_DIR
        
        # 설정 로드
        config_path = config_path or CONFIG_FILE
        self.config = self._load_config(config_path)
        
        # WordPress 설정
        self.wp_url = self.config.get("wordpress", {}).get("url", "")
        self.wp_user = self.config.get("wordpress", {}).get("username", "")
        self.wp_password = self.config.get("wordpress", {}).get("app_password", "")
        
        # 페이지네이션 설정
        self.items_per_page = self.config.get("pagination", {}).get("items_per_page", 20)
        self.dashboard_items = self.config.get("pagination", {}).get("dashboard_items", 50)
        
        # 카테고리 매핑
        self.categories = self.config.get("categories", {
            "it": "IT/Tech",
            "ai": "AI",
            "economy": "Economy",
            "life": "Lifestyle",
            "global": "Global"
        })
        
        print("🚀 Blog Builder initialized")
        print(f"📁 BASE_DIR: {self.base_dir}")
        print(f"📝 CONTENTS_DIR: {self.contents_dir}")
        print(f"📊 DATA_DIR: {self.data_dir}")
        print(f"📡 FEED_DIR: {self.feed_dir}")
        
        # 디렉토리 검증 및 생성
        self._verify_directories()
    
    def _verify_directories(self) -> None:
        """디렉토리 구조 검증 및 필요 시 생성"""
        
        # contents/ 검증 (필수 - 없으면 에러)
        if not self.contents_dir.exists():
            print(f"\n❌ 에러: contents/ 디렉토리가 존재하지 않습니다!")
            print(f"   경로: {self.contents_dir}")
            print(f"\n해결 방법:")
            print(f"   mkdir -p {self.contents_dir}")
            print(f"   # 그 후 Markdown 파일을 contents/에 저장하세요")
            sys.exit(1)
        
        # data/ 생성 (없으면 자동 생성)
        if not self.data_dir.exists():
            print(f"📁 Creating data/ directory: {self.data_dir}")
            self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # feed/ 생성 (없으면 자동 생성)
        if not self.feed_dir.exists():
            print(f"📁 Creating feed/ directory: {self.feed_dir}")
            self.feed_dir.mkdir(parents=True, exist_ok=True)
        
        # 카테고리별 data 폴더 생성
        for category_key in self.categories.keys():
            category_data_dir = self.data_dir / category_key
            category_data_dir.mkdir(parents=True, exist_ok=True)
        
        print("✅ Directory structure verified")
    
    def _load_config(self, config_path: Path) -> Dict:
        """Load configuration from JSON file"""
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _get_wordpress_headers(self) -> Dict[str, str]:
        """Generate WordPress REST API authentication headers"""
        if not self.wp_user or not self.wp_password:
            return {}
        
        credentials = f"{self.wp_user}:{self.wp_password}"
        token = base64.b64encode(credentials.encode()).decode()
        
        return {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }
    
    def read_markdown_posts(self) -> List[Dict[str, Any]]:
        """
        Read all Markdown posts from contents/ directory
        
        Returns:
            List of post dictionaries with metadata and content
        """
        posts = []
        
        if not self.contents_dir.exists():
            print(f"⚠️ No contents/ directory found at {self.contents_dir}")
            return posts
        
        # contents/ 폴더의 모든 .md 파일 읽기
        md_files = list(self.contents_dir.glob("*.md"))
        
        if not md_files:
            print(f"⚠️ No Markdown files found in {self.contents_dir}")
            return posts
        
        for md_file in md_files:
            try:
                post = frontmatter.load(md_file)
                
                # Extract Front Matter metadata
                metadata = post.metadata
                content = post.content
                
                # Convert Markdown to HTML
                html_content = markdown.markdown(
                    content,
                    extensions=['extra', 'codehilite', 'toc']
                )
                
                # 카테고리 추출 (Front Matter에서)
                category_key = metadata.get("category", "it")
                category_name = self.categories.get(category_key, category_key)
                
                # 날짜 변환
                date_value = metadata.get("date", datetime.now().strftime("%Y-%m-%d"))
                if hasattr(date_value, 'strftime'):
                    date_str = date_value.strftime("%Y-%m-%d")
                else:
                    date_str = str(date_value)
                
                # Build post object
                post_data = {
                    "title": metadata.get("title", "Untitled"),
                    "canonical_url": metadata.get("canonical_url", ""),
                    "category": category_name,
                    "category_key": category_key,
                    "date": date_str,
                    "summary": metadata.get("summary", ""),
                    "image": metadata.get("image", ""),
                    "tags": metadata.get("tags", []),
                    "content": html_content,
                    "markdown_content": content,
                    "file_path": str(md_file),
                    "slug": md_file.stem,
                    "type": "markdown"
                }
                
                posts.append(post_data)
                print(f"✅ Loaded: {post_data['title']} ({category_name})")
                
            except Exception as e:
                print(f"❌ Error reading {md_file}: {e}")
        
        # Sort by date (newest first)
        posts.sort(key=lambda x: x['date'], reverse=True)
        
        print(f"📚 Total posts loaded: {len(posts)}")
        return posts
    
    def generate_dashboard_json(self, posts: List[Dict[str, Any]]) -> None:
        """
        Generate data/dashboard_summary.json for fast loading on main page
        
        Args:
            posts: List of all posts
        """
        # Take only the latest N posts for dashboard
        dashboard_posts = posts[:self.dashboard_items]
        
        # Generate summary data (without full content)
        summary_data = {
            "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total": len(posts),
            "articles": []
        }
        
        for post in dashboard_posts:
            article = {
                "title": post["title"],
                "source": "AI Life Studio",
                "time": self._format_time_ago(post["date"]),
                "summary": post["summary"][:200] + "..." if len(post["summary"]) > 200 else post["summary"],
                "link": post.get("canonical_url") or f"/article.html?slug={post['slug']}",
                "image": post["image"],
                "category": post["category"],
                "type": post["type"],
                "slug": post["slug"],
                "canonical_url": post.get("canonical_url", "")
            }
            summary_data["articles"].append(article)
        
        # Save dashboard JSON to data/
        dashboard_file = self.data_dir / "dashboard_summary.json"
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Generated data/dashboard_summary.json ({len(dashboard_posts)} items)")
    
    def generate_paginated_json(self, posts: List[Dict[str, Any]]) -> None:
        """
        Generate paginated JSON files per category in data/
        
        Args:
            posts: List of all posts
        """
        # Group posts by category
        category_posts = {}
        for post in posts:
            cat_key = post["category_key"]
            if cat_key not in category_posts:
                category_posts[cat_key] = []
            category_posts[cat_key].append(post)
        
        # Generate paginated files for each category
        for cat_key, cat_posts in category_posts.items():
            cat_dir = self.data_dir / cat_key
            cat_dir.mkdir(parents=True, exist_ok=True)
            
            # Paginate posts
            total_pages = (len(cat_posts) + self.items_per_page - 1) // self.items_per_page
            
            for page in range(total_pages):
                start_idx = page * self.items_per_page
                end_idx = start_idx + self.items_per_page
                page_posts = cat_posts[start_idx:end_idx]
                
                page_data = {
                    "category": self.categories[cat_key],
                    "page": page + 1,
                    "total_pages": total_pages,
                    "total_items": len(cat_posts),
                    "articles": []
                }
                
                for post in page_posts:
                    article = {
                        "title": post["title"],
                        "source": "AI Life Studio",
                        "time": self._format_time_ago(post["date"]),
                        "summary": post["summary"],
                        "content": post["content"],
                        "link": post.get("canonical_url") or f"/article.html?slug={post['slug']}",
                        "image": post["image"],
                        "category": post["category"],
                        "type": post["type"],
                        "slug": post["slug"],
                        "canonical_url": post.get("canonical_url", ""),
                        "tags": post.get("tags", [])
                    }
                    page_data["articles"].append(article)
                
                # Save page JSON to data/{category}/
                page_file = cat_dir / f"page_{page + 1}.json"
                with open(page_file, 'w', encoding='utf-8') as f:
                    json.dump(page_data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Generated data/{cat_key}/page_{page + 1}.json ({len(page_posts)} items)")
    
    def generate_rss_feed(self, posts: List[Dict[str, Any]]) -> None:
        """
        Generate feed/rss.xml for WordPress and RSS readers
        
        Args:
            posts: List of all posts
        """
        # Take latest 20 posts for RSS
        rss_posts = posts[:20]
        
        # Generate RSS XML
        rss_xml = self._build_rss_xml(rss_posts)
        
        # Save RSS to feed/
        rss_file = self.feed_dir / "rss.xml"
        with open(rss_file, 'w', encoding='utf-8') as f:
            f.write(rss_xml)
        
        print(f"✅ Generated feed/rss.xml ({len(rss_posts)} items)")
    
    def generate_full_export(self, posts: List[Dict[str, Any]]) -> None:
        """
        Generate feed/full_export.json for WordPress import
        
        Args:
            posts: List of all posts
        """
        export_data = {
            "version": "1.0.0",
            "exported_at": datetime.now().isoformat(),
            "total_posts": len(posts),
            "posts": []
        }
        
        for post in posts:
            export_post = {
                "title": post["title"],
                "content": post["content"],
                "excerpt": post["summary"],
                "date": post["date"],
                "slug": post["slug"],
                "category": post["category"],
                "tags": post.get("tags", []),
                "canonical_url": post.get("canonical_url", ""),
                "image": post["image"]
            }
            export_data["posts"].append(export_post)
        
        # Save full export to feed/
        export_file = self.feed_dir / "full_export.json"
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Generated feed/full_export.json ({len(posts)} posts)")
    
    def _build_rss_xml(self, posts: List[Dict[str, Any]]) -> str:
        """Build RSS 2.0 XML format"""
        
        rss_items = []
        for post in posts:
            item = f"""
    <item>
      <title><![CDATA[{post['title']}]]></title>
      <link>{post.get('canonical_url') or 'https://ailifestudio.github.io/'}</link>
      <description><![CDATA[{post['summary']}]]></description>
      <content:encoded><![CDATA[{post['content']}]]></content:encoded>
      <pubDate>{self._format_rfc822_date(post['date'])}</pubDate>
      <guid isPermaLink="false">{post['slug']}</guid>
      <category><![CDATA[{post['category']}]]></category>
    </item>"""
            rss_items.append(item)
        
        rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>AI Life Studio Blog</title>
    <link>https://ailifestudio.github.io/</link>
    <description>AI와 테크 뉴스를 자동으로 큐레이팅하는 블로그</description>
    <language>ko</language>
    <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
{''.join(rss_items)}
  </channel>
</rss>"""
        
        return rss_xml
    
    def _format_rfc822_date(self, date_str: str) -> str:
        """Convert YYYY-MM-DD to RFC 822 format"""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime('%a, %d %b %Y 00:00:00 +0000')
        except:
            return datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    def _format_time_ago(self, date_str: str) -> str:
        """Format date as relative time (e.g., '2시간 전')"""
        try:
            post_date = datetime.strptime(date_str, "%Y-%m-%d")
            now = datetime.now()
            delta = now - post_date
            
            if delta.days == 0:
                return "오늘"
            elif delta.days == 1:
                return "어제"
            elif delta.days < 7:
                return f"{delta.days}일 전"
            elif delta.days < 30:
                weeks = delta.days // 7
                return f"{weeks}주 전"
            elif delta.days < 365:
                months = delta.days // 30
                return f"{months}개월 전"
            else:
                years = delta.days // 365
                return f"{years}년 전"
        except:
            return date_str
    
    def sync_to_wordpress(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Sync posts to WordPress via REST API (Optional)
        
        Args:
            posts: List of posts to sync
        
        Returns:
            Dictionary with sync results
        """
        if not self.wp_url or not self.wp_user or not self.wp_password:
            print("⚠️ WordPress credentials not configured - skipping WordPress sync")
            return {"success": 0, "failed": 0, "skipped": len(posts)}
        
        results = {
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "errors": []
        }
        
        headers = self._get_wordpress_headers()
        wp_api_url = f"{self.wp_url}/wp-json/wp/v2/posts"
        
        for post in posts:
            try:
                # Check if post already exists (by slug)
                search_url = f"{wp_api_url}?slug={post['slug']}"
                search_response = requests.get(search_url, headers=headers, timeout=10)
                
                existing_post = None
                if search_response.status_code == 200 and search_response.json():
                    existing_post = search_response.json()[0]
                
                # Prepare WordPress post data
                wp_post_data = {
                    "title": post["title"],
                    "content": post["content"],
                    "excerpt": post["summary"],
                    "status": "publish",
                    "slug": post["slug"]
                }
                
                if existing_post:
                    # Update existing post
                    post_id = existing_post["id"]
                    update_url = f"{wp_api_url}/{post_id}"
                    response = requests.post(update_url, headers=headers, json=wp_post_data, timeout=30)
                    
                    if response.status_code in [200, 201]:
                        results["success"] += 1
                        print(f"✅ Updated in WordPress: {post['title']}")
                    else:
                        results["failed"] += 1
                        error_msg = f"Failed to update {post['title']}: {response.status_code}"
                        results["errors"].append(error_msg)
                        print(f"❌ {error_msg}")
                else:
                    # Create new post
                    response = requests.post(wp_api_url, headers=headers, json=wp_post_data, timeout=30)
                    
                    if response.status_code in [200, 201]:
                        results["success"] += 1
                        print(f"✅ Created in WordPress: {post['title']}")
                    else:
                        results["failed"] += 1
                        error_msg = f"Failed to create {post['title']}: {response.status_code}"
                        results["errors"].append(error_msg)
                        print(f"❌ {error_msg}")
            
            except requests.exceptions.Timeout:
                results["failed"] += 1
                error_msg = f"Timeout syncing {post['title']}"
                results["errors"].append(error_msg)
                print(f"⏱️ {error_msg}")
            
            except Exception as e:
                results["failed"] += 1
                error_msg = f"Error syncing {post['title']}: {str(e)}"
                results["errors"].append(error_msg)
                print(f"❌ {error_msg}")
        
        print(f"\n📊 WordPress Sync Results:")
        print(f"   ✅ Success: {results['success']}")
        print(f"   ❌ Failed: {results['failed']}")
        print(f"   ⏭️ Skipped: {results['skipped']}")
        
        return results
    
    def build_all(self) -> None:
        """
        Main build process - orchestrates all build steps
        
        Process:
        1. Read Markdown posts from contents/
        2. Generate data/dashboard_summary.json
        3. Generate data/{category}/page_*.json
        4. Generate feed/rss.xml
        5. Generate feed/full_export.json
        6. Sync to WordPress (optional, safe fallback if fails)
        """
        print("\n" + "="*60)
        print("🚀 Starting Blog Build Process")
        print("="*60 + "\n")
        
        # Step 1: Read Markdown posts
        print("📖 Step 1: Reading Markdown posts from contents/...")
        posts = self.read_markdown_posts()
        
        if not posts:
            print("⚠️ No posts found - exiting")
            return
        
        # Step 2: Generate dashboard JSON
        print("\n📊 Step 2: Generating data/dashboard_summary.json...")
        self.generate_dashboard_json(posts)
        
        # Step 3: Generate paginated JSON
        print("\n📄 Step 3: Generating data/{category}/page_*.json...")
        self.generate_paginated_json(posts)
        
        # Step 4: Generate RSS feed
        print("\n📡 Step 4: Generating feed/rss.xml...")
        self.generate_rss_feed(posts)
        
        # Step 5: Generate full export
        print("\n📦 Step 5: Generating feed/full_export.json...")
        self.generate_full_export(posts)
        
        # Step 6: Sync to WordPress (optional, safe fallback)
        print("\n🌐 Step 6: Syncing to WordPress (optional)...")
        try:
            wp_results = self.sync_to_wordpress(posts)
            
            # WordPress failure doesn't stop deployment
            if wp_results["failed"] > 0:
                print("\n⚠️ WordPress sync had failures, but build continues")
        
        except Exception as e:
            print(f"\n⚠️ WordPress sync failed: {e}")
            print("   Build continues regardless")
        
        print("\n" + "="*60)
        print("✅ Blog Build Complete!")
        print("="*60)
        print("\n📦 Generated files:")
        print(f"   - {self.data_dir}/dashboard_summary.json")
        print(f"   - {self.data_dir}/{{category}}/page_*.json")
        print(f"   - {self.feed_dir}/rss.xml")
        print(f"   - {self.feed_dir}/full_export.json")
        print("\n🚀 Ready for deployment")


def main():
    """Main entry point"""
    import sys
    
    # Check for config file argument
    config_path = None
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    
    # Initialize and run builder
    builder = BlogBuilder(config_path)
    builder.build_all()


if __name__ == "__main__":
    main()
