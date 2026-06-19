import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  TextInput,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import type { CreamDataStore } from '../../shared/src/store';
import type { DatabaseState, Contact } from '../../shared/src/types';

interface Props {
  navigation: any;
}

const ContactsScreen: React.FC<Props> = ({ navigation }) => {
  const [searchQuery, setSearchQuery] = useState('');
  
  // Access data from navigation params or context
  const dataStore: CreamDataStore = navigation.getParam?.('dataStore') || (global as any).dataStore;
  const data: DatabaseState = dataStore?.getState() || { contacts: [] };
  
  const filteredContacts = data.contacts.filter(c => 
    `${c.firstName} ${c.lastName}`.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.emails.some(e => e.value.toLowerCase().includes(searchQuery.toLowerCase()))
  ).sort((a, b) => a.lastName.localeCompare(b.lastName));

  const renderContact = ({ item }: { item: Contact }) => (
    <TouchableOpacity
      style={styles.contactItem}
      onPress={() => navigation.navigate('ContactDetail', { contactId: item.id })}
    >
      <View style={styles.avatar}>
        <Text style={styles.avatarText}>{item.firstName[0]}{item.lastName[0]}</Text>
      </View>
      <View style={styles.contactInfo}>
        <Text style={styles.contactName}>{item.firstName} {item.lastName}</Text>
        {item.emails[0] && (
          <Text style={styles.contactEmail}>{item.emails[0].value}</Text>
        )}
      </View>
      <Icon name="chevron-right" size={24} color="#ccc" />
    </TouchableOpacity>
  );

  const handleAddContact = () => {
    const newContact = dataStore.addContact({
      firstName: '',
      lastName: '',
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
    navigation.navigate('ContactDetail', { contactId: newContact.id, isNew: true });
  };

  return (
    <View style={styles.container}>
      <View style={styles.searchBar}>
        <Icon name="magnify" size={24} color="#666" style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder="Search contacts..."
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
      </View>

      <FlatList
        data={filteredContacts}
        keyExtractor={item => item.id}
        renderItem={renderContact}
        contentContainerStyle={styles.list}
      />

      <TouchableOpacity style={styles.fab} onPress={handleAddContact}>
        <Icon name="plus" size={28} color="#fff" />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  searchBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    margin: 16,
    borderRadius: 8,
    paddingHorizontal: 12,
    elevation: 2,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    height: 48,
    fontSize: 16,
  },
  list: {
    padding: 16,
  },
  contactItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 16,
    marginBottom: 8,
    borderRadius: 8,
    elevation: 1,
  },
  avatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#2196F3',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  avatarText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  contactInfo: {
    flex: 1,
  },
  contactName: {
    fontSize: 16,
    fontWeight: '600',
  },
  contactEmail: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  fab: {
    position: 'absolute',
    right: 16,
    bottom: 16,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#2196F3',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 4,
  },
});

export default ContactsScreen;