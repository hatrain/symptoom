import { Button, StyleSheet, TextInput } from 'react-native';
import React, { useState } from 'react';
import { Text, View } from '@/components/Themed';
import AsyncStorage from '@react-native-async-storage/async-storage';
import SERVER_URL from './statics';
import { router } from 'expo-router';



export default function LoginScreen() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const validateForm = () => {
      if (!username || !password) {
        setError('Username and password are required');
        return false;
      }
      setError('');
      return true;
    };
  
    const handleSubmit = async (event: { preventDefault: () => void; }) => {
      event.preventDefault();
      if (!validateForm()) return;
      setLoading(true);
  
      const formDetails = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
  
      try {
        const requestString = SERVER_URL + '/token';
        const response = await fetch(requestString, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
          },
          body: formDetails,
        });
  
        setLoading(false);
  
        if (response.ok) {
          const data = await response.json();
          AsyncStorage.setItem('token', data.access_token);
          router.replace('/home');
        } else {
          const errorData = await response.json();
          setError(errorData.detail || 'Authentication failed!');
          AsyncStorage.removeItem('token');
        }
      } catch (error) {
        setLoading(false);
        setError('An error occurred. Please try again later.' + error);
      }
    };

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
      })


return (
  <View style={styles.container}>
  <Text style={styles.title}>Login Screen</Text>
  <Text>Username:</Text>
  <TextInput
    style={{ height: 40, borderColor: 'gray', borderWidth: 1, width: '80%' }}
    onChangeText={setUsername}
    value={username}
  />
  <TextInput
      style={{ height: 40, borderColor: 'gray', borderWidth: 1, width: '80%' }}
      onChangeText={setPassword}
      value={password}
      secureTextEntry={true}
  />
  <Button
      onPress={handleSubmit}
      title={loading ? 'Logging in...' : 'Login'}
      disabled={loading}
  />
  {error ? <Text style={{ color: 'red' }}>{JSON.stringify(error)}</Text> : null}
</View>
)};