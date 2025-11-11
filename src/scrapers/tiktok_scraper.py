"""
TikTok Scraper - Professional scraping with rate limiting and error handling
"""
import asyncio
import json
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from playwright.async_api import async_playwright, Browser, Page
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@dataclass
class TikTokVideo:
    """TikTok video data model"""
    id: str
    description: str
    author: str
    author_id: str
    create_time: int
    music_title: str
    music_author: str
    stats: Dict[str, int]
    hashtags: List[str]
    video_url: str
    cover_url: str
    duration: int
    scraped_at: str


@dataclass
class TikTokUser:
    """TikTok user data model"""
    id: str
    username: str
    nickname: str
    signature: str
    avatar_url: str
    verified: bool
    follower_count: int
    following_count: int
    video_count: int
    heart_count: int
    scraped_at: str


class TikTokScraper:
    """Professional TikTok scraper with advanced features"""
    
    def __init__(self, headless: bool = True, max_retries: int = 3):
        self.headless = headless
        self.max_retries = max_retries
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
    async def __aenter__(self):
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def initialize(self):
        """Initialize browser and page"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await context.new_page()
        
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def search_videos(
        self,
        keyword: str,
        limit: int = 50,
        sort_by: str = "relevance"
    ) -> List[TikTokVideo]:
        """
        Search TikTok videos by keyword
        
        Args:
            keyword: Search keyword
            limit: Maximum number of videos to fetch
            sort_by: Sort order (relevance, date)
            
        Returns:
            List of TikTokVideo objects
        """
        console.print(f"[cyan]Searching for:[/cyan] {keyword}")
        
        videos = []
        url = f"https://www.tiktok.com/search?q={keyword}"
        
        try:
            await self.page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)
            
            # Scroll to load more videos
            for _ in range(limit // 10):
                await self.page.evaluate("window.scrollBy(0, window.innerHeight)")
                await asyncio.sleep(2)
            
            # Extract video data from page
            video_data = await self.page.evaluate("""
                () => {
                    const videos = [];
                    const items = document.querySelectorAll('[data-e2e="search-video-item"]');
                    
                    items.forEach(item => {
                        try {
                            const link = item.querySelector('a');
                            const desc = item.querySelector('[data-e2e="search-video-desc"]');
                            const author = item.querySelector('[data-e2e="search-video-author"]');
                            const stats = item.querySelectorAll('[data-e2e="search-video-stats"] strong');
                            
                            if (link && desc && author) {
                                videos.push({
                                    video_url: link.href,
                                    description: desc.textContent,
                                    author: author.textContent,
                                    likes: stats[0]?.textContent || '0',
                                    comments: stats[1]?.textContent || '0',
                                    shares: stats[2]?.textContent || '0'
                                });
                            }
                        } catch (e) {
                            console.error('Error parsing video:', e);
                        }
                    });
                    
                    return videos;
                }
            """)
            
            # Process and structure data
            for idx, data in enumerate(video_data[:limit]):
                video = TikTokVideo(
                    id=data.get('video_url', '').split('/')[-1] or f"video_{idx}",
                    description=data.get('description', ''),
                    author=data.get('author', ''),
                    author_id='',
                    create_time=int(datetime.now().timestamp()),
                    music_title='',
                    music_author='',
                    stats={
                        'likes': self._parse_count(data.get('likes', '0')),
                        'comments': self._parse_count(data.get('comments', '0')),
                        'shares': self._parse_count(data.get('shares', '0')),
                        'views': 0
                    },
                    hashtags=self._extract_hashtags(data.get('description', '')),
                    video_url=data.get('video_url', ''),
                    cover_url='',
                    duration=0,
                    scraped_at=datetime.now().isoformat()
                )
                videos.append(video)
            
            console.print(f"[green]✓[/green] Found {len(videos)} videos")
            return videos
            
        except Exception as e:
            console.print(f"[red]✗ Error:[/red] {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def get_user_profile(self, username: str) -> Optional[TikTokUser]:
        """
        Get TikTok user profile data
        
        Args:
            username: TikTok username
            
        Returns:
            TikTokUser object or None
        """
        console.print(f"[cyan]Fetching profile:[/cyan] @{username}")
        
        url = f"https://www.tiktok.com/@{username}"
        
        try:
            await self.page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            
            # Extract user data
            user_data = await self.page.evaluate("""
                () => {
                    const getCount = (selector) => {
                        const el = document.querySelector(selector);
                        return el ? el.textContent.trim() : '0';
                    };
                    
                    return {
                        nickname: document.querySelector('[data-e2e="user-title"]')?.textContent || '',
                        signature: document.querySelector('[data-e2e="user-bio"]')?.textContent || '',
                        following: getCount('[data-e2e="following-count"]'),
                        followers: getCount('[data-e2e="followers-count"]'),
                        likes: getCount('[data-e2e="likes-count"]'),
                        videos: getCount('[data-e2e="video-count"]')
                    };
                }
            """)
            
            user = TikTokUser(
                id=username,
                username=username,
                nickname=user_data.get('nickname', username),
                signature=user_data.get('signature', ''),
                avatar_url='',
                verified=False,
                follower_count=self._parse_count(user_data.get('followers', '0')),
                following_count=self._parse_count(user_data.get('following', '0')),
                video_count=self._parse_count(user_data.get('videos', '0')),
                heart_count=self._parse_count(user_data.get('likes', '0')),
                scraped_at=datetime.now().isoformat()
            )
            
            console.print(f"[green]✓[/green] Profile fetched")
            return user
            
        except Exception as e:
            console.print(f"[red]✗ Error:[/red] {str(e)}")
            return None
    
    async def get_trending_hashtags(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get trending hashtags
        
        Args:
            limit: Maximum number of hashtags
            
        Returns:
            List of trending hashtag data
        """
        console.print("[cyan]Fetching trending hashtags...[/cyan]")
        
        try:
            await self.page.goto("https://www.tiktok.com/discover", wait_until="networkidle")
            await asyncio.sleep(2)
            
            hashtags_data = await self.page.evaluate("""
                () => {
                    const hashtags = [];
                    const items = document.querySelectorAll('[data-e2e="discover-hashtag"]');
                    
                    items.forEach(item => {
                        const tag = item.querySelector('a');
                        const views = item.querySelector('[data-e2e="hashtag-views"]');
                        
                        if (tag) {
                            hashtags.push({
                                name: tag.textContent.trim(),
                                url: tag.href,
                                views: views?.textContent || '0'
                            });
                        }
                    });
                    
                    return hashtags;
                }
            """)
            
            console.print(f"[green]✓[/green] Found {len(hashtags_data)} trending hashtags")
            return hashtags_data[:limit]
            
        except Exception as e:
            console.print(f"[red]✗ Error:[/red] {str(e)}")
            return []
    
    def _parse_count(self, count_str: str) -> int:
        """Parse count strings like '1.2M', '50.3K' to integers"""
        if not count_str or count_str == '0':
            return 0
        
        count_str = count_str.upper().replace(',', '')
        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        
        for suffix, multiplier in multipliers.items():
            if suffix in count_str:
                try:
                    return int(float(count_str.replace(suffix, '')) * multiplier)
                except ValueError:
                    return 0
        
        try:
            return int(count_str)
        except ValueError:
            return 0
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        import re
        return re.findall(r'#(\w+)', text)


async def main():
    """CLI interface for scraper"""
    if len(sys.argv) < 3:
        console.print("[yellow]Usage:[/yellow] python tiktok_scraper.py <command> <args>")
        console.print("Commands:")
        console.print("  search <keyword> [limit]")
        console.print("  user <username>")
        console.print("  trending [limit]")
        return
    
    command = sys.argv[1]
    
    async with TikTokScraper(headless=True) as scraper:
        if command == "search":
            keyword = sys.argv[2]
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50
            videos = await scraper.search_videos(keyword, limit)
            print(json.dumps([asdict(v) for v in videos], indent=2))
            
        elif command == "user":
            username = sys.argv[2]
            user = await scraper.get_user_profile(username)
            if user:
                print(json.dumps(asdict(user), indent=2))
                
        elif command == "trending":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
            hashtags = await scraper.get_trending_hashtags(limit)
            print(json.dumps(hashtags, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
