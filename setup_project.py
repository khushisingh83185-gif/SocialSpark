import os
from pathlib import Path

def create_structure(base_path: str):
    structure = [
        "frontend/src/components",
        "frontend/src/pages",
        "frontend/src/services",
        "frontend/src/assets",
        "backend/app/routes",
        "backend/app/models",
        "backend/app/schemas",
        "backend/app/services",
        "backend/app/utils",
        "analytics/sql_queries",
        "ml/models",
        "data/raw",
        "data/processed",
        "data/sample",
        "dashboard/powerbi",
        "docs",
        "tests"
    ]

    files = [
        "backend/requirements.txt",
        "backend/app/main.py",
        "analytics/data_cleaning.py",
        "analytics/eda.py",
        "analytics/feature_engineering.py",
        "ml/train.py",
        "ml/predict.py",
        "ml/preprocessing.py",
        "ml/evaluate.py",
        "docs/PRD.md",
        "docs/database-schema.md",
        "docs/API.md",
        ".env.example",
        ".gitignore",
        "README.md",
        "requirements.txt"
    ]

    base = Path(base_path)
    
    # Create directories
    for d in structure:
        (base / d).mkdir(parents=True, exist_ok=True)
        # Create an empty .gitkeep so git tracks empty dirs
        with open(base / d / ".gitkeep", "w") as f:
            pass
            
    # Create empty files
    for f in files:
        file_path = base / f
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()

    print("Project structure created successfully!")

if __name__ == "__main__":
    create_structure(r"C:\Users\Lenovo\Desktop\SocialSpark")
