import React from 'react';
import { StyleSheet,ActivityIndicator, View } from 'react-native';


const Loading: React.FC = () => {
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
  

  