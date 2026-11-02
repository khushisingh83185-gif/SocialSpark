import React, { useState, useRef } from 'react';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true);
    } else if (e.type === 'dragleave') {
      setIsDragging(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (selectedFile) => {
    setError(null);
    const validTypes = ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'];
    
    if (!validTypes.includes(selectedFile.type) && !selectedFile.name.endsWith('.csv') && !selectedFile.name.endsWith('.xlsx')) {
      setError("Please upload a valid CSV or Excel file.");
      return;
    }
    
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setIsUploading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await fetch('http://127.0.0.1:8000/data/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Upload failed with status: ${response.status}`);
      }
      
      const data = await response.json();
      setReport(data);
    } catch (err) {
      setError(err.message || "An error occurred during upload.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <h1>Data Upload Hub</h1>
      <p className="subtitle">Upload your raw social media dataset for automatic cleaning and quality analysis.</p>
      
      {!report ? (
        <div style={{ maxWidth: '700px' }}>
          <div 
            className={`dropzone ${isDragging ? 'active' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current.click()}
          >
            <div className="drop-icon">☁️</div>
            <h3 style={{ marginBottom: '8px', color: 'var(--color-navy)' }}>
              {file ? file.name : "Drag & drop your dataset here"}
            </h3>
            <p style={{ color: '#64748b', marginBottom: '24px' }}>
              {file ? `${(file.size / 1024).toFixed(2)} KB` : "Supports .csv and .xlsx formats"}
            </p>
            <button className="btn-primary" onClick={(e) => { e.stopPropagation(); fileInputRef.current.click(); }}>
              {file ? "Change File" : "Browse Files"}
            </button>
            <input 
              type="file" 
              ref={fileInputRef} 
              style={{ display: 'none' }} 
              accept=".csv, .xlsx"
              onChange={handleChange}
            />
          </div>
          
          {error && (
            <div style={{ marginTop: '16px', color: 'var(--color-danger)', background: '#FEFCBF', padding: '12px', borderRadius: '8px' }}>
              ⚠️ {error}
            </div>
          )}
          
          {file && (
            <div style={{ marginTop: '24px', textAlign: 'right' }}>
              <button 
                className="btn-primary" 
                onClick={handleUpload} 
                disabled={isUploading}
                style={{ padding: '14px 32px' }}
              >
                {isUploading ? 'Uploading & Processing...' : 'Start Analytics Engine ✨'}
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="quality-report animate-fade-in">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
            <span style={{ fontSize: '2rem' }}>✅</span>
            <div>
              <h2 style={{ color: 'var(--color-success)' }}>Dataset Processed Successfully</h2>
              <p style={{ color: '#64748b' }}>Filename: {report.filename}</p>
            </div>
          </div>
          
          <h3 style={{ marginTop: '32px', marginBottom: '16px' }}>Data Quality Report</h3>
          
          <div className="card-grid">
            <div className="stat-card success">
              <div className="stat-title">Total Rows Processed</div>
              <div className="stat-value">{report.quality_report.total_rows.toLocaleString()}</div>
            </div>
            
            <div className="stat-card">
              <div className="stat-title">Columns Detected</div>
              <div className="stat-value">{report.quality_report.total_columns}</div>
            </div>
            
            <div className={`stat-card ${report.quality_report.duplicate_rows > 0 ? 'warning' : 'success'}`}>
              <div className="stat-title">Duplicate Rows Fixed</div>
              <div className="stat-value">{report.quality_report.duplicate_rows}</div>
            </div>
          </div>

          {report.quality_report.missing_required_columns.length > 0 && (
            <div className="stat-card error" style={{ marginTop: '24px' }}>
              <div className="stat-title" style={{ color: 'var(--color-danger)' }}>Missing Required Columns</div>
              <p style={{ marginTop: '8px' }}>
                {report.quality_report.missing_required_columns.join(", ")}
              </p>
            </div>
          )}

          <div style={{ marginTop: '40px' }}>
            <button className="btn-primary" onClick={() => window.alert("Navigate to dashboard (Feature coming soon)")}>
              View Analytics Dashboard 📊
            </button>
            <button 
              style={{ marginLeft: '16px', background: 'transparent', border: '1px solid #cbd5e1', padding: '12px 24px', borderRadius: '12px', cursor: 'pointer' }}
              onClick={() => setReport(null)}
            >
              Upload Another File
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
