import logging
from pathlib import Path
from typing import List

# === Logger Configuration ===
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class DirectoryManager:
    """Handles creation and management of project directories"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        
    def get_directory_structure(self) -> List[str]:
        return [
            # Main directories
            "data/raw", "data/processed", "data/features", "data/splits", "data/quality_reports",
            
            # Source code
            "src/data", "src/models/candidate_generation", "src/models/ranking",
            "src/models/online_learning", "src/evaluation", "src/serving", "src/utils",
            
            # Configs and scripts
            "configs", "scripts", "notebooks",
            
            # Tests
            "tests/unit", "tests/integration", "tests/performance",
            
            # Documentation & outputs
            "docs", "reports", "models/checkpoints", "models/artifacts",
            
            # Deployment
            "docker", "deployment/k8s", "deployment/terraform",
            
            # Demos and frontend
            "demo", "frontend"
        ]
    
    def get_python_packages(self) -> List[str]:
        return [
            "src", "src/data", "src/models", 
            "src/models/candidate_generation", "src/models/ranking", "src/models/online_learning",
            "src/evaluation", "src/serving", "src/utils",
            "tests", "tests/unit", "tests/integration"
        ]
    
    def create_directories(self) -> bool:
        try:
            logger.info("📁 Creating project directory structure...")
            for dir_path in self.get_directory_structure():
                full_path = self.project_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Created directory: {full_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create directories: {e}")
            return False
    
    def create_python_packages(self) -> bool:
        try:
            logger.info("🐍 Creating Python package __init__.py files...")
            for package in self.get_python_packages():
                init_file = self.project_root / package / "__init__.py"
                init_file.touch(exist_ok=True)
                logger.debug(f"Created: {init_file}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create Python packages: {e}")
            return False

if __name__ == "__main__":
    root = Path.cwd()
    manager = DirectoryManager(project_root=root)
    
    success_dirs = manager.create_directories()
    success_pkgs = manager.create_python_packages()

    if success_dirs and success_pkgs:
        logger.info("✅ Project structure created successfully.")
    else:
        logger.warning("⚠️ Project structure setup encountered issues.")
