// Core Types for CREAM PIM (Time & Chaos Clone)

export interface Contact {
  id: string;
  firstName: string;
  lastName: string;
  company?: string;
  jobTitle?: string;
  emails: EmailField[];
  phones: PhoneField[];
  addresses: AddressField[];
  websites: string[];
  customFields: CustomField[];
  notes: string;
  category: string;
  groups: string[];
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
  lastContactedAt?: Date;
  birthDate?: Date;
  anniversaryDate?: Date;
  linkedAppointments: string[];
  linkedTasks: string[];
  linkedProjects: string[];
  history: ContactHistory[];
}

export interface EmailField {
  id: string;
  label: string;
  value: string;
  isPrimary: boolean;
}

export interface PhoneField {
  id: string;
  label: string;
  value: string;
  isPrimary: boolean;
}

export interface AddressField {
  id: string;
  label: string;
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
  isPrimary: boolean;
}

export interface CustomField {
  id: string;
  label: string;
  value: string;
  type: 'text' | 'number' | 'date' | 'boolean' | 'select';
}

export interface ContactHistory {
  id: string;
  type: 'created' | 'modified' | 'email' | 'call' | 'meeting' | 'note';
  description: string;
  timestamp: Date;
  userId?: string;
}

export interface Appointment {
  id: string;
  title: string;
  description?: string;
  location?: string;
  startTime: Date;
  endTime: Date;
  isAllDay: boolean;
  isRecurring: boolean;
  recurrencePattern?: RecurrencePattern;
  color: string;
  category: string;
  priority: 'low' | 'medium' | 'high';
  status: 'scheduled' | 'completed' | 'cancelled' | 'postponed';
  reminderMinutes: number;
  reminders: Reminder[];
  linkedContacts: string[];
  linkedTasks: string[];
  linkedProject?: string;
  notes: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface RecurrencePattern {
  frequency: 'daily' | 'weekly' | 'monthly' | 'yearly';
  interval: number;
  daysOfWeek?: number[];
  dayOfMonth?: number;
  monthOfYear?: number;
  endDate?: Date;
  occurrences?: number;
}

export interface Reminder {
  id: string;
  minutesBefore: number;
  method: 'popup' | 'email' | 'sms';
  triggered: boolean;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  dueDate?: Date;
  completedAt?: Date;
  priority: 'low' | 'medium' | 'high';
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  isRecurring: boolean;
  recurrencePattern?: RecurrencePattern;
  category: string;
  tags: string[];
  linkedContacts: string[];
  linkedAppointments: string[];
  linkedProject?: string;
  estimatedDuration?: number;
  actualDuration?: number;
  reminderMinutes?: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  color: string;
  status: 'active' | 'completed' | 'cancelled' | 'on_hold';
  priority: 'low' | 'medium' | 'high';
  startDate?: Date;
  dueDate?: Date;
  completedAt?: Date;
  progress: number;
  tasks: string[];
  appointments: string[];
  linkedContacts: string[];
  notes: string;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface Category {
  id: string;
  name: string;
  color: string;
  icon?: string;
  type: 'contact' | 'appointment' | 'task' | 'project';
}

export interface Group {
  id: string;
  name: string;
  description?: string;
  memberIds: string[];
  createdAt: Date;
}

export interface DatabaseState {
  contacts: Contact[];
  appointments: Appointment[];
  tasks: Task[];
  projects: Project[];
  categories: Category[];
  groups: Group[];
  settings: AppSettings;
  version: number;
}

export interface AppSettings {
  defaultReminderMinutes: number;
  defaultTaskPriority: 'low' | 'medium' | 'high';
  defaultAppointmentDuration: number;
  workingHours: {
    start: string;
    end: string;
  };
  weekStartDay: number;
  theme: 'light' | 'dark' | 'system';
  language: string;
  dateFormat: string;
  timeFormat: '12h' | '24h';
  backupEnabled: boolean;
  backupInterval: number;
  backupLocation?: string;
  lastBackupAt?: Date;
}

export type ViewMode = 'day' | 'week' | 'month' | 'agenda';

export interface CalendarEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  allDay: boolean;
  color: string;
  type: 'appointment' | 'task';
  data: Appointment | Task;
}

export interface SearchResult {
  type: 'contact' | 'appointment' | 'task' | 'project';
  item: Contact | Appointment | Task | Project;
  score: number;
}

export interface ImportExportOptions {
  format: 'csv' | 'json' | 'vcard' | 'ical';
  dateRange?: { start: Date; end: Date };
  categories?: string[];
  includeArchived?: boolean;
}

export interface DuplicateContact {
  contact: Contact;
  duplicates: Contact[];
  matchScore: number;
}

export interface BackupInfo {
  id: string;
  name: string;
  createdAt: Date;
  size: number;
  type: 'auto' | 'manual';
}