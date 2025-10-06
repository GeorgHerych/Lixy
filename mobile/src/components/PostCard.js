import { Image, StyleSheet, Text, View } from 'react-native';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

export default function PostCard({ post }) {
  const formattedDate = dayjs(post.pub_date).fromNow();
  const avatar = post.member?.avatar_url;

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        {avatar ? (
          <Image source={{ uri: avatar }} style={styles.avatar} />
        ) : (
          <View style={[styles.avatar, styles.placeholder]} />
        )}
        <View>
          <Text style={styles.author}>{post.member?.username}</Text>
          <Text style={styles.date}>{formattedDate}</Text>
        </View>
      </View>
      <Text style={styles.title}>{post.title}</Text>
      {post.content ? <Text style={styles.content}>{post.content}</Text> : null}
      {post.attachments?.[0]?.attachment ? (
        <Image source={{ uri: post.attachments[0].url || post.attachments[0].attachment }} style={styles.preview} />
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#111827',
    shadowOpacity: 0.08,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 8 },
    elevation: 2
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    gap: 12
  },
  avatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#ede9fe'
  },
  placeholder: {
    backgroundColor: '#ddd6fe'
  },
  author: {
    fontWeight: '600',
    fontSize: 16
  },
  date: {
    color: '#6b7280',
    marginTop: 2
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 8
  },
  content: {
    color: '#4b5563',
    lineHeight: 20,
    marginBottom: 12
  },
  preview: {
    width: '100%',
    height: 200,
    borderRadius: 12,
    backgroundColor: '#f3f4f6'
  }
});
