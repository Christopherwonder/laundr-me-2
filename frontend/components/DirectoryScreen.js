import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from 'react-native';

const API_URL = 'http://localhost:8000';

const searchDirectory = async (query = '') => {
  console.log(`Mock searching directory with query: ${query}`);
  // Simulate a network request delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Return a mock success response
  return {
    profiles: [
      { laundr_id: 'user_1', name: 'Alice Johnson', specialty: 'Graphic Designer' },
      { laundr_id: 'user_2', name: 'Bob Williams', specialty: 'Web Developer' },
      { laundr_id: 'user_3', name: 'Charlie Brown', specialty: 'Data Scientist' },
      { laundr_id: 'user_4', name: 'Diana Prince', specialty: 'Marketing Expert' },
    ],
  };
};

export default function DirectoryScreen() {
  const [directoryData, setDirectoryData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadDirectory = async () => {
      try {
        const result = await searchDirectory();
        setDirectoryData(result.profiles);
      } catch (e) {
        setError(e.message);
      } finally {
        setIsLoading(false);
      }
    };

    loadDirectory();
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.itemContainer}>
      <View style={styles.avatar} />
      <View style={styles.itemTextContainer}>
        <Text style={styles.itemName}>{item.name}</Text>
        <Text style={styles.itemRole}>{item.specialty}</Text>
      </View>
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
      <Text style={styles.title}>Directory</Text>
      <FlatList
        data={directoryData}
        renderItem={renderItem}
        keyExtractor={(item) => item.laundr_id}
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
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: '#333',
    marginRight: 15,
  },
  itemTextContainer: {
    flex: 1,
  },
  itemName: {
    fontSize: 18,
    color: '#FFFFFF',
    fontFamily: 'NunitoSans-Bold',
  },
  itemRole: {
    fontSize: 14,
    color: '#cccccc',
    fontFamily: 'NunitoSans-Regular',
  },
  errorText: {
    color: '#F44336',
    fontSize: 16,
    fontFamily: 'NunitoSans-Regular',
  },
});
