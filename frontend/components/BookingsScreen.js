import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
} from "react-native";

const API_URL = "http://localhost:8000";

const fetchBookings = async () => {
  console.log("Mock fetching bookings");
  // Simulate a network request delay
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Return a mock success response
  return [
    {
      id: "booking_1",
      client_id: "client_A",
      freelancer_id: "freelancer_X",
      price: 150,
      status: "APPROVED",
    },
    {
      id: "booking_2",
      client_id: "client_B",
      freelancer_id: "freelancer_Y",
      price: 200,
      status: "PENDING",
    },
    {
      id: "booking_3",
      client_id: "client_C",
      freelancer_id: "freelancer_Z",
      price: 75,
      status: "COMPLETED",
    },
    {
      id: "booking_4",
      client_id: "client_D",
      freelancer_id: "freelancer_X",
      price: 300,
      status: "CANCELLED",
    },
  ];
};

export default function BookingsScreen() {
  const [bookingsData, setBookingsData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadBookings = async () => {
      try {
        const result = await fetchBookings();
        setBookingsData(result);
      } catch (e) {
        setError(e.message);
      } finally {
        setIsLoading(false);
      }
    };

    loadBookings();
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.itemContainer}>
      <View style={styles.itemTextContainer}>
        <Text style={styles.itemName}>Booking #{item.id.slice(0, 8)}</Text>
        <Text style={styles.itemDetails}>
          From: {item.client_id} to {item.freelancer_id}
        </Text>
        <Text style={styles.itemDetails}>Price: ${item.price}</Text>
      </View>
      <Text style={[styles.itemStatus, { color: getStatusColor(item.status) }]}>
        {item.status}
      </Text>
    </View>
  );

  const getStatusColor = (status) => {
    switch (status) {
      case "APPROVED":
        return "#4CAF50";
      case "PENDING":
        return "#FFC107";
      case "COMPLETED":
        return "#2196F3";
      case "CANCELLED":
        return "#F44336";
      default:
        return "#FFFFFF";
    }
  };

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
      <Text style={styles.title}>Your Bookings</Text>
      <FlatList
        data={bookingsData}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
      />
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
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#FFFFFF",
    marginBottom: 20,
    fontFamily: "NunitoSans-Bold",
  },
  itemContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#1a1a1a",
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
  },
  itemTextContainer: {
    flex: 1,
  },
  itemName: {
    fontSize: 18,
    color: "#FFFFFF",
    fontFamily: "NunitoSans-Bold",
  },
  itemDetails: {
    fontSize: 14,
    color: "#cccccc",
    fontFamily: "NunitoSans-Regular",
  },
  itemStatus: {
    fontSize: 14,
    fontFamily: "NunitoSans-Regular",
    fontWeight: "bold",
  },
  errorText: {
    color: "#F44336",
    fontSize: 16,
    fontFamily: "NunitoSans-Regular",
  },
});
