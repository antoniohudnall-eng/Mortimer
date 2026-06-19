import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { CreamDataStore } from '../shared/src/store';
import type { DatabaseState } from '../shared/src/types';
import ContactsScreen from './src/screens/ContactsScreen';
import ContactDetailScreen from './src/screens/ContactDetailScreen';
import CalendarScreen from './src/screens/CalendarScreen';
import TasksScreen from './src/screens/TasksScreen';
import TaskDetailScreen from './src/screens/TaskDetailScreen';
import ProjectsScreen from './src/screens/ProjectsScreen';
import ProjectDetailScreen from './src/screens/ProjectDetailScreen';
import SettingsScreen from './src/screens/SettingsScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Create singleton data store
const dataStore = new CreamDataStore();

// Persistence setup
dataStore.setPersistCallback(async (data) => {
  try {
    await AsyncStorage.setItem('creamData', JSON.stringify(data));
  } catch (e) {
    console.error('Failed to save data:', e);
  }
});

// Load data on startup
const loadData = async () => {
  try {
    const saved = await AsyncStorage.getItem('creamData');
    if (saved) {
      dataStore.importFromJSON(saved);
    }
  } catch (e) {
    console.error('Failed to load data:', e);
  }
};

// Contacts Stack
function ContactsStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="ContactsList" component={ContactsScreen} options={{ title: 'Contacts' }} />
      <Stack.Screen name="ContactDetail" component={ContactDetailScreen} options={{ title: 'Contact' }} />
    </Stack.Navigator>
  );
}

// Tasks Stack
function TasksStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="TasksList" component={TasksScreen} options={{ title: 'Tasks' }} />
      <Stack.Screen name="TaskDetail" component={TaskDetailScreen} options={{ title: 'Task' }} />
    </Stack.Navigator>
  );
}

// Projects Stack
function ProjectsStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="ProjectsList" component={ProjectsScreen} options={{ title: 'Projects' }} />
      <Stack.Screen name="ProjectDetail" component={ProjectDetailScreen} options={{ title: 'Project' }} />
    </Stack.Navigator>
  );
}

function App(): React.JSX.Element {
  const [data, setData] = useState<DatabaseState>(dataStore.getState());
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadData().then(() => {
      setData(dataStore.getState());
      setIsLoading(false);
    });

    const unsubscribe = dataStore.subscribe((newData) => {
      setData(newData);
    });

    return unsubscribe;
  }, []);

  if (isLoading) {
    return null; // Or a splash screen
  }

  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName: string;
            switch (route.name) {
              case 'Contacts':
                iconName = focused ? 'account-group' : 'account-group-outline';
                break;
              case 'Calendar':
                iconName = focused ? 'calendar' : 'calendar-outline';
                break;
              case 'Tasks':
                iconName = focused ? 'checkbox-marked' : 'checkbox-blank-outline';
                break;
              case 'Projects':
                iconName = focused ? 'folder' : 'folder-outline';
                break;
              case 'Settings':
                iconName = focused ? 'cog' : 'cog-outline';
                break;
              default:
                iconName = 'help-circle';
            }
            return <Icon name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: '#2196F3',
          tabBarInactiveTintColor: 'gray',
        })}
      >
        <Tab.Screen name="Contacts" options={{ headerShown: false }>
          {() => <ContactsStack />}
        </Tab.Screen>
        <Tab.Screen name="Calendar">
          {() => <CalendarScreen dataStore={dataStore} data={data} />}
        </Tab.Screen>
        <Tab.Screen name="Tasks" options={{ headerShown: false }>
          {() => <TasksStack />}
        </Tab.Screen>
        <Tab.Screen name="Projects" options={{ headerShown: false }>
          {() => <ProjectsStack />}
        </Tab.Screen>
        <Tab.Screen name="Settings">
          {() => <SettingsScreen dataStore={dataStore} data={data} />}
        </Tab.Screen>
      </Tab.Navigator>
    </NavigationContainer>
  );
}

export default App;