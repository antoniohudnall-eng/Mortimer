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
import DateTimePicker from '@react-native-community/datetimepicker';
import type { CreamDataStore } from '../../shared/src/store';
import type { Task } from '../../shared/src/types';

interface Props {
  navigation: any;
  route: any;
}

const TaskDetailScreen: React.FC<Props> = ({ navigation, route }) => {
  const { taskId, isNew } = route.params;
  const dataStore: CreamDataStore = (global as any).dataStore;
  const [task, setTask] = useState<Task | null>(null);
  const [isEditing, setIsEditing] = useState(isNew);
  const [showDatePicker, setShowDatePicker] = useState(false);
  
  const [editedTask, setEditedTask] = useState<Partial<Task>>({
    title: '',
    description: '',
    priority: 'medium',
    status: 'pending',
    category: 'General',
    tags: [],
    linkedContacts: [],
    linkedAppointments: [],
  });

  useEffect(() => {
    if (taskId) {
      const found = dataStore.getState().tasks.find(t => t.id === taskId);
      if (found) {
        setTask(found);
        setEditedTask(found);
      }
    }
  }, [taskId]);

  const handleSave = () => {
    if (!editedTask.title) {
      Alert.alert('Error', 'Title is required');
      return;
    }

    if (isNew) {
      dataStore.addTask(editedTask as Omit<Task, 'id' | 'createdAt' | 'updatedAt'>);
    } else if (taskId) {
      dataStore.updateTask(taskId, editedTask);
    }
    navigation.goBack();
  };

  const handleDelete = () => {
    Alert.alert(
      'Delete Task',
      'Are you sure you want to delete this task?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Delete', 
          style: 'destructive',
          onPress: () => {
            if (taskId) {
              dataStore.deleteTask(taskId);
            }
            navigation.goBack();
          }
        },
      ]
    );
  };

  const onDateChange = (event: any, selectedDate?: Date) => {
    setShowDatePicker(false);
    if (selectedDate) {
      setEditedTask({ ...editedTask, dueDate: selectedDate });
    }
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
              <TouchableOpacity onPress={() => setIsEditing(false)} style={styles.headerBtn}>
                <Text style={styles.cancelBtn}>Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity onPress={handleSave} style={styles.headerBtn}>
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
            <Text style={styles.label}>Title *</Text>
            <TextInput
              style={styles.input}
              value={editedTask.title || ''}
              onChangeText={text => setEditedTask({ ...editedTask, title: text })}
              placeholder="Task title"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Description</Text>
            <TextInput
              style={[styles.input, styles.textArea]}
              value={editedTask.description || ''}
              onChangeText={text => setEditedTask({ ...editedTask, description: text })}
              placeholder="Add details..."
              multiline
              numberOfLines={4}
            />
          </View>

          <View style={styles.row}>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Priority</Text>
              <View style={styles.priorityButtons}>
                {['low', 'medium', 'high'].map(p => (
                  <TouchableOpacity
                    key={p}
                    style={[
                      styles.priorityBtn,
                      editedTask.priority === p && styles[`priority${p.charAt(0).toUpperCase() + p.slice(1)}`]
                    ]}
                    onPress={() => setEditedTask({ ...editedTask, priority: p as any })}
                  >
                    <Text style={[styles.priorityBtnText, editedTask.priority === p && styles.priorityBtnTextActive]}>
                      {p.charAt(0).toUpperCase() + p.slice(1)}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Due Date</Text>
            <TouchableOpacity 
              style={styles.dateButton}
              onPress={() => setShowDatePicker(true)}
            >
              <Icon name="calendar" size={20} color="#666" />
              <Text style={styles.dateText}>
                {editedTask.dueDate 
                  ? editedTask.dueDate.toLocaleDateString() 
                  : 'Select date'}
              </Text>
            </TouchableOpacity>
          </View>

          {showDatePicker && (
            <DateTimePicker
              value={editedTask.dueDate || new Date()}
              mode="date"
              onChange={onDateChange}
            />
          )}
        </View>
      ) : (
        <View style={styles.detailView}>
          <View style={styles.taskHeader}>
            <Text style={styles.taskTitle}>{task?.title}</Text>
            {task?.description && (
              <Text style={styles.taskDescription}>{task.description}</Text>
            )}
          </View>

          <View style={styles.infoSection}>
            <View style={styles.infoRow}>
              <Icon name="flag" size={20} color="#666" />
              <Text style={styles.infoLabel}>Priority</Text>
              <View style={[styles.priorityBadge, styles[`priority${task?.priority.charAt(0).toUpperCase() + task?.priority.slice(1)}`]]}>
                <Text style={styles.priorityBadgeText}>{task?.priority}</Text>
              </View>
            </View>

            {task?.dueDate && (
              <View style={styles.infoRow}>
                <Icon name="calendar" size={20} color="#666" />
                <Text style={styles.infoLabel}>Due</Text>
                <Text style={styles.infoValue}>{task.dueDate.toLocaleDateString()}</Text>
              </View>
            )}

            <View style={styles.infoRow}>
              <Icon name="check-circle" size={20} color="#666" />
              <Text style={styles.infoLabel}>Status</Text>
              <Text style={styles.infoValue}>{task?.status}</Text>
            </View>
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
  priorityButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  priorityBtn: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
  },
  priorityBtnText: {
    color: '#666',
    fontWeight: '500',
  },
  priorityBtnTextActive: {
    color: '#fff',
  },
  priorityLow: {
    backgroundColor: '#4CAF50',
  },
  priorityMedium: {
    backgroundColor: '#FF9800',
  },
  priorityHigh: {
    backgroundColor: '#F44336',
  },
  dateButton: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
  },
  dateText: {
    marginLeft: 12,
    fontSize: 16,
    color: '#333',
  },
  detailView: {
    padding: 16,
  },
  taskHeader: {
    marginBottom: 24,
  },
  taskTitle: {
    fontSize: 24,
    fontWeight: '600',
    marginBottom: 8,
  },
  taskDescription: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
  infoSection: {
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    padding: 16,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
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
  priorityBadge: {
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  priorityBadgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
});

export default TaskDetailScreen;