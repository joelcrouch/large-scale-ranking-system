"""
Amazon Reviews 2023 Dataset Setup Script
Downloads and preprocesses the latest Amazon dataset from McAuley Lab
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
import requests
import gzip
import shutil
from typing import Dict, List, Optional
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

class AmazonDataSetup:
    """Setup class for Amazon Reviews 2023 dataset"""
    
    def __init__(self, data_dir: str = "data/raw/amazon_2023"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Available categories with their approximate sizes
        self.categories = {
            'All_Beauty': {'reviews': '701K', 'items': '113K', 'size': 'Small'},
            'Digital_Music': {'reviews': '130K', 'items': '71K', 'size': 'Small'},
            'Gift_Cards': {'reviews': '152K', 'items': '1K', 'size': 'Small'},
            'Magazine_Subscriptions': {'reviews': '72K', 'items': '3K', 'size': 'Small'},
            'Software': {'reviews': '5M', 'items': '89K', 'size': 'Medium'},
            'Video_Games': {'reviews': '5M', 'items': '137K', 'size': 'Medium'},
            'Electronics': {'reviews': '44M', 'items': '1.6M', 'size': 'Large'},
            'Books': {'reviews': '30M', 'items': '4.4M', 'size': 'Large'},
            'Clothing_Shoes_and_Jewelry': {'reviews': '66M', 'items': '7.2M', 'size': 'Very Large'},
        }
        
        # Base URLs for the dataset
        self.base_url = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/"
        
    def list_available_categories(self) -> Dict:
        """List all available categories with their statistics"""
        logger.info("Available Amazon categories:")
        for category, stats in self.categories.items():
            logger.info(f"  {category}: {stats['reviews']} reviews, {stats['items']} items ({stats['size']} dataset)")
        return self.categories
    
    def download_category_data(self, category: str, include_metadata: bool = True) -> bool:
        """Download data for a specific category"""
        if category not in self.categories:
            logger.error(f"Category '{category}' not available. Use list_available_categories() to see options.")
            return False
            
        logger.info(f"Downloading Amazon {category} dataset...")
        
        # Create category directory
        category_dir = self.data_dir / category
        category_dir.mkdir(exist_ok=True)
        
        # Download review data
        review_url = f"{self.base_url}review_categories/{category}.jsonl.gz"
        review_file = category_dir / f"{category}_reviews.jsonl.gz"
        
        success = self._download_file(review_url, review_file)
        if not success:
            return False
            
        # Download metadata if requested
        if include_metadata:
            meta_url = f"{self.base_url}meta_categories/meta_{category}.jsonl.gz"
            meta_file = category_dir / f"meta_{category}.jsonl.gz"
            success = self._download_file(meta_url, meta_file)
            if not success:
                logger.warning(f"Could not download metadata for {category}")
        
        # Extract files
        self._extract_gz_file(review_file)
        if include_metadata and meta_file.exists():
            self._extract_gz_file(meta_file)
            
        logger.info(f"Successfully downloaded {category} dataset")
        return True
    
    def _download_file(self, url: str, filepath: Path) -> bool:
        """Download a file with progress bar"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as file, tqdm(
                desc=filepath.name,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    size = file.write(chunk)
                    pbar.update(size)
                    
            return True
            
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            return False
    
    def _extract_gz_file(self, gz_filepath: Path):
        """Extract a gzipped file"""
        extracted_path = gz_filepath.with_suffix('')
        
        with gzip.open(gz_filepath, 'rb') as f_in:
            with open(extracted_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                
        logger.info(f"Extracted {extracted_path}")
    
    def load_reviews_jsonl(self, category: str, max_records: Optional[int] = None) -> List[Dict]:
        """Load review data from JSONL file"""
        filepath = self.data_dir / category / f"{category}_reviews.jsonl"
        
        if not filepath.exists():
            logger.error(f"Review file not found: {filepath}")
            return []
        
        reviews = []
        with open(filepath, 'r') as f:
            for i, line in enumerate(f):
                if max_records and i >= max_records:
                    break
                try:
                    review = json.loads(line.strip())
                    reviews.append(review)
                except json.JSONDecodeError:
                    continue
                    
        logger.info(f"Loaded {len(reviews)} reviews from {category}")
        return reviews
    
    def load_metadata_jsonl(self, category: str, max_records: Optional[int] = None) -> List[Dict]:
        """Load metadata from JSONL file"""
        filepath = self.data_dir / category / f"meta_{category}.jsonl"
        
        if not filepath.exists():
            logger.warning(f"Metadata file not found: {filepath}")
            return []
        
        metadata = []
        with open(filepath, 'r') as f:
            for i, line in enumerate(f):
                if max_records and i >= max_records:
                    break
                try:
                    meta = json.loads(line.strip())
                    metadata.append(meta)
                except json.JSONDecodeError:
                    continue
                    
        logger.info(f"Loaded {len(metadata)} metadata records from {category}")
        return metadata
    
    def convert_to_standard_format(self, category: str, max_records: Optional[int] = None) -> Dict[str, pd.DataFrame]:
        """Convert Amazon data to standard format for the ranking system"""
        logger.info(f"Converting {category} data to standard format...")
        
        # Load raw data
        reviews = self.load_reviews_jsonl(category, max_records)
        metadata = self.load_metadata_jsonl(category, max_records)
        
        if not reviews:
            logger.error("No review data available")
            return {}
        
        # Convert reviews to DataFrame
        reviews_df = pd.DataFrame(reviews)
        
        # Standardize column names
        column_mapping = {
            'user_id': 'userId',
            'asin': 'itemId',  # Using asin as item ID
            'parent_asin': 'parentItemId',
            'rating': 'rating',
            'timestamp': 'timestamp',
            'title': 'review_title',
            'text': 'review_text',
            'helpful_vote': 'helpful_votes',
            'verified_purchase': 'verified_purchase'
        }
        
        # Rename columns that exist
        for old_col, new_col in column_mapping.items():
            if old_col in reviews_df.columns:
                reviews_df = reviews_df.rename(columns={old_col: new_col})
        
        # Clean and process data
        reviews_df = self._clean_reviews_data(reviews_df)
        
        # Convert metadata to DataFrame if available
        items_df = pd.DataFrame()
        if metadata:
            items_df = pd.DataFrame(metadata)
            items_df = self._clean_metadata(items_df)
        
        # Create interaction matrix format
        interactions_df = reviews_df[['userId', 'itemId', 'rating', 'timestamp']].copy()
        
        result = {
            'ratings': interactions_df,
            'reviews': reviews_df,
            'items': items_df
        }
        
        logger.info(f"Converted data shapes:")
        for name, df in result.items():
            logger.info(f"  {name}: {df.shape}")
            
        return result
    
    def _clean_reviews_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess review data"""
        # Remove rows with missing essential fields
        df = df.dropna(subset=['userId', 'itemId', 'rating'])
        
        # Convert rating to numeric
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df = df.dropna(subset=['rating'])
        
        # Filter valid ratings (1-5 scale)
        df = df[(df['rating'] >= 1) & (df['rating'] <= 5)]
        
        # Convert timestamp to proper format if needed
        if 'timestamp' in df.columns:
            # Handle different timestamp formats
            df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
            # Convert from milliseconds to seconds if needed
            df.loc[df['timestamp'] > 1e10, 'timestamp'] = df.loc[df['timestamp'] > 1e10, 'timestamp'] / 1000
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['userId', 'itemId'])
        
        logger.info(f"Cleaned reviews: {len(df)} interactions")
        return df
    
    def _clean_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess item metadata"""
        # Use parent_asin as the main item ID for consistency
        if 'parent_asin' in df.columns:
            df['itemId'] = df['parent_asin']
        elif 'asin' in df.columns:
            df['itemId'] = df['asin']
        
        # Clean title
        if 'title' in df.columns:
            df['title'] = df['title'].fillna('Unknown Title')
        
        # Process categories
        if 'categories' in df.columns:
            df['main_category'] = df['categories'].apply(
                lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'Unknown'
            )
        
        # Extract numeric price
        if 'price' in df.columns:
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Remove duplicates by itemId
        df = df.drop_duplicates(subset=['itemId'])
        
        logger.info(f"Cleaned metadata: {len(df)} items")
        return df
    
    def save_processed_data(self, data: Dict[str, pd.DataFrame], category: str):
        """Save processed data in multiple formats"""
        output_dir = Path("data/processed") / f"amazon_{category.lower()}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for name, df in data.items():
            if df.empty:
                continue
                
            # Save as Parquet (efficient)
            parquet_path = output_dir / f"{name}.parquet"
            df.to_parquet(parquet_path, index=False)
            
            # Save as CSV (readable)
            csv_path = output_dir / f"{name}.csv"
            df.to_csv(csv_path, index=False)
            
            logger.info(f"Saved {name}: {parquet_path}")
    
    def quick_setup_small_dataset(self) -> Dict[str, pd.DataFrame]:
        """Quick setup with a small dataset for testing"""
        logger.info("Setting up small Amazon dataset for testing...")
        
        category = "All_Beauty"
        review_url = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/All_Beauty.jsonl.gz"
        meta_url = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_All_Beauty.jsonl.gz"

        category_dir = self.data_dir / category
        category_dir.mkdir(exist_ok=True)

        review_file = category_dir / f"{category}_reviews.jsonl.gz"
        meta_file = category_dir / f"meta_{category}.jsonl.gz"
        
        logger.info(f"Downloading Amazon {category} dataset...")

        success_review = self._download_file(review_url, review_file)
        if not success_review:
            logger.error("Failed to download review data")
            return {}

        success_meta = self._download_file(meta_url, meta_file)
        if not success_meta:
            logger.warning("Could not download metadata")
        
        self._extract_gz_file(review_file)
        if meta_file.exists():
            self._extract_gz_file(meta_file)

        logger.info(f"Successfully downloaded {category} dataset")
        
        # Convert to standard format with limited records for testing
        data = self.convert_to_standard_format(category, max_records=10000)
        
        # Save processed data
        self.save_processed_data(data, category)
        
        return data
    
    def setup_medium_dataset(self, category: str = "Video_Games") -> Dict[str, pd.DataFrame]:
        """Setup medium-sized dataset for development"""
        logger.info(f"Setting up medium Amazon dataset: {category}")
        
        success = self.download_category_data(category, include_metadata=True)
        if not success:
            logger.error("Failed to download data")
            return {}
        
        # Convert to standard format
        data = self.convert_to_standard_format(category)
        
        # Save processed data
        self.save_processed_data(data, category)
        
        return data


def main():
    """Main function for standalone execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Amazon Reviews 2023 dataset")
    parser.add_argument("--category", default="Digital_Music", 
                       help="Category to download (default: Digital_Music)")
    parser.add_argument("--quick", action="store_true",
                       help="Quick setup with small dataset")
    parser.add_argument("--list", action="store_true",
                       help="List available categories")
    parser.add_argument("--max-records", type=int, default=None,
                       help="Maximum records to process (for testing)")
    
    args = parser.parse_args()
    
    setup = AmazonDataSetup()
    
    if args.list:
        setup.list_available_categories()
        return
    
    if args.quick:
        data = setup.quick_setup_small_dataset()
    else:
        setup.download_category_data(args.category)
        data = setup.convert_to_standard_format(args.category, args.max_records)
        setup.save_processed_data(data, args.category)
    
    if data:
        print(f"\nDataset setup complete!")
        print(f"Data shapes:")
        for name, df in data.items():
            print(f"  {name}: {df.shape}")
    else:
        print("Setup failed!")


if __name__ == "__main__":
    main()
