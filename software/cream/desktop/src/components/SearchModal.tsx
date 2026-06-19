import React, { useState, useMemo } from 'react';
import { Search, X, User, Calendar, CheckSquare, Folder } from 'lucide-react';
import type { CreamDataStore } from '../shared/src/store';
import type { Contact, Appointment, Task, Project } from '../shared/src/types';

interface SearchModalProps {
  dataStore: CreamDataStore;
  onClose: () => void;
}

const SearchModal: React.FC<SearchModalProps> = ({ dataStore, onClose }) => {
  const [query, setQuery] = useState('');

  const results = useMemo(() => {
    if (!query.trim()) return { contacts: [], appointments: [], tasks: [], projects: [] };
    return dataStore.search(query);
  }, [query, dataStore]);

  const totalResults = results.contacts.length + results.appointments.length + results.tasks.length + results.projects.length;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="search-modal" onClick={e => e.stopPropagation()}>
        <div className="search-header">
          <Search size={20} />
          <input
            type="text"
            placeholder="Search contacts, appointments, tasks, projects..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
          />
          <button className="close-btn" onClick={onClose}><X size={20} /></button>
        </div>

        {query && (
          <div className="search-results">
            {totalResults === 0 ? (
              <div className="no-results">No results found for "{query}"</div>
            ) : (
              <>
                {results.contacts.length > 0 && (
                  <div className="result-section">
                    <div className="result-header">
                      <User size={16} /> Contacts ({results.contacts.length})
                    </div>
                    {results.contacts.map(contact => (
                      <div key={contact.id} className="result-item">
                        <div className="result-title">{contact.firstName} {contact.lastName}</div>
                        {contact.emails[0] && <div className="result-meta">{contact.emails[0].value}</div>}
                      </div>
                    ))}
                  </div>
                )}

                {results.appointments.length > 0 && (
                  <div className="result-section">
                    <div className="result-header">
                      <Calendar size={16} /> Appointments ({results.appointments.length})
                    </div>
                    {results.appointments.map(appt => (
                      <div key={appt.id} className="result-item">
                        <div className="result-title">{appt.title}</div>
                        <div className="result-meta">{new Date(appt.startTime).toLocaleDateString()}</div>
                      </div>
                    ))}
                  </div>
                )}

                {results.tasks.length > 0 && (
                  <div className="result-section">
                    <div className="result-header">
                      <CheckSquare size={16} /> Tasks ({results.tasks.length})
                    </div>
                    {results.tasks.map(task => (
                      <div key={task.id} className="result-item">
                        <div className="result-title">{task.title}</div>
                        <div className="result-meta">{task.status} · {task.priority} priority</div>
                      </div>
                    ))}
                  </div>
                )}

                {results.projects.length > 0 && (
                  <div className="result-section">
                    <div className="result-header">
                      <Folder size={16} /> Projects ({results.projects.length})
                    </div>
                    {results.projects.map(project => (
                      <div key={project.id} className="result-item">
                        <div className="result-title">{project.name}</div>
                        <div className="result-meta">{project.status} · {project.progress}% complete</div>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        )}

        <div className="search-footer">
          <kbd>↑↓</kbd> navigate · <kbd>↵</kbd> select · <kbd>Esc</kbd> close
        </div>
      </div>
    </div>
  );
};

export default SearchModal;