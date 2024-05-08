import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRootNavigationState, Redirect } from 'expo-router';
import { useEffect } from 'react';
import verifyAuth from './auth';


export default function InitalRouting() {
  useEffect(() => {
    const verifyToken = async () => {
      let token = await AsyncStorage.getItem('token');
      console.log(token);

      if (!token) {
        window.location.href = '/login';
        return;
      }
      
      try {
        const response = await fetch(`http://localhost:8000/verify-token/${token}`);

        if (!response.ok) {
          throw new Error('Token verification failed');
        }
        else
        {
          window.location.href = '/home';
        }
      } catch (error) {
        AsyncStorage.removeItem('token');
        window.location.href = '/login';
      }
    };

    verifyToken();
  }, []);
  const rootNavigationState = useRootNavigationState();


  if (!rootNavigationState?.key) return null;


  return <Redirect href={'/loading'} />
}