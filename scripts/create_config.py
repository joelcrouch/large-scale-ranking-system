import logging
from pathlib import Path
from typing import Dict
import yaml

# === Logger setup ===
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class ConfigManager:
    """Handles creation of configuration files"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_dir = project_root / "configs"
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def get_main_config(self) -> Dict:
        return {
            "project": {
                "name": "large-scale-ranking-system",
                "version": "0.1.0",
                "description": "Production-ready ranking system"
            },
            "data": {
                "raw_data_path": "data/raw",
                "processed_data_path": "data/processed",
                "feature_store_path": "data/features", 
                "splits_path": "data/splits"
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    
    def get_data_config(self) -> Dict:
        return {
            "datasets": {
                "amazon_reviews": {
                    "url": "https://amazon-reviews-pds.s3.amazonaws.com/",
                    "categories": ["Electronics", "Books", "Movies_and_TV"],
                    "format": "json.gz"
                },
                "movielens": {
                    "url": "https://files.grouplens.org/datasets/movielens/ml-25m.zip",
                    "format": "csv"
                }
            },
            "preprocessing": {
                "min_user_interactions": 5,
                "min_item_interactions": 5,
                "test_size": 0.2,
                "val_size": 0.1,
                "random_state": 42
            },
            "feature_engineering": {
                "user_features": ["age", "gender", "occupation"],
                "item_features": ["category", "price", "rating", "description"],
                "interaction_features": ["rating", "timestamp", "helpful_votes"]
            }
        }
    
    def get_logging_config(self) -> str:
        return '''version: 1
disable_existing_loggers: False

formatters:
  standard:
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  detailed:
    format: "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
    stream: ext://sys.stdout

  file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: detailed
    filename: logs/ranking_system.log
    maxBytes: 10485760
    backupCount: 5

loggers:
  ranking_system:
    level: DEBUG
    handlers: [console, file]
    propagate: False

root:
  level: INFO
  handlers: [console]
'''

    def create_main_config(self) -> bool:
        try:
            logger.info("📄 Creating main_config.yaml...")
            with open(self.config_dir / "main_config.yaml", 'w') as f:
                yaml.dump(self.get_main_config(), f, default_flow_style=False)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create main config: {e}")
            return False
    
    def create_data_config(self) -> bool:
        try:
            logger.info("📄 Creating data_config.yaml...")
            with open(self.config_dir / "data_config.yaml", 'w') as f:
                yaml.dump(self.get_data_config(), f, default_flow_style=False)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create data config: {e}")
            return False
    
    def create_logging_config(self) -> bool:
        try:
            logger.info("📄 Creating logging_config.yaml...")
            (self.project_root / "logs").mkdir(exist_ok=True)
            with open(self.config_dir / "logging_config.yaml", 'w') as f:
                f.write(self.get_logging_config())
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create logging config: {e}")
            return False

if __name__ == "__main__":
    project_root = Path.cwd()
    config_mgr = ConfigManager(project_root)

    success_main = config_mgr.create_main_config()
    success_data = config_mgr.create_data_config()
    success_logging = config_mgr.create_logging_config()

    if success_main and success_data and success_logging:
        logger.info("✅ All configuration files created successfully.")
    else:
        logger.warning("⚠️ Some configuration files failed to generate.")
