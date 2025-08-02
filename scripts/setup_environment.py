import subprocess
from pathlib import Path

def setup_environment():
    requirements = [
        # === Production dependencies ===
        "torch>=2.0.0", "torchvision>=0.15.0",
        #"tensorflow>=2.13.0", 
        "scikit-learn>=1.3.0",
        "scipy>=1.10.0", "numpy>=1.24.0",
        "pandas>=2.0.0", "polars>=0.18.0",
        "pyarrow>=12.0.0", "dask>=2023.1.0",
        "transformers>=4.30.0", "sentence-transformers>=2.2.0",
        "gensim>=4.3.0", "implicit>=0.7.0",
        "faiss-cpu>=1.7.4", "annoy>=1.17.0", "hnswlib>=0.7.0",
        "optuna>=3.2.0", "wandb>=0.15.0", "mlflow>=2.4.0",
        "matplotlib>=3.7.0", "seaborn>=0.12.0",
        "plotly>=5.14.0", "altair>=5.0.0",
        "fastapi>=0.100.0", "uvicorn>=0.22.0",
        "streamlit>=1.24.0", "gradio>=3.35.0",
        "redis>=4.6.0", "pymongo>=4.4.0", "sqlalchemy>=2.0.0",
        "tqdm>=4.65.0", "click>=8.1.0", "pyyaml>=6.0",
        "python-dotenv>=1.0.0", "requests>=2.31.0", "nbformat>=5.8.0",

        # === Dev dependencies ===
        "pytest>=7.4.0", "pytest-cov>=4.1.0", "pytest-mock>=3.11.0",
        "black>=23.0.0", "flake8>=6.0.0", "mypy>=1.4.0",
        "pre-commit>=3.3.0", "jupyter>=1.0.0", "jupyterlab>=4.0.0"
    ]

    requirements_path = Path.cwd() / "requirements.txt"

    try:
        print("📝 Writing to requirements.txt...")
        requirements_path.write_text("\n".join(requirements))
        print(f"✅ requirements.txt written to: {requirements_path}")

        print("📦 Installing dependencies...")
        subprocess.check_call(["python3", "-m", "pip", "install"] + requirements)
        print("✅ All dependencies installed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        print("⚠️ Check the above error and consider installing packages manually or updating your Python version.")

if __name__ == "__main__":
    setup_environment()
