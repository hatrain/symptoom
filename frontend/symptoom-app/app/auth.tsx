import AsyncStorage from "@react-native-async-storage/async-storage";
import { router } from 'expo-router';
import SERVER_URL from './statics';

const verifyAuth = async() =>{
    let token = await AsyncStorage.getItem('token');
      console.log(token);

      if (!token) {
        router.replace('/login');
        return;
      }
      
      try {
        const requestString = SERVER_URL + '/verify-token/' + token;
        const response = await fetch(requestString);

        if (!response.ok) {
          throw new Error('Token verification failed');
        }
      } catch (error) {
        AsyncStorage.removeItem('token');
        window.location.href = '/login';
      }
    
    }
    
export default verifyAuth;