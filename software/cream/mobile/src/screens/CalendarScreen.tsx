import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Modal,
} from 'react-native';
import { Calendar } from 'react-native-calendars';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { format, isSameDay } from 'date-fns';
import type { CreamDataStore } from '../../shared/src/store';
import type { DatabaseState, Appointment } from '../../shared/src/types';

interface Props {
  dataStore: CreamDataStore;
  data: DatabaseState;
}

const CalendarScreen: React.FC<Props> = ({ dataStore, data }) => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [showAddModal, setShowAddModal] = useState(false);

  // Get appointments for selected date
  const dayAppointments = data.appointments.filter(a => 
    isSameDay(new Date(a.startTime), selectedDate)
  ).sort((a, b) => new Date(a.startTime).getTime() - new Date(b.startTime).getTime());

  // Build marked dates for calendar
  const markedDates: any = {};
  data.appointments.forEach(a => {
    const dateStr = format(new Date(a.startTime), 'yyyy-MM-dd');
    if (!markedDates[dateStr]) {
      markedDates[dateStr] = { marked: true, dotColor: a.color || '#2196F3' };
    }
  });
  
  const selectedStr = format(selectedDate, 'yyyy-MM-dd');
  markedDates[selectedStr] = { 
    ...markedDates[selectedStr], 
    selected: true, 
    selectedColor: '#2196F3' 
  };

  const renderAppointment = ({ item }: { item: Appointment }) => (
    <TouchableOpacity style={styles.appointmentCard}>
      <View style={[styles.colorStrip, { backgroundColor: item.color || '#2196F3' }]} />
      <View style={styles.appointmentContent}>
        <Text style={styles.appointmentTitle}>{item.title}</Text>
        <View style={styles.timeRow}>
          <Icon name="clock-outline" size={14} color="#666" />
          <Text style={styles.timeText}>
            {format(new Date(item.startTime), 'h:mm a')} - {format(new Date(item.endTime), 'h:mm a')}
          </Text>
        </View>
        
        {item.location && (
          <View style={styles.locationRow}>
            <Icon name="map-marker-outline" size={14} color="#666" />
            <Text style={styles.locationText}>{item.location}</Text>
          </View>
        )}
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Calendar
        current={format(selectedDate, 'yyyy-MM-dd')}
        markedDates={markedDates}
        onDayPress={(day: any) => setSelectedDate(new Date(day.timestamp))}
        theme={{
          selectedDayBackgroundColor: '#2196F3',
          todayTextColor: '#2196F3',
          arrowColor: '#2196F3',
        }}
      />

      <View style={styles.dayHeader}>
        <Text style={styles.dayTitle}>
          {format(selectedDate, 'EEEE, MMMM d')}
        </Text>
        <Text style={styles.appointmentCount}>
          {dayAppointments.length} appointments
        </Text>
      </View>

      <FlatList
        data={dayAppointments}
        keyExtractor={item => item.id}
        renderItem={renderAppointment}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Icon name="calendar-blank" size={48} color="#ccc" />
            <Text style={styles.emptyText}>No appointments today</Text>
          </View>
        }
      />

      <TouchableOpacity style={styles.fab} onPress={() => setShowAddModal(true)}>
        <Icon name="plus" size={28} color="#fff" />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  dayHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#f5f5f5',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  dayTitle: {
    fontSize: 18,
    fontWeight: '600',
  },
  appointmentCount: {
    fontSize: 14,
    color: '#666',
  },
  list: {
    padding: 16,
  },
  appointmentCard: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderRadius: 8,
    marginBottom: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    overflow: 'hidden',
  },
  colorStrip: {
    width: 4,
  },
  appointmentContent: {
    flex: 1,
    padding: 16,
  },
  appointmentTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  timeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  timeText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
  },
  locationRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 4,
  },
  locationText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
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

export default CalendarScreen;