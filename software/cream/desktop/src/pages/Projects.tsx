import React, { useState } from 'react';
import { Plus, Edit2, Trash2, Check, Folder, Calendar, Users, Clock, TrendingUp } from 'lucide-react';
import { format } from 'date-fns';
import type { CreamDataStore } from '../shared/src/store';
import type { DatabaseState, Project } from '../shared/src/types';

interface ProjectsPageProps {
  dataStore: CreamDataStore;
  data: DatabaseState;
}

const ProjectsPage: React.FC<ProjectsPageProps> = ({ dataStore, data }) => {
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const filteredProjects = data.projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      project.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' ? true : project.status === filter;
    return matchesSearch && matchesFilter;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return '#4CAF50';
      case 'completed': return '#2196F3';
      case 'on_hold': return '#FF9800';
      case 'cancelled': return '#F44336';
      default: return '#888';
    }
  };

  const getProjectTasks = (projectId: string) => {
    return data.tasks.filter(t => t.linkedProject === projectId);
  };

  const getProjectAppointments = (projectId: string) => {
    return data.appointments.filter(a => a.linkedProject === projectId);
  };

  return (
    <div className="page projects-page">
      <div className="page-header">
        <div className="search-bar">
          <input 
            type="text" 
            placeholder="Search projects..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <button className="btn-primary" onClick={() => setShowAddModal(true)}>
          <Plus size={16} /> New Project
        </button>
      </div>

      <div className="filter-tabs">
        {['all', 'active', 'completed', 'on_hold'].map(f => (
          <button 
            key={f}
            className={`tab ${filter === f ? 'active' : ''}`}
            onClick={() => setFilter(f)}
          >
            {f === 'on_hold' ? 'On Hold' : f.charAt(0).toUpperCase() + f.slice(1)}
            {f === 'all' && `(${data.projects.length})`}
          </button>
        ))}
      </div>

      <div className="projects-grid">
        {filteredProjects.map(project => (
          <div key={project.id} className="project-card">
            <div className="project-header" style={{ borderLeftColor: project.color }}>
              <div className="project-title" onClick={() => setSelectedProject(project)}>
                <Folder size={20} />
                {project.name}
              </div>
              <span className="status-badge" style={{ backgroundColor: getStatusColor(project.status) }}>
                {project.status}
              </span>
            </div>
            
            {project.description && <p className="project-desc">{project.description}</p>}
            
            <div className="project-stats">
              <div className="stat">
                <Check size={14} />
                {getProjectTasks(project.id).filter(t => t.status === 'completed').length}/{getProjectTasks(project.id).length} Tasks
              </div>
              <div className="stat">
                <Calendar size={14} />
                {getProjectAppointments(project.id).length} Events
              </div>
            </div>

            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${project.progress}%`, backgroundColor: project.color }} />
            </div>
            <span className="progress-text">{project.progress}% Complete</span>
            
            <div className="project-actions">
              <button onClick={() => setEditingProject(project)}><Edit2 size={16} /> Edit</button>
              <button onClick={() => dataStore.deleteProject(project.id)}><Trash2 size={16} /> Delete</button>
            </div>
          </div>
        ))}
      </div>

      {showAddModal && (
        <ProjectEditModal
          project={null}
          onClose={() => setShowAddModal(false)}
          onSave={(project) => {
            dataStore.addProject(project);
            setShowAddModal(false);
          }}
        />
      )}

      {editingProject && (
        <ProjectEditModal
          project={editingProject}
          onClose={() => setEditingProject(null)}
          onSave={(updates) => {
            dataStore.updateProject(editingProject.id, updates);
            setEditingProject(null);
          }}
        />
      )}

      {selectedProject && (
        <ProjectDetailModal
          project={selectedProject}
          data={data}
          dataStore={dataStore}
          onClose={() => setSelectedProject(null)}
        />
      )}
    </div>
  );
};

const ProjectEditModal: React.FC<{
  project: Project | null;
  onClose: () => void;
  onSave: (project: any) => void;
}> = ({ project, onClose, onSave }) => {
  const [name, setName] = useState(project?.name || '');
  const [description, setDescription] = useState(project?.description || '');
  const [status, setStatus] = useState(project?.status || 'active');
  const [priority, setPriority] = useState(project?.priority || 'medium');
  const [color, setColor] = useState(project?.color || '#4CAF50');
  const [startDate, setStartDate] = useState(project?.startDate ? format(project.startDate, 'yyyy-MM-dd') : '');
  const [dueDate, setDueDate] = useState(project?.dueDate ? format(project.dueDate, 'yyyy-MM-dd') : '');

  const handleSave = () => {
    onSave({
      name,
      description,
      status,
      priority,
      color,
      startDate: startDate ? new Date(startDate) : undefined,
      dueDate: dueDate ? new Date(dueDate) : undefined,
      progress: project?.progress || 0,
      tasks: project?.tasks || [],
      appointments: project?.appointments || [],
      linkedContacts: project?.linkedContacts || [],
      notes: project?.notes || '',
      tags: project?.tags || [],
    });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h3>{project ? 'Edit Project' : 'New Project'}</h3>
        
        <div className="form-group">
          <label>Name *</label>
          <input value={name} onChange={e => setName(e.target.value)} />
        </div>
        
        <div className="form-group">
          <label>Description</label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} rows={3} />
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label>Status</label>
            <select value={status} onChange={e => setStatus(e.target.value)}>
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="on_hold">On Hold</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Priority</label>
            <select value={priority} onChange={e => setPriority(e.target.value)}>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
        </div>
        
        <div className="form-group">
          <label>Color</label>
          <div className="color-picker">
            {['#F44336', '#E91E63', '#9C27B0', '#673AB7', '#2196F3', '#03A9F4', '#4CAF50', '#FF9800', '#FF5722', '#795548'].map(c => (
              <button
                key={c}
                className={color === c ? 'active' : ''}
                style={{ backgroundColor: c }}
                onClick={() => setColor(c)}
              />
            ))}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Start Date</label>
            <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
          </div>
          
          <div className="form-group">
            <label>Due Date</label>
            <input type="date" value={dueDate} onChange={e => setDueDate(e.target.value)} />
          </div>
        </div>
        
        <div className="modal-actions">
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={handleSave} disabled={!name}>Save</button>
        </div>
      </div>
    </div>
  );
};

const ProjectDetailModal: React.FC<{
  project: Project;
  data: DatabaseState;
  dataStore: CreamDataStore;
  onClose: () => void;
}> = ({ project, data, dataStore, onClose }) => {
  const tasks = data.tasks.filter(t => t.linkedProject === project.id);
  const appointments = data.appointments.filter(a => a.linkedProject === project.id);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal modal-large" onClick={e => e.stopPropagation()}>
        <div className="modal-header" style={{ borderLeft: `4px solid ${project.color}` }>
          <h2>{project.name}</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {project.description && <p>{project.description}</p>}

          <div className="project-progress">
            <div className="progress-bar large">
              <div className="progress-fill" style={{ width: `${project.progress}%`, backgroundColor: project.color }} />
            </div>
            <span>{project.progress}% Complete</span>
          </div>

          <div className="project-sections">
            <div className="project-section">
              <h3><Check size={18} /> Tasks ({tasks.length})</h3>
              {tasks.map(task => (
                <div key={task.id} className={`project-item ${task.status === 'completed' ? 'completed' : ''}`}>
                  <input 
                    type="checkbox" 
                    checked={task.status === 'completed'}
                    onChange={() => {
                      if (task.status === 'completed') {
                        dataStore.updateTask(task.id, { status: 'pending' });
                      } else {
                        dataStore.markTaskComplete(task.id);
                      }
                    }}
                  />
                  {task.title}
                  <span className={`priority ${task.priority}`}>{task.priority}</span>
                </div>
              ))}
            </div>

            <div className="project-section">
              <h3><Calendar size={18} /> Appointments ({appointments.length})</h3>
              {appointments.map(appt => (
                <div key={appt.id} className="project-item">
                  {format(appt.startTime, 'MMM d, h:mm a')} - {appt.title}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectsPage;