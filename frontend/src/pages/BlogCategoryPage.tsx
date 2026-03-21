import { useEffect, useState } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { Box, Typography, Divider, Paper, Chip, CircularProgress, Button, Stack, Pagination } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { apiURL } from '../api';

interface PostSummary {
  title: string;
  slug: string;
  excerpt: string;
  published_at: string;
  main_image: string | null;
  categories: { name: string; slug: string }[];
  author: { username: string; display_name: string; profile_picture: string | null } | null;
}

interface PagedCategoryResponse {
  category: { name: string; slug: string };
  count: number;
  total_pages: number;
  page: number;
  results: PostSummary[];
}

function BlogCategoryPage() {
  const { slug } = useParams<{ slug: string }>();
  const [data, setData] = useState<PagedCategoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [page, setPage] = useState(1);

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams({ page: String(page) });
    fetch(`${apiURL}/blog/category/${slug}/?${params}`)
      .then(r => {
        if (r.status === 404) { setNotFound(true); setLoading(false); return null; }
        return r.json();
      })
      .then(d => { if (d) { setData(d); setLoading(false); } })
      .catch(() => setLoading(false));
  }, [slug, page]);

  useEffect(() => {
    if (data) document.title = `Top8er | ${data.category.name}`;
    else document.title = 'Top8er | Blog';
  }, [data]);

  if (loading) return (
    <Box sx={{ display: 'flex', justifyContent: 'center', py: 10 }}>
      <CircularProgress color="secondary" />
    </Box>
  );

  if (notFound || !data) return (
    <Box sx={{ py: 4, maxWidth: 780, mx: 'auto' }}>
      <Typography variant="h5" fontWeight={700} gutterBottom>Category not found</Typography>
      <Button component={RouterLink} to="/blog" startIcon={<ArrowBackIcon />} color="secondary">Back to Blog</Button>
    </Box>
  );

  const posts = data.results;

  return (
    <Box sx={{ py: 4, maxWidth: 780, mx: 'auto' }}>
      <Button component={RouterLink} to="/blog" startIcon={<ArrowBackIcon />} color="secondary" sx={{ mb: 3 }}>
        Back to Blog
      </Button>

      <Box sx={{ mb: 4 }}>
        <Typography variant="overline" color="secondary" letterSpacing={2}>Category</Typography>
        <Typography variant="h4" fontWeight={800}>{data.category.name}</Typography>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {posts.length === 0 ? (
        <Typography color="text.secondary">No posts in this category.</Typography>
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
                {post.main_image && (
                  <Box component="img" src={post.main_image} alt={post.title}
                    sx={{ width: '100%', height: 200, objectFit: 'cover', display: 'block' }} />
                )}
                <Box sx={{ p: 3 }}>
                  <Stack direction="row" flexWrap="wrap" gap={0.5} sx={{ mb: 1 }}>
                    <Chip
                      label={new Date(post.published_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                      size="small" variant="outlined" color="secondary"
                    />
                    {post.categories.map(cat => (
                      <Chip key={cat.slug} label={cat.name} size="small" variant="outlined" />
                    ))}
                  </Stack>
                  <Typography variant="h6" fontWeight={700} gutterBottom>{post.title}</Typography>
                  {post.excerpt && <Typography variant="body2" color="text.secondary">{post.excerpt}</Typography>}
                  {post.author && (
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                      By {post.author.display_name}
                    </Typography>
                  )}
                </Box>
              </Paper>
            ))}
          </Box>

          {data.total_pages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={data.total_pages}
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

export default BlogCategoryPage;
