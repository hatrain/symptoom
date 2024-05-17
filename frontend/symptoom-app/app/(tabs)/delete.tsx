import { StyleSheet } from 'react-native';

import EditScreenInfo from '@/components/EditScreenInfo';
import { Text, View } from '@/components/Themed';
import { useEffect } from 'react';
import verifyAuth from '../auth';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function DeleteScreen() {
  AsyncStorage.removeItem('token');
  //TODO: Add the ability to delete items
  useEffect(() => {
    verifyAuth();
  }, []);
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Delete Screen</Text>
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
});
