import { Box, Typography, Paper, Divider, Link, Avatar } from '@mui/material';
import CodeIcon from '@mui/icons-material/Code';
import BrushIcon from '@mui/icons-material/Brush';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';

interface Person {
  handle: string;
  role: string;
  description: string;
  links: { label: string; href: string }[];
  icon: React.ReactNode;
}

const TEAM: Person[] = [
  {
    handle: '@Riokaru',
    role: 'Developer',
    description: 'Built and maintains Top8er. Full-stack development, backend image generation, tournament API integrations, and the React frontend.',
    links: [
      { label: 'Twitter / X', href: 'https://twitter.com/Riokaru' },
      { label: 'Ko-fi', href: 'https://ko-fi.com/riokaru' },
      { label: 'Patreon', href: 'https://www.patreon.com/Riokaru' },
    ],
    icon: <CodeIcon />,
  },
  {
    handle: '@Elenriqu3',
    role: 'Original Template Designer',
    description: 'Designed the original Top8er graphic template that started it all. The iconic layout used by hundreds of tournaments.',
    links: [
      { label: 'Twitter / X', href: 'https://twitter.com/Elenriqu3' },
    ],
    icon: <BrushIcon />,
  },
];

function PersonCard({ person }: { person: Person }) {
  return (
    <Paper
      variant="outlined"
      sx={{ p: 2.5, display: 'flex', gap: 2, alignItems: 'flex-start' }}
    >
      <Avatar sx={{ bgcolor: 'secondary.main', width: 48, height: 48, flexShrink: 0 }}>
        {person.icon}
      </Avatar>
      <Box>
        <Typography variant="subtitle1" fontWeight={700}>{person.handle}</Typography>
        <Typography variant="caption" color="secondary.main" letterSpacing={1} display="block" mb={1}>
          {person.role.toUpperCase()}
        </Typography>
        <Typography variant="body2" color="text.secondary" mb={1.5}>
          {person.description}
        </Typography>
        <Box sx={{ display: 'flex', gap: 1.5, flexWrap: 'wrap' }}>
          {person.links.map(l => (
            <Link key={l.label} href={l.href} target="_blank" rel="noopener" color="secondary" variant="body2">
              {l.label}
            </Link>
          ))}
        </Box>
      </Box>
    </Paper>
  );
}

function AboutPage() {
  return (
    <Box sx={{ py: 4, maxWidth: 780, mx: 'auto' }}>

      <Box sx={{ mb: 4 }}>
        <Typography variant="overline" color="secondary" letterSpacing={2}>About</Typography>
        <Typography variant="h4" fontWeight={800} gutterBottom>
          What is Top8er?
        </Typography>
        <Typography color="text.secondary" mb={2}>
          Top8er is a free, browser-based tournament graphic generator for the competitive
          gaming community. Upload your player data — or import directly from start.gg,
          Challonge, Tonamel, or ParryGG — and generate a polished top 8 (or top 6, top 1)
          graphic in seconds.
        </Typography>
        <Typography color="text.secondary">
          No software to install, no account required. Just pick your game, fill in the
          players, and download the image.
        </Typography>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {/* Features */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" fontWeight={700} mb={2}>Features</Typography>
        <Box
          component="ul"
          sx={{ m: 0, pl: 3, color: 'text.secondary', '& li': { mb: 0.75 } }}
        >
          <li>Support for 100+ games across fighting games, platform fighters, TCGs, and more</li>
          <li>Multiple template styles (Top 8, Top 8 2023, Top 6, Top 1)</li>
          <li>Direct tournament import from start.gg, Challonge, Tonamel, and ParryGG</li>
          <li>Custom character art — select from the game's roster, upload your own, or link an image</li>
          <li>Country and pride flag support for player nationality display</li>
          <li>Fully free and open source</li>
        </Box>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {/* Team */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" fontWeight={700} mb={2}>The Team</Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {TEAM.map(p => <PersonCard key={p.handle} person={p} />)}
        </Box>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {/* Community */}
      <Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
          <SportsEsportsIcon color="secondary" />
          <Typography variant="h6" fontWeight={700}>Open Source</Typography>
        </Box>
        <Typography color="text.secondary" mb={1.5}>
          Top8er is open source and welcomes contributions — new game data, template fixes,
          or bug reports are all appreciated.
        </Typography>
        <Link
          href="https://github.com/ShonTitor/Top8er"
          target="_blank"
          rel="noopener"
          color="secondary"
        >
          View on GitHub
        </Link>
      </Box>

    </Box>
  );
}

export default AboutPage;
