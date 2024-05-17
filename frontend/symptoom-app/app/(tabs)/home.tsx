import { StyleSheet, Button, TextInput, Platform } from 'react-native';
import { Text, View } from '@/components/Themed';
import { useEffect, useState } from 'react';
import verifyAuth from '../auth';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import DateTimePicker, { DateTimePickerEvent } from '@react-native-community/datetimepicker';
import SERVER_URL from '../statics';


export default function Home() {
  //TODO: Add/test the ability to add new items
  //state to store our token from local storage
  const [token, setToken] = useState<string | null>(null);

  //others
  const [date, setDate] = useState(new Date());
  const [show, setShow] = useState(false);

  const onChange = (event: DateTimePickerEvent, selectedDate: Date | undefined) => {
    const currentDate = selectedDate || date;
    setShow(Platform.OS === 'ios');
    setDate(currentDate);
    handleChange('date', currentDate.toISOString());
  };
  const showDatepicker = () => {
    console.log(show)
    setShow(true);
  };

  //state to store data from the server
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
  
  useEffect(() => {
    verifyAuth();
  }, []);

  useEffect(() => {
    const getToken = async () => {
      const result = await AsyncStorage.getItem('token');
      setToken(result);
    };

    getToken();
  }, []);

  const handleChange = (name: any, value: any) => {
    let parsedValue = value;
    
    if (name === 'severity' || name === 'sleep_rating') {
      parsedValue = parseInt(value);
    } else if (name === 'work_day') {
      parsedValue = value.toLowerCase() === 'true';
    }

    setFormData(prevState => ({ ...prevState, [name]: parsedValue }));
  };

  const handleSubmit = async () => {
    try {
      let requestString = `${SERVER_URL}/create-symptom-episode/${token}`;

      const response = await axios.post(requestString, formData);

      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };


  
  
  
  return (
    
    <View style={styles.container}>
    <Text style={styles.title}>Add a Symptom</Text>
    <Button onPress={showDatepicker} title="Select Date" />
    {show && (
      <DateTimePicker
        testID="dateTimePicker"
        value={date}
        mode={'date'}
        is24Hour={true}
        display="default"
        onChange={onChange}
      />
    )}
    <TextInput
      style={styles.input}
      onChangeText={(text) => handleChange('severity', text)}
      placeholder="Severity (1-10)"
    />
    <TextInput
      style={styles.input}
      onChangeText={(text) => handleChange('notes', text)}
      placeholder="Notes"
    />
    <TextInput
      style={styles.input}
      onChangeText={(text) => handleChange('mood', text)}
      placeholder="Mood"
    />
    <TextInput
      style={styles.input}
      onChangeText={(text) => handleChange('weather', text)}
      placeholder="Weather"
    />
    <TextInput
      style={styles.input}
      onChangeText={(text) => handleChange('food_eaten', text)}
      placeholder="Food Eaten"
    />
    <TextInput
      style={styles.input}
      onChangeText={(text) => handleChange('medications_before', text)}
      placeholder="Medications Before"
    />
    <TextInput
      style={styles.input}
      onChangeText={(text) => handleChange('medications_after', text)}
      placeholder="Medications After"
    />
    <TextInput
      style={styles.input}
      onChangeText={(text) => handleChange('activities', text)}
      placeholder="Activities"
    />
    <TextInput
      style={styles.input}
      onChangeText={(text) => handleChange('work_day', text)}
      placeholder="Work Day (true/false)"
    />
    <TextInput
      style={styles.input}
      onChangeText={(text) => handleChange('sleep_rating', text)}
      placeholder="Sleep Rating (1-10)"
    />
    <Button title="Submit" onPress={handleSubmit} />
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
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    width: '80%',
  },
});
