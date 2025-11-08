# 🎬 TT-Search

<div align="center">

**Professional TikTok Search, Analytics & Data Extraction**

[![npm version](https://img.shields.io/npm/v/tt-search.svg)](https://www.npmjs.com/package/tt-search)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

Powerful hybrid Node.js/Python toolkit for TikTok data extraction with Apache Parquet storage and ML-powered analytics.

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [API](#-api) • [CLI](#-cli)

</div>

---

## ✨ Features

### 🔍 **Advanced Search**
- Search videos by keywords with intelligent pagination
- Get user profiles and statistics
- Discover trending hashtags
- Real-time data extraction

### 💾 **Professional Storage**
- **Apache Parquet** format with columnar compression
- Multiple compression algorithms (Snappy, Gzip, LZ4, Zstd)
- Efficient data partitioning
- Export to JSON, CSV, Excel

### 📊 **ML-Powered Analytics**
- Content clustering using K-Means
- Virality prediction with engagement scoring
- Hashtag trend analysis
- Author performance metrics
- TF-IDF based content similarity

### 🚀 **Performance**
- Async/await architecture
- Rate limiting and retry logic
- Smart caching system
- Optimized data processing

### 🛠️ **Developer Experience**
- Full TypeScript support
- Comprehensive CLI
- Interactive mode
- Rich error handling
- Detailed logging

---

## 📦 Installation

```bash
npm install tt-search
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

Or using the setup script:

```bash
npm run setup:python
```

### System Requirements

- Node.js 18.0+
- Python 3.10+
- pip
- Playwright (for web scraping)

---

## 🚀 Quick Start

### JavaScript/TypeScript API

```typescript
import TTSearch from 'tt-search';

const ttSearch = new TTSearch({
  headless: true,
  dataPath: './data',
  maxRetries: 3
});

// Search for videos
const result = await ttSearch.searchVideos({
  keyword: 'ai technology',
  limit: 50,
  sortBy: 'relevance'
});

if (result.success) {
  console.log(`Found ${result.data.length} videos`);
  
  // Save to Parquet
  await ttSearch.saveToParquet(result.data, {
    outputPath: 'ai_videos.parquet',
    compression: 'snappy'
  });
}

// Get user profile
const userResult = await ttSearch.getUserProfile('username');
if (userResult.success) {
  console.log(userResult.data);
}

// Get trending hashtags
const trending = await ttSearch.getTrendingHashtags(20);
console.log(trending.data);

// Generate analytics report
await ttSearch.generateReport(
  'ai_videos.parquet',
  'analytics_report.json'
);
```

### Command Line Interface

```bash
# Search videos
tt-search search "ai technology" --limit 100 --output ai_videos.parquet

# Get user profile
tt-search user @username --json

# Get trending hashtags
tt-search trending --limit 30

# Export to different formats
tt-search export ai_videos.parquet --format json
tt-search export ai_videos.parquet --format csv
tt-search export ai_videos.parquet --format excel

# Analytics
tt-search analytics ai_videos.parquet --report

# Interactive mode
tt-search interactive
```

---

## 🔧 API Reference

### Constructor

```typescript
const ttSearch = new TTSearch(config?: TTSearchConfig)
```

**Config Options:**
- `pythonPath?: string` - Path to Python executable (default: 'python3')
- `dataPath?: string` - Base path for data storage (default: './data')
- `headless?: boolean` - Run browser in headless mode (default: true)
- `maxRetries?: number` - Maximum retry attempts (default: 3)
- `cacheEnabled?: boolean` - Enable caching (default: true)
- `rateLimit?: number` - Rate limit for requests (default: 10)

### Methods

#### `searchVideos(options: SearchOptions)`

Search TikTok videos by keyword.

```typescript
interface SearchOptions {
  keyword: string;
  limit?: number;        // Default: 50
  sortBy?: 'relevance' | 'date' | 'likes';
}
```

**Returns:** `Promise<ScraperResult<TikTokVideo[]>>`

#### `getUserProfile(username: string)`

Get TikTok user profile data.

**Returns:** `Promise<ScraperResult<TikTokUser>>`

#### `getTrendingHashtags(limit?: number)`

Get trending hashtags.

**Returns:** `Promise<ScraperResult<TikTokHashtag[]>>`

#### `saveToParquet(videos: TikTokVideo[], options?: StorageOptions)`

Save videos to Parquet format with compression.

```typescript
interface StorageOptions {
  outputPath?: string;
  format?: 'parquet' | 'json' | 'csv' | 'excel';
  compression?: 'snappy' | 'gzip' | 'lz4' | 'zstd';
  partitionBy?: string;
}
```

**Returns:** `Promise<ScraperResult<string>>`

#### `exportData(parquetFile: string, format: 'json' | 'csv' | 'excel', outputFile?: string)`

Export Parquet data to different formats.

**Returns:** `Promise<ScraperResult<string>>`

#### `getAnalytics(parquetFile: string)`

Get comprehensive analytics overview.

**Returns:** `Promise<ScraperResult<OverviewStats>>`

#### `generateReport(parquetFile: string, outputFile?: string)`

Generate detailed analytics report.

**Returns:** `Promise<ScraperResult<string>>`

---

## 🎯 CLI Commands

### Search

```bash
tt-search search <keyword> [options]

Options:
  -l, --limit <number>    Maximum number of videos (default: 50)
  -s, --sort <type>       Sort by (relevance|date|likes)
  -o, --output <file>     Output file (Parquet format)
  --json                  Output as JSON
```

### User Profile

```bash
tt-search user <username> [options]

Options:
  --json                  Output as JSON
```

### Trending

```bash
tt-search trending [options]

Options:
  -l, --limit <number>    Maximum number of hashtags (default: 20)
  --json                  Output as JSON
```

### Export

```bash
tt-search export <file> [options]

Options:
  -f, --format <type>     Output format (json|csv|excel)
  -o, --output <file>     Output file path
```

### Analytics

```bash
tt-search analytics <file> [options]

Options:
  -r, --report            Generate full report
  -o, --output <file>     Report output file
```

### Interactive Mode

```bash
tt-search interactive
# or
tt-search i
```

---

## 📊 Data Types

### TikTokVideo

```typescript
interface TikTokVideo {
  id: string;
  description: string;
  author: string;
  authorId: string;
  createTime: number;
  musicTitle: string;
  musicAuthor: string;
  stats: {
    likes: number;
    comments: number;
    shares: number;
    views: number;
  };
  hashtags: string[];
  videoUrl: string;
  coverUrl: string;
  duration: number;
  scrapedAt: string;
}
```

### TikTokUser

```typescript
interface TikTokUser {
  id: string;
  username: string;
  nickname: string;
  signature: string;
  avatarUrl: string;
  verified: boolean;
  followerCount: number;
  followingCount: number;
  videoCount: number;
  heartCount: number;
  scrapedAt: string;
}
```

---

## 🧪 Advanced Examples

### Batch Processing

```typescript
const keywords = ['ai', 'machine learning', 'robotics'];

for (const keyword of keywords) {
  const result = await ttSearch.searchVideos({ keyword, limit: 100 });
  
  if (result.success) {
    await ttSearch.saveToParquet(result.data, {
      outputPath: `${keyword}_videos.parquet`,
      compression: 'snappy'
    });
  }
  
  // Rate limiting
  await new Promise(resolve => setTimeout(resolve, 2000));
}
```

### Analytics Pipeline

```typescript
// 1. Search and save
const result = await ttSearch.searchVideos({
  keyword: 'trending dance',
  limit: 200
});

const parquetFile = 'trending_dance.parquet';
await ttSearch.saveToParquet(result.data, { outputPath: parquetFile });

// 2. Export to multiple formats
await ttSearch.exportData(parquetFile, 'json', 'data.json');
await ttSearch.exportData(parquetFile, 'csv', 'data.csv');
await ttSearch.exportData(parquetFile, 'excel', 'data.xlsx');

// 3. Generate analytics report
await ttSearch.generateReport(parquetFile, 'report.json');
```

### Custom Python Scripts

You can also use the Python modules directly:

```python
from python.scrapers.tiktok_scraper import TikTokScraper
from python.storage.parquet_storage import ParquetStorage
from python.analytics.analytics import TikTokAnalytics

# Scraping
async with TikTokScraper() as scraper:
    videos = await scraper.search_videos("ai", limit=100)

# Storage
storage = ParquetStorage()
storage.save_videos(videos, filename="ai_videos.parquet")

# Analytics
analytics = TikTokAnalytics("ai_videos.parquet")
analytics.print_overview()
analytics.cluster_content(n_clusters=5)
```

---

## 🏗️ Architecture

```
tt-search/
├── src/                    # TypeScript source
│   ├── core/              # Core TTSearch class
│   ├── types/             # TypeScript definitions
│   ├── cli/               # CLI interface
│   └── utils/             # Utilities
├── python/                # Python backend
│   ├── scrapers/          # TikTok scrapers
│   ├── storage/           # Parquet storage
│   ├── analytics/         # ML analytics
│   └── processors/        # Data processors
├── data/                  # Data storage
│   ├── videos/           # Video data
│   ├── users/            # User data
│   └── analytics/        # Analytics output
└── tests/                # Test suites
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

MIT © Brashkie

---

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Please respect TikTok's Terms of Service and rate limits. The authors are not responsible for any misuse of this software.

---

## 🙏 Acknowledgments

- Apache Parquet for efficient data storage
- Playwright for reliable web automation
- scikit-learn for machine learning capabilities
- The open-source community

---

<div align="center">

**Made with ❤️ by [Brashkie](https://github.com/brashkie)**

[⭐ Star this repo](https://github.com/brashkie/tt-search) if you find it useful!

</div>
