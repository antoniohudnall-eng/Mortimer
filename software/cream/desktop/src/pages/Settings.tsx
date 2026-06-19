import React, { useState } from 'react';
import { Download, Upload, Database, Archive, Trash2, Settings as SettingsIcon, Info } from 'lucide-react';
import type { CreamDataStore } from '../shared/src/store';
import type { DatabaseState } from '../shared/src/types';

interface SettingsPageProps {
  dataStore: CreamDataStore;
  data: DatabaseState;
}

const SettingsPage: React.FC<SettingsPageProps> = ({ dataStore, data }) => {
  const [activeTab, setActiveTab] = useState('general');
  const [exportMessage, setExportMessage] = useState('');
  const [importMessage, setImportMessage] = useState('');
  const [archiveMessage, setArchiveMessage] = useState('');

  const handleExportJSON = () => {
    const json = dataStore.exportToJSON();
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cream-backup-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    setExportMessage('Data exported successfully!');
    setTimeout(() => setExportMessage(''), 3000);
  };

  const handleExportCSV = (type: 'contacts' | 'appointments' | 'tasks' | 'projects') => {
    const csv = dataStore.exportToCSV(type);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cream-${type}-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
      const json = e.target?.result as string;
      if (dataStore.importFromJSON(json)) {
        setImportMessage('Data imported successfully!');
      } else {
        setImportMessage('Import failed. Please check the file.');
      }
      setTimeout(() => setImportMessage(''), 3000);
    };
    reader.readAsText(file);
  };

  const handleArchiveOld = () => {
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
    const result = dataStore.archiveOldData(sixMonthsAgo);
    setArchiveMessage(`Archived ${result.appointments} appointments and ${result.tasks} tasks.`);
    setTimeout(() => setArchiveMessage(''), 3000);
  };

  const stats = dataStore.getStatistics();

  return (
    <div className="page settings-page">
      <div className="settings-sidebar">
        {['general', 'data', 'about'].map(tab => (
          <button 
            key={tab}
            className={activeTab === tab ? 'active' : ''}
            onClick={() => setActiveTab(tab)}
          >
            {tab === 'general' && <><SettingsIcon size={18} /> General</>}
            {tab === 'data' && <><Database size={18} /> Data Management</>}
            {tab === 'about' && <><Info size={18} /> About</>}
          </button>
        ))}
      </div>

      <div className="settings-content">
        {activeTab === 'general' && (
          <div className="settings-section">
            <h2>General Settings</h2>
            
            <div className="setting-group">
              <h3>Application Statistics</h3>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-value">{stats.totalContacts}</div>
                  <div className="stat-label">Contacts</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.totalAppointments}</div>
                  <div className="stat-label">Appointments</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.totalTasks}</div>
                  <div className="stat-label">Total Tasks</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.completedTasks}</div>
                  <div className="stat-label">Completed</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.activeProjects}</div>
                  <div className="stat-label">Active Projects</div>
                </div>
              </div>
            </div>

            <div className="setting-group">
              <h3>Preferences</h3>
              <div className="setting-item">
                <label>Default Reminder Time (minutes)</label>
                <input 
                  type="number" 
                  value={data.settings.defaultReminderMinutes}
                  onChange={e => dataStore.updateSettings({ defaultReminderMinutes: parseInt(e.target.value) })}
                />
              </div>
              <div className="setting-item">
                <label>Default Appointment Duration (minutes)</label>
                <input 
                  type="number" 
                  value={data.settings.defaultAppointmentDuration}
                  onChange={e => dataStore.updateSettings({ defaultAppointmentDuration: parseInt(e.target.value) })}
                />
              </div>
              <div className="setting-item">
                <label>Theme</label>
                <select 
                  value={data.settings.theme}
                  onChange={e => dataStore.updateSettings({ theme: e.target.value as any })}
                >
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="system">System</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'data' && (
          <div className="settings-section">
            <h2>Data Management</h2>
            
            <div className="setting-group">
              <h3><Download size={18} /> Export Data</h3>
              <button className="btn-secondary" onClick={handleExportJSON}>
                Export Full Backup (JSON)
              </button>
              <div className="export-csv">
                <span>Export as CSV:</span>
                {(['contacts', 'appointments', 'tasks', 'projects'] as const).map(type => (
                  <button key={type} onClick={() => handleExportCSV(type)}>
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </button>
                ))}
              </div>
              {exportMessage && <div className="message success">{exportMessage}</div>}
            </div>

            <div className="setting-group">
              <h3><Upload size={18} /> Import Data</h3>
              <input type="file" accept=".json" onChange={handleImport} />
              {importMessage && <div className={`message ${importMessage.includes('success') ? 'success' : 'error'}`}>{importMessage}</div>}
            </div>

            <div className="setting-group">
              <h3><Archive size={18} /> Archive Old Data</h3>
              <p>Archive appointments and tasks older than 6 months.</p>
              <button className="btn-secondary" onClick={handleArchiveOld}>
                Archive Old Data
              </button>
              {archiveMessage && <div className="message success">{archiveMessage}</div>}
            </div>
          </div>
        )}

        {activeTab === 'about' && (
          <div className="settings-section">
            <h2>About CREAM</h2>
            <div className="about-card">
              <div className="logo-large">🍦</div>
              <h1>CREAM PIM</h1>
              <p className="version">Version 1.0.0</p>
              <p>A Time & Chaos inspired Personal Information Manager</p>
              <p>Built with ❤️ by Performance Supply Depot LLC</p>
              <div className="about-links">
                <a href="#">Documentation</a>
                <a href="#">Support</a>
                <a href="#">License</a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SettingsPage;