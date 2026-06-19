import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { 
  Users, Calendar, CheckSquare, FolderKanban, Settings, 
  Search, Bell, Menu, X, Archive, Database 
} from 'lucide-react';
import { CreamDataStore } from '../shared/src/store';
import type { DatabaseState } from '../shared/src/types';
import ContactsPage from './pages/Contacts';
import CalendarPage from './pages/Calendar';
import TasksPage from './pages/Tasks';
import ProjectsPage from './pages/Projects';
import SettingsPage from './pages/Settings';
import SearchModal from './components/SearchModal';
import './styles.css';

const App: React.FC = () => {
  const [dataStore] = useState(() => new CreamDataStore());
  const [data, setData] = useState<DatabaseState>(dataStore.getState());
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchOpen, setSearchOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const unsubscribe = dataStore.subscribe((newData) => {
      setData(newData);
    });
    return unsubscribe;
  }, [dataStore]);

  const navItems = [
    { path: '/', icon: Users, label: 'Contacts', badge: data.contacts.length },
    { path: '/calendar', icon: Calendar, label: 'Calendar', badge: data.appointments.length },
    { path: '/tasks', icon: CheckSquare, label: 'Tasks', badge: data.tasks.filter(t => t.status !== 'completed').length },
    { path: '/projects', icon: FolderKanban, label: 'Projects', badge: data.projects.filter(p => p.status === 'active').length },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <div className="app">
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h1 className="logo">
            <span className="logo-icon">🍦</span>
            <span className="logo-text">CREAM</span>
          </h1>
          <button className="toggle-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
        
        <nav className="nav">
          {navItems.map(item => (
            <Link 
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <item.icon size={20} />
              <span className="nav-label">{item.label}</span>
              {item.badge !== undefined && item.badge > 0 && (
                <span className="badge">{item.badge}</span>
              )}
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          <button className="nav-item" onClick={() => setSearchOpen(true)}>
            <Search size={20} />
            <span className="nav-label">Quick Search</span>
            <kbd>Ctrl+K</kbd>
          </button>
        </div>
      </aside>

      <main className="main-content">
        <header className="top-bar">
          <div className="top-bar-left">
            <h2>{navItems.find(n => n.path === location.pathname)?.label || 'CREAM'}</h2>
          </div>
          <div className="top-bar-right">
            <button className="icon-btn" title="Notifications">
              <Bell size={20} />
              {data.appointments.some(a => {
                const now = new Date();
                const reminder = new Date(a.startTime);
                reminder.setMinutes(reminder.getMinutes() - a.reminderMinutes);
                return reminder <= now && a.startTime > now && a.status === 'scheduled';
              }) && <span className="notification-dot" />}
            </button>
          </div>
        </header>

        <div className="page-content">
          <Routes>
            <Route path="/" element={<ContactsPage dataStore={dataStore} data={data} />} />
            <Route path="/calendar" element={<CalendarPage dataStore={dataStore} data={data} />} />
            <Route path="/tasks" element={<TasksPage dataStore={dataStore} data={data} />} />
            <Route path="/projects" element={<ProjectsPage dataStore={dataStore} data={data} />} />
            <Route path="/settings" element={<SettingsPage dataStore={dataStore} data={data} />} />
          </Routes>
        </div>
      </main>

      {searchOpen && (
        <SearchModal 
          dataStore={dataStore} 
          onClose={() => setSearchOpen(false)} 
        />
      )}
    </div>
  );
};

export default App;