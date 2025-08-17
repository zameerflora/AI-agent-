import { Text, View, StyleSheet } from "react-native";

export default function aboutScreen() {
  return (
    <View
      style={styles.container}>
      <Text style={styles.text}>About Screen</Text>
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