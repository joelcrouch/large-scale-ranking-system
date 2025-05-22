import logging
from pathlib import Path

# === Logger Configuration ===
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class FileManager:
    """Handles creation of various project files"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        
    def create_gitignore(self) -> bool:
        """Create .gitignore file"""
        try:
            logger.info("Creating .gitignore...")
            
            content = '''# Data files
data/raw/
data/processed/
*.csv
*.json.gz
*.tsv.gz
*.parquet

# Model artifacts
models/
*.pkl
*.pt
*.pth
*.onnx

# Logs and outputs
logs/
*.log
wandb/
mlruns/

# Environment
.env
.venv/
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Testing
.coverage
.pytest_cache/
.tox/
htmlcov/

# Documentation
docs/_build/

# OS
.DS_Store
Thumbs.db
'''
            
            with open(self.project_root / ".gitignore", 'w') as f:
                f.write(content)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to create .gitignore: {e}")
            return False
    
    def create_makefile(self) -> bool:
        """Create Makefile"""
        try:
            logger.info("Creating Makefile...")
            
            content = '''# Makefile for Large-Scale Ranking System

.PHONY: help install install-dev setup test clean lint type-check

help:
\t@echo "Available commands:"
\t@echo "  install      Install production dependencies"
\t@echo "  install-dev  Install development dependencies"
\t@echo "  setup        Set up the project environment"
\t@echo "  test         Run tests"
\t@echo "  clean        Clean up generated files"
\t@echo "  lint         Run linting"
\t@echo "  type-check   Run type checking"

install:
\tpip install -r requirements.txt

install-dev:
\tpip install -r requirements.txt
\tpip install -r requirements-dev.txt

setup:
\tpython scripts/setup_phase1.py
\tpython scripts/validate_data.py

test:
\tpytest tests/ -v

clean:
\tfind . -type f -name "*.pyc" -delete
\tfind . -type d -name "__pycache__" -delete
\tfind . -type d -name ".pytest_cache" -exec rm -rf {} +
\tfind . -type d -name "*.egg-info" -exec rm -rf {} +

lint:
\tblack src/ tests/
\tflake8 src/ tests/

type-check:
\tmypy src/

data-download:
\tbash scripts/download_amazon_data.sh

notebook:
\tjupyter lab notebooks/
'''
            
            with open(self.project_root / "Makefile", 'w') as f:
                f.write(content)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to create Makefile: {e}")
            return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python create_files.py <project_root_path>")
        sys.exit(1)
    
    project_root = Path(sys.argv[1])
    file_manager = FileManager(project_root)
    
    success_gitignore = file_manager.create_gitignore()
    success_makefile = file_manager.create_makefile()
    
    if success_gitignore and success_makefile:
        logger.info("✅ All project files created successfully.")
    else:
        logger.error("❌ Some files failed to be created.")
