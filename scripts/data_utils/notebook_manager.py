import logging
from pathlib import Path
import nbformat as nbf

# === Logger Configuration ===
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class NotebookManager:
    """Handles creation of initial notebooks"""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def create_eda_notebook(self) -> bool:
        """Create exploratory data analysis notebook"""
        try:
            logger.info("Creating EDA notebook...")

            content = '''# Exploratory Data Analysis

## 1. Dataset Overview
- Load and examine the basic structure
- Check data types and missing values
- Analyze distributions

## 2. User Analysis
- User interaction patterns
- Activity distributions
- Cold start analysis

## 3. Item Analysis  
- Item popularity distributions
- Category analysis
- Content feature analysis

## 4. Interaction Analysis
- Rating distributions
- Temporal patterns
- Sparsity analysis

## 5. Insights and Recommendations
- Data quality issues
- Preprocessing strategies
- Feature engineering opportunities
'''

            notebook_path = self.project_root / "notebooks" / "01_exploratory_data_analysis.ipynb"
            notebook_path.parent.mkdir(parents=True, exist_ok=True)

            nb = nbf.v4.new_notebook()
            nb.cells = [nbf.v4.new_markdown_cell(content)]

            with open(notebook_path, 'w') as f:
                nbf.write(nb, f)

            return True

        except Exception as e:
            logger.error(f"Failed to create EDA notebook: {e}")
            return False
