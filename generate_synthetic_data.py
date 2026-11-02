import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(num_rows=5000):
    platforms = ['Instagram', 'YouTube', 'TikTok', 'LinkedIn', 'X']
    content_types = ['Video', 'Image', 'Carousel', 'Text', 'Link']
    categories = ['Education', 'Entertainment', 'Technology', 'Lifestyle', 'Marketing']
    
    data = []
    base_date = datetime(2023, 1, 1)
    
    for i in range(num_rows):
        platform = random.choice(platforms)
        content_type = random.choice(content_types)
        
        # Simulating realistic engagement based on platform
        followers = random.randint(1000, 500000)
        reach = random.randint(int(followers * 0.05), int(followers * 0.8))
        views = int(reach * random.uniform(1.1, 1.5)) if content_type == 'Video' else reach
        
        likes = int(views * random.uniform(0.01, 0.15))
        comments = int(likes * random.uniform(0.05, 0.3))
        shares = int(likes * random.uniform(0.01, 0.2))
        saves = int(likes * random.uniform(0.02, 0.25))
        
        post_date = base_date + timedelta(days=random.randint(0, 365))
        post_time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
        
        video_duration = round(random.uniform(15, 600), 1) if content_type == 'Video' else 0.0
        
        data.append({
            'post_id': f"POST_{i+1:05d}",
            'platform': platform,
            'post_date': post_date.strftime('%Y-%m-%d'),
            'post_time': post_time,
            'content_type': content_type,
            'content_category': random.choice(categories),
            'followers': followers,
            'impressions': int(reach * random.uniform(1.0, 1.2)),
            'reach': reach,
            'views': views,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'saves': saves,
            'video_duration': video_duration,
            'caption_length': random.randint(20, 2200),
            'hashtag_count': random.randint(0, 30)
        })
        
    df = pd.DataFrame(data)
    
    # Introduce some realistic data quality issues (missing values, duplicates)
    # 1. Nulls in content_category
    mask_cc = np.random.rand(num_rows) < 0.05
    df.loc[mask_cc, 'content_category'] = np.nan
    
    # 2. Add duplicates
    duplicates = df.sample(n=50, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    df.to_csv("data/sample/sample_social_data.csv", index=False)
    print("Generated 5,000 synthetic records with intentional realistic data quality issues.")

if __name__ == "__main__":
    generate_sample_data()
