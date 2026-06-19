import React, { useState } from 'react';
import { Plus, Edit2, Trash2, Check, Calendar, Clock, AlertCircle } from 'lucide-react';
import { format, isToday, isPast, addDays } from 'date-fns';
import type { CreamDataStore } from '../shared/src/store';
import type { DatabaseState, Task } from '../shared/src/types';

interface TasksPageProps {
  dataStore: CreamDataStore;
  data: DatabaseState;
}

const TasksPage: React.FC<TasksPageProps> = ({ dataStore, data }) => {
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);

  const filteredTasks = data.tasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = 
      filter === 'all' ? true :
      filter === 'pending' ? task.status !== 'completed' :
      filter === 'completed' ? task.status === 'completed' :
      filter === 'high' ? task.priority === 'high' :
      filter === 'overdue' ? task.dueDate && isPast(task.dueDate) && task.status !== 'completed' :
      true;
    return matchesSearch && matchesFilter;
  });

  const sortedTasks = [...filteredTasks].sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    if (a.dueDate && b.dueDate) return a.dueDate.getTime() - b.dueDate.getTime();
    return 0;
  });

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return '#F44336';
      case 'medium': return '#FF9800';
      case 'low': return '#4CAF50';
      default: return '#888';
    }
  };

  const getStatusIcon = (task: Task) => {
    if (task.status === 'completed') return <Check size={18} color="#4CAF50" />;
    if (task.dueDate && isPast(task.dueDate)) return <AlertCircle size={18} color="#F44336" />;
    if (task.priority === 'high') return <AlertCircle size={18} color="#F44336" />;
    return <Clock size={18} color="#888" />;
  };

  return (
    <div className="page tasks-page">
      <div className="page-header">
        <div className="search-bar">
          <input 
            type="text" 
            placeholder="Search tasks..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <button className="btn-primary" onClick={() => setShowAddModal(true)}>
          <Plus size={16} /> Add Task
        </button>
      </div>

      <div className="filter-tabs">
        {['all', 'pending', 'completed', 'high', 'overdue'].map(f => (
          <button 
            key={f}
            className={`tab ${filter === f ? 'active' : ''}`}
            onClick={() => setFilter(f)}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)} 
            {f === 'all' && `(${data.tasks.length})`}
            {f === 'pending' && `(${data.tasks.filter(t => t.status !== 'completed').length})`}
            {f === 'completed' && `(${data.tasks.filter(t => t.status === 'completed').length})`}
          </button>
        ))}
      </div>

      <div className="tasks-list">
        {sortedTasks.map(task => (
          <div 
            key={task.id} 
            className={`task-item ${task.status === 'completed' ? 'completed' : ''}`}
          >
            <div className="task-checkbox">
              <input 
                type="checkbox" 
                checked={task.status === 'completed'}
                onChange={() => {
                  if (task.status === 'completed') {
                    dataStore.updateTask(task.id, { status: 'pending', completedAt: undefined });
                  } else {
                    dataStore.markTaskComplete(task.id);
                  }
                }}
              />
            </div>
            
            <div className="task-content">
              <div className="task-title" onClick={() => setEditingTask(task)}>
                {task.title}
              </div>
              
              {task.description && <div className="task-desc">{task.description}</div>}
              
              <div className="task-meta">
                <span className="priority-badge" style={{ backgroundColor: getPriorityColor(task.priority) }}>
                  {task.priority}
                </span>
                {task.dueDate && (
                  <span className={`due-date ${isPast(task.dueDate) && task.status !== 'completed' ? 'overdue' : ''}`}>
                    <Calendar size={12} />
                    {isToday(task.dueDate) ? 'Today' : format(task.dueDate, 'MMM d')}
                  </span>
                )}
                {task.linkedProject && (
                  <span className="linked-project">
                    Project: {data.projects.find(p => p.id === task.linkedProject)?.name}
                  </span>
                )}
              </div>
            </div>
            
            <div className="task-actions">
              {getStatusIcon(task)}
              <button onClick={() => setEditingTask(task)}><Edit2 size={16} /></button>
              <button onClick={() => dataStore.deleteTask(task.id)}><Trash2 size={16} /></button>
            </div>
          </div>
        ))}
      </div>

      {showAddModal && (
        <TaskEditModal
          task={null}
          data={data}
          onClose={() => setShowAddModal(false)}
          onSave={(task) => {
            dataStore.addTask(task);
            setShowAddModal(false);
          }}
        />
      )}

      {editingTask && (
        <TaskEditModal
          task={editingTask}
          data={data}
          onClose={() => setEditingTask(null)}
          onSave={(updates) => {
            dataStore.updateTask(editingTask.id, updates);
            setEditingTask(null);
          }}
        />
      )}
    </div>
  );
};

const TaskEditModal: React.FC<{
  task: Task | null;
  data: DatabaseState;
  onClose: () => void;
  onSave: (task: any) => void;
}> = ({ task, data, onClose, onSave }) => {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [priority, setPriority] = useState(task?.priority || 'medium');
  const [dueDate, setDueDate] = useState(task?.dueDate ? format(task.dueDate, 'yyyy-MM-dd') : '');
  const [linkedProject, setLinkedProject] = useState(task?.linkedProject || '');
  const [isRecurring, setIsRecurring] = useState(task?.isRecurring || false);

  const handleSave = () => {
    onSave({
      title,
      description,
      priority,
      dueDate: dueDate ? new Date(dueDate) : undefined,
      linkedProject: linkedProject || undefined,
      isRecurring,
      category: 'General',
      tags: [],
      linkedContacts: task?.linkedContacts || [],
      linkedAppointments: task?.linkedAppointments || [],
      status: task?.status || 'pending',
    });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h3>{task ? 'Edit Task' : 'New Task'}</h3>
        
        <div className="form-group">
          <label>Title *</label>
          <input value={title} onChange={e => setTitle(e.target.value)} />
        </div>
        
        <div className="form-group">
          <label>Description</label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} rows={3} />
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label>Priority</label>
            <select value={priority} onChange={e => setPriority(e.target.value)}>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Due Date</label>
            <input type="date" value={dueDate} onChange={e => setDueDate(e.target.value)} />
          </div>
        </div>
        
        <div className="form-group">
          <label>Project</label>
          <select value={linkedProject} onChange={e => setLinkedProject(e.target.value)}>
            <option value="">None</option>
            {data.projects.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>

        <div className="form-group checkbox">
          <label>
            <input type="checkbox" checked={isRecurring} onChange={e => setIsRecurring(e.target.checked)} />
            Recurring Task
          </label>
        </div>
        
        <div className="modal-actions">
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={handleSave} disabled={!title}>Save</button>
        </div>
      </div>
    </div>
  );
};

export default TasksPage;