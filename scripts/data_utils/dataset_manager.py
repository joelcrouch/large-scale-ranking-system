import logging
from pathlib import Path
import urllib.request
import zipfile

# === Logger Configuration ===
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class DatasetManager:
    """Handles dataset downloading and management"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.data_dir = project_root / "data"

    def download_movielens(self) -> bool:
        """Download MovieLens dataset"""
        try:
            logger.info("Downloading MovieLens dataset...")

            url = "https://files.grouplens.org/datasets/movielens/ml-25m.zip"
            target_path = self.data_dir / "raw" / "ml-25m.zip"
            target_path.parent.mkdir(parents=True, exist_ok=True)

            if target_path.exists():
                logger.info("MovieLens dataset already exists")
                return True

            urllib.request.urlretrieve(url, target_path)

            with zipfile.ZipFile(target_path, 'r') as zip_ref:
                zip_ref.extractall(self.data_dir / "raw")

            logger.info("MovieLens dataset downloaded and extracted")
            return True

        except Exception as e:
            logger.error(f"Failed to download MovieLens dataset: {e}")
            return False

    def create_amazon_download_script(self) -> bool:
        """Create script to download Amazon dataset"""
        try:
            logger.info("Creating Amazon download script...")

            script_content = '''#!/bin/bash
# Amazon Product Reviews Dataset Download Script
# Run this script when you're ready to download the large Amazon dataset

echo "Downloading Amazon Product Reviews dataset..."
echo "Warning: This will download several GB of data"

# Create directory
mkdir -p data/raw/amazon

# Download specific categories (modify as needed)
categories=("Electronics" "Books" "Movies_and_TV")

for category in "${categories[@]}"; do
    echo "Downloading $category reviews..."
    wget -P data/raw/amazon/ "https://amazon-reviews-pds.s3.amazonaws.com/tsv/amazon_reviews_us_${category}_v1_00.tsv.gz"
done

echo "Download complete!"
'''

            script_path = self.project_root / "scripts" / "download_amazon_data.sh"
            script_path.parent.mkdir(parents=True, exist_ok=True)

            with open(script_path, 'w') as f:
                f.write(script_content)

            script_path.chmod(0o755)
            return True

        except Exception as e:
            logger.error(f"Failed to create Amazon download script: {e}")
            return False
