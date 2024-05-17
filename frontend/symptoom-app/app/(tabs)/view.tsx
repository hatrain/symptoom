import { FlatList, StyleSheet } from 'react-native';
import { Text, View } from '@/components/Themed';
import { useEffect, useState } from 'react';
import verifyAuth from '../auth';
import AsyncStorage from '@react-native-async-storage/async-storage';
import SERVER_URL from '../statics';

export default function ViewScreen() {
  //TODO: Add the ability to edit items in the list
  //state to store our token from local storage
  const [token, setToken] = useState<string | null>(null);

  //state to store data from the server
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    verifyAuth();
    AsyncStorage.getItem('token').then(value => {
      setToken(value);
      if (value) {
        let requestString = SERVER_URL + '/all-symptom-episodes/';
        fetch(requestString + value, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          },
        })
          .then(response => response.json())
          .then(json => setData(json.symptom_episodes))
          .catch(error => console.error(error));
      }
    });
  }, []);
  console.log(data);

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
