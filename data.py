from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
import io
import sys
import os

# Adjust path to import analytics module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from analytics.data_cleaning import analyze_dataset_quality, clean_social_media_data
from app.models.database import get_db

router = APIRouter(prefix="/data", tags=["data"])

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV and Excel are supported.")
    
    try:
        contents = await file.read()
        
        # Parse data
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
            
        # 1. Quality Analysis
        quality_metrics = analyze_dataset_quality(df)
        
        # 2. Cleaning
        cleaned_df = clean_social_media_data(df)
        
        # Save sample to processed directory to use for dashboard/analytics
        processed_path = os.path.join(os.path.dirname(__file__), '../../..', 'data', 'processed', 'cleaned_data.csv')
        cleaned_df.to_csv(processed_path, index=False)
        
        return {
            "message": "File uploaded and processed successfully",
            "filename": file.filename,
            "quality_report": quality_metrics,
            "cleaned_rows": len(cleaned_df),
            "columns": list(cleaned_df.columns)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
