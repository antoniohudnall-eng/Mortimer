import React, { useState } from 'react';
import type { CreamDataStore } from '../shared/src/store';
import type { DatabaseState, Contact } from '../shared/src/types';
import { Plus, Edit2, Trash2, User, Mail, Phone, MoreHorizontal, Merge, Users } from 'lucide-react';

interface ContactsPageProps {
  dataStore: CreamDataStore;
  data: DatabaseState;
}

const ContactsPage: React.FC<ContactsPageProps> = ({ dataStore, data }) => {
  const [selectedContact, setSelectedContact] = useState<Contact | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState('all');
  const [showDuplicateFinder, setShowDuplicateFinder] = useState(false);

  const filteredContacts = data.contacts.filter(c => {
    const matchesSearch = `${c.firstName} ${c.lastName}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.emails.some(e => e.value.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesTab = activeTab === 'all' || c.category === activeTab;
    return matchesSearch && matchesTab;
  });

  const categories = [...new Set(data.contacts.map(c => c.category))];

  const handleAddContact = () => {
    const newContact = dataStore.addContact({
      firstName: 'New',
      lastName: 'Contact',
      emails: [],
      phones: [],
      addresses: [],
      websites: [],
      customFields: [],
      notes: '',
      category: 'Personal',
      groups: [],
      tags: [],
      linkedAppointments: [],
      linkedTasks: [],
      linkedProjects: [],
      history: [],
    });
    setSelectedContact(newContact);
    setIsEditing(true);
  };

  const handleDelete = (id: string) => {
    dataStore.deleteContact(id);
    setSelectedContact(null);
  };

  const duplicates = dataStore.findDuplicates();

  return (
    <div className="page contacts-page">
      <div className="page-header">
        <div className="search-bar">
          <input 
            type="text" 
            placeholder="Search contacts..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="page-actions">
          <button className="btn-secondary" onClick={() => setShowDuplicateFinder(true)}>
            <Merge size={16} /> Duplicates
          </button>
          <button className="btn-primary" onClick={handleAddContact}>
            <Plus size={16} /> Add Contact
          </button>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'all' ? 'active' : ''}`}
          onClick={() => setActiveTab('all')}
        >
          All Contacts ({data.contacts.length})
        </button>
        {categories.map(cat => (
          <button 
            key={cat}
            className={`tab ${activeTab === cat ? 'active' : ''}`}
            onClick={() => setActiveTab(cat)}
          >
            {cat} ({data.contacts.filter(c => c.category === cat).length})
          </button>
        ))}
      </div>

      <div className="content-split">
        <div className="list-pane">
          {filteredContacts.map(contact => (
            <div 
              key={contact.id}
              className={`list-item ${selectedContact?.id === contact.id ? 'selected' : ''}`}
              onClick={() => { setSelectedContact(contact); setIsEditing(false); }}
            >
              <div className="contact-avatar">
                {contact.firstName[0]}{contact.lastName[0]}
              </div>
              <div className="contact-info">
                <div className="contact-name">{contact.firstName} {contact.lastName}</div>
                <div className="contact-meta">
                  {contact.emails[0]?.value && <span><Mail size={12} /> {contact.emails[0].value}</span>}
                  {contact.phones[0]?.value && <span><Phone size={12} /> {contact.phones[0].value}</span>}
                </div>
              </div>
              <span className="category-badge" style={{ background: data.categories.find(c => c.name === contact.category)?.color || '#888' }}>
                {contact.category}
              </span>
            </div>
          ))}
        </div>

        <div className="detail-pane">
          {selectedContact ? (
            <div className="contact-detail">
              {isEditing ? (
                <ContactEditForm 
                  contact={selectedContact}
                  dataStore={dataStore}
                  onCancel={() => setIsEditing(false)}
                  onSave={(updated) => {
                    dataStore.updateContact(selectedContact.id, updated);
                    setIsEditing(false);
                  }}
                />
              ) : (
                <>
                  <div className="detail-header">
                    <div className="contact-avatar large">
                      {selectedContact.firstName[0]}{selectedContact.lastName[0]}
                    </div>
                    <div className="detail-actions">
                      <button onClick={() => setIsEditing(true)}><Edit2 size={16} /></button>
                      <button onClick={() => handleDelete(selectedContact.id)}><Trash2 size={16} /></button>
                    </div>
                  </div>

                  <h2>{selectedContact.firstName} {selectedContact.lastName}</h2>
                  
                  {selectedContact.company && <p className="subtitle">{selectedContact.jobTitle} at {selectedContact.company}</p>}

                  <div className="contact-section">
                    <h3>Contact Info</h3>
                    {selectedContact.emails.map(e => (
                      <div key={e.id} className="info-row">
                        <span className="label">{e.label}</span>
                        <a href={`mailto:${e.value}`}>{e.value}</a>
                      </div>
                    ))}
                    {selectedContact.phones.map(p => (
                      <div key={p.id} className="info-row">
                        <span className="label">{p.label}</span>
                        <a href={`tel:${p.value}`}>{p.value}</a>
                      </div>
                    ))}
                  </div>

                  {selectedContact.linkedAppointments.length > 0 && (
                    <div className="contact-section">
                      <h3>Linked Appointments ({selectedContact.linkedAppointments.length})</h3>
                    </div>
                  )}

                  {selectedContact.linkedTasks.length > 0 && (
                    <div className="contact-section">
                      <h3>Linked Tasks ({selectedContact.linkedTasks.length})</h3>
                    </div>
                  )}

                  {selectedContact.notes && (
                    <div className="contact-section">
                      <h3>Notes</h3>
                      <p>{selectedContact.notes}</p>
                    </div>
                  )}
                </>
              )}
            </div>
          ) : (
            <div className="empty-state">
              <User size={48} />
              <p>Select a contact to view details</p>
            </div>
          )}
        </div>
      </div>

      {showDuplicateFinder && (
        <DuplicateFinderModal 
          duplicates={duplicates}
          dataStore={dataStore}
          onClose={() => setShowDuplicateFinder(false)}
        />
      )}
    </div>
  );
};

const ContactEditForm: React.FC<{
  contact: Contact;
  dataStore: CreamDataStore;
  onCancel: () => void;
  onSave: (contact: Partial<Contact>) => void;
}> = ({ contact, onCancel, onSave }) => {
  const [formData, setFormData] = useState(contact);

  return (
    <div className="contact-form">
      <div className="form-group">
        <label>First Name</label>
        <input 
          value={formData.firstName}
          onChange={e => setFormData({ ...formData, firstName: e.target.value })}
        />
      </div>
      <div className="form-group">
        <label>Last Name</label>
        <input 
          value={formData.lastName}
          onChange={e => setFormData({ ...formData, lastName: e.target.value })}
        />
      </div>
      <div className="form-group">
        <label>Company</label>
        <input 
          value={formData.company || ''}
          onChange={e => setFormData({ ...formData, company: e.target.value })}
        />
      </div>
      <div className="form-group">
        <label>Job Title</label>
        <input 
          value={formData.jobTitle || ''}
          onChange={e => setFormData({ ...formData, jobTitle: e.target.value })}
        />
      </div>
      <div className="form-group">
        <label>Notes</label>
        <textarea 
          value={formData.notes}
          onChange={e => setFormData({ ...formData, notes: e.target.value })}
          rows={4}
        />
      </div>
      
      <div className="form-actions">
        <button className="btn-secondary" onClick={onCancel}>Cancel</button>
        <button className="btn-primary" onClick={() => onSave(formData)}>Save</button>
      </div>
    </div>
  );
};

const DuplicateFinderModal: React.FC<{
  duplicates: ReturnType<CreamDataStore['findDuplicates']>;
  dataStore: CreamDataStore;
  onClose: () => void;
}> = ({ duplicates, dataStore, onClose }) => {
  if (duplicates.length === 0) {
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h2>No Duplicates Found</h2>
          <p>Great! No duplicate contacts were detected.</p>
          <button className="btn-primary" onClick={onClose}>Close</button>
        </div>
      </div>
    );
  }

  return (
    <div className="modal-overlay">
      <div className="modal modal-large">
        <h2>Duplicate Contacts Found ({duplicates.length})</h2>
        <div className="duplicate-list">
          {duplicates.map(dup => (
            <div key={dup.contact.id} className="duplicate-item">
              <div className="duplicate-group">
                <div className="duplicate-keep">
                  <strong>Keep: {dup.contact.firstName} {dup.contact.lastName}</strong>
                </div>
                <div className="duplicate-merge">
                  {dup.duplicates.map(d => (
                    <div key={d.id}>{d.firstName} {d.lastName} - Match: {Math.round(dup.matchScore * 100)}%</div>
                  ))}
                </div>
              </div>
              <button 
                className="btn-primary"
                onClick={() => {
                  dataStore.mergeContacts(dup.contact.id, dup.duplicates.map(d => d.id));
                }}
              >
                Merge
              </button>
            </div>
          ))}
        </div>
        <div className="modal-actions">
          <button className="btn-secondary" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
};

export default ContactsPage;