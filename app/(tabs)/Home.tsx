import { Link } from "expo-router";
import { Text, View, StyleSheet, ScrollView, SafeAreaView } from "react-native";
import {Stack, useRouter} from "expo-router";
import{ COLORS, icons, images, SIZES } from "../../constants";


export default function Index() {
  return (
    <View
      style={styles.container}>
      <Text style={styles.text}>HELLO WORLD</Text>
     
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#c5c3aeff",
  },

  text: {
    color: "#050505ff",
    fontSize: 20,
  },

  button: {
    fontSize: 20,
    textDecorationLine: "underline",
    color: "#43cc4aff",
  },
});