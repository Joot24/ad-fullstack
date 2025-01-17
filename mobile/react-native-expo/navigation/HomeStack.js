import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from '../screens/home/HomeScreen';
import PortfolioStack from "./PortfolioStack";

const Stack = createNativeStackNavigator();

const HomeStack = () => {
    return (
        <Stack.Navigator initialRouteName="Home">
            <Stack.Screen name="Home" component={HomeScreen} options={{ headerTitle: 'Home' }} />
            <Stack.Screen name="PortfolioStack" component={PortfolioStack} options={{ headerShown: false }} />
        </Stack.Navigator>
    );
};

export default HomeStack;
