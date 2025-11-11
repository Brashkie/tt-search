"""
TikTok Analytics - Advanced analytics and ML-powered insights
"""
import sys
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
sns.set_style("whitegrid")


class TikTokAnalytics:
    """Professional analytics for TikTok data with ML insights"""
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize analytics
        
        Args:
            data_path: Path to Parquet data file
        """
        self.data_path = data_path
        self.df: Optional[pd.DataFrame] = None
        
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, path: str):
        """Load data from Parquet file"""
        console.print(f"[cyan]Loading data from {path}...[/cyan]")
        self.df = pd.read_parquet(path)
        console.print(f"[green]✓[/green] Loaded {len(self.df)} records")
    
    def get_overview_stats(self) -> Dict[str, Any]:
        """Get overview statistics of the dataset"""
        if self.df is None or self.df.empty:
            return {}
        
        stats = {
            'total_videos': len(self.df),
            'unique_authors': self.df['author'].nunique() if 'author' in self.df else 0,
            'total_likes': int(self.df['likes'].sum()) if 'likes' in self.df else 0,
            'total_comments': int(self.df['comments'].sum()) if 'comments' in self.df else 0,
            'total_shares': int(self.df['shares'].sum()) if 'shares' in self.df else 0,
            'total_views': int(self.df['views'].sum()) if 'views' in self.df else 0,
            'avg_likes': float(self.df['likes'].mean()) if 'likes' in self.df else 0,
            'avg_comments': float(self.df['comments'].mean()) if 'comments' in self.df else 0,
            'avg_shares': float(self.df['shares'].mean()) if 'shares' in self.df else 0,
            'avg_engagement': self._calculate_avg_engagement(),
            'date_range': self._get_date_range()
        }
        
        return stats
    
    def print_overview(self):
        """Print formatted overview statistics"""
        stats = self.get_overview_stats()
        
        if not stats:
            console.print("[yellow]⚠ No data loaded[/yellow]")
            return
        
        table = Table(title="📊 TikTok Data Overview")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        
        table.add_row("Total Videos", f"{stats['total_videos']:,}")
        table.add_row("Unique Authors", f"{stats['unique_authors']:,}")
        table.add_row("Total Likes", f"{stats['total_likes']:,}")
        table.add_row("Total Comments", f"{stats['total_comments']:,}")
        table.add_row("Total Shares", f"{stats['total_shares']:,}")
        table.add_row("Total Views", f"{stats['total_views']:,}")
        table.add_row("Avg Engagement", f"{stats['avg_engagement']:.2%}")
        table.add_row("Date Range", stats['date_range'])
        
        console.print(table)
    
    def get_top_videos(
        self,
        metric: str = 'likes',
        limit: int = 10
    ) -> pd.DataFrame:
        """
        Get top videos by specified metric
        
        Args:
            metric: Metric to sort by (likes, comments, shares, views)
            limit: Number of top videos to return
            
        Returns:
            DataFrame with top videos
        """
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        if metric not in self.df.columns:
            console.print(f"[yellow]⚠ Metric '{metric}' not found[/yellow]")
            return pd.DataFrame()
        
        top = self.df.nlargest(limit, metric)
        
        console.print(f"\n[cyan]Top {limit} Videos by {metric.title()}:[/cyan]")
        for idx, row in enumerate(top.itertuples(), 1):
            console.print(f"{idx}. @{row.author}: {row.description[:50]}...")
            console.print(f"   {metric}: {getattr(row, metric):,}")
        
        return top
    
    def get_top_authors(
        self,
        metric: str = 'likes',
        limit: int = 10
    ) -> pd.DataFrame:
        """
        Get top authors by aggregated metric
        
        Args:
            metric: Metric to aggregate (likes, comments, shares, views)
            limit: Number of top authors to return
            
        Returns:
            DataFrame with top authors
        """
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        author_stats = self.df.groupby('author').agg({
            metric: 'sum',
            'id': 'count'
        }).rename(columns={'id': 'video_count'})
        
        author_stats = author_stats.sort_values(metric, ascending=False).head(limit)
        
        console.print(f"\n[cyan]Top {limit} Authors by {metric.title()}:[/cyan]")
        
        table = Table()
        table.add_column("Rank", style="cyan")
        table.add_column("Author", style="yellow")
        table.add_column("Videos", style="blue")
        table.add_column(metric.title(), style="green")
        
        for idx, (author, row) in enumerate(author_stats.iterrows(), 1):
            table.add_row(
                str(idx),
                f"@{author}",
                f"{int(row['video_count']):,}",
                f"{int(row[metric]):,}"
            )
        
        console.print(table)
        return author_stats
    
    def analyze_hashtags(self, limit: int = 20) -> List[Tuple[str, int]]:
        """
        Analyze most popular hashtags
        
        Args:
            limit: Number of top hashtags to return
            
        Returns:
            List of (hashtag, count) tuples
        """
        if self.df is None or 'hashtags' not in self.df.columns:
            return []
        
        # Flatten all hashtags
        all_hashtags = []
        for hashtags in self.df['hashtags']:
            if isinstance(hashtags, list):
                all_hashtags.extend(hashtags)
        
        # Count occurrences
        from collections import Counter
        hashtag_counts = Counter(all_hashtags)
        top_hashtags = hashtag_counts.most_common(limit)
        
        console.print(f"\n[cyan]Top {limit} Hashtags:[/cyan]")
        
        table = Table()
        table.add_column("Rank", style="cyan")
        table.add_column("Hashtag", style="yellow")
        table.add_column("Count", style="green")
        
        for idx, (tag, count) in enumerate(top_hashtags, 1):
            table.add_row(str(idx), f"#{tag}", f"{count:,}")
        
        console.print(table)
        return top_hashtags
    
    def cluster_content(
        self,
        n_clusters: int = 5,
        max_features: int = 100
    ) -> pd.DataFrame:
        """
        Cluster videos by content similarity using K-Means
        
        Args:
            n_clusters: Number of clusters
            max_features: Maximum TF-IDF features
            
        Returns:
            DataFrame with cluster assignments
        """
        if self.df is None or 'description' not in self.df.columns:
            console.print("[yellow]⚠ No description data available[/yellow]")
            return pd.DataFrame()
        
        console.print(f"[cyan]Clustering videos into {n_clusters} groups...[/cyan]")
        
        # Prepare text data
        descriptions = self.df['description'].fillna('')
        
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        
        # K-Means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(tfidf_matrix)
        
        # Add cluster assignments
        self.df['cluster'] = clusters
        
        # Analyze clusters
        console.print("\n[cyan]Cluster Analysis:[/cyan]")
        
        for cluster_id in range(n_clusters):
            cluster_data = self.df[self.df['cluster'] == cluster_id]
            
            console.print(f"\n[yellow]Cluster {cluster_id}:[/yellow]")
            console.print(f"  Videos: {len(cluster_data)}")
            console.print(f"  Avg Likes: {cluster_data['likes'].mean():.0f}")
            
            # Get top terms for this cluster
            cluster_indices = np.where(clusters == cluster_id)[0]
            cluster_tfidf = tfidf_matrix[cluster_indices].mean(axis=0).A1
            top_terms_idx = cluster_tfidf.argsort()[-5:][::-1]
            top_terms = [vectorizer.get_feature_names_out()[i] for i in top_terms_idx]
            
            console.print(f"  Top Terms: {', '.join(top_terms)}")
        
        return self.df[['id', 'description', 'cluster', 'likes', 'comments']]
    
    def calculate_engagement_score(self) -> pd.Series:
        """
        Calculate engagement score for each video
        
        Returns:
            Series with engagement scores
        """
        if self.df is None:
            return pd.Series()
        
        # Weighted engagement formula
        engagement = (
            self.df['likes'] * 1.0 +
            self.df['comments'] * 2.0 +  # Comments are more valuable
            self.df['shares'] * 3.0      # Shares are most valuable
        )
        
        # Normalize by views if available
        if 'views' in self.df.columns and self.df['views'].sum() > 0:
            engagement = engagement / (self.df['views'] + 1)
        
        return engagement
    
    def predict_virality(self) -> pd.DataFrame:
        """
        Predict video virality based on features
        
        Returns:
            DataFrame with virality predictions
        """
        if self.df is None or len(self.df) < 10:
            console.print("[yellow]⚠ Insufficient data for prediction[/yellow]")
            return pd.DataFrame()
        
        console.print("[cyan]Analyzing virality patterns...[/cyan]")
        
        # Calculate features
        self.df['engagement_score'] = self.calculate_engagement_score()
        self.df['description_length'] = self.df['description'].str.len()
        self.df['hashtag_count'] = self.df['hashtags'].apply(
            lambda x: len(x) if isinstance(x, list) else 0
        )
        
        # Define virality threshold (top 20%)
        virality_threshold = self.df['engagement_score'].quantile(0.8)
        self.df['is_viral'] = self.df['engagement_score'] > virality_threshold
        
        # Analyze viral vs non-viral
        viral_df = self.df[self.df['is_viral']]
        non_viral_df = self.df[~self.df['is_viral']]
        
        console.print("\n[cyan]Virality Analysis:[/cyan]")
        console.print(f"Viral Videos: {len(viral_df)} ({len(viral_df)/len(self.df)*100:.1f}%)")
        console.print(f"\nViral vs Non-Viral Characteristics:")
        console.print(f"  Avg Description Length: {viral_df['description_length'].mean():.0f} vs {non_viral_df['description_length'].mean():.0f}")
        console.print(f"  Avg Hashtags: {viral_df['hashtag_count'].mean():.1f} vs {non_viral_df['hashtag_count'].mean():.1f}")
        console.print(f"  Avg Likes: {viral_df['likes'].mean():.0f} vs {non_viral_df['likes'].mean():.0f}")
        
        return self.df[['id', 'description', 'engagement_score', 'is_viral']]
    
    def generate_report(self, output_file: str = "analytics_report.json") -> str:
        """
        Generate comprehensive analytics report
        
        Args:
            output_file: Output file path
            
        Returns:
            Path to generated report
        """
        console.print("[cyan]Generating comprehensive analytics report...[/cyan]")
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'overview': self.get_overview_stats(),
            'top_videos': self.get_top_videos(limit=10).to_dict('records'),
            'top_authors': self.get_top_authors(limit=10).to_dict(),
            'top_hashtags': self.analyze_hashtags(limit=20)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        console.print(f"[green]✓[/green] Report saved to: {output_file}")
        return output_file
    
    def _calculate_avg_engagement(self) -> float:
        """Calculate average engagement rate"""
        if self.df is None or self.df.empty:
            return 0.0
        
        total_engagement = (
            self.df['likes'].sum() +
            self.df['comments'].sum() +
            self.df['shares'].sum()
        )
        
        total_views = self.df['views'].sum() if 'views' in self.df else total_engagement
        
        if total_views == 0:
            return 0.0
        
        return total_engagement / total_views
    
    def _get_date_range(self) -> str:
        """Get date range of scraped data"""
        if self.df is None or 'scraped_at' not in self.df.columns:
            return "Unknown"
        
        min_date = self.df['scraped_at'].min()
        max_date = self.df['scraped_at'].max()
        
        return f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"


def main():
    """CLI interface for analytics"""
    if len(sys.argv) < 3:
        console.print("[yellow]Usage:[/yellow] python analytics.py <parquet_file> <command>")
        console.print("Commands:")
        console.print("  overview - Show overview statistics")
        console.print("  top <metric> [limit] - Show top videos")
        console.print("  authors <metric> [limit] - Show top authors")
        console.print("  hashtags [limit] - Analyze hashtags")
        console.print("  cluster [n_clusters] - Cluster content")
        console.print("  virality - Predict virality")
        console.print("  report [output_file] - Generate full report")
        return
    
    parquet_file = sys.argv[1]
    command = sys.argv[2]
    
    analytics = TikTokAnalytics(parquet_file)
    
    if command == "overview":
        analytics.print_overview()
        
    elif command == "top":
        metric = sys.argv[3] if len(sys.argv) > 3 else 'likes'
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        analytics.get_top_videos(metric, limit)
        
    elif command == "authors":
        metric = sys.argv[3] if len(sys.argv) > 3 else 'likes'
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        analytics.get_top_authors(metric, limit)
        
    elif command == "hashtags":
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        analytics.analyze_hashtags(limit)
        
    elif command == "cluster":
        n_clusters = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        result = analytics.cluster_content(n_clusters)
        print(result.to_json(orient='records', indent=2))
        
    elif command == "virality":
        result = analytics.predict_virality()
        print(result.to_json(orient='records', indent=2))
        
    elif command == "report":
        output_file = sys.argv[3] if len(sys.argv) > 3 else 'analytics_report.json'
        analytics.generate_report(output_file)


if __name__ == "__main__":
    main()
