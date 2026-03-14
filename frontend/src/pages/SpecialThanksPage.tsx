import { Box, Typography, Divider, Paper, Chip, Link } from '@mui/material';
import FavoriteIcon from '@mui/icons-material/Favorite';

interface Contributor {
  handle: string;
  contribution: string;
  link?: string;
}

const CONTRIBUTORS: Contributor[] = [
  { handle: '@Elenriqu3', contribution: 'Original Top 8 template design', link: 'https://twitter.com/Elenriqu3' },
  { handle: 'SleepDistorted', contribution: 'Top8er logo', link: 'https://www.youtube.com/@sleepDistorted' },
];

const PLATFORMS = [
  'start.gg',
  'Challonge',
  'Tonamel',
  'ParryGG',
];

const COMMUNITIES = [
  'The fighting game community (FGC), especially the Venezuelan FGC',
  'Platform fighter scenes worldwide',
  'TCG tournament organizers',
  'All the people who have contributed assets to add games to Top8er',
  'Everyone who has used Top8er at their events',
];

const USBESTIES = ['3rdStrike', 'Avend', 'CartezSoul', 'Luigic7'];

function SpecialThanksPage() {
  return (
    <Box sx={{ py: 4, maxWidth: 780, mx: 'auto' }}>

      <Box sx={{ mb: 4 }}>
        <Typography variant="overline" color="secondary" letterSpacing={2}>Credits</Typography>
        <Typography variant="h4" fontWeight={800} gutterBottom>
          Special Thanks
        </Typography>
        <Typography color="text.secondary">
          Top8er wouldn't exist without the contributions of these people and communities.
        </Typography>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {/* Contributors */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" fontWeight={700} mb={2}>Contributors</Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
          {CONTRIBUTORS.map(c => (
            <Paper key={c.handle} variant="outlined" sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
              <FavoriteIcon sx={{ color: 'secondary.main', flexShrink: 0 }} fontSize="small" />
              <Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  {c.link ? (
                    <Link href={c.link} target="_blank" rel="noopener" color="secondary" variant="subtitle2" fontWeight={700}>
                      {c.handle}
                    </Link>
                  ) : (
                    <Typography variant="subtitle2" fontWeight={700}>{c.handle}</Typography>
                  )}
                </Box>
                <Typography variant="body2" color="text.secondary">{c.contribution}</Typography>
              </Box>
            </Paper>
          ))}
        </Box>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {/* Tournament platforms */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" fontWeight={700} mb={1}>Tournament Platforms</Typography>
        <Typography variant="body2" color="text.secondary" mb={2}>
          Thanks to these platforms for providing APIs that make tournament import possible.
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {PLATFORMS.map(p => (
            <Chip key={p} label={p} variant="outlined" color="secondary" size="small" />
          ))}
        </Box>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {/* USBesties */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" fontWeight={700} mb={1}>USBesties</Typography>
        <Typography variant="body2" color="text.secondary" mb={2}>
          My besties from university — including but not limited to:
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {USBESTIES.map(name => (
            <Chip key={name} label={name} variant="outlined" color="secondary" size="small" />
          ))}
        </Box>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {/* Community */}
      <Box>
        <Typography variant="h6" fontWeight={700} mb={1}>The Community</Typography>
        <Box
          component="ul"
          sx={{ m: 0, pl: 3, color: 'text.secondary', '& li': { mb: 0.75 } }}
        >
          {COMMUNITIES.map(c => (
            <li key={c}><Typography variant="body2" color="text.secondary">{c}</Typography></li>
          ))}
        </Box>
      </Box>

    </Box>
  );
}

export default SpecialThanksPage;
