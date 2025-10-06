import { useState } from 'react';
import { FlatList, RefreshControl, SafeAreaView, StyleSheet, Text, TextInput, View } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { fetchPosts } from '../services/api';
import PostCard from './PostCard';

export default function FeedScreen() {
  const [search, setSearch] = useState('');
  const { data, isFetching, refetch } = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
    staleTime: 30_000
  });

  const filtered = (data ?? []).filter((post) => {
    const normalized = search.trim().toLowerCase();
    if (!normalized) {
      return true;
    }
    return (
      post.title?.toLowerCase().includes(normalized) ||
      post.member?.username?.toLowerCase().includes(normalized)
    );
  });

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.header}>
        <Text style={styles.title}>Lixy</Text>
        <Text style={styles.subtitle}>Стрічка для мобільного застосунку</Text>
      </View>
      <TextInput
        style={styles.input}
        placeholder="Пошук за назвою або автором"
        value={search}
        onChangeText={setSearch}
      />
      <FlatList
        data={filtered}
        keyExtractor={(item) => String(item.id)}
        contentContainerStyle={styles.listContent}
        refreshControl={<RefreshControl refreshing={isFetching} onRefresh={refetch} />}
        renderItem={({ item }) => <PostCard post={item} />}
        ListEmptyComponent={<Text style={styles.empty}>Немає дописів</Text>}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    paddingHorizontal: 16
  },
  header: {
    paddingVertical: 24,
    alignItems: 'flex-start'
  },
  title: {
    fontSize: 32,
    fontWeight: '700'
  },
  subtitle: {
    marginTop: 4,
    color: '#6b7280'
  },
  input: {
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#d1d5db',
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginBottom: 16,
    backgroundColor: '#ffffff'
  },
  listContent: {
    paddingBottom: 24,
    gap: 12
  },
  empty: {
    textAlign: 'center',
    color: '#6b7280',
    marginTop: 48
  }
});
