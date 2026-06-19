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
import type { Project } from '../../shared/src/types';

interface Props {
  navigation: any;
  route: any;
}

const ProjectDetailScreen: React.FC<Props> = ({ navigation, route }) => {
  const { projectId, isNew } = route.params;
  const dataStore: CreamDataStore = (global as any).dataStore;
  const [project, setProject] = useState<Project | null>(null);
  const [isEditing, setIsEditing] = useState(isNew);
  
  const [editedProject, setEditedProject] = useState<Partial<Project>>({
    name: '',
    description: '',
    status: 'active',
    priority: 'medium',
    color: '#4CAF50',
    progress: 0,
    tasks: [],
    appointments: [],
    linkedContacts: [],
    notes: '',
    tags: [],
  });

  const colors = ['#F44336', '#E91E63', '#9C27B0', '#673AB7', '#2196F3', '#03A9F4', '#4CAF50', '#FF9800', '#FF5722'];

  useEffect(() => {
    if (projectId) {
      const found = dataStore.getState().projects.find(p => p.id === projectId);
      if (found) {
        setProject(found);
        setEditedProject(found);
      }
    }
  }, [projectId]);

  const handleSave = () => {
    if (!editedProject.name) {
      Alert.alert('Error', 'Project name is required');
      return;
    }

    if (isNew) {
      dataStore.addProject(editedProject as Omit<Project, 'id' | 'createdAt' | 'updatedAt'>);
    } else if (projectId) {
      dataStore.updateProject(projectId, editedProject);
    }
    navigation.goBack();
  };

  const handleDelete = () => {
    Alert.alert(
      'Delete Project',
      'Are you sure you want to delete this project?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Delete', 
          style: 'destructive',
          onPress: () => {
            if (projectId) {
              dataStore.deleteProject(projectId);
            }
            navigation.goBack();
          }
        },
      ]
    );
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Icon name="arrow-left" size={24} color="#333" />
        </TouchableOpacity>
        
        <View style={styles.headerActions}>
          {isEditing ? (
            <>
              <TouchableOpacity onPress={() => setIsEditing(false)}>
                <Text style={styles.cancelBtn}>Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity onPress={handleSave}>
                <Text style={styles.saveBtn}>Save</Text>
              </TouchableOpacity>
            </>
          ) : (
            <>
              <TouchableOpacity onPress={() => setIsEditing(true)} style={styles.headerBtn}>
                <Icon name="pencil" size={20} color="#2196F3" />
              </TouchableOpacity>
              <TouchableOpacity onPress={handleDelete} style={styles.headerBtn}>
                <Icon name="delete" size={20} color="#F44336" />
              </TouchableOpacity>
            </>
          )}
        </View>
      </View>

      {isEditing ? (
        <View style={styles.form}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Name *</Text>
            <TextInput
              style={styles.input}
              value={editedProject.name}
              onChangeText={text => setEditedProject({ ...editedProject, name: text })}
              placeholder="Project name"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Description</Text>
            <TextInput
              style={[styles.input, styles.textArea]}
              value={editedProject.description || ''}
              onChangeText={text => setEditedProject({ ...editedProject, description: text })}
              placeholder="Add description..."
              multiline
              numberOfLines={4}
            />
          </View>

          <View style={styles.row}>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Status</Text>
              <View style={styles.statusButtons}>
                {['active', 'completed', 'on_hold'].map(s => (
                  <TouchableOpacity
                    key={s}
                    style={[
                      styles.statusBtn,
                      editedProject.status === s && styles.statusBtnActive
                    ]}
                    onPress={() => setEditedProject({ ...editedProject, status: s as any })}
                  >
                    <Text style={[styles.statusBtnText, editedProject.status === s && styles.statusBtnTextActive]}>
                      {s === 'on_hold' ? 'On Hold' : s.charAt(0).toUpperCase() + s.slice(1)}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Color</Text>
            <View style={styles.colorPicker}>
              {colors.map(color => (
                <TouchableOpacity
                  key={color}
                  style={[
                    styles.colorOption,
                    { backgroundColor: color },
                    editedProject.color === color && styles.colorOptionSelected
                  ]}
                  onPress={() => setEditedProject({ ...editedProject, color })}
                />
              ))}
            </View>
          </View>
        </View>
      ) : (
        <View style={styles.detailView}>
          <View style={styles.projectHeader}>
            <View style={[styles.colorDot, { backgroundColor: project?.color }]} />
            <Text style={styles.projectName}>{project?.name}</Text>
          </View>
          
          {project?.description && (
            <Text style={styles.description}>{project.description}</Text>
          )}
          
          <View style={styles.infoSection}>
            <View style={styles.infoRow}>
              <Icon name="information" size={20} color="#666" />
              <Text style={styles.infoLabel}>Status</Text>
              <Text style={styles.infoValue}>{project?.status}</Text>
            </View>
          </View>
          
          <View style={styles.progressSection}>
            <Text style={styles.progressLabel}>Progress</Text>
            <View style={styles.progressBar}>
              <View style={[styles.progressFill, { 
                width: `${project?.progress || 0}%`, 
                backgroundColor: project?.color 
              }]} />
            </View>
            <Text style={styles.progressText}>{project?.progress || 0}% complete</Text>
          </View>
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
  row: {
    flexDirection: 'row',
    gap: 16,
  },
  statusButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  statusBtn: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
  },
  statusBtnActive: {
    backgroundColor: '#2196F3',
  },
  statusBtnText: {
    color: '#666',
    fontWeight: '500',
  },
  statusBtnTextActive: {
    color: '#fff',
  },
  colorPicker: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  colorOption: {
    width: 40,
    height: 40,
    borderRadius: 20,
  },
  colorOptionSelected: {
    borderWidth: 3,
    borderColor: '#333',
  },
  detailView: {
    padding: 16,
  },
  projectHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  colorDot: {
    width: 16,
    height: 16,
    borderRadius: 8,
    marginRight: 12,
  },
  projectName: {
    fontSize: 24,
    fontWeight: '600',
    flex: 1,
  },
  description: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
    marginBottom: 24,
  },
  infoSection: {
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    padding: 16,
    marginBottom: 24,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
  },
  infoLabel: {
    marginLeft: 12,
    flex: 1,
    fontSize: 14,
    color: '#666',
  },
  infoValue: {
    fontSize: 14,
    fontWeight: '500',
  },
  progressSection: {
    marginTop: 16,
  },
  progressLabel: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  progressText: {
    marginTop: 8,
    fontSize: 14,
    color: '#666',
  },
});

export default ProjectDetailScreen;