import React, { useState } from "react";
import { useFonts } from "expo-font";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import KYCScreen from "./components/KYCScreen";
import LoadsScreen from "./components/LoadsScreen";
import DirectoryScreen from "./components/DirectoryScreen";
import BookingsScreen from "./components/BookingsScreen";
import ActivityScreen from "./components/ActivityScreen";
import ProfileScreen from "./components/ProfileScreen";

const Tab = createBottomTabNavigator();

export default function App() {
  const [fontsLoaded] = useFonts({
    "NunitoSans-Regular": require("./assets/fonts/NunitoSans-Regular.ttf"),
    "NunitoSans-Bold": require("./assets/fonts/NunitoSans-Bold.ttf"),
    "NunitoSans-Medium": require("./assets/fonts/NunitoSans-Medium.ttf"),
  });
  const [isKycVerified, setKycVerified] = useState(false);

  if (!fontsLoaded) {
    return null;
  }

  if (!isKycVerified) {
    return <KYCScreen onKycVerified={setKycVerified} />;
  }

  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Loads" component={LoadsScreen} />
        <Tab.Screen name="Directory" component={DirectoryScreen} />
        <Tab.Screen name="Bookings" component={BookingsScreen} />
        <Tab.Screen name="Activity" component={ActivityScreen} />
        <Tab.Screen name="Profile" component={ProfileScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
