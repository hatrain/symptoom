import { StyleSheet } from 'react-native';
import React, { useState } from 'react';
import { Text, View } from '@/components/Themed';
import AsyncStorage from '@react-native-async-storage/async-storage';


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
  
      const formDetails = new URLSearchParams();
      formDetails.append('username', username);
      formDetails.append('password', password);
  
      try {
        const response = await fetch('http://localhost:8000/token', {
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
          window.location.href = '/';
        } else {
          const errorData = await response.json();
          setError(errorData.detail || 'Authentication failed!');
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
      <Text>Username:</Text>
      <Text>Password:</Text>  
    <Text style={styles.title}>Login Screen</Text>
</View>
)};


// saved code
{/* <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                /> */}
{/* <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                /> */}

{/* <button type="submit" disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}
            </button> */}

    //         <div>
    //     <form onSubmit={handleSubmit}>
            
                
                
            
            
    //         {error && <p style={{ color: 'red' }}>{error}</p>}
    //     </form>
    // </div>