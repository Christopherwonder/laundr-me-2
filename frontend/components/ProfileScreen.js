import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
} from "react-native";

const API_URL = "http://localhost:8000";

const fetchProfile = async (userId) => {
  console.log(`Mock fetching profile for userId: ${userId}`);
  // Simulate a network request delay
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Return a mock success response
  return {
    first_name: "John",
    last_name: "Doe",
    laundr_id: "johndoe",
    email: "john.doe@example.com",
    kyc_status: "Verified",
  };
};

export default function ProfileScreen() {
  const [profileData, setProfileData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const userId = 1;
        const result = await fetchProfile(userId);
        setProfileData(result);
      } catch (e) {
        setError(e.message);
      } finally {
        setIsLoading(false);
      }
    };

    loadProfile();
  }, []);

  if (isLoading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#FF0088" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorText}>Error: {error}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.avatar} />
        <Text style={styles.name}>
          {profileData?.first_name} {profileData?.last_name}
        </Text>
        <Text style={styles.laundrId}>@{profileData?.laundr_id}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Account Details</Text>
        <View style={styles.infoRow}>
          <Text style={styles.label}>Email</Text>
          <Text style={styles.value}>{profileData?.email}</Text>
        </View>
        <View style={styles.infoRow}>
          <Text style={styles.label}>KYC Status</Text>
          <Text style={styles.value}>{profileData?.kyc_status}</Text>
        </View>
      </View>

      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Logout</Text>
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
  centered: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#000000",
  },
  header: {
    alignItems: "center",
    marginBottom: 30,
  },
  avatar: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: "#333",
    marginBottom: 15,
  },
  name: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#FFFFFF",
    fontFamily: "NunitoSans-Bold",
  },
  laundrId: {
    fontSize: 16,
    color: "#cccccc",
    fontFamily: "NunitoSans-Regular",
  },
  card: {
    backgroundColor: "#1a1a1a",
    borderRadius: 10,
    padding: 20,
    marginBottom: 30,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#FFFFFF",
    marginBottom: 15,
    fontFamily: "NunitoSans-Bold",
  },
  infoRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 10,
  },
  label: {
    fontSize: 16,
    color: "#cccccc",
    fontFamily: "NunitoSans-Regular",
  },
  value: {
    fontSize: 16,
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
  errorText: {
    color: "#F44336",
    fontSize: 16,
    fontFamily: "NunitoSans-Regular",
  },
});
