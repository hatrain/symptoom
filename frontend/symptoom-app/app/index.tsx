import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRootNavigationState, Redirect } from 'expo-router';
import { useEffect } from 'react';
import verifyAuth from './auth';
import Loading from './loading';
//TODO: Fix the index error on the frontend when the app loads natively.


export default function InitalRouting() {
  const rootNavigationState = useRootNavigationState();
  if (!rootNavigationState?.key) return null;
  return <Loading/>
}