import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import UploadPage from './pages/UploadPage';

function App() {
  const [activeTab, setActiveTab] = useState('upload');

  return (
    <div className="app-container">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="main-content glass-panel animate-fade-in" style={{ margin: '20px 20px 20px 280px' }}>
        {activeTab === 'upload' && <UploadPage />}
        {activeTab === 'dashboard' && (
          <div>
            <h1>Analytics Dashboard</h1>
            <p className="subtitle">Visualizing insights and metrics.</p>
            <div className="stat-card">
              <p>Please upload a dataset first to view the dashboard.</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
