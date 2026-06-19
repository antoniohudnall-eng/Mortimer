import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import type { CreamDataStore } from '../../shared/src/store';
import type { DatabaseState, Project } from '../../shared/src/types';

interface Props {
  navigation: any;
}

const ProjectsScreen: React.FC<Props> = ({ navigation }) => {
  const [filter, setFilter] = useState('all');
  const dataStore: CreamDataStore = (global as any).dataStore;
  const data: DatabaseState = dataStore?.getState() || { projects: [] };

  const filteredProjects = data.projects.filter(project => {
    if (filter === 'active') return project.status === 'active';
    if (filter === 'completed') return project.status === 'completed';
    return true;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return '#4CAF50';
      case 'completed': return '#2196F3';
      case 'on_hold': return '#FF9800';
      case 'cancelled': return '#F44336';
      default: return '#888';
    }
  };

  const getProjectTasks = (projectId: string) => {
    return data.tasks.filter(t => t.linkedProject === projectId);
  };

  const renderProject = ({ item }: { item: Project }) => {
    const tasks = getProjectTasks(item.id);
    const completedTasks = tasks.filter(t => t.status === 'completed').length;
    
    return (
      <TouchableOpacity 
        style={styles.projectCard}
        onPress={() => navigation.navigate('ProjectDetail', { projectId: item.id })}
      >
        <View style={[styles.colorIndicator, { backgroundColor: item.color }]} />
        <View style={styles.projectContent}>
          <View style={styles.projectHeader}>
            <Text style={styles.projectName}>{item.name}</Text>
            <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) }]}>
              <Text style={styles.statusText}>{item.status}</Text>
            </View>
          </View>
          
          {item.description && (
            <Text style={styles.projectDesc} numberOfLines={2}>
              {item.description}
            </Text>
          )}
          
          <View style={styles.projectStats}>
            <View style={styles.stat}>
              <Icon name="check-circle" size={14} color="#666" />
              <Text style={styles.statText}>{completedTasks}/{tasks.length} tasks</Text>
            </View>
          </View>
          
          <View style={styles.progressContainer}>
            <View style={styles.progressBar}>
              <View style={[styles.progressFill, { width: `${item.progress}%`, backgroundColor: item.color }]} />
            </View>
            <Text style={styles.progressText}>{item.progress}%</Text>
          </View>
        </View>
      </TouchableOpacity>
    );
  };

  const handleAddProject = () => {
    navigation.navigate('ProjectDetail', { projectId: null, isNew: true });
  };

  return (
    <View style={styles.container}>
      <View style={styles.filterBar}>
        {['all', 'active', 'completed'].map(f => (
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
        data={filteredProjects}
        keyExtractor={item => item.id}
        renderItem={renderProject}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Icon name="folder-outline" size={64} color="#ccc" />
            <Text style={styles.emptyText}>No projects found</Text>
          </View>
        }
      />

      <TouchableOpacity style={styles.fab} onPress={handleAddProject}>
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
  projectCard: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderRadius: 8,
    marginBottom: 12,
    elevation: 1,
    overflow: 'hidden',
  },
  colorIndicator: {
    width: 4,
  },
  projectContent: {
    flex: 1,
    padding: 16,
  },
  projectHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  projectName: {
    fontSize: 16,
    fontWeight: '600',
    flex: 1,
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  projectDesc: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  projectStats: {
    flexDirection: 'row',
    marginBottom: 12,
  },
  stat: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  statText: {
    fontSize: 13,
    color: '#666',
    marginLeft: 4,
  },
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  progressBar: {
    flex: 1,
    height: 6,
    backgroundColor: '#e0e0e0',
    borderRadius: 3,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 3,
  },
  progressText: {
    fontSize: 12,
    color: '#666',
    width: 40,
    textAlign: 'right',
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

export default ProjectsScreen;