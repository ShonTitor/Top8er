import { useEffect, useState, useCallback } from 'react';
import { Box, Typography, Divider, Paper, Chip, CircularProgress, TextField, InputAdornment, Stack, Pagination, Avatar } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { Link as RouterLink, useSearchParams } from 'react-router-dom';
import { apiURL } from '../api';

interface AuthorBrief {
  username: string;
  display_name: string;
  profile_picture: string | null;
}

interface PostSummary {
  title: string;
  slug: string;
  excerpt: string;
  published_at: string;
  main_image: string | null;
  categories: { name: string; slug: string }[];
  author: AuthorBrief | null;
}

interface Category {
  name: string;
  slug: string;
}

interface PagedResponse {
  count: number;
  total_pages: number;
  page: number;
  results: PostSummary[];
}

function BlogPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [paged, setPaged] = useState<PagedResponse | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState(searchParams.get('q') ?? '');
  const [debouncedSearch, setDebouncedSearch] = useState(searchParams.get('q') ?? '');
  const activeCategory = searchParams.get('category') ?? '';
  const page = parseInt(searchParams.get('page') ?? '1', 10);

  useEffect(() => { document.title = 'Top8er | Blog'; }, []);

  useEffect(() => {
    fetch(`${apiURL}/blog/categories/`)
      .then(r => r.json())
      .then(data => setCategories(data))
      .catch(() => {});
  }, []);

  useEffect(() => {
    const t = setTimeout(() => setDebouncedSearch(search), 350);
    return () => clearTimeout(t);
  }, [search]);

  // Sync debounced search to URL, resetting page to 1
  useEffect(() => {
    setSearchParams(prev => {
      const next = new URLSearchParams(prev);
      if (debouncedSearch) next.set('q', debouncedSearch);
      else next.delete('q');
      next.delete('page');
      return next;
    }, { replace: true });
  }, [debouncedSearch]); // eslint-disable-line react-hooks/exhaustive-deps

  const setCategory = (slug: string) => {
    setSearchParams(prev => {
      const next = new URLSearchParams(prev);
      if (slug) next.set('category', slug);
      else next.delete('category');
      next.delete('page');
      return next;
    });
  };

  const setPage = (value: number) => {
    setSearchParams(prev => {
      const next = new URLSearchParams(prev);
      if (value > 1) next.set('page', String(value));
      else next.delete('page');
      return next;
    });
  };

  const fetchPosts = useCallback(() => {
    const params = new URLSearchParams();
    if (debouncedSearch) params.set('q', debouncedSearch);
    if (activeCategory) params.set('category', activeCategory);
    params.set('page', String(page));
    setLoading(true);
    fetch(`${apiURL}/blog/?${params}`)
      .then(r => r.json())
      .then(data => { setPaged(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, [debouncedSearch, activeCategory, page]);

  useEffect(() => { fetchPosts(); }, [fetchPosts]);

  const posts = paged?.results ?? [];

  return (
    <Box sx={{ py: 4, maxWidth: 780, mx: 'auto' }}>

      <Box sx={{ mb: 4 }}>
        <Typography variant="overline" color="secondary" letterSpacing={2}>Blog</Typography>
        <Typography variant="h4" fontWeight={800} gutterBottom>
          News &amp; Updates
        </Typography>
        <Typography color="text.secondary">
          The latest updates, new game support, and announcements from Top8er.
        </Typography>
      </Box>

      <TextField
        fullWidth
        size="small"
        placeholder="Search posts…"
        value={search}
        onChange={e => setSearch(e.target.value)}
        sx={{ mb: 2 }}
        slotProps={{
          input: {
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon fontSize="small" />
              </InputAdornment>
            ),
          },
        }}
      />

      {categories.length > 0 && (
        <Stack direction="row" flexWrap="wrap" gap={1} sx={{ mb: 3 }}>
          <Chip
            label="All"
            color={activeCategory === '' ? 'secondary' : 'default'}
            variant={activeCategory === '' ? 'filled' : 'outlined'}
            onClick={() => setCategory('')}
            size="small"
          />
          {categories.map(cat => (
            <Chip
              key={cat.slug}
              label={cat.name}
              color={activeCategory === cat.slug ? 'secondary' : 'default'}
              variant={activeCategory === cat.slug ? 'filled' : 'outlined'}
              onClick={() => setCategory(activeCategory === cat.slug ? '' : cat.slug)}
              size="small"
            />
          ))}
        </Stack>
      )}

      <Divider sx={{ mb: 4 }} />

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
          <CircularProgress color="secondary" />
        </Box>
      ) : posts.length === 0 ? (
        <Typography color="text.secondary">No posts found.</Typography>
      ) : (
        <>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {posts.map(post => (
              <Paper
                key={post.slug}
                variant="outlined"
                component={RouterLink}
                to={`/blog/${post.slug}`}
                sx={{
                  display: 'block',
                  textDecoration: 'none',
                  color: 'inherit',
                  overflow: 'hidden',
                  '&:hover': { borderColor: 'secondary.main' },
                  transition: 'border-color 0.15s',
                }}
              >
                <Box sx={{ display: 'flex' }}>
                {post.main_image && (
                  <Box
                    component="img"
                    src={post.main_image}
                    alt={post.title}
                    sx={{ width: 140, flexShrink: 0, objectFit: 'cover', display: 'block' }}
                  />
                )}
                <Box sx={{ p: 3, flex: 1, minWidth: 0 }}>
                  <Stack direction="row" flexWrap="wrap" gap={0.5} sx={{ mb: 1 }}>
                    <Chip
                      label={new Date(post.published_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                      size="small"
                      variant="outlined"
                      color="secondary"
                    />
                    {post.categories.map(cat => (
                      <Chip key={cat.slug} label={cat.name} size="small" variant="outlined" />
                    ))}
                  </Stack>
                  <Typography variant="h6" fontWeight={700} gutterBottom>{post.title}</Typography>
                  {post.excerpt && (
                    <Typography variant="body2" color="text.secondary">{post.excerpt}</Typography>
                  )}
                  {post.author && (
                    <Stack direction="row" alignItems="center" spacing={0.75} sx={{ mt: 1 }}>
                      {post.author.profile_picture && (
                        <Avatar src={post.author.profile_picture} alt={post.author.display_name} sx={{ width: 20, height: 20 }} />
                      )}
                      <Typography variant="caption" color="text.secondary">
                        By {post.author.display_name}
                      </Typography>
                    </Stack>
                  )}
                </Box>
              </Box>
              </Paper>
            ))}
          </Box>

          {paged && paged.total_pages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={paged.total_pages}
                page={page}
                onChange={(_, value) => { setPage(value); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                color="secondary"
                shape="rounded"
              />
            </Box>
          )}
        </>
      )}

    </Box>
  );
}

export default BlogPage;
