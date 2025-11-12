# 🚀 TT-Search - Quick Start Guide

## 📦 What's Included

A complete, professional NPM package for TikTok data extraction with:
- **2,400+ lines of production code**
- **TypeScript + Python hybrid architecture**
- **Apache Parquet storage**
- **ML-powered analytics**
- **CLI + API interfaces**

## ⚡ 3-Step Setup

### 1. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
python3 -m playwright install chromium
```

Or use the automated setup:

```bash
chmod +x setup.sh
./setup.sh
```

### 2. Build the Project

```bash
npm run build
```

### 3. Start Using!

#### CLI Usage
```bash
# Search videos
tt-search search "artificial intelligence" --limit 50 --output ai_videos.parquet

# Get user profile
tt-search user @username

# Trending hashtags
tt-search trending --limit 20

# Interactive mode
tt-search interactive
```

#### API Usage
```typescript
import TTSearch from 'tt-search';

const ttSearch = new TTSearch();

// Search videos
const result = await ttSearch.searchVideos({
  keyword: 'ai technology',
  limit: 50
});

// Save to Parquet
await ttSearch.saveToParquet(result.data, {
  outputPath: 'data.parquet'
});

// Run analytics
await ttSearch.generateReport('data.parquet');
```

## 📁 Project Structure

```
tt-search/
├── src/                    # TypeScript source code
│   ├── core/              # Main TTSearch class
│   ├── types/             # Type definitions
│   └── cli/               # CLI interface
├── python/                # Python backend
│   ├── scrapers/         # TikTok scraping
│   ├── storage/          # Parquet storage
│   ├── analytics/        # ML analytics
│   └── processors/       # Data processing
├── examples/             # Usage examples
├── tests/                # Test suites
└── docs/                 # Documentation
```

## 🎯 Key Files

| File | Purpose |
|------|---------|
| `src/core/TTSearch.ts` | Main API class |
| `src/cli/index.ts` | CLI interface |
| `python/scrapers/tiktok_scraper.py` | TikTok scraper |
| `python/storage/parquet_storage.py` | Parquet I/O |
| `python/analytics/analytics.py` | Analytics engine |
| `package.json` | NPM configuration |
| `requirements.txt` | Python dependencies |

## 🔧 NPM Scripts

```bash
npm run build          # Build TypeScript
npm run dev            # Development mode
npm test               # Run tests
npm run lint           # Lint code
npm run format         # Format code
npm run setup:python   # Install Python deps
```

## 📚 Examples

### Example 1: Basic Search
```bash
tt-search search "machine learning" --limit 30
```

### Example 2: Save and Analyze
```bash
tt-search search "tech" --limit 100 --output tech.parquet
tt-search analytics tech.parquet --report
```

### Example 3: Export Data
```bash
tt-search export tech.parquet --format json
tt-search export tech.parquet --format csv
tt-search export tech.parquet --format excel
```

### Example 4: TypeScript API
```typescript
import TTSearch from './src';

async function main() {
  const ttSearch = new TTSearch();
  
  const videos = await ttSearch.searchVideos({
    keyword: 'coding',
    limit: 50
  });
  
  await ttSearch.saveToParquet(videos.data, {
    outputPath: 'coding_videos.parquet'
  });
  
  await ttSearch.generateReport('coding_videos.parquet');
}

main();
```

### Example 5: Python Direct
```python
from python.scrapers.tiktok_scraper import TikTokScraper

async with TikTokScraper() as scraper:
    videos = await scraper.search_videos("ai", limit=50)
```

## 🎨 Features Showcase

### Data Extraction ✅
- Video search with filters
- User profiles
- Trending hashtags
- Rate limiting
- Error handling

### Storage ✅
- Parquet format
- Multiple compression
- Export to JSON/CSV/Excel
- Efficient partitioning

### Analytics ✅
- Overview statistics
- Top videos/authors
- Hashtag analysis
- Content clustering
- Virality prediction

### Developer Tools ✅
- TypeScript types
- CLI interface
- Interactive mode
- Rich error messages
- Comprehensive docs

## 🐛 Troubleshooting

### Python not found
```bash
# On macOS/Linux
which python3
# Set in config
const ttSearch = new TTSearch({ pythonPath: '/usr/bin/python3' });
```

### Playwright issues
```bash
# Reinstall browsers
python3 -m playwright install --force chromium
```

### Permission denied
```bash
chmod +x setup.sh
chmod +x examples/python-example.py
```

## 📖 Documentation

- **README.md** - Main documentation
- **docs/ARCHITECTURE.md** - Architecture details
- **CONTRIBUTING.md** - Contribution guide
- **CHANGELOG.md** - Version history
- **PROJECT_SUMMARY.md** - Project overview

## 🚀 Publishing to NPM

```bash
# Login to NPM
npm login

# Publish package
npm publish

# Or publish scoped package
npm publish --access public
```

## 💡 Pro Tips

1. **Use Interactive Mode**: `tt-search interactive` for guided usage
2. **Batch Processing**: Loop through keywords for bulk scraping
3. **Cache Results**: Use Parquet for efficient data reuse
4. **Analytics First**: Generate reports before exporting
5. **Rate Limiting**: Respect TikTok's rate limits

## 🎓 Learning Path

1. ✅ Run setup script
2. ✅ Try CLI examples
3. ✅ Explore API usage
4. ✅ Check Python examples
5. ✅ Read architecture docs
6. ✅ Contribute improvements

## ⚠️ Important Notes

- **Rate Limits**: Respect TikTok's rate limits
- **ToS Compliance**: Use responsibly and legally
- **Data Privacy**: Handle user data carefully
- **Performance**: Start small, scale gradually

## 🤝 Getting Help

- **Issues**: Open a GitHub issue
- **Discussions**: Join GitHub discussions
- **Examples**: Check `/examples` folder
- **Docs**: Read full documentation

## 🌟 Next Steps

1. Explore all CLI commands
2. Try API integration
3. Run analytics on sample data
4. Customize for your use case
5. Share feedback and contribute!

---

**Ready to extract TikTok data like a pro? Start with:**

```bash
tt-search interactive
```

**Made with ❤️ by Brashkie**
