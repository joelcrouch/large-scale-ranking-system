import logging
from pathlib import Path

# === Logger Configuration ===
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class ScriptManager:
    """Handles creation of utility scripts"""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def create_validation_script(self) -> bool:
        """Create data validation script"""
        try:
            logger.info("Creating data validation script...")

            content = '''#!/usr/bin/env python3
"""
Data validation and quality check script
Run after downloading datasets to verify integrity
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys

def validate_movielens_data(data_path: Path) -> bool:
    """Validate MovieLens dataset"""
    logger = logging.getLogger(__name__)

    # Check if files exist
    required_files = ["ratings.csv", "movies.csv", "tags.csv", "links.csv"]
    ml_path = data_path / "ml-25m"

    for file in required_files:
        file_path = ml_path / file
        if not file_path.exists():
            logger.error(f"Missing required file: {file}")
            return False

    # Load and validate ratings
    ratings = pd.read_csv(ml_path / "ratings.csv")
    logger.info(f"Ratings shape: {ratings.shape}")
    logger.info(f"Unique users: {ratings['userId'].nunique()}")
    logger.info(f"Unique movies: {ratings['movieId'].nunique()}")

    # Basic validation
    assert ratings['rating'].min() >= 0.5
    assert ratings['rating'].max() <= 5.0
    assert ratings['userId'].notna().all()
    assert ratings['movieId'].notna().all()

    logger.info("MovieLens data validation passed!")
    return True

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data_path = Path("data/raw")

    if validate_movielens_data(data_path):
        print("All validations passed!")
    else:
        print("Validation failed!")
        sys.exit(1)
'''

            script_path = self.project_root / "scripts" / "validate_data.py"
            script_path.parent.mkdir(parents=True, exist_ok=True)

            with open(script_path, 'w') as f:
                f.write(content)

            return True

        except Exception as e:
            logger.error(f"Failed to create validation script: {e}")
            return False
