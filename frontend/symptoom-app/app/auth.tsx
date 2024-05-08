import AsyncStorage from "@react-native-async-storage/async-storage";

const verifyAuth = async() =>{
    let token = await AsyncStorage.getItem('token');
      console.log(token);

      if (!token) {
        //the following line causes an infinite loop
        //window.location.href = '/login';
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