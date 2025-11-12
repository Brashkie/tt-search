/**
 * Type definitions for TT-Search
 */

export interface TikTokVideoStats {
  likes: number;
  comments: number;
  shares: number;
  views: number;
}

export interface TikTokVideo {
  id: string;
  description: string;
  author: string;
  authorId: string;
  createTime: number;
  musicTitle: string;
  musicAuthor: string;
  stats: TikTokVideoStats;
  hashtags: string[];
  videoUrl: string;
  coverUrl: string;
  duration: number;
  scrapedAt: string;
}

export interface TikTokUser {
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

export interface TikTokHashtag {
  name: string;
  url: string;
  views: string;
}

export interface SearchOptions {
  keyword: string;
  limit?: number;
  sortBy?: 'relevance' | 'date' | 'likes';
}

export interface StorageOptions {
  outputPath?: string;
  format?: 'parquet' | 'json' | 'csv' | 'excel';
  compression?: 'snappy' | 'gzip' | 'lz4' | 'zstd';
  partitionBy?: string;
}

export interface AnalyticsOptions {
  dataPath: string;
  metric?: 'likes' | 'comments' | 'shares' | 'views';
  limit?: number;
}

export interface OverviewStats {
  totalVideos: number;
  uniqueAuthors: number;
  totalLikes: number;
  totalComments: number;
  totalShares: number;
  totalViews: number;
  avgLikes: number;
  avgComments: number;
  avgShares: number;
  avgEngagement: number;
  dateRange: string;
}

export interface ClusterResult {
  id: string;
  description: string;
  cluster: number;
  likes: number;
  comments: number;
}

export interface ViralityPrediction {
  id: string;
  description: string;
  engagementScore: number;
  isViral: boolean;
}

export interface ExportOptions {
  inputFile: string;
  outputFile?: string;
  format: 'json' | 'csv' | 'excel';
}

export interface TTSearchConfig {
  pythonPath?: string;
  dataPath?: string;
  headless?: boolean;
  maxRetries?: number;
  cacheEnabled?: boolean;
  rateLimit?: number;
}

export interface ScraperResult<T> {
  success: boolean;
  data?: T;
  error?: string;
  meta?: {
    duration: number;
    timestamp: string;
  };
}

export type LogLevel = 'info' | 'warn' | 'error' | 'debug';

export interface Logger {
  info(message: string, meta?: any): void;
  warn(message: string, meta?: any): void;
  error(message: string, meta?: any): void;
  debug(message: string, meta?: any): void;
}
