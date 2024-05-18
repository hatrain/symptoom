import { Alert, Button, FlatList, StyleSheet } from 'react-native';
import { Text, View } from '@/components/Themed';
import { useEffect, useState } from 'react';
import verifyAuth from '../auth';
import AsyncStorage from '@react-native-async-storage/async-storage';
import SERVER_URL from '../statics';
import axios from 'axios';
import { router, useFocusEffect } from 'expo-router';
import React from 'react';

export default function ManageScreen() {
  //TODO: Add the ability to edit items in the list
  //state to store data for editing or deleting items
  const [formData, setFormData] = useState({
    date: '', //standard datetime
    severity: '', //scale integer 1-10
    notes: '', //string, a decent amount of text
    mood: '', //string, a decent amount of text
    weather: '', //pick from a list of standard weather conditions
    food_eaten: '', //string, a decent amount of text
    medications_before: '', //string, a decent amount of text
    medications_after: '', //string, a decent amount of text
    activities: '', //string, a decent amount of text
    work_day: '', //boolean
    sleep_rating: '', //scale integer 1-10
  });

  //state to store our token from local storage
  const [token, setToken] = useState<string | null>(null);

  //state to store data from the server
  const [data, setData] = useState<any[]>([]);

  //func for fetchin data from the server
  const fetchData = async (token: string) => {
    let requestString = SERVER_URL + '/all-symptom-episodes/';
    const response = await fetch(requestString + token, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });
    const json = await response.json();
    setData(json.symptom_episodes);
  };

  useFocusEffect(
    React.useCallback(() => {
      AsyncStorage.getItem('token').then(value => {
        setToken(value);
        if (value) {
          fetchData(value);
        }
      });
    }, [])
  );

  useEffect(() => {
    verifyAuth();
    AsyncStorage.getItem('token').then(value => {
      setToken(value);
      if (value) {
        fetchData(value);
      }
    });
  }, []);

  
  console.log(data);

  const deleteItem = (id: string) => {
    Alert.alert(
        "Delete Item",
        "Are you sure you want to delete this item?",
        [
          {
            text: "Cancel",
            onPress: () => console.log("Cancel Pressed"),
            style: "cancel"
          },
          { 
            text: "OK", 
            onPress: async () => {
              let requestString = `${SERVER_URL}/delete-symptom-episode/${token}/${id}`;
              // Call the API with fetch or axios
              const response = await axios.delete(requestString);
              if (token) {
                fetchData(token); // Refresh the list after delete
              }
            } 
          }
        ]
      );
    };
  

  return (
    <View style={styles.container}>
      <FlatList
        data={data}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text>Date: {item.date}</Text>
            <Text>Severity: {item.severity}</Text>
            <Text>Notes: {item.notes}</Text>
            <Text>Mood: {item.mood}</Text>
            <Text>Weather: {item.weather}</Text>
            <Text>Food Eaten: {item.food_eaten}</Text>
            <Text>Medications Before: {item.medications_before}</Text>
            <Text>Medications After: {item.medications_after}</Text>
            <Text>Activities: {item.activities}</Text>
            <Text>Work Day: {item.work_day}</Text>
            <Text>Sleep Rating: {item.sleep_rating}</Text>
            <Button title="Edit" onPress={() => router.replace('/edit')} />
            <Button title="Delete" onPress={() => deleteItem(item.id)} />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  item: {
    padding: 10,
    marginVertical: 8,
    marginHorizontal: 16,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
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
