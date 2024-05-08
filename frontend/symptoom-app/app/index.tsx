import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRootNavigationState, Redirect } from 'expo-router';
import { useEffect } from 'react';
import verifyAuth from './auth';
import Loading from './loading';


export default function InitalRouting() {
  const rootNavigationState = useRootNavigationState();
  if (!rootNavigationState?.key) return null;
  return <Loading/>
}