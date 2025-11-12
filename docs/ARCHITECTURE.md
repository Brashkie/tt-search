cat > /mnt/user-data/outputs/ARCHITECTURE.md << 'ENDOFFILE'
# TT-Search Architecture

## Overview

TT-Search is a hybrid Node.js/Python application that provides professional TikTok data extraction, storage, and analytics capabilities. The architecture is designed for scalability, maintainability, and performance.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface  │  JavaScript API  │  TypeScript Types      │
├─────────────────────────────────────────────────────────────┤
│                     Node.js Layer (TypeScript)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   TTSearch   │  │  CLI Handler │  │    Utils     │     │
│  │     Core     │  │   Commander  │  │   Helpers    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                          ↓                                   │
│                   IPC Bridge (spawn)                        │
│                          ↓                                   │
├─────────────────────────────────────────────────────────────┤
│                    Python Layer (Python 3.10+)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Scrapers   │  │   Storage    │  │  Analytics   │     │
│  │  Playwright  │  │   Parquet    │  │  ML Models   │     │
│  │   TikTok     │  │  PyArrow     │  │  sklearn     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         ↓                  ↓                  ↓             │
├─────────────────────────────────────────────────────────────┤
│                        Data Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Videos     │  │    Users     │  │  Analytics   │     │
│  │  .parquet    │  │  .parquet    │  │    .json     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Node.js Layer (Frontend)

**Technology Stack:**
- TypeScript 5.3
- Node.js 18+
- Commander.js (CLI)
- Chalk, Ora (UI)

**Responsibilities:**
- API interface for developers
- CLI command handling
- Configuration management
- Python process orchestration
- Error handling and logging

**Key Classes:**

#### TTSearch Core
```typescript
class TTSearch {
  - searchVideos(options: SearchOptions)
  - getUserProfile(username: string)
  - getTrendingHashtags(limit: number)
  - saveToParquet(videos: TikTokVideo[], options: StorageOptions)
  - exportData(parquetFile: string, format: string)
  - getAnalytics(parquetFile: string)
  - generateReport(parquetFile: string, outputFile: string)
}
```

### 2. Python Layer (Backend)

**Technology Stack:**
- Python 3.10+
- Playwright (web automation)
- PyArrow (Parquet I/O)
- Pandas (data processing)
- scikit-learn (ML)

**Responsibilities:**
- Web scraping and data extraction
- Data storage and compression
- Analytics and ML processing
- Data transformation

**Key Modules:**

#### TikTok Scraper
```python
class TikTokScraper:
  - search_videos(keyword, limit)
  - get_user_profile(username)
  - get_trending_hashtags(limit)
```

#### Parquet Storage
```python
class ParquetStorage:
  - save_videos(videos, partition_by, filename)
  - load_videos(filename, filters)
  - export_to_json(parquet_file, output_file)
  - export_to_csv(parquet_file, output_file)
  - export_to_excel(parquet_file, output_file)
```

#### Analytics Engine
```python
class TikTokAnalytics:
  - get_overview_stats()
  - get_top_videos(metric, limit)
  - analyze_hashtags(limit)
  - cluster_content(n_clusters)
  - predict_virality()
```

## Data Flow

### 1. Search Flow
```
User Input → CLI/API → TTSearch.searchVideos()
  ↓
Python TikTokScraper.search_videos()
  ↓
Playwright Browser Automation
  ↓
Raw TikTok Data
  ↓
Data Cleaning & Transformation
  ↓
Structured TikTokVideo Objects
  ↓
Return to Node.js
  ↓
Optional: Save to Parquet
```

### 2. Storage Flow
```
TikTokVideo[] → TTSearch.saveToParquet()
  ↓
Python ParquetStorage.save_videos()
  ↓
DataFrame Creation with Schema
  ↓
PyArrow Table Conversion
  ↓
Parquet Write with Compression
  ↓
File Path Return
```

### 3. Analytics Flow
```
Parquet File → TTSearch.getAnalytics()
  ↓
Python TikTokAnalytics.load_data()
  ↓
Feature Engineering
  ↓
Statistical Analysis
  ↓
ML Processing (Clustering, Prediction)
  ↓
Results Aggregation
  ↓
JSON Report Generation
```

## Storage Format

### Parquet Schema

**Videos Table:**
```
- id: string
- description: string
- author: string
- author_id: string
- create_time: int64
- music_title: string
- music_author: string
- likes: int64
- comments: int64
- shares: int64
- views: int64
- hashtags: list<string>
- video_url: string
- cover_url: string
- duration: int32
- scraped_at: timestamp
```

**Compression:**
- Algorithm: Snappy (default), Gzip, LZ4, Zstd
- Row Group Size: 10,000 rows
- Dictionary Encoding: Enabled
- Statistics: Enabled

## Performance Optimizations

### 1. Scraping
- Async/await pattern for concurrent requests
- Rate limiting to avoid blocking
- Retry logic with exponential backoff
- Browser pooling for efficiency

### 2. Storage
- Columnar compression (Parquet)
- Efficient predicate pushdown
- Partitioning by author/date
- Dictionary encoding for strings

### 3. Analytics
- Vectorized operations with NumPy/Pandas
- Lazy loading with filters
- Batch processing for large datasets
- Incremental updates

## Scalability Considerations

### Horizontal Scaling
- Stateless design allows multiple instances
- Shared data layer via network storage
- Queue-based task distribution (future)

### Vertical Scaling
- Efficient memory usage with streaming
- Chunked processing for large datasets
- Resource limits and monitoring

## Security

### Data Privacy
- Local data storage by default
- No data sent to external services
- User credentials never stored

### Rate Limiting
- Configurable request limits
- Exponential backoff on errors
- User-agent rotation (optional)

## Error Handling

### Levels
1. **Network Errors**: Retry with backoff
2. **Parsing Errors**: Log and continue
3. **Storage Errors**: Rollback and notify
4. **Fatal Errors**: Exit with status code

### Logging
- Rich console output for CLI
- Structured logging for API
- Error tracking with context

## Testing Strategy

### Unit Tests
- TypeScript: Jest
- Python: pytest
- Coverage target: 80%+

### Integration Tests
- End-to-end CLI workflows
- Python module integration
- Parquet I/O verification

## Future Enhancements

### Planned Features
1. **Real-time Streaming**: WebSocket support
2. **Advanced Filtering**: Complex query DSL
3. **Video Download**: Direct video capture
4. **Sentiment Analysis**: NLP integration
5. **Network Graphs**: Social network analysis
6. **Redis Caching**: Distributed cache
7. **GraphQL API**: Alternative API interface
8. **Web Dashboard**: React-based UI
9. **Docker Support**: Containerization
10. **CI/CD Pipeline**: Automated testing and deployment

## Dependencies

### Core Dependencies
- **Node.js**: Runtime environment
- **TypeScript**: Type safety
- **Python**: Backend processing
- **Playwright**: Web automation
- **PyArrow**: Parquet I/O
- **Pandas**: Data manipulation
- **scikit-learn**: Machine learning

### Development Dependencies
- **Jest**: Testing framework
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **pytest**: Python testing

## Deployment

### NPM Package
```bash
npm publish
```

### Local Installation
```bash
npm link
```

### Docker (Future)
```bash
docker build -t tt-search .
docker run -it tt-search
```

## Maintenance

### Version Updates
- Semantic versioning (MAJOR.MINOR.PATCH)
- Changelog maintenance
- Breaking changes documentation

### Dependency Updates
- Regular security audits
- Compatible version updates
- Testing before deployment

---

**Last Updated**: 2024-11-08  
**Version**: 1.0.0  
**Author**: Brashkie
ENDOFFILE
ls -lh /mnt/user-data/outputs/ARCHITECTURE.md
