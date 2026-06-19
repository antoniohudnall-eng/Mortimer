import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { format, isPast, isToday } from 'date-fns';
import type { CreamDataStore } from '../../shared/src/store';
import type { DatabaseState, Task } from '../../shared/src/types';

interface Props {
  navigation: any;
}

const TasksScreen: React.FC<Props> = ({ navigation }) => {
  const [filter, setFilter] = useState('pending');
  const dataStore: CreamDataStore = (global as any).dataStore;
  const data: DatabaseState = dataStore?.getState() || { tasks: [] };

  const filteredTasks = data.tasks.filter(task => {
    if (filter === 'pending') return task.status !== 'completed';
    if (filter === 'completed') return task.status === 'completed';
    if (filter === 'high') return task.priority === 'high';
    if (filter === 'overdue') return task.dueDate && isPast(task.dueDate) && task.status !== 'completed';
    return true;
  }).sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    if (a.dueDate && b.dueDate) {
      return a.dueDate.getTime() - b.dueDate.getTime();
    }
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

  const toggleTask = (task: Task) => {
    if (task.status === 'completed') {
      dataStore.updateTask(task.id, { status: 'pending', completedAt: undefined });
    } else {
      dataStore.markTaskComplete(task.id);
    }
  };

  const renderTask = ({ item }: { item: Task }) => (
    <TouchableOpacity 
      style={[styles.taskCard, item.status === 'completed' && styles.completedCard]}
      onPress={() => navigation.navigate('TaskDetail', { taskId: item.id })}
    >
      <TouchableOpacity 
        style={styles.checkbox}
        onPress={() => toggleTask(item)}
      >
        <Icon 
          name={item.status === 'completed' ? 'checkbox-marked' : 'checkbox-blank-outline'} 
          size={24} 
          color={item.status === 'completed' ? '#4CAF50' : '#666'} 
        />
      </TouchableOpacity>

      <View style={styles.taskContent}>
        <Text style={[styles.taskTitle, item.status === 'completed' && styles.completedText]}>
          {item.title}
        </Text>
        
        {item.description && <Text style={styles.taskDesc}>{item.description}</Text>}
        
        <View style={styles.taskMeta}>
          <View style={[styles.priorityBadge, { backgroundColor: getPriorityColor(item.priority) }]}>
            <Text style={styles.priorityText}>{item.priority.toUpperCase()}</Text>
          </View>
          
          {item.dueDate && (
            <Text style={[
              styles.dueDate,
              isPast(item.dueDate) && item.status !== 'completed' && styles.overdue
            ]}>
              {isToday(item.dueDate) ? 'Today' : format(item.dueDate, 'MMM d')}
            </Text>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );

  const handleAddTask = () => {
    navigation.navigate('TaskDetail', { taskId: null, isNew: true });
  };

  return (
    <View style={styles.container}>
      <View style={styles.filterBar}>
        {['pending', 'completed', 'high', 'overdue', 'all'].map(f => (
          <TouchableOpacity
            key={f}
            style={[styles.filterBtn, filter === f && styles.filterBtnActive]}
            onPress={() => setFilter(f)}
          >
            <Text style={[styles.filterText, filter === f && styles.filterTextActive]}>
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <FlatList
        data={filteredTasks}
        keyExtractor={item => item.id}
        renderItem={renderTask}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Icon name="check-circle-outline" size={64} color="#ccc" />
            <Text style={styles.emptyText}>No tasks found</Text>
          </View>
        }
      />

      <TouchableOpacity style={styles.fab} onPress={handleAddTask}>
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
  filterBar: {
    flexDirection: 'row',
    padding: 12,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  filterBtn: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    marginRight: 8,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
  },
  filterBtnActive: {
    backgroundColor: '#2196F3',
  },
  filterText: {
    fontSize: 14,
    color: '#666',
  },
  filterTextActive: {
    color: '#fff',
    fontWeight: '600',
  },
  list: {
    padding: 16,
  },
  taskCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    elevation: 1,
  },
  completedCard: {
    opacity: 0.7,
  },
  checkbox: {
    marginRight: 12,
  },
  taskContent: {
    flex: 1,
  },
  taskTitle: {
    fontSize: 16,
    fontWeight: '500',
  },
  completedText: {
    textDecorationLine: 'line-through',
    color: '#888',
  },
  taskDesc: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  taskMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  priorityBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    marginRight: 8,
  },
  priorityText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: '600',
  },
  dueDate: {
    fontSize: 13,
    color: '#666',
  },
  overdue: {
    color: '#F44336',
    fontWeight: '600',
  },
  emptyState: {
    alignItems: 'center',
    padding: 48,
  },
  emptyText: {
    marginTop: 16,
    fontSize: 16,
    color: '#999',
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

export default TasksScreen;