import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from "react-native";
import { authenticate } from "../utils/auth";

const API_URL = "http://localhost:8000"; // Assuming the backend is running on port 8000

const sendLoad = async (amount, senderId, recipientId) => {
  console.log(
    `Mock sending load of ${amount} from ${senderId} to ${recipientId}`,
  );
  // Simulate a network request delay
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Return a mock success response
  return {
    transaction_id: `mock_tx_${Date.now()}`,
    status: "completed",
    amount: parseFloat(amount),
  };
};

export default function LoadsScreen() {
  const [loadAmount, setLoadAmount] = useState("100");
  const [fee, setFee] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  // Real-time fee calculation
  useEffect(() => {
    const amount = parseFloat(loadAmount);
    if (!isNaN(amount)) {
      const calculatedFee = amount * 0.025;
      setFee(calculatedFee);
    } else {
      setFee(0);
    }
  }, [loadAmount]);

  const handleBookLoad = async () => {
    const isAuthenticated = await authenticate();
    if (!isAuthenticated) {
      Alert.alert("Error", "Authentication failed.");
      return;
    }

    setIsLoading(true);
    try {
      const senderId = "user_123";
      const recipientId = "user_456";
      const result = await sendLoad(loadAmount, senderId, recipientId);
      Alert.alert(
        "Success",
        `Load sent successfully! Transaction ID: ${result.transaction_id}`,
      );
    } catch (error) {
      Alert.alert("Error", error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Send a Load</Text>

      <View style={styles.card}>
        <Text style={styles.label}>Amount</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter amount"
          placeholderTextColor="#888"
          value={loadAmount}
          onChangeText={setLoadAmount}
          keyboardType="numeric"
        />

        <View style={styles.feeContainer}>
          <Text style={styles.feeLabel}>Fee (2.5% estimate)</Text>
          <Text style={styles.feeText}>${fee.toFixed(2)}</Text>
        </View>
      </View>

      <TouchableOpacity
        style={styles.button}
        onPress={handleBookLoad}
        disabled={isLoading}
      >
        <Text style={styles.buttonText}>
          {isLoading ? "Sending..." : "→ Send Load"}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#000000",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#FFFFFF",
    marginBottom: 20,
    fontFamily: "NunitoSans-Bold",
  },
  card: {
    backgroundColor: "#1a1a1a",
    borderRadius: 10,
    padding: 20,
    marginBottom: 30,
  },
  label: {
    fontSize: 16,
    color: "#cccccc",
    marginBottom: 10,
    fontFamily: "NunitoSans-Regular",
  },
  input: {
    width: "100%",
    height: 50,
    backgroundColor: "#000",
    borderRadius: 10,
    paddingHorizontal: 15,
    color: "#FFFFFF",
    fontFamily: "NunitoSans-Regular",
    borderWidth: 1,
    borderColor: "#333",
  },
  feeContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 20,
  },
  feeLabel: {
    fontSize: 16,
    color: "#cccccc",
    fontFamily: "NunitoSans-Regular",
  },
  feeText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#FFFFFF",
    fontFamily: "NunitoSans-Bold",
  },
  button: {
    width: "100%",
    height: 50,
    backgroundColor: "#FF0088",
    borderRadius: 10,
    justifyContent: "center",
    alignItems: "center",
    shadowColor: "rgba(255, 0, 136, 0.6)",
    shadowOffset: {
      width: 0,
      height: 0,
    },
    shadowOpacity: 1,
    shadowRadius: 20,
    elevation: 5,
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "bold",
    fontFamily: "NunitoSans-Bold",
  },
});
