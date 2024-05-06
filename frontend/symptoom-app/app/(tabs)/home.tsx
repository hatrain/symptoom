import { StyleSheet, Button } from 'react-native';
import { Text, View } from '@/components/Themed';


export default function Home() {
  return (
    
    <View style={styles.container}>
      <Text style={styles.title}>Log a Symptoom</Text>
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      <Button title="Add Entry" onPress={() => console.log('Button clicked!')} />
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
