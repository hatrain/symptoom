import { StyleSheet, Button } from 'react-native';
import EditScreenInfo from '@/components/EditScreenInfo';
import { Text, View } from '@/components/Themed';
import React, { useEffect } from 'react';
import { useState } from 'react';
import httpClient from "@/components/httpclient";
import { User } from '@/interfaces/user';

export default function Home() {
  return (
    
    <View style={styles.container}>
      <div>
      <h1>Welcome to this React Application</h1>
      {user != null ? (
        <div>
          <h2>Logged in</h2>
          <h3>ID: {user.id}</h3>
          <h3>Email: {user.email}</h3>

          <button onClick={logoutUser}>Logout</button>
        </div>
      ) : (
        <div>
          <p>You are not logged in</p>
          <div>
            <a href="/authenticate">
              <button>Login</button>
            </a>
            <a href="/createuser">
              <button>Register</button>
            </a>
          </div>
        </div>
      )}
    </div>
      <Text style={styles.title}>Log a Symptoom</Text>
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      <Button title="Add Entry" onPress={() => console.log('Button clicked!')} />
    </View>
  );
  
}
 
const [user, setUser] = useState<User | null>(null);

  const logoutUser = async () => {
    await httpClient.post("//localhost:5000/logout");
    window.location.href = "/";
  };

  useEffect(() => {
    (async () => {
      try {
        const resp = await httpClient.get("//localhost:5000/@me");
        setUser(resp.data);
      } catch (error) {
        console.log("Not authenticated");
      }
    })();
  }, []);

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
