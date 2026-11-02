import pandas as pd
import numpy as np
from io import BytesIO

REQUIRED_COLUMNS = [
    'post_id', 'platform', 'post_date', 'content_type',
    'likes', 'comments', 'shares', 'saves'
]

def analyze_dataset_quality(df: pd.DataFrame) -> dict:
    """Analyze the dataset for quality metrics before cleaning."""
    missing_values = df.isnull().sum().to_dict()
    duplicate_rows = int(df.duplicated().sum())
    
    # Check for missing required columns
    missing_req = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_required_columns": missing_req,
        "duplicate_rows": duplicate_rows,
        "missing_values_per_column": {k: int(v) for k, v in missing_values.items() if v > 0}
    }

def clean_social_media_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the social media dataset."""
    df_cleaned = df.copy()
    
    # 1. Remove duplicate rows
    df_cleaned.drop_duplicates(inplace=True)
    
    # 2. Standardize column names (lowercase, strip spaces)
    df_cleaned.columns = df_cleaned.columns.str.lower().str.strip()
    
    # 3. Handle missing values (fill numerical with 0, categorical with 'Unknown')
    num_cols = df_cleaned.select_dtypes(include=[np.number]).columns
    cat_cols = df_cleaned.select_dtypes(include=['object']).columns
    df_cleaned[num_cols] = df_cleaned[num_cols].fillna(0)
    df_cleaned[cat_cols] = df_cleaned[cat_cols].fillna('Unknown')
    
    # 4. Standardize dates
    if 'post_date' in df_cleaned.columns:
        df_cleaned['post_date'] = pd.to_datetime(df_cleaned['post_date'], errors='coerce')
        # Extract derived features
        df_cleaned['day_of_week'] = df_cleaned['post_date'].dt.day_name()
        df_cleaned['month'] = df_cleaned['post_date'].dt.month_name()
        df_cleaned['weekend_flag'] = df_cleaned['post_date'].dt.dayofweek.isin([5, 6]).astype(int)
    
    # 5. Calculate derived engagement metrics
    engagement_cols = ['likes', 'comments', 'shares', 'saves']
    available_cols = [col for col in engagement_cols if col in df_cleaned.columns]
    
    if available_cols:
        df_cleaned['total_engagement'] = df_cleaned[available_cols].sum(axis=1)
    
    # Engagement rate (engagement / reach * 100)
    if 'total_engagement' in df_cleaned.columns and 'reach' in df_cleaned.columns:
        df_cleaned['engagement_rate'] = np.where(
            df_cleaned['reach'] > 0, 
            (df_cleaned['total_engagement'] / df_cleaned['reach']) * 100, 
            0
        )
    
    # 6. Detect and fix invalid negative values
    for col in num_cols:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].apply(lambda x: max(x, 0))
            
    return df_cleaned
