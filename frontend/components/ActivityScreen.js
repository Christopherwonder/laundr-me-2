import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from 'react-native';

const API_URL = 'http://localhost:8000';

const fetchActivity = async (userId) => {
  console.log(`Mock fetching activity for userId: ${userId}`);
  // Simulate a network request delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Return a mock success response
  return {
    items: [
      { id: 'act_1', type: 'Deposit', timestamp: '2023-10-27T10:00:00Z', details: { amount: 500 } },
      { id: 'act_2', type: 'Payment', timestamp: '2023-10-26T15:30:00Z', details: { amount: -50 } },
      { id: 'act_3', type: 'Booking', timestamp: '2023-10-25T11:00:00Z', details: { amount: -150 } },
      { id: 'act_4', type: 'Withdrawal', timestamp: '2023-10-24T18:45:00Z', details: { amount: -200 } },
    ],
  };
};

const ICONS = {
  deposit: '↓',
  withdrawal: '↑',
  payment: '→',
  booking: '🗓️',
  default: '•',
};

const getIconForType = (type) => {
  return ICONS[type.toLowerCase()] || ICONS.default;
};

export default function ActivityScreen() {
  const [activityData, setActivityData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadActivity = async () => {
      try {
        const userId = 'user_123';
        const result = await fetchActivity(userId);
        setActivityData(result.items);
      } catch (e) {
        setError(e.message);
      } finally {
        setIsLoading(false);
      }
    };

    loadActivity();
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.itemContainer}>
      <View style={styles.iconContainer}>
        <Text style={styles.icon}>{getIconForType(item.type)}</Text>
      </View>
      <View style={styles.itemTextContainer}>
        <Text style={styles.itemType}>{item.type}</Text>
        <Text style={styles.itemDate}>{new Date(item.timestamp).toLocaleDateString()}</Text>
      </View>
      <Text style={[styles.itemAmount, { color: item.details.amount > 0 ? '#4CAF50' : '#F44336' }]}>
        {item.details.amount > 0 ? '+' : '-'}${Math.abs(item.details.amount)}
      </Text>
    </View>
  );

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
      <Text style={styles.title}>Your Activity</Text>
      <FlatList
        data={activityData}
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
    backgroundColor: '#000000',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000000',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 20,
    fontFamily: 'NunitoSans-Bold',
  },
  itemContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1a1a1a',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#333',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  icon: {
    fontSize: 20,
    color: '#FFFFFF',
  },
  itemTextContainer: {
    flex: 1,
  },
  itemType: {
    fontSize: 18,
    color: '#FFFFFF',
    fontFamily: 'NunitoSans-Bold',
  },
  itemDate: {
    fontSize: 14,
    color: '#cccccc',
    fontFamily: 'NunitoSans-Regular',
  },
  itemAmount: {
    fontSize: 18,
    fontFamily: 'NunitoSans-Bold',
  },
  errorText: {
    color: '#F44336',
    fontSize: 16,
    fontFamily: 'NunitoSans-Regular',
  },
});
