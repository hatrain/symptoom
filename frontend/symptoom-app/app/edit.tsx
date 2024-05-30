import { StatusBar } from 'expo-status-bar';
import { Platform, StyleSheet } from 'react-native';
import { Text, View } from '@/components/Themed';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useEffect, useState } from 'react';
import verifyAuth from './auth';


export default function EditScreen() {
  const [currentSymptomID, setCurrentSymptomID] = useState<string | null>(null);
  useEffect(() => {
    verifyAuth();
    // Check for "currentSymptomID" item in AsyncStorage
    AsyncStorage.getItem('currentSymptomID').then(id => {
      // If it exists, assign it to a new variable and proceed to edit screen
      if (id !== null) {
        setCurrentSymptomID(id);
      }
    });
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Modal</Text>
      {currentSymptomID && <Text>Current Symptom ID: {currentSymptomID}</Text>}
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />

      {/* Use a light status bar on iOS to account for the black space above the modal */}
      <StatusBar style={Platform.OS === 'ios' ? 'light' : 'auto'} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
