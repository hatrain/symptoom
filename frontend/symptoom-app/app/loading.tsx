import React, { useEffect } from 'react';
import { StyleSheet,ActivityIndicator, View } from 'react-native';
import verifyAuth from './auth';
import { router } from 'expo-router';


const Loading: React.FC = () => {
  useEffect(() => {
    verifyAuth();
  }, []);

  useEffect(() => {
    router.replace('/home');
  }, []);

    return (
    <View style={[styles.container, styles.horizontal]}>
        <ActivityIndicator size="large" />
    </View>
    );
};

export default Loading;

const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
    },
    horizontal: {
      flexDirection: 'row',
      justifyContent: 'space-around',
      padding: 10,
    },
  });
  

  