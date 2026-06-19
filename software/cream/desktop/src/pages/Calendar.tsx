import React, { useState, useMemo } from 'react';
import { 
  format, addDays, startOfMonth, endOfMonth, startOfWeek, endOfWeek, 
  eachDayOfInterval, isSameMonth, isSameDay, addMonths, subMonths 
} from 'date-fns';
import { ChevronLeft, ChevronRight, Clock, MapPin, Users } from 'lucide-react';
import type { CreamDataStore } from '../shared/src/store';
import type { DatabaseState, Appointment, ViewMode } from '../shared/src/types';

interface CalendarPageProps {
  dataStore: CreamDataStore;
  data: DatabaseState;
}

const CalendarPage: React.FC<CalendarPageProps> = ({ dataStore, data }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [viewMode, setViewMode] = useState<ViewMode>('month');
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);

  const appointments = useMemo(() => {
    switch (viewMode) {
      case 'day':
        return dataStore.getAppointmentsForDay(currentDate);
      case 'week':
        return dataStore.getAppointmentsForWeek(currentDate);
      case 'month':
        return dataStore.getAppointmentsForMonth(currentDate);
      default:
        return data.appointments;
    }
  }, [data, currentDate, viewMode]);

  const navigateDate = (direction: 'prev' | 'next') => {
    if (direction === 'prev') {
      setCurrentDate(viewMode === 'month' ? subMonths(currentDate, 1) : addDays(currentDate, viewMode === 'week' ? -7 : -1));
    } else {
      setCurrentDate(viewMode === 'month' ? addMonths(currentDate, 1) : addDays(currentDate, viewMode === 'week' ? 7 : 1));
    }
  };

  const goToToday = () => setCurrentDate(new Date());

  const getAppointmentColor = (appt: Appointment) => {
    const category = data.categories.find(c => c.name === appt.category && c.type === 'appointment');
    return appt.color || category?.color || '#2196F3';
  };

  const renderMonthView = () => {
    const monthStart = startOfMonth(currentDate);
    const monthEnd = endOfMonth(monthStart);
    const calendarStart = startOfWeek(monthStart);
    const calendarEnd = endOfWeek(monthEnd);
    const days = eachDayOfInterval({ start: calendarStart, end: calendarEnd });

    return (
      <div className="calendar-grid">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} className="calendar-header-cell">{day}</div>
        ))}
        {days.map(day => {
          const dayAppointments = dataStore.getAppointmentsForDay(day);
          const isCurrentMonth = isSameMonth(day, currentDate);
          const isToday = isSameDay(day, new Date());
          
          return (
            <div 
              key={day.toISOString()} 
              className={`calendar-cell ${!isCurrentMonth ? 'other-month' : ''} ${isToday ? 'today' : ''}`}
              onClick={() => setCurrentDate(day)}
            >
              <span className="day-number">{format(day, 'd')}</span>
              <div className="day-appointments">
                {dayAppointments.slice(0, 3).map(appt => (
                  <div 
                    key={appt.id}
                    className="mini-appointment"
                    style={{ backgroundColor: getAppointmentColor(appt) }}
                    onClick={(e) => { e.stopPropagation(); setSelectedAppointment(appt); }}
                  >
                    {appt.title}
                  </div>
                ))}
                {dayAppointments.length > 3 && (
                  <div className="more-appointments">+{dayAppointments.length - 3} more</div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  const renderWeekView = () => {
    const weekStart = startOfWeek(currentDate);
    const days = eachDayOfInterval({ start: weekStart, end: endOfWeek(currentDate) });

    return (
      <div className="week-view">
        {days.map(day => {
          const dayAppointments = dataStore.getAppointmentsForDay(day);
          return (
            <div key={day.toISOString()} className={`week-column ${isSameDay(day, new Date()) ? 'today' : ''}`}>
              <div className="week-header">
                <div className="day-name">{format(day, 'EEE')}</div>
                <div className="day-number">{format(day, 'd')}</div>
              </div>
              <div className="week-events">
                {dayAppointments.map(appt => (
                  <div 
                    key={appt.id}
                    className="week-appointment"
                    style={{ 
                      backgroundColor: getAppointmentColor(appt),
                      top: `${(appt.startTime.getHours() - 8) * 60 + appt.startTime.getMinutes()}px`,
                      height: `${(appt.endTime.getTime() - appt.startTime.getTime()) / 60000}px`,
                    }}
                    onClick={() => setSelectedAppointment(appt)}
                  >
                    <div className="event-time">{format(appt.startTime, 'h:mm a')}</div>
                    <div className="event-title">{appt.title}</div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  const renderDayView = () => {
    const hours = Array.from({ length: 14 }, (_, i) => i + 8);
    
    return (
      <div className="day-view">
        <div className="day-header">
          <h3>{format(currentDate, 'EEEE, MMMM d, yyyy')}</h3>
        </div>
        <div className="day-grid">
          <div className="time-column">
            {hours.map(hour => (
              <div key={hour} className="time-slot">
                {format(new Date().setHours(hour, 0, 0, 0), 'h:mm a')}
              </div>
            ))}
          </div>
          
          <div className="events-column">
            {appointments.map(appt => (
              <div 
                key={appt.id}
                className="day-appointment"
                style={{ 
                  backgroundColor: getAppointmentColor(appt),
                  top: `${(appt.startTime.getHours() - 8) * 60 + appt.startTime.getMinutes()}px`,
                  height: `${(appt.endTime.getTime() - appt.startTime.getTime()) / 60000}px`,
                }}
                onClick={() => setSelectedAppointment(appt)}
              >
                <div className="event-title">{appt.title}</div>
                <div className="event-time">{format(appt.startTime, 'h:mm a')} - {format(appt.endTime, 'h:mm a')}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="page calendar-page">
      <div className="page-header">
        <div className="calendar-nav">
          <button onClick={() => navigateDate('prev')}><ChevronLeft /></button>
          <h2>{format(currentDate, viewMode === 'month' ? 'MMMM yyyy' : 'MMMM d, yyyy')}</h2>
          <button onClick={() => navigateDate('next')}><ChevronRight /></button>
          <button className="btn-secondary" onClick={goToToday}>Today</button>
        </div>

        <div className="view-toggle">
          {(['month', 'week', 'day'] as ViewMode[]).map(mode => (
            <button 
              key={mode}
              className={viewMode === mode ? 'active' : ''}
              onClick={() => setViewMode(mode)}
            >
              {mode.charAt(0).toUpperCase() + mode.slice(1)}
            </button>
          ))}
        </div>

        <button className="btn-primary" onClick={() => setShowAddModal(true)}>
          + New Appointment
        </button>
      </div>

      <div className="calendar-content">
        {viewMode === 'month' && renderMonthView()}
        {viewMode === 'week' && renderWeekView()}
        {viewMode === 'day' && renderDayView()}
      </div>

      {selectedAppointment && (
        <AppointmentDetailModal 
          appointment={selectedAppointment}
          data={data}
          onClose={() => setSelectedAppointment(null)}
          onDelete={() => {
            dataStore.deleteAppointment(selectedAppointment.id);
            setSelectedAppointment(null);
          }}
          onEdit={(updates) => {
            dataStore.updateAppointment(selectedAppointment.id, updates);
            setSelectedAppointment(null);
          }}
        />
      )}

      {showAddModal && (
        <AddAppointmentModal
          data={data}
          initialDate={currentDate}
          onClose={() => setShowAddModal(false)}
          onSave={(appt) => {
            dataStore.addAppointment(appt);
            setShowAddModal(false);
          }}
        />
      )}
    </div>
  );
};

const AppointmentDetailModal: React.FC<{
  appointment: Appointment;
  data: DatabaseState;
  onClose: () => void;
  onDelete: () => void;
  onEdit: (updates: Partial<Appointment>) => void;
}> = ({ appointment, data, onClose, onDelete, onEdit }) => (
  <div className="modal-overlay" onClick={onClose}>
    <div className="modal" onClick={e => e.stopPropagation()}>
      <div className="modal-header" style={{ borderLeft: `4px solid ${appointment.color || '#2196F3'}` }>
        <h3>{appointment.title}</h3>
        <button className="close-btn" onClick={onClose}>×</button>
      </div>
      
      <div className="modal-body">
        <div className="detail-row">
          <Clock size={18} />
          <span>{format(appointment.startTime, 'EEEE, MMMM d')} · {format(appointment.startTime, 'h:mm a')} - {format(appointment.endTime, 'h:mm a')}</span>
        </div>
        
        {appointment.location && (
          <div className="detail-row">
            <MapPin size={18} />
            <span>{appointment.location}</span>
          </div>
        )}
        
        {appointment.linkedContacts.length > 0 && (
          <div className="detail-row">
            <Users size={18} />
            <span>
              {appointment.linkedContacts.map(id => {
                const c = data.contacts.find(x => x.id === id);
                return c ? `${c.firstName} ${c.lastName}` : id;
              }).join(', ')}
            </span>
          </div>
        )}
        
        {appointment.notes && (
          <div className="detail-section">
            <h4>Notes</h4>
            <p>{appointment.notes}</p>
          </div>
        )}
      </div>
      
      <div className="modal-footer">
        <button className="btn-danger" onClick={onDelete}>Delete</button>
        <button className="btn-primary" onClick={() => onEdit({ status: 'completed' })}>Mark Complete</button>
      </div>
    </div>
  </div>
);

const AddAppointmentModal: React.FC<{
  data: DatabaseState;
  initialDate: Date;
  onClose: () => void;
  onSave: (appt: Omit<Appointment, 'id' | 'createdAt' | 'updatedAt'>) => void;
}> = ({ data, initialDate, onClose, onSave }) => {
  const [title, setTitle] = useState('');
  const [startTime, setStartTime] = useState(initialDate);
  const [duration, setDuration] = useState(60);
  const [location, setLocation] = useState('');
  const [notes, setNotes] = useState('');
  const [selectedContacts, setSelectedContacts] = useState<string[]>([]);
  const [color, setColor] = useState('#2196F3');

  const handleSave = () => {
    const endTime = new Date(startTime.getTime() + duration * 60000);
    onSave({
      title,
      startTime,
      endTime,
      location,
      notes,
      isAllDay: false,
      isRecurring: false,
      color,
      category: 'Work',
      priority: 'medium',
      status: 'scheduled',
      reminderMinutes: 15,
      reminders: [],
      linkedContacts: selectedContacts,
      linkedTasks: [],
    });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h3>New Appointment</h3>
        
        <div className="form-group">
          <label>Title *</label>
          <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Meeting title" />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Start Time</label>
            <input 
              type="datetime-local" 
              value={format(startTime, "yyyy-MM-dd'T'HH:mm")}
              onChange={e => setStartTime(new Date(e.target.value))}
            />
          </div>
          <div className="form-group">
            <label>Duration (min)</label>
            <input type="number" value={duration} onChange={e => setDuration(parseInt(e.target.value))} />
          </div>
        </div>

        <div className="form-group">
          <label>Location</label>
          <input value={location} onChange={e => setLocation(e.target.value)} placeholder="Add location" />
        </div>

        <div className="form-group">
          <label>Color</label>
          <div className="color-picker">
            {['#F44336', '#E91E63', '#9C27B0', '#673AB7', '#2196F3', '#03A9F4', '#4CAF50', '#FF9800'].map(c => (
              <button
                key={c}
                className={color === c ? 'active' : ''}
                style={{ backgroundColor: c }}
                onClick={() => setColor(c)}
              />
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Notes</label>
          <textarea value={notes} onChange={e => setNotes(e.target.value)} rows={3} />
        </div>

        <div className="modal-actions">
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={handleSave} disabled={!title}>Save</button>
        </div>
      </div>
    </div>
  );
};

export default CalendarPage;