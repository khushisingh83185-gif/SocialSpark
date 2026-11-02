import React from 'react';

// We will look for logo.png in the public folder or assets.
// To avoid Vite build errors before the user saves the file, we use a string path.
const logoUrl = '/logo.png';

export default function Sidebar({ activeTab, setActiveTab }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <img 
            src={logoUrl} 
            alt="SocialSpark Logo" 
            onError={(e) => {
                e.target.onerror = null; 
                e.target.src = "https://ui-avatars.com/api/?name=SS&background=FFB6C1&color=fff&rounded=true&bold=true";
            }}
        />
        <span>SocialSpark</span>
      </div>
      
      <nav className="sidebar-nav">
        <div 
          className={`nav-item ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          <span style={{ fontSize: '1.2rem' }}>📁</span>
          <span>Data Upload</span>
        </div>
        
        <div 
          className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          <span style={{ fontSize: '1.2rem' }}>📊</span>
          <span>Dashboard</span>
        </div>
      </nav>
      
      <div style={{ marginTop: 'auto', textAlign: 'center', fontSize: '0.8rem', color: '#94a3b8' }}>
        ANALYZE • PREDICT • GROW
      </div>
    </aside>
  );
}
