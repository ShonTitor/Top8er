import { useEffect, useState } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { Box, Typography, Divider, Paper, Chip, CircularProgress, Button, Avatar, Stack, IconButton, Pagination } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import TwitterIcon from '@mui/icons-material/Twitter';
import InstagramIcon from '@mui/icons-material/Instagram';
import YouTubeIcon from '@mui/icons-material/YouTube';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';
import { apiURL } from '../api';

interface AuthorFull {
  username: string;
  display_name: string;
  profile_picture: string | null;
  description: string;
  twitter: string;
  instagram: string;
  twitch: string;
  youtube: string;
  bluesky: string;
  discord: string;
}

interface PostSummary {
  title: string;
  slug: string;
  excerpt: string;
  published_at: string;
  main_image: string | null;
  categories: { name: string; slug: string }[];
}

interface PagedAuthorResponse {
  author: AuthorFull;
  count: number;
  total_pages: number;
  page: number;
  results: PostSummary[];
}

function BlogAuthorPage() {
  const { username } = useParams<{ username: string }>();
  const [data, setData] = useState<PagedAuthorResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [page, setPage] = useState(1);

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams({ page: String(page) });
    fetch(`${apiURL}/blog/author/${username}/?${params}`)
      .then(r => {
        if (r.status === 404) { setNotFound(true); setLoading(false); return null; }
        return r.json();
      })
      .then(d => { if (d) { setData(d); setLoading(false); } })
      .catch(() => setLoading(false));
  }, [username, page]);

  useEffect(() => {
    if (data) document.title = `Top8er | ${data.author.display_name}`;
    else document.title = 'Top8er | Blog';
  }, [data]);

  if (loading) return (
    <Box sx={{ display: 'flex', justifyContent: 'center', py: 10 }}>
      <CircularProgress color="secondary" />
    </Box>
  );

  if (notFound || !data) return (
    <Box sx={{ py: 4, maxWidth: 780, mx: 'auto' }}>
      <Typography variant="h5" fontWeight={700} gutterBottom>Author not found</Typography>
      <Button component={RouterLink} to="/blog" startIcon={<ArrowBackIcon />} color="secondary">Back to Blog</Button>
    </Box>
  );

  const { author, results: posts } = data;

  return (
    <Box sx={{ py: 4, maxWidth: 780, mx: 'auto' }}>
      <Button component={RouterLink} to="/blog" startIcon={<ArrowBackIcon />} color="secondary" sx={{ mb: 3 }}>
        Back to Blog
      </Button>

      {/* Author header */}
      <Box sx={{ display: 'flex', gap: 3, alignItems: 'flex-start', mb: 4, flexWrap: 'wrap' }}>
        <Avatar
          src={author.profile_picture || undefined}
          alt={author.display_name}
          sx={{ width: 88, height: 88, flexShrink: 0 }}
        />
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <Typography variant="overline" color="secondary" letterSpacing={2}>Author</Typography>
          <Typography variant="h4" fontWeight={800}>{author.display_name}</Typography>
          {author.description && (
            <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>{author.description}</Typography>
          )}
          <Stack direction="row" spacing={0.5} sx={{ mt: 1.5 }}>
            {author.twitter && (
              <IconButton size="small" component="a" href={`https://twitter.com/${author.twitter}`} target="_blank" rel="noopener noreferrer">
                <TwitterIcon fontSize="small" />
              </IconButton>
            )}
            {author.instagram && (
              <IconButton size="small" component="a" href={`https://instagram.com/${author.instagram}`} target="_blank" rel="noopener noreferrer">
                <InstagramIcon fontSize="small" />
              </IconButton>
            )}
            {author.twitch && (
              <IconButton size="small" component="a" href={`https://twitch.tv/${author.twitch}`} target="_blank" rel="noopener noreferrer">
                <SportsEsportsIcon fontSize="small" />
              </IconButton>
            )}
            {author.youtube && (
              <IconButton size="small" component="a" href={author.youtube} target="_blank" rel="noopener noreferrer">
                <YouTubeIcon fontSize="small" />
              </IconButton>
            )}
            {author.bluesky && (
              <IconButton size="small" component="a" href={`https://bsky.app/profile/${author.bluesky}`} target="_blank" rel="noopener noreferrer">
                <Typography variant="caption" fontWeight={700} sx={{ lineHeight: 1, px: 0.25 }}>BSky</Typography>
              </IconButton>
            )}
            {author.discord && (
              <Chip label={author.discord} size="small" variant="outlined" sx={{ ml: 0.5 }} />
            )}
          </Stack>
        </Box>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {posts.length === 0 ? (
        <Typography color="text.secondary">No posts yet.</Typography>
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
                    sx={{ width: '100%', height: 180, objectFit: 'cover', display: 'block' }} />
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

export default BlogAuthorPage;
