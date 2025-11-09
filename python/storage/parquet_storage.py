"""
Parquet Storage Manager - Professional data storage with compression and optimization
"""
import os
import json
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


class ParquetStorage:
    """Professional Parquet storage manager with compression and partitioning"""
    
    # Define schemas for different data types
    VIDEO_SCHEMA = pa.schema([
        ('id', pa.string()),
        ('description', pa.string()),
        ('author', pa.string()),
        ('author_id', pa.string()),
        ('create_time', pa.int64()),
        ('music_title', pa.string()),
        ('music_author', pa.string()),
        ('likes', pa.int64()),
        ('comments', pa.int64()),
        ('shares', pa.int64()),
        ('views', pa.int64()),
        ('hashtags', pa.list_(pa.string())),
        ('video_url', pa.string()),
        ('cover_url', pa.string()),
        ('duration', pa.int32()),
        ('scraped_at', pa.timestamp('ms'))
    ])
    
    USER_SCHEMA = pa.schema([
        ('id', pa.string()),
        ('username', pa.string()),
        ('nickname', pa.string()),
        ('signature', pa.string()),
        ('avatar_url', pa.string()),
        ('verified', pa.bool_()),
        ('follower_count', pa.int64()),
        ('following_count', pa.int64()),
        ('video_count', pa.int64()),
        ('heart_count', pa.int64()),
        ('scraped_at', pa.timestamp('ms'))
    ])
    
    def __init__(
        self,
        storage_path: str = "./data",
        compression: str = "snappy"
    ):
        """
        Initialize Parquet storage
        
        Args:
            storage_path: Base path for data storage
            compression: Compression algorithm (snappy, gzip, lz4, zstd)
        """
        self.storage_path = Path(storage_path)
        self.compression = compression
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Create necessary directories"""
        dirs = ['videos', 'users', 'hashtags', 'analytics', 'temp']
        for dir_name in dirs:
            (self.storage_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    def save_videos(
        self,
        videos: List[Dict[str, Any]],
        partition_by: Optional[str] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        Save videos to Parquet with optimal compression
        
        Args:
            videos: List of video dictionaries
            partition_by: Column to partition by (e.g., 'author', 'date')
            filename: Custom filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if not videos:
            console.print("[yellow]⚠ No videos to save[/yellow]")
            return ""
        
        console.print(f"[cyan]Saving {len(videos)} videos to Parquet...[/cyan]")
        
        # Prepare data
        df = self._prepare_video_dataframe(videos)
        
        # Generate filename
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"videos_{timestamp}.parquet"
        
        filepath = self.storage_path / "videos" / filename
        
        # Convert to PyArrow Table with schema
        table = pa.Table.from_pandas(df, schema=self.VIDEO_SCHEMA)
        
        # Write with compression and optimization
        pq.write_table(
            table,
            filepath,
            compression=self.compression,
            use_dictionary=True,
            write_statistics=True,
            row_group_size=10000
        )
        
        file_size = filepath.stat().st_size / (1024 * 1024)  # MB
        console.print(f"[green]✓[/green] Saved to: {filepath}")
        console.print(f"[green]✓[/green] File size: {file_size:.2f} MB")
        console.print(f"[green]✓[/green] Compression: {self.compression}")
        
        return str(filepath)
    
    def save_users(
        self,
        users: List[Dict[str, Any]],
        filename: Optional[str] = None
    ) -> str:
        """
        Save users to Parquet
        
        Args:
            users: List of user dictionaries
            filename: Custom filename
            
        Returns:
            Path to saved file
        """
        if not users:
            console.print("[yellow]⚠ No users to save[/yellow]")
            return ""
        
        console.print(f"[cyan]Saving {len(users)} users to Parquet...[/cyan]")
        
        df = self._prepare_user_dataframe(users)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"users_{timestamp}.parquet"
        
        filepath = self.storage_path / "users" / filename
        
        table = pa.Table.from_pandas(df, schema=self.USER_SCHEMA)
        
        pq.write_table(
            table,
            filepath,
            compression=self.compression,
            use_dictionary=True,
            write_statistics=True
        )
        
        console.print(f"[green]✓[/green] Saved to: {filepath}")
        return str(filepath)
    
    def load_videos(
        self,
        filename: Optional[str] = None,
        filters: Optional[List] = None
    ) -> pd.DataFrame:
        """
        Load videos from Parquet with optional filtering
        
        Args:
            filename: Specific file to load (loads all if None)
            filters: PyArrow filters for predicate pushdown
            
        Returns:
            DataFrame with video data
        """
        videos_path = self.storage_path / "videos"
        
        if filename:
            filepath = videos_path / filename
            if not filepath.exists():
                console.print(f"[red]✗ File not found: {filepath}[/red]")
                return pd.DataFrame()
            
            console.print(f"[cyan]Loading videos from {filename}...[/cyan]")
            df = pd.read_parquet(filepath, filters=filters)
        else:
            console.print("[cyan]Loading all videos...[/cyan]")
            parquet_files = list(videos_path.glob("*.parquet"))
            
            if not parquet_files:
                console.print("[yellow]⚠ No parquet files found[/yellow]")
                return pd.DataFrame()
            
            dfs = [pd.read_parquet(f, filters=filters) for f in parquet_files]
            df = pd.concat(dfs, ignore_index=True)
        
        console.print(f"[green]✓[/green] Loaded {len(df)} videos")
        return df
    
    def load_users(self, filename: Optional[str] = None) -> pd.DataFrame:
        """Load users from Parquet"""
        users_path = self.storage_path / "users"
        
        if filename:
            filepath = users_path / filename
            df = pd.read_parquet(filepath)
        else:
            parquet_files = list(users_path.glob("*.parquet"))
            if not parquet_files:
                return pd.DataFrame()
            dfs = [pd.read_parquet(f) for f in parquet_files]
            df = pd.concat(dfs, ignore_index=True)
        
        console.print(f"[green]✓[/green] Loaded {len(df)} users")
        return df
    
    def export_to_json(
        self,
        parquet_file: str,
        output_file: Optional[str] = None
    ) -> str:
        """
        Export Parquet to JSON
        
        Args:
            parquet_file: Input Parquet file path
            output_file: Output JSON file path
            
        Returns:
            Path to JSON file
        """
        console.print("[cyan]Exporting to JSON...[/cyan]")
        
        df = pd.read_parquet(parquet_file)
        
        if output_file is None:
            output_file = parquet_file.replace('.parquet', '.json')
        
        df.to_json(output_file, orient='records', indent=2, date_format='iso')
        
        console.print(f"[green]✓[/green] Exported to: {output_file}")
        return output_file
    
    def export_to_csv(
        self,
        parquet_file: str,
        output_file: Optional[str] = None
    ) -> str:
        """Export Parquet to CSV"""
        console.print("[cyan]Exporting to CSV...[/cyan]")
        
        df = pd.read_parquet(parquet_file)
        
        if output_file is None:
            output_file = parquet_file.replace('.parquet', '.csv')
        
        df.to_csv(output_file, index=False)
        
        console.print(f"[green]✓[/green] Exported to: {output_file}")
        return output_file
    
    def export_to_excel(
        self,
        parquet_file: str,
        output_file: Optional[str] = None
    ) -> str:
        """Export Parquet to Excel"""
        console.print("[cyan]Exporting to Excel...[/cyan]")
        
        df = pd.read_parquet(parquet_file)
        
        if output_file is None:
            output_file = parquet_file.replace('.parquet', '.xlsx')
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        
        console.print(f"[green]✓[/green] Exported to: {output_file}")
        return output_file
    
    def get_statistics(self, parquet_file: str) -> Dict[str, Any]:
        """
        Get detailed statistics about a Parquet file
        
        Args:
            parquet_file: Path to Parquet file
            
        Returns:
            Dictionary with statistics
        """
        parquet_file_obj = pq.ParquetFile(parquet_file)
        
        stats = {
            'num_rows': parquet_file_obj.metadata.num_rows,
            'num_columns': parquet_file_obj.metadata.num_columns,
            'num_row_groups': parquet_file_obj.metadata.num_row_groups,
            'file_size_mb': Path(parquet_file).stat().st_size / (1024 * 1024),
            'compression': parquet_file_obj.metadata.row_group(0).column(0).compression,
            'created_by': parquet_file_obj.metadata.created_by,
            'schema': parquet_file_obj.schema_arrow,
        }
        
        return stats
    
    def print_info(self, parquet_file: str):
        """Print detailed information about a Parquet file"""
        stats = self.get_statistics(parquet_file)
        
        table = Table(title=f"Parquet File Info: {Path(parquet_file).name}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Rows", f"{stats['num_rows']:,}")
        table.add_row("Columns", str(stats['num_columns']))
        table.add_row("Row Groups", str(stats['num_row_groups']))
        table.add_row("File Size", f"{stats['file_size_mb']:.2f} MB")
        table.add_row("Compression", stats['compression'])
        
        console.print(table)
        console.print("\n[cyan]Schema:[/cyan]")
        console.print(stats['schema'])
    
    def _prepare_video_dataframe(self, videos: List[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare video data for Parquet storage"""
        processed = []
        
        for video in videos:
            # Extract stats if nested
            stats = video.get('stats', {})
            
            processed.append({
                'id': video.get('id', ''),
                'description': video.get('description', ''),
                'author': video.get('author', ''),
                'author_id': video.get('author_id', ''),
                'create_time': video.get('create_time', 0),
                'music_title': video.get('music_title', ''),
                'music_author': video.get('music_author', ''),
                'likes': stats.get('likes', 0) if isinstance(stats, dict) else 0,
                'comments': stats.get('comments', 0) if isinstance(stats, dict) else 0,
                'shares': stats.get('shares', 0) if isinstance(stats, dict) else 0,
                'views': stats.get('views', 0) if isinstance(stats, dict) else 0,
                'hashtags': video.get('hashtags', []),
                'video_url': video.get('video_url', ''),
                'cover_url': video.get('cover_url', ''),
                'duration': video.get('duration', 0),
                'scraped_at': pd.to_datetime(video.get('scraped_at', datetime.now().isoformat()))
            })
        
        return pd.DataFrame(processed)
    
    def _prepare_user_dataframe(self, users: List[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare user data for Parquet storage"""
        processed = []
        
        for user in users:
            processed.append({
                'id': user.get('id', ''),
                'username': user.get('username', ''),
                'nickname': user.get('nickname', ''),
                'signature': user.get('signature', ''),
                'avatar_url': user.get('avatar_url', ''),
                'verified': user.get('verified', False),
                'follower_count': user.get('follower_count', 0),
                'following_count': user.get('following_count', 0),
                'video_count': user.get('video_count', 0),
                'heart_count': user.get('heart_count', 0),
                'scraped_at': pd.to_datetime(user.get('scraped_at', datetime.now().isoformat()))
            })
        
        return pd.DataFrame(processed)


def main():
    """CLI interface for storage operations"""
    if len(sys.argv) < 2:
        console.print("[yellow]Usage:[/yellow] python parquet_storage.py <command> <args>")
        console.print("Commands:")
        console.print("  info <parquet_file>")
        console.print("  export <parquet_file> <format> [output_file]")
        console.print("  stats <parquet_file>")
        return
    
    command = sys.argv[1]
    storage = ParquetStorage()
    
    if command == "info":
        parquet_file = sys.argv[2]
        storage.print_info(parquet_file)
        
    elif command == "export":
        parquet_file = sys.argv[2]
        format = sys.argv[3].lower()
        output_file = sys.argv[4] if len(sys.argv) > 4 else None
        
        if format == "json":
            storage.export_to_json(parquet_file, output_file)
        elif format == "csv":
            storage.export_to_csv(parquet_file, output_file)
        elif format == "excel":
            storage.export_to_excel(parquet_file, output_file)
        else:
            console.print(f"[red]✗ Unknown format: {format}[/red]")
            
    elif command == "stats":
        parquet_file = sys.argv[2]
        stats = storage.get_statistics(parquet_file)
        console.print(json.dumps(stats, indent=2, default=str))


if __name__ == "__main__":
    main()
