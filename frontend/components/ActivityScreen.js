import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from 'react-native';

const API_URL = 'http://localhost:8000';

const fetchActivity = async (userId) => {
  try {
    const response = await fetch(`${API_URL}/analytics/activity/${userId}`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch activity');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching activity:', error);
    throw error;
  }
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
