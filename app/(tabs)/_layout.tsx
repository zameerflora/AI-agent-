import { Tabs } from "expo-router";
import { Ionicons, MaterialIcons } from "@expo/vector-icons";
import { TouchableOpacity } from "react-native";

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: "#10180bff",
        headerStyle: { backgroundColor: "#56684bff" },
        headerTintColor: "#050202ff",
        tabBarStyle: { backgroundColor: "#56684bff" },
        tabBarInactiveTintColor: "#f9f7f7ff",
      }}
    >
      <Tabs.Screen 
        name="Home" 
        options={{
          headerTitle: "GREENWISH",
          tabBarIcon: ({ focused, color }) => (
            <Ionicons 
              name={focused ? "home-sharp" : "home-outline"}
              color={color}
              size={24}
            />
          ),
          headerLeft: () => (
            <screenHeaderBtn iconUrl={iconSet.meun} dimensions="60%" />
          ),

          headerRight: () => (
            <screenHeaderBtn iconUrl={iconSet.profilr} dimensions="80%" />
         
        }}
      />
      <Tabs.Screen 
        name="Favorite" 
        options={{
          headerTitle: "Favorite",
          tabBarIcon: ({ focused, color }) => (    
            <Ionicons 
              name={focused ? "heart" : "heart-outline"}
              color={color}
              size={24}
            />
          ),
          headerRight: () => (
            <TouchableOpacity 
              style={{ marginRight: 15 }}
              onPress={() => console.log('Filter pressed')}
            >
              <MaterialIcons name="filter-list" size={24} color="#050202ff" />
            </TouchableOpacity>
          ),
        }}               
      />
      <Tabs.Screen 
        name="About" 
        options={{
          headerTitle: "About GREENWISH",
          tabBarIcon: ({ focused, color }) => (    
            <Ionicons 
              name={focused ? "information-circle" : "information-circle-outline"}
              color={color}
              size={24}
            />
          ),
          headerLeft: () => (
            <TouchableOpacity 
              style={{ marginLeft: 15 }}
              onPress={() => console.log('Back pressed')}
            >
              <Ionicons name="arrow-back" size={24} color="#050202ff" />
            </TouchableOpacity>
          ),
        }} 
      />
    </Tabs>
  );
}
       
                        