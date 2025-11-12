"""
Data Processor - Advanced data cleaning and transformation
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import re
from rich.console import Console

console = Console()


class DataProcessor:
    """Professional data processor with cleaning and transformation utilities"""
    
    def __init__(self):
        self.console = console
    
    def clean_video_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean video data with missing value handling and normalization"""
        console.print("[cyan]Cleaning video data...[/cyan]")
        
        cleaned_df = df.copy()
        
        # Handle missing values
        cleaned_df['description'] = cleaned_df['description'].fillna('')
        cleaned_df['author'] = cleaned_df['author'].fillna('unknown')
        cleaned_df['music_title'] = cleaned_df['music_title'].fillna('')
        
        # Fill numeric columns with 0
        numeric_columns = ['likes', 'comments', 'shares', 'views', 'duration']
        for col in numeric_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce').fillna(0)
        
        # Remove duplicates
        initial_count = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates(subset=['id'], keep='first')
        removed = initial_count - len(cleaned_df)
        
        if removed > 0:
            console.print(f"[yellow]Removed {removed} duplicate videos[/yellow]")
        
        # Normalize text fields
        cleaned_df['description'] = cleaned_df['description'].apply(self._clean_text)
        
        # Convert timestamps
        if 'scraped_at' in cleaned_df.columns:
            cleaned_df['scraped_at'] = pd.to_datetime(cleaned_df['scraped_at'], errors='coerce')
        
        console.print(f"[green]✓[/green] Cleaned {len(cleaned_df)} videos")
        return cleaned_df
    
    def calculate_engagement_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate advanced engagement metrics"""
        console.print("[cyan]Calculating engagement metrics...[/cyan]")
        
        df_copy = df.copy()
        
        # Basic engagement rate
        if 'views' in df_copy.columns and df_copy['views'].sum() > 0:
            df_copy['engagement_rate'] = (
                (df_copy['likes'] + df_copy['comments'] + df_copy['shares']) / 
                (df_copy['views'] + 1)
            )
        else:
            df_copy['engagement_rate'] = 0
        
        # Weighted engagement score
        df_copy['engagement_score'] = (
            df_copy['likes'] * 1.0 +
            df_copy['comments'] * 2.0 +
            df_copy['shares'] * 3.0
        )
        
        # Virality coefficient
        df_copy['virality_coefficient'] = (
            df_copy['shares'] / (df_copy['likes'] + 1)
        )
        
        # Comment ratio
        df_copy['comment_ratio'] = (
            df_copy['comments'] / (df_copy['likes'] + 1)
        )
        
        console.print("[green]✓[/green] Calculated engagement metrics")
        return df_copy
    
    def extract_hashtag_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract hashtag-related features"""
        df_copy = df.copy()
        
        # Count hashtags
        df_copy['hashtag_count'] = df_copy['hashtags'].apply(
            lambda x: len(x) if isinstance(x, list) else 0
        )
        
        # Check for popular hashtag patterns
        df_copy['has_fyp'] = df_copy['hashtags'].apply(
            lambda x: any(tag.lower() in ['fyp', 'foryou', 'foryoupage'] 
                         for tag in x) if isinstance(x, list) else False
        )
        
        return df_copy
    
    def extract_text_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract features from text content"""
        df_copy = df.copy()
        
        if 'description' not in df_copy.columns:
            return df_copy
        
        # Length features
        df_copy['description_length'] = df_copy['description'].str.len()
        df_copy['word_count'] = df_copy['description'].str.split().str.len()
        
        # Emoji count
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            "]+", flags=re.UNICODE)
        
        df_copy['emoji_count'] = df_copy['description'].apply(
            lambda x: len(emoji_pattern.findall(x))
        )
        
        return df_copy
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not isinstance(text, str):
            return ''
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def feature_engineering_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """Run complete feature engineering pipeline"""
        console.print("[cyan]Running feature engineering pipeline...[/cyan]")
        
        # Clean data
        df = self.clean_video_data(df)
        
        # Calculate engagement metrics
        df = self.calculate_engagement_metrics(df)
        
        # Extract hashtag features
        df = self.extract_hashtag_features(df)
        
        # Extract text features
        df = self.extract_text_features(df)
        
        console.print("[green]✓[/green] Feature engineering complete")
        return df


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        console.print("[yellow]Usage:[/yellow] python data_processor.py <input_parquet> <output_parquet>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        
        df = pd.read_parquet(input_file)
        processor = DataProcessor()
        processed_df = processor.feature_engineering_pipeline(df)
        processed_df.to_parquet(output_file, compression='snappy')
        console.print(f"[green]✓[/green] Saved to {output_file}")
