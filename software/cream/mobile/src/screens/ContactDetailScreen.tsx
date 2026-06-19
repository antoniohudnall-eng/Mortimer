import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import type { CreamDataStore } from '../../shared/src/store';
import type { Contact } from '../../shared/src/types';

interface Props {
  navigation: any;
  route: any;
}

const ContactDetailScreen: React.FC<Props> = ({ navigation, route }) => {
  const { contactId, isNew } = route.params;
  const dataStore: CreamDataStore = (global as any).dataStore;
  const [contact, setContact] = useState<Contact | null>(null);
  const [isEditing, setIsEditing] = useState(isNew);
  const [editedContact, setEditedContact] = useState<Partial<Contact>>({});

  useEffect(() => {
    const c = dataStore.getContact(contactId);
    if (c) {
      setContact(c);
      setEditedContact(c);
    }
  }, [contactId]);

  const handleSave = () => {
    if (editedContact.firstName && editedContact.lastName) {
      dataStore.updateContact(contactId, editedContact);
      setIsEditing(false);
      const updated = dataStore.getContact(contactId);
      if (updated) setContact(updated);
    }
  };

  const handleDelete = () => {
    Alert.alert(
      'Delete Contact',
      'Are you sure you want to delete this contact?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Delete', 
          style: 'destructive',
          onPress: () => {
            dataStore.deleteContact(contactId);
            navigation.goBack();
          }
        },
      ]
    );
  };

  if (!contact) return null;

  if (isEditing) {
    return (
      <ScrollView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => setIsEditing(false)}>
            <Text style={styles.cancelBtn}>Cancel</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={handleSave}>
            <Text style={styles.saveBtn}>Save</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.form}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>First Name</Text>
            <TextInput
              style={styles.input}
              value={editedContact.firstName || ''}
              onChangeText={text => setEditedContact({ ...editedContact, firstName: text })}
              placeholder="First name"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Last Name</Text>
            <TextInput
              style={styles.input}
              value={editedContact.lastName || ''}
              onChangeText={text => setEditedContact({ ...editedContact, lastName: text })}
              placeholder="Last name"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Company</Text>
            <TextInput
              style={styles.input}
              value={editedContact.company || ''}
              onChangeText={text => setEditedContact({ ...editedContact, company: text })}
              placeholder="Company"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Notes</Text>
            <TextInput
              style={[styles.input, styles.textArea]}
              value={editedContact.notes || ''}
              onChangeText={text => setEditedContact({ ...editedContact, notes: text })}
              placeholder="Notes"
              multiline
              numberOfLines={4}
            />
          </View>
        </View>
      </ScrollView>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Icon name="arrow-left" size={24} color="#333" />
        </TouchableOpacity>
        <View style={styles.headerActions}>
          <TouchableOpacity onPress={() => setIsEditing(true)} style={styles.headerBtn}>
            <Icon name="pencil" size={20} color="#2196F3" />
          </TouchableOpacity>
          <TouchableOpacity onPress={handleDelete} style={styles.headerBtn}>
            <Icon name="delete" size={20} color="#F44336" />
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.profile}>
        <View style={styles.avatarLarge}>
          <Text style={styles.avatarLargeText}>
            {contact.firstName[0]}{contact.lastName[0]}
          </Text>
        </View>
        <Text style={styles.name}>{contact.firstName} {contact.lastName}</Text>
        {contact.company && <Text style={styles.company}>{contact.company}</Text>}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Contact Information</Text>
        
        {contact.emails.map(email => (
          <View key={email.id} style={styles.infoRow}>
            <Icon name="email-outline" size={20} color="#666" />
            <View style={styles.infoContent}>
              <Text style={styles.infoLabel}>{email.label}</Text>
              <Text style={styles.infoValue}>{email.value}</Text>
            </View>
          </View>
        ))}

        {contact.phones.map(phone => (
          <View key={phone.id} style={styles.infoRow}>
            <Icon name="phone-outline" size={20} color="#666" />
            <View style={styles.infoContent}>
              <Text style={styles.infoLabel}>{phone.label}</Text>
              <Text style={styles.infoValue}>{phone.value}</Text>
            </View>
          </View>
        ))}
      </View>

      {contact.notes && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Notes</Text>
          <Text style={styles.notes}>{contact.notes}</Text>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  headerActions: {
    flexDirection: 'row',
    gap: 16,
  },
  headerBtn: {
    padding: 8,
  },
  cancelBtn: {
    fontSize: 16,
    color: '#666',
  },
  saveBtn: {
    fontSize: 16,
    color: '#2196F3',
    fontWeight: '600',
  },
  profile: {
    alignItems: 'center',
    padding: 32,
    backgroundColor: '#f9f9f9',
  },
  avatarLarge: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#2196F3',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  avatarLargeText: {
    fontSize: 36,
    color: '#fff',
    fontWeight: 'bold',
  },
  name: {
    fontSize: 24,
    fontWeight: '600',
  },
  company: {
    fontSize: 16,
    color: '#666',
    marginTop: 4,
  },
  section: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    textTransform: 'uppercase',
    marginBottom: 12,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  infoContent: {
    marginLeft: 12,
  },
  infoLabel: {
    fontSize: 12,
    color: '#666',
  },
  infoValue: {
    fontSize: 16,
    marginTop: 2,
  },
  notes: {
    fontSize: 16,
    lineHeight: 24,
    color: '#333',
  },
  form: {
    padding: 16,
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
    color: '#333',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  textArea: {
    height: 100,
    textAlignVertical: 'top',
  },
});

export default ContactDetailScreen;