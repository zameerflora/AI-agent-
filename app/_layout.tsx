import { Stack } from "expo-router";
import { LogBox } from "react-native";

// Ignore all log messages
LogBox.ignoreAllLogs(true);

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen 
        name="(tabs)" 
        options={{ 
          headerShown: false
        }} 
      />
    </Stack>
  );
}
