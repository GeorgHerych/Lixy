import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import ukLocale from 'dayjs/locale/uk';
import { fetchPosts } from './api/client.js';
import PostCard from './components/PostCard.jsx';

dayjs.extend(relativeTime);

function Header({ onRefresh, loading }) {
  return (
    <header className="header">
      <div className="header__content">
        <h1 className="header__title">Lixy соціальна стрічка</h1>
        <button className="header__button" onClick={onRefresh} disabled={loading}>
          {loading ? 'Оновлюємо…' : 'Оновити'}
        </button>
      </div>
    </header>
  );
}

function Filters({ onQueryChange }) {
  const [search, setSearch] = useState('');

  const handleChange = (event) => {
    const value = event.target.value;
    setSearch(value);
    onQueryChange(value);
  };

  return (
    <section className="filters">
      <input
        className="filters__search"
        type="search"
        value={search}
        onChange={handleChange}
        placeholder="Пошук за назвою чи автором"
      />
    </section>
  );
}

export default function App() {
  const [query, setQuery] = useState('');
  const {
    data,
    isFetching,
    refetch
  } = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
    staleTime: 30_000
  });

  const filteredPosts = useMemo(() => {
    if (!data) {
      return [];
    }

    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      return data;
    }

    return data.filter((post) => {
      const title = post.title?.toLowerCase() ?? '';
      const author = post.member?.username?.toLowerCase() ?? '';
      return title.includes(normalized) || author.includes(normalized);
    });
  }, [data, query]);

  return (
    <div className="page">
      <Header onRefresh={() => refetch()} loading={isFetching} />
      <Filters onQueryChange={setQuery} />
      <main className="grid">
        {filteredPosts.length === 0 && (
          <p className="empty">Поки що немає публікацій для відображення.</p>
        )}
        {filteredPosts.map((post) => (
          <PostCard key={post.id} post={post} locale={ukLocale} />
        ))}
      </main>
    </div>
  );
}
