// CREAM Data Store - Centralized state management with persistence

import type { Contact, Appointment, Task, Project, Category, Group, DatabaseState, AppSettings, DuplicateContact } from './types.js';
import { v4 as uuidv4 } from 'uuid';
import { format, isSameDay, isSameWeek, isSameMonth, startOfDay, endOfDay, startOfWeek, endOfWeek, startOfMonth, endOfMonth } from 'date-fns';

const DEFAULT_SETTINGS: AppSettings = {
  defaultReminderMinutes: 15,
  defaultTaskPriority: 'medium',
  defaultAppointmentDuration: 60,
  workingHours: { start: '09:00', end: '17:00' },
  weekStartDay: 0,
  theme: 'system',
  language: 'en',
  dateFormat: 'MM/dd/yyyy',
  timeFormat: '12h',
  backupEnabled: true,
  backupInterval: 24,
};

export class CreamDataStore {
  private data: DatabaseState;
  private listeners: Set<(data: DatabaseState) => void>;
  private persistCallback?: (data: DatabaseState) => Promise<void>;

  constructor(initialData?: Partial<DatabaseState>) {
    this.listeners = new Set();
    this.data = {
      contacts: [],
      appointments: [],
      tasks: [],
      projects: [],
      categories: this.getDefaultCategories(),
      groups: [],
      settings: DEFAULT_SETTINGS,
      version: 1,
      ...initialData,
    };
  }

  private getDefaultCategories(): Category[] {
    return [
      { id: 'cat-1', name: 'Personal', color: '#4CAF50', type: 'contact' },
      { id: 'cat-2', name: 'Business', color: '#2196F3', type: 'contact' },
      { id: 'cat-3', name: 'Family', color: '#E91E63', type: 'contact' },
      { id: 'cat-4', name: 'Work', color: '#FF9800', type: 'appointment' },
      { id: 'cat-5', name: 'Personal', color: '#9C27B0', type: 'appointment' },
      { id: 'cat-6', name: 'High', color: '#F44336', type: 'task' },
      { id: 'cat-7', name: 'Medium', color: '#FF9800', type: 'task' },
      { id: 'cat-8', name: 'Low', color: '#4CAF50', type: 'task' },
    ];
  }

  setPersistCallback(callback: (data: DatabaseState) => Promise<void>) {
    this.persistCallback = callback;
  }

  subscribe(listener: (data: DatabaseState) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private notify(): void {
    this.listeners.forEach(listener => listener(this.data));
    this.persistCallback?.(this.data).catch(console.error);
  }

  getState(): DatabaseState {
    return { ...this.data };
  }

  // Contacts
  addContact(contact: Omit<Contact, 'id' | 'createdAt' | 'updatedAt'>): Contact {
    const newContact: Contact = {
      ...contact,
      id: uuidv4(),
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    this.data.contacts.push(newContact);
    this.notify();
    return newContact;
  }

  updateContact(id: string, updates: Partial<Contact>): Contact | null {
    const index = this.data.contacts.findIndex(c => c.id === id);
    if (index === -1) return null;
    this.data.contacts[index] = {
      ...this.data.contacts[index],
      ...updates,
      updatedAt: new Date(),
    };
    this.notify();
    return this.data.contacts[index];
  }

  deleteContact(id: string): boolean {
    const index = this.data.contacts.findIndex(c => c.id === id);
    if (index === -1) return false;
    this.data.contacts.splice(index, 1);
    // Clean up links
    this.data.appointments.forEach(a => {
      a.linkedContacts = a.linkedContacts.filter(cid => cid !== id);
    });
    this.data.tasks.forEach(t => {
      t.linkedContacts = t.linkedContacts.filter(cid => cid !== id);
    });
    this.notify();
    return true;
  }

  getContact(id: string): Contact | undefined {
    return this.data.contacts.find(c => c.id === id);
  }

  getContacts(options?: { category?: string; group?: string; search?: string }): Contact[] {
    let contacts = this.data.contacts;
    if (options?.category) {
      contacts = contacts.filter(c => c.category === options.category);
    }
    if (options?.group) {
      contacts = contacts.filter(c => c.groups.includes(options.group!));
    }
    if (options?.search) {
      const term = options.search.toLowerCase();
      contacts = contacts.filter(c => 
        c.firstName.toLowerCase().includes(term) ||
        c.lastName.toLowerCase().includes(term) ||
        c.emails.some(e => e.value.toLowerCase().includes(term)) ||
        c.phones.some(p => p.value.includes(term))
      );
    }
    return contacts.sort((a, b) => a.lastName.localeCompare(b.lastName));
  }

  findDuplicates(): DuplicateContact[] {
    const duplicates: DuplicateContact[] = [];
    const processed = new Set<string>();

    for (const contact of this.data.contacts) {
      if (processed.has(contact.id)) continue;

      const dups: Contact[] = [];
      for (const other of this.data.contacts) {
        if (other.id === contact.id || processed.has(other.id)) continue;
        
        const score = this.calculateMatchScore(contact, other);
        if (score > 0.7) {
          dups.push(other);
          processed.add(other.id);
        }
      }

      if (dups.length > 0) {
        duplicates.push({ contact, duplicates: dups, matchScore: 1 });
        processed.add(contact.id);
      }
    }

    return duplicates;
  }

  private calculateMatchScore(a: Contact, b: Contact): number {
    let score = 0;
    if (a.firstName.toLowerCase() === b.firstName.toLowerCase()) score += 0.3;
    if (a.lastName.toLowerCase() === b.lastName.toLowerCase()) score += 0.3;
    if (a.emails.some(ea => b.emails.some(eb => ea.value === eb.value))) score += 0.4;
    if (a.phones.some(pa => b.phones.some(pb => pa.value === pb.value))) score += 0.4;
    return score;
  }

  mergeContacts(keepId: string, mergeIds: string[]): Contact | null {
    const keep = this.getContact(keepId);
    if (!keep) return null;

    for (const mergeId of mergeIds) {
      const merge = this.getContact(mergeId);
      if (!merge) continue;

      // Merge fields
      merge.emails.forEach(e => {
        if (!keep.emails.some(ke => ke.value === e.value)) {
          keep.emails.push(e);
        }
      });
      merge.phones.forEach(p => {
        if (!keep.phones.some(kp => kp.value === p.value)) {
          keep.phones.push(p);
        }
      });
      merge.groups.forEach(g => {
        if (!keep.groups.includes(g)) keep.groups.push(g);
      });

      // Add to history
      keep.history.push({
        id: uuidv4(),
        type: 'modified',
        description: `Merged with ${merge.firstName} ${merge.lastName}`,
        timestamp: new Date(),
      });

      this.deleteContact(mergeId);
    }

    keep.updatedAt = new Date();
    this.notify();
    return keep;
  }

  findAndReplaceContacts(field: keyof Contact, find: string, replace: string): number {
    let count = 0;
    this.data.contacts.forEach(c => {
      if (typeof c[field] === 'string' && c[field].includes(find)) {
        (c as any)[field] = c[field].replace(new RegExp(find, 'g'), replace);
        c.updatedAt = new Date();
        count++;
      }
    });
    if (count > 0) this.notify();
    return count;
  }

  // Appointments
  addAppointment(appointment: Omit<Appointment, 'id' | 'createdAt' | 'updatedAt'>): Appointment {
    const newAppt: Appointment = {
      ...appointment,
      id: uuidv4(),
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    this.data.appointments.push(newAppt);
    this.notify();
    return newAppt;
  }

  updateAppointment(id: string, updates: Partial<Appointment>): Appointment | null {
    const index = this.data.appointments.findIndex(a => a.id === id);
    if (index === -1) return null;
    this.data.appointments[index] = {
      ...this.data.appointments[index],
      ...updates,
      updatedAt: new Date(),
    };
    this.notify();
    return this.data.appointments[index];
  }

  deleteAppointment(id: string): boolean {
    const index = this.data.appointments.findIndex(a => a.id === id);
    if (index === -1) return false;
    this.data.appointments.splice(index, 1);
    this.notify();
    return true;
  }

  getAppointments(options?: { startDate?: Date; endDate?: Date; contactId?: string; projectId?: string }): Appointment[] {
    let appts = this.data.appointments;
    if (options?.startDate) {
      appts = appts.filter(a => a.startTime >= options.startDate!);
    }
    if (options?.endDate) {
      appts = appts.filter(a => a.startTime <= options.endDate!);
    }
    if (options?.contactId) {
      appts = appts.filter(a => a.linkedContacts.includes(options.contactId!));
    }
    if (options?.projectId) {
      appts = appts.filter(a => a.linkedProject === options.projectId);
    }
    return appts.sort((a, b) => a.startTime.getTime() - b.startTime.getTime());
  }

  getAppointmentsForDay(date: Date): Appointment[] {
    return this.data.appointments.filter(a => isSameDay(a.startTime, date));
  }

  getAppointmentsForWeek(date: Date): Appointment[] {
    return this.data.appointments.filter(a => isSameWeek(a.startTime, { weekStartsOn: this.data.settings.weekStartDay }));
  }

  getAppointmentsForMonth(date: Date): Appointment[] {
    return this.data.appointments.filter(a => isSameMonth(a.startTime, date));
  }

  // Tasks
  addTask(task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>): Task {
    const newTask: Task = {
      ...task,
      id: uuidv4(),
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    this.data.tasks.push(newTask);
    this.notify();
    return newTask;
  }

  updateTask(id: string, updates: Partial<Task>): Task | null {
    const index = this.data.tasks.findIndex(t => t.id === id);
    if (index === -1) return null;
    this.data.tasks[index] = {
      ...this.data.tasks[index],
      ...updates,
      updatedAt: new Date(),
    };
    this.notify();
    return this.data.tasks[index];
  }

  deleteTask(id: string): boolean {
    const index = this.data.tasks.findIndex(t => t.id === id);
    if (index === -1) return false;
    this.data.tasks.splice(index, 1);
    this.notify();
    return true;
  }

  getTasks(options?: { dueDate?: Date; status?: string; priority?: string; contactId?: string; projectId?: string }): Task[] {
    let tasks = this.data.tasks;
    if (options?.dueDate) {
      tasks = tasks.filter(t => t.dueDate && isSameDay(t.dueDate, options.dueDate!));
    }
    if (options?.status) {
      tasks = tasks.filter(t => t.status === options.status);
    }
    if (options?.priority) {
      tasks = tasks.filter(t => t.priority === options.priority);
    }
    if (options?.contactId) {
      tasks = tasks.filter(t => t.linkedContacts.includes(options.contactId!));
    }
    if (options?.projectId) {
      tasks = tasks.filter(t => t.linkedProject === options.projectId);
    }
    return tasks.sort((a, b) => {
      const priorityOrder = { high: 0, medium: 1, low: 2 };
      if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      }
      if (a.dueDate && b.dueDate) {
        return a.dueDate.getTime() - b.dueDate.getTime();
      }
      return 0;
    });
  }

  markTaskComplete(id: string): Task | null {
    return this.updateTask(id, { status: 'completed', completedAt: new Date() });
  }

  // Projects
  addProject(project: Omit<Project, 'id' | 'createdAt' | 'updatedAt'>): Project {
    const newProject: Project = {
      ...project,
      id: uuidv4(),
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    this.data.projects.push(newProject);
    this.notify();
    return newProject;
  }

  updateProject(id: string, updates: Partial<Project>): Project | null {
    const index = this.data.projects.findIndex(p => p.id === id);
    if (index === -1) return null;
    this.data.projects[index] = {
      ...this.data.projects[index],
      ...updates,
      updatedAt: new Date(),
    };
    this.calculateProjectProgress(id);
    this.notify();
    return this.data.projects[index];
  }

  deleteProject(id: string): boolean {
    const index = this.data.projects.findIndex(p => p.id === id);
    if (index === -1) return false;
    this.data.projects.splice(index, 1);
    this.notify();
    return true;
  }

  getProject(id: string): Project | undefined {
    return this.data.projects.find(p => p.id === id);
  }

  getProjects(options?: { status?: string }): Project[] {
    let projects = this.data.projects;
    if (options?.status) {
      projects = projects.filter(p => p.status === options.status);
    }
    return projects.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
  }

  private calculateProjectProgress(projectId: string): void {
    const project = this.getProject(projectId);
    if (!project) return;

    const tasks = this.getTasks({ projectId });
    if (tasks.length === 0) {
      project.progress = 0;
      return;
    }

    const completed = tasks.filter(t => t.status === 'completed').length;
    project.progress = Math.round((completed / tasks.length) * 100);
  }

  // Search
  search(query: string): { contacts: Contact[]; appointments: Appointment[]; tasks: Task[]; projects: Project[] } {
    const term = query.toLowerCase();
    return {
      contacts: this.data.contacts.filter(c => 
        c.firstName.toLowerCase().includes(term) ||
        c.lastName.toLowerCase().includes(term) ||
        c.emails.some(e => e.value.toLowerCase().includes(term)) ||
        c.notes.toLowerCase().includes(term)
      ),
      appointments: this.data.appointments.filter(a => 
        a.title.toLowerCase().includes(term) ||
        a.description?.toLowerCase().includes(term) ||
        a.location?.toLowerCase().includes(term)
      ),
      tasks: this.data.tasks.filter(t => 
        t.title.toLowerCase().includes(term) ||
        t.description?.toLowerCase().includes(term)
      ),
      projects: this.data.projects.filter(p => 
        p.name.toLowerCase().includes(term) ||
        p.description?.toLowerCase().includes(term)
      ),
    };
  }

  // Import/Export
  exportToJSON(): string {
    return JSON.stringify(this.data, null, 2);
  }

  exportToCSV(type: 'contacts' | 'appointments' | 'tasks' | 'projects'): string {
    switch (type) {
      case 'contacts':
        return this.contactsToCSV();
      case 'appointments':
        return this.appointmentsToCSV();
      case 'tasks':
        return this.tasksToCSV();
      case 'projects':
        return this.projectsToCSV();
    }
  }

  private contactsToCSV(): string {
    const headers = ['ID', 'First Name', 'Last Name', 'Company', 'Job Title', 'Category', 'Notes', 'Created At'];
    const rows = this.data.contacts.map(c => [
      c.id, c.firstName, c.lastName, c.company || '', c.jobTitle || '', c.category, c.notes, c.createdAt.toISOString(),
    ]);
    return [headers.join(','), ...rows.map(r => r.map(v => `"${v}"`).join(','))].join('\n');
  }

  private appointmentsToCSV(): string {
    const headers = ['ID', 'Title', 'Start Time', 'End Time', 'Location', 'Category', 'Status'];
    const rows = this.data.appointments.map(a => [
      a.id, a.title, a.startTime.toISOString(), a.endTime.toISOString(), a.location || '', a.category, a.status,
    ]);
    return [headers.join(','), ...rows.map(r => r.map(v => `"${v}"`).join(','))].join('\n');
  }

  private tasksToCSV(): string {
    const headers = ['ID', 'Title', 'Due Date', 'Priority', 'Status', 'Category'];
    const rows = this.data.tasks.map(t => [
      t.id, t.title, t.dueDate?.toISOString() || '', t.priority, t.status, t.category,
    ]);
    return [headers.join(','), ...rows.map(r => r.map(v => `"${v}"`).join(','))].join('\n');
  }

  private projectsToCSV(): string {
    const headers = ['ID', 'Name', 'Description', 'Status', 'Progress', 'Created At'];
    const rows = this.data.projects.map(p => [
      p.id, p.name, p.description || '', p.status, p.progress.toString(), p.createdAt.toISOString(),
    ]);
    return [headers.join(','), ...rows.map(r => r.map(v => `"${v}"`).join(','))].join('\n');
  }

  importFromJSON(json: string): boolean {
    try {
      const data = JSON.parse(json) as DatabaseState;
      this.data = {
        ...data,
        contacts: data.contacts.map(c => ({ ...c, createdAt: new Date(c.createdAt), updatedAt: new Date(c.updatedAt) })),
        appointments: data.appointments.map(a => ({ ...a, startTime: new Date(a.startTime), endTime: new Date(a.endTime), createdAt: new Date(a.createdAt), updatedAt: new Date(a.updatedAt) })),
        tasks: data.tasks.map(t => ({ ...t, dueDate: t.dueDate ? new Date(t.dueDate) : undefined, createdAt: new Date(t.createdAt), updatedAt: new Date(t.updatedAt) })),
        projects: data.projects.map(p => ({ ...p, createdAt: new Date(p.createdAt), updatedAt: new Date(p.updatedAt) })),
      };
      this.notify();
      return true;
    } catch (e) {
      console.error('Import failed:', e);
      return false;
    }
  }

  // Settings
  updateSettings(settings: Partial<AppSettings>): void {
    this.data.settings = { ...this.data.settings, ...settings };
    this.notify();
  }

  getSettings(): AppSettings {
    return { ...this.data.settings };
  }

  // Archive old data
  archiveOldData(beforeDate: Date): { appointments: number; tasks: number } {
    let apptCount = 0;
    let taskCount = 0;

    this.data.appointments = this.data.appointments.filter(a => {
      if (a.endTime < beforeDate && a.status === 'completed') {
        apptCount++;
        return false;
      }
      return true;
    });

    this.data.tasks = this.data.tasks.filter(t => {
      if (t.dueDate && t.dueDate < beforeDate && t.status === 'completed') {
        taskCount++;
        return false;
      }
      return true;
    });

    if (apptCount > 0 || taskCount > 0) this.notify();
    return { appointments: apptCount, tasks: taskCount };
  }

  // Statistics
  getStatistics(): { totalContacts: number; totalAppointments: number; totalTasks: number; completedTasks: number; activeProjects: number } {
    return {
      totalContacts: this.data.contacts.length,
      totalAppointments: this.data.appointments.length,
      totalTasks: this.data.tasks.length,
      completedTasks: this.data.tasks.filter(t => t.status === 'completed').length,
      activeProjects: this.data.projects.filter(p => p.status === 'active').length,
    };
  }
}

export default CreamDataStore;