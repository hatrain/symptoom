import AsyncStorage from "@react-native-async-storage/async-storage";
import { router } from 'expo-router';

const verifyAuth = async() =>{
    let token = await AsyncStorage.getItem('token');
      console.log(token);

      if (!token) {
        router.replace('/login');
        return;
      }
      
      try {
        const response = await fetch(`http://localhost:8000/verify-token/${token}`);

        if (!response.ok) {
          throw new Error('Token verification failed');
        }
      } catch (error) {
        AsyncStorage.removeItem('token');
        window.location.href = '/login';
      }
    
    }
    
export default verifyAuth;