# 블로그 자동화 스크립트

## 사용법

### 1. 기본 실행 (영문 뉴스)
```bash
python news_crawler.py
```

### 2. 한글 뉴스 소스로 실행
```bash
python news_crawler.py config_korean.json
```

### 3. 커스텀 설정으로 실행
```bash
python news_crawler.py my_config.json
```

## 설정 파일 수정

`config.json` 또는 `config_korean.json` 파일을 열어 다음을 수정할 수 있습니다:

### RSS 피드 추가/제거
```json
{
  "name": "사이트 이름",
  "url": "RSS 피드 URL",
  "max_items": 3
}
```

### 최대 기사 수 변경
```json
{
  "max_articles": 20
}
```

### AI 요약 활성화/비활성화
```json
{
  "use_ai_summary": true
}
```

## OpenAI API 키 설정

### 방법 1: 환경 변수 (권장)
```bash
export OPENAI_API_KEY="your-api-key-here"
python news_crawler.py
```

### 방법 2: 설정 파일
```json
{
  "openai_api_key": "your-api-key-here"
}
```

## 출력 파일

스크립트 실행 후 `data.json` 파일이 생성됩니다. 이 파일을 메인 디렉토리로 복사하세요:

```bash
cp data.json ../data.json
```

## 한국어 RSS 피드 추천

| 사이트 | RSS URL |
|--------|---------|
| 테크M | http://www.techm.kr/rss/allArticle.xml |
| AI타임스 | https://www.aitimes.com/rss/allArticle.xml |
| 블로터 | https://www.bloter.net/feed |
| IT조선 | http://it.chosun.com/site/data/rss/rss.xml |
| 지디넷코리아 | https://zdnet.co.kr/rss/allArticle.xml |
| 디지털데일리 | http://www.ddaily.co.kr/rss/index.xml |
| 보안뉴스 | https://www.boannews.com/media/news_rss.xml |

## 영문 RSS 피드 추천

| 사이트 | RSS URL |
|--------|---------|
| TechCrunch | https://techcrunch.com/feed/ |
| The Verge | https://www.theverge.com/rss/index.xml |
| Hacker News | https://hnrss.org/frontpage |
| MIT Tech Review | https://www.technologyreview.com/feed/ |
| Ars Technica | https://feeds.arstechnica.com/arstechnica/index |
| Wired | https://www.wired.com/feed/rss |

## 문제 해결

### ImportError 발생시
```bash
pip install -r requirements.txt
```

### 인코딩 오류시 (Windows)
스크립트 실행 전:
```bash
set PYTHONIOENCODING=utf-8
```

### RSS 피드 연결 오류시
- 인터넷 연결 확인
- RSS URL이 유효한지 확인
- 해당 사이트가 접근 가능한지 확인
