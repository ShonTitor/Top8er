import { useEffect, useState } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import DOMPurify from 'dompurify';
import { apiURL } from '../api';
import { Box, Typography, Divider, Chip, CircularProgress, Button, Avatar, Stack, IconButton, Paper } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import TwitterIcon from '@mui/icons-material/Twitter';
import InstagramIcon from '@mui/icons-material/Instagram';
import YouTubeIcon from '@mui/icons-material/YouTube';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';

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

interface Post {
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  published_at: string;
  main_image: string | null;
  categories: { name: string; slug: string }[];
  author: AuthorFull | null;
}

interface RelatedPost {
  title: string;
  slug: string;
  main_image: string | null;
  published_at: string;
}

function AuthorCard({ author }: { author: AuthorFull }) {
  return (
    <Box sx={{ display: 'flex', gap: 2, p: 2.5, border: '1px solid', borderColor: 'divider', borderRadius: 2, mt: 5 }}>
      <Avatar
        src={author.profile_picture || undefined}
        alt={author.display_name}
        sx={{ width: 64, height: 64, flexShrink: 0 }}
      />
      <Box sx={{ flex: 1, minWidth: 0 }}>
        <Typography
          variant="subtitle1"
          fontWeight={700}
          component={RouterLink}
          to={`/blog/author/${author.username}`}
          sx={{ textDecoration: 'none', color: 'inherit', '&:hover': { textDecoration: 'underline' } }}
        >
          {author.display_name}
        </Typography>
        {author.description && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
            {author.description}
          </Typography>
        )}
        <Stack direction="row" spacing={0.5} sx={{ mt: 1 }}>
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
  );
}

function Sidebar({ related }: { related: RelatedPost[] }) {
  if (related.length === 0) return null;
  return (
    <Box
      component="aside"
      sx={{
        width: 240,
        flexShrink: 0,
        display: { xs: 'none', lg: 'block' },
      }}
    >
      <Typography variant="overline" color="secondary" letterSpacing={2} sx={{ mb: 1.5, display: 'block' }}>
        Related Posts
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
        {related.map(p => (
          <Paper
            key={p.slug}
            variant="outlined"
            component={RouterLink}
            to={`/blog/${p.slug}`}
            sx={{
              display: 'block',
              textDecoration: 'none',
              color: 'inherit',
              overflow: 'hidden',
              '&:hover': { borderColor: 'secondary.main' },
              transition: 'border-color 0.15s',
            }}
          >
            {p.main_image && (
              <Box
                component="img"
                src={p.main_image}
                alt={p.title}
                sx={{ width: '100%', height: 110, objectFit: 'cover', display: 'block' }}
              />
            )}
            <Box sx={{ p: 1.5 }}>
              <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 0.5 }}>
                {new Date(p.published_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}
              </Typography>
              <Typography variant="body2" fontWeight={600} sx={{ lineHeight: 1.3 }}>
                {p.title}
              </Typography>
            </Box>
          </Paper>
        ))}
      </Box>
    </Box>
  );
}

function BlogPostPage() {
  const { slug } = useParams<{ slug: string }>();
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [related, setRelated] = useState<RelatedPost[]>([]);

  useEffect(() => {
    fetch(`${apiURL}/blog/${slug}/`)
      .then(r => {
        if (r.status === 404) { setNotFound(true); setLoading(false); return null; }
        return r.json();
      })
      .then(data => {
        if (data) { setPost(data); setLoading(false); }
      })
      .catch(() => setLoading(false));
  }, [slug]);

  useEffect(() => {
    if (!post || post.categories.length === 0) return;
    const firstCat = post.categories[0].slug;
    fetch(`${apiURL}/blog/?category=${firstCat}&page=1`)
      .then(r => r.json())
      .then(data => {
        const others = (data.results as RelatedPost[]).filter(p => p.slug !== slug).slice(0, 5);
        setRelated(others);
      })
      .catch(() => {});
  }, [post, slug]);

  useEffect(() => {
    if (post) document.title = `Top8er | ${post.title}`;
    else document.title = 'Top8er | Blog';
  }, [post]);

  if (loading) return (
    <Box sx={{ display: 'flex', justifyContent: 'center', py: 10 }}>
      <CircularProgress color="secondary" />
    </Box>
  );

  if (notFound || !post) return (
    <Box sx={{ py: 4, maxWidth: 780, mx: 'auto' }}>
      <Typography variant="h5" fontWeight={700} gutterBottom>Post not found</Typography>
      <Button component={RouterLink} to="/blog" startIcon={<ArrowBackIcon />} color="secondary">
        Back to Blog
      </Button>
    </Box>
  );

  return (
    <Box sx={{ py: 4, maxWidth: 1100, mx: 'auto', display: 'flex', gap: 5, alignItems: 'flex-start' }}>

      {/* Main content */}
      <Box sx={{ flex: 1, minWidth: 0 }}>
        <Button component={RouterLink} to="/blog" startIcon={<ArrowBackIcon />} color="secondary" sx={{ mb: 3 }}>
          Back to Blog
        </Button>

        {post.main_image && (
          <Box
            component="img"
            src={post.main_image}
            alt={post.title}
            sx={{ width: '100%', maxHeight: 400, objectFit: 'cover', borderRadius: 2, display: 'block', mb: 3 }}
          />
        )}

        <Stack direction="row" flexWrap="wrap" gap={0.5} sx={{ mb: 1.5 }}>
          <Chip
            label={new Date(post.published_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
            size="small"
            variant="outlined"
            color="secondary"
          />
          {post.categories.map(cat => (
            <Chip
              key={cat.slug}
              label={cat.name}
              size="small"
              variant="outlined"
              component={RouterLink}
              to={`/blog/category/${cat.slug}`}
              clickable
            />
          ))}
        </Stack>

        <Typography variant="h4" fontWeight={800} gutterBottom>{post.title}</Typography>
        {post.excerpt && (
          <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 2 }}>
            {post.excerpt}
          </Typography>
        )}

        <Divider sx={{ mb: 4 }} />

        <Box
          sx={{ color: 'text.primary', lineHeight: 1.8, '& p': { mb: 2 }, '& h2,h3': { mt: 3, mb: 1 } }}
          dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(post.content) }}
        />

        {post.author && <AuthorCard author={post.author} />}
      </Box>

      {/* Sidebar */}
      <Sidebar related={related} />

    </Box>
  );
}

export default BlogPostPage;
