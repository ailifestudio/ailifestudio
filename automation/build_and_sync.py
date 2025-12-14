#!/usr/bin/env python3
"""
OSMU (One Source Multi Use) Build and Sync System
==================================================
Markdown → GitHub Pages (Fast Dashboard) → WordPress (SEO Original)

Author: AI Life Studio
Date: 2025-12-12
License: MIT

Features:
- Reads Markdown files with Front Matter (canonical_url, category, etc.)
- Generates split JSON files for GitHub Pages (dashboard_summary.json, data/{category}/page_{n}.json)
- Syncs posts to WordPress via REST API with duplicate prevention
- Implements canonical URL system for SEO link juice to WordPress
- Safe fallback: WordPress failure doesn't stop GitHub Pages deployment
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


class OSMUBuilder:
    """One Source Multi Use Content Builder"""
    
    def __init__(self, config_path: str = "automation/config_osmu.json"):
        """
        Initialize OSMU Builder
        
        Args:
            config_path: Path to configuration file containing WordPress credentials
        """
        self.base_dir = Path(__file__).parent.parent
        self.posts_dir = self.base_dir / "_posts"
        self.data_dir = self.base_dir / "data"
        self.config = self._load_config(config_path)
        
        # WordPress REST API configuration
        self.wp_url = self.config.get("wordpress", {}).get("url", "")
        self.wp_user = self.config.get("wordpress", {}).get("username", "")
        self.wp_password = self.config.get("wordpress", {}).get("app_password", "")
        
        # Pagination settings
        self.items_per_page = self.config.get("pagination", {}).get("items_per_page", 20)
        self.dashboard_items = self.config.get("pagination", {}).get("dashboard_items", 50)
        
        # Category mapping
        self.categories = {
            "ai-tech": "AI/테크",
            "economy": "경제",
            "life": "라이프",
            "global": "글로벌"
        }
        
        print("🚀 OSMU Builder initialized")
        print(f"📁 Posts directory: {self.posts_dir}")
        print(f"📊 Data directory: {self.data_dir}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        config_file = self.base_dir / config_path
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
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
        Read all Markdown posts from _posts directory
        
        Returns:
            List of post dictionaries with metadata and content
        """
        posts = []
        
        if not self.posts_dir.exists():
            print("⚠️ No _posts directory found")
            return posts
        
        # Scan all category directories
        for category_dir in self.posts_dir.iterdir():
            if not category_dir.is_dir():
                continue
            
            category_key = category_dir.name
            category_name = self.categories.get(category_key, category_key)
            
            # Read all .md files in category
            for md_file in category_dir.glob("*.md"):
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
                    
                    # Build post object
                    # Convert date to string if it's a date object
                    date_value = metadata.get("date", datetime.now().strftime("%Y-%m-%d"))
                    if hasattr(date_value, 'strftime'):
                        date_str = date_value.strftime("%Y-%m-%d")
                    else:
                        date_str = str(date_value)
                    
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
                    print(f"✅ Loaded: {post_data['title']}")
                    
                except Exception as e:
                    print(f"❌ Error reading {md_file}: {e}")
        
        # Sort by date (newest first)
        posts.sort(key=lambda x: x['date'], reverse=True)
        
        print(f"📚 Total posts loaded: {len(posts)}")
        return posts
    
    def generate_dashboard_json(self, posts: List[Dict[str, Any]]) -> None:
        """
        Generate dashboard_summary.json for fast loading on main page
        
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
        
        # Save dashboard JSON
        dashboard_file = self.base_dir / "dashboard_summary.json"
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Generated dashboard_summary.json ({len(dashboard_posts)} items)")
    
    def generate_paginated_json(self, posts: List[Dict[str, Any]]) -> None:
        """
        Generate paginated JSON files per category
        
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
                
                # Save page JSON
                page_file = cat_dir / f"page_{page + 1}.json"
                with open(page_file, 'w', encoding='utf-8') as f:
                    json.dump(page_data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Generated {cat_key}/page_{page + 1}.json ({len(page_posts)} items)")
    
    def sync_to_wordpress(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Sync posts to WordPress via REST API
        
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
                # Check if post already exists (by canonical URL or slug)
                canonical_url = post.get("canonical_url", "")
                
                # Search for existing post
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
                    "slug": post["slug"],
                    "categories": self._get_wp_category_id(post["category"]),
                    "tags": self._get_wp_tag_ids(post.get("tags", []))
                }
                
                if existing_post:
                    # Update existing post
                    post_id = existing_post["id"]
                    update_url = f"{wp_api_url}/{post_id}"
                    response = requests.post(update_url, headers=headers, json=wp_post_data, timeout=30)
                    
                    if response.status_code in [200, 201]:
                        # Update canonical URL in post metadata
                        canonical_url = response.json().get("link", "")
                        self._update_post_canonical_url(post["file_path"], canonical_url)
                        
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
                        # Save canonical URL to Markdown Front Matter
                        canonical_url = response.json().get("link", "")
                        self._update_post_canonical_url(post["file_path"], canonical_url)
                        
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
    
    def _update_post_canonical_url(self, file_path: str, canonical_url: str) -> None:
        """Update canonical URL in Markdown Front Matter"""
        try:
            post = frontmatter.load(file_path)
            post.metadata["canonical_url"] = canonical_url
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            print(f"   📝 Updated canonical URL: {canonical_url}")
        except Exception as e:
            print(f"   ⚠️ Failed to update canonical URL: {e}")
    
    def _get_wp_category_id(self, category: str) -> List[int]:
        """Get WordPress category ID (stub - implement based on your WordPress setup)"""
        # This is a stub - you should implement actual category lookup
        category_map = {
            "AI/테크": 1,
            "경제": 2,
            "라이프": 3,
            "글로벌": 4
        }
        return [category_map.get(category, 1)]
    
    def _get_wp_tag_ids(self, tags: List[str]) -> List[int]:
        """Get WordPress tag IDs (stub - implement based on your WordPress setup)"""
        # This is a stub - you should implement actual tag lookup/creation
        return []
    
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
    
    def build_all(self) -> None:
        """
        Main build process - orchestrates all build steps
        
        Process:
        1. Read Markdown posts
        2. Generate dashboard JSON
        3. Generate paginated JSON files
        4. Sync to WordPress (safe fallback if fails)
        """
        print("\n" + "="*60)
        print("🚀 Starting OSMU Build Process")
        print("="*60 + "\n")
        
        # Step 1: Read Markdown posts
        print("📖 Step 1: Reading Markdown posts...")
        posts = self.read_markdown_posts()
        
        if not posts:
            print("⚠️ No posts found - exiting")
            return
        
        # Step 2: Generate dashboard JSON
        print("\n📊 Step 2: Generating dashboard JSON...")
        self.generate_dashboard_json(posts)
        
        # Step 3: Generate paginated JSON
        print("\n📄 Step 3: Generating paginated JSON files...")
        self.generate_paginated_json(posts)
        
        # Step 4: Sync to WordPress (safe fallback)
        print("\n🌐 Step 4: Syncing to WordPress...")
        try:
            wp_results = self.sync_to_wordpress(posts)
            
            # WordPress failure doesn't stop deployment
            if wp_results["failed"] > 0:
                print("\n⚠️ WordPress sync had failures, but GitHub Pages deployment continues")
        
        except Exception as e:
            print(f"\n⚠️ WordPress sync failed: {e}")
            print("   GitHub Pages deployment continues regardless")
        
        print("\n" + "="*60)
        print("✅ OSMU Build Complete!")
        print("="*60)
        print("\n📦 Generated files:")
        print("   - dashboard_summary.json (main page)")
        print("   - data/{category}/page_*.json (paginated data)")
        print("\n🚀 Ready for GitHub Pages deployment")


def main():
    """Main entry point"""
    import sys
    
    # Check for config file argument
    config_path = sys.argv[1] if len(sys.argv) > 1 else "automation/config_osmu.json"
    
    # Initialize and run builder
    builder = OSMUBuilder(config_path)
    builder.build_all()


if __name__ == "__main__":
    main()
