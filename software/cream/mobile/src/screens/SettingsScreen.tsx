import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { CreamDataStore } from '../../shared/src/store';
import type { DatabaseState } from '../../shared/src/types';

interface Props {
  dataStore: CreamDataStore;
  data: DatabaseState;
}

const SettingsScreen: React.FC<Props> = ({ dataStore, data }) => {
  const [showStats, setShowStats] = useState(true);
  const stats = dataStore.getStatistics();

  const handleExport = async () => {
    try {
      const json = dataStore.exportToJSON();
      await AsyncStorage.setItem('cream-export', json);
      Alert.alert('Success', 'Data exported to storage');
    } catch (e) {
      Alert.alert('Error', 'Failed to export data');
    }
  };

  const handleClearData = () => {
    Alert.alert(
      'Clear All Data',
      'This will delete all contacts, appointments, tasks, and projects. Are you sure?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Clear', 
          style: 'destructive',
          onPress: async () => {
            await AsyncStorage.removeItem('creamData');
            Alert.alert('Success', 'All data cleared');
          }
        },
      ]
    );
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Settings</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Statistics</Text>
        
        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.totalContacts}</Text>
            <Text style={styles.statLabel}>Contacts</Text>
          </View>
          
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.totalAppointments}</Text>
            <Text style={styles.statLabel}>Appointments</Text>
          </View>
          
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.totalTasks}</Text>
            <Text style={styles.statLabel}>Tasks</Text>
          </View>
          
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.completedTasks}</Text>
            <Text style={styles.statLabel}>Completed</Text>
          </View>
          
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.activeProjects}</Text>
            <Text style={styles.statLabel}>Projects</Text>
          </View>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Data Management</Text>
        
        <TouchableOpacity style={styles.actionRow} onPress={handleExport}>
          <Icon name="export" size={24} color="#2196F3" />
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>Export Data</Text>
            <Text style={styles.actionDesc}>Backup all data to JSON</Text>
          </View>
          <Icon name="chevron-right" size={20} color="#ccc" />
        </TouchableOpacity>

        <TouchableOpacity style={styles.actionRow} onPress={handleClearData}>
          <Icon name="delete-sweep" size={24} color="#F44336" />
          <View style={styles.actionContent}>
            <Text style={[styles.actionTitle, { color: '#F44336' }]}>Clear All Data</Text>
            <Text style={styles.actionDesc}>Delete everything (cannot be undone)</Text>
          </View>
          <Icon name="chevron-right" size={20} color="#ccc" />
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>
        
        <View style={styles.aboutCard}>
          <Text style={styles.aboutEmoji}>🍦</Text>
          <Text style={styles.aboutTitle}>CREAM PIM</Text>
          <Text style={styles.aboutVersion}>Version 1.0.0</Text>
          <Text style={styles.aboutDesc}>
            A Time & Chaos inspired Personal Information Manager
          </Text>
          <Text style={styles.aboutCopyright}>© Performance Supply Depot LLC</Text>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
  },
  section: {
    marginTop: 16,
    backgroundColor: '#fff',
    padding: 16,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    textTransform: 'uppercase',
    marginBottom: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  statCard: {
    width: '30%',
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 28,
    fontWeight: '700',
    color: '#2196F3',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  actionRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  actionContent: {
    flex: 1,
    marginLeft: 16,
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: '500',
  },
  actionDesc: {
    fontSize: 13,
    color: '#666',
    marginTop: 2,
  },
  aboutCard: {
    alignItems: 'center',
    padding: 24,
  },
  aboutEmoji: {
    fontSize: 48,
    marginBottom: 12,
  },
  aboutTitle: {
    fontSize: 20,
    fontWeight: '600',
  },
  aboutVersion: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  aboutDesc: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginTop: 12,
    lineHeight: 20,
  },
  aboutCopyright: {
    fontSize: 12,
    color: '#999',
    marginTop: 16,
  },
});

export default SettingsScreen;