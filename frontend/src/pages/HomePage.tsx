import { useState, useEffect } from 'react';
import {
  Box, Typography, ToggleButton, ToggleButtonGroup, TextField,
  Paper, CircularProgress, InputAdornment, Tabs, Tab, Tooltip,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/top8er_square_white.svg';

interface Game {
  slug: string;
  path: string;
  full_name: string;
  hasIcons: boolean;
}

interface Category {
  category_name: string;
  games: Game[];
}

interface TemplateMeta {
  name: string;
  label: string;
  player_number: number;
  requiresIcons: boolean;
}

function GameCard({ game, onClick }: { game: Game; onClick: () => void }) {
  const apiURL = import.meta.env.VITE_TOP8ER_API_URL as string;
  // Strip "/api" suffix to get the static root
  const staticRoot = apiURL.replace(/\/api$/, '');
  const logoSrc = `${staticRoot}/static/logos/${game.path}.png`;

  return (
    <Tooltip title={game.full_name} placement="top" enterDelay={400}>
      <Paper
        variant="outlined"
        onClick={onClick}
        sx={{
          width: 88,
          cursor: 'pointer',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          p: 0.75,
          gap: 0.5,
          transition: 'border-color 0.15s, background-color 0.15s',
          '&:hover': {
            borderColor: 'secondary.main',
            bgcolor: 'rgba(0,139,139,0.08)',
          },
        }}
      >
        <Box
          component="img"
          src={logoSrc}
          alt={game.full_name}
          sx={{ width: 64, height: 64, objectFit: 'contain', display: 'block' }}
          onError={(e: React.SyntheticEvent<HTMLImageElement>) => {
            e.currentTarget.style.display = 'none';
          }}
        />
        <Typography
          variant="caption"
          align="center"
          sx={{
            fontSize: 10,
            lineHeight: 1.2,
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
            color: 'text.secondary',
          }}
        >
          {game.full_name}
        </Typography>
      </Paper>
    </Tooltip>
  );
}

function HomePage() {
  const apiURL = import.meta.env.VITE_TOP8ER_API_URL as string;
  const staticRoot = apiURL.replace(/\/api$/, '');
  const navigate = useNavigate();

  const [templates, setTemplates] = useState<TemplateMeta[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedTemplate, setSelectedTemplate] = useState('top8er');
  const [search, setSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState(0);

  useEffect(() => {
    Promise.all([
      fetch(apiURL + '/templates/').then(r => r.json()),
      fetch(apiURL + '/games/').then(r => r.json()),
    ]).then(([tmplData, gamesData]: [TemplateMeta[], Category[]]) => {
      setTemplates(tmplData);
      if (tmplData.length > 0) setSelectedTemplate(tmplData[0].name);
      setCategories(gamesData);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const selectedTemplateMeta = templates.find(t => t.name === selectedTemplate);
  const requiresIcons = selectedTemplateMeta?.requiresIcons ?? false;

  const handleTemplateChange = (_: React.MouseEvent, val: string | null) => {
    if (val) setSelectedTemplate(val);
  };

  const handleGameClick = (game: Game) => {
    navigate(`/beta/template/${selectedTemplate}/game/${game.slug || game.path}`);
  };

  const isSearching = search.trim().length > 0;

  const filterGames = (games: Game[]) =>
    requiresIcons ? games.filter(g => g.hasIcons) : games;

  const searchResults: Game[] = isSearching
    ? filterGames(categories.flatMap(c => c.games)).filter(g =>
        g.full_name.toLowerCase().includes(search.toLowerCase())
      )
    : [];

  const currentGames = isSearching
    ? searchResults
    : filterGames(categories[activeCategory]?.games ?? []);

  return (
    <Box sx={{ py: 4, maxWidth: 1000, mx: 'auto' }}>

      {/* Hero */}
      <Box sx={{ textAlign: 'center', mb: 5 }}>
        <Box
          component="img"
          src={logo}
          alt="Top8er logo"
          sx={{ width: 80, height: 80, mb: 2, opacity: 0.9 }}
        />
        <Typography variant="h3" fontWeight={800} letterSpacing={2} gutterBottom>
          Top8er.com
        </Typography>
        <Typography variant="h6" color="text.secondary" fontWeight={300}>
          Tournament graphic generator for the competitive gaming community
        </Typography>
      </Box>

      {/* Template selector */}
      <Paper variant="outlined" sx={{ p: 2, mb: 3 }}>
        <Typography variant="overline" color="text.secondary" display="block" mb={1.5} letterSpacing={1}>
          Template
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
          <AutoFixHighIcon color="secondary" />
          <ToggleButtonGroup
            value={selectedTemplate}
            exclusive
            onChange={handleTemplateChange}
            size="small"
          >
            {templates.map(t => (
              <ToggleButton key={t.name} value={t.name} sx={{ px: 1.5, py: 0.75, flexDirection: 'column', gap: 0.5 }}>
                <Box
                  component="img"
                  src={`${staticRoot}/static/template_samples/${t.name}.png`}
                  alt={t.label}
                  sx={{ width: 120, height: 'auto', display: 'block', borderRadius: 0.5 }}
                  onError={(e: React.SyntheticEvent<HTMLImageElement>) => {
                    e.currentTarget.style.display = 'none';
                  }}
                />
                <Typography variant="caption" sx={{ fontSize: 11, lineHeight: 1 }}>
                  {t.label}
                </Typography>
              </ToggleButton>
            ))}
          </ToggleButtonGroup>
          {requiresIcons && (
            <Typography variant="caption" color="text.disabled" sx={{ fontStyle: 'italic' }}>
              Only games with icon support are shown
            </Typography>
          )}
        </Box>
      </Paper>

      {/* Game browser */}
      <Paper elevation={2} sx={{ overflow: 'hidden' }}>
        <Box sx={{ px: 2, pt: 2, pb: 1 }}>
          <TextField
            placeholder="Search games…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            size="small"
            fullWidth
            color="secondary"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            }}
          />
        </Box>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
            <CircularProgress color="secondary" />
          </Box>
        ) : (
          <>
            {!isSearching && (
              <Box sx={{ display: 'flex', alignItems: 'center', borderBottom: 1, borderColor: 'divider' }}>
                <Tabs
                  value={activeCategory}
                  onChange={(_, v) => setActiveCategory(v)}
                  variant="scrollable"
                  scrollButtons="auto"
                  textColor="secondary"
                  indicatorColor="secondary"
                  sx={{ px: 1, flex: 1 }}
                >
                  {categories.map(cat => {
                    const count = filterGames(cat.games).length;
                    return (
                      <Tab
                        key={cat.category_name}
                        label={`${cat.category_name} (${count})`}
                        sx={{ fontSize: 13 }}
                      />
                    );
                  })}
                </Tabs>
                <Typography variant="caption" color="text.secondary" sx={{ px: 2, whiteSpace: 'nowrap' }}>
                  {filterGames(categories.flatMap(c => c.games)).length} games
                </Typography>
              </Box>
            )}

            {isSearching && (
              <Typography variant="caption" color="text.secondary" sx={{ px: 2, pt: 1, display: 'block' }}>
                {searchResults.length} result{searchResults.length !== 1 ? 's' : ''}
              </Typography>
            )}

            <Box
              sx={{
                p: 2,
                display: 'flex',
                flexWrap: 'wrap',
                gap: 1,
                minHeight: 160,
                alignContent: 'flex-start',
              }}
            >
              {currentGames.length === 0 ? (
                <Typography color="text.disabled" sx={{ alignSelf: 'center', mx: 'auto', py: 4 }}>
                  No games found
                </Typography>
              ) : (
                currentGames.map(game => (
                  <GameCard
                    key={game.path}
                    game={game}
                    onClick={() => handleGameClick(game)}
                  />
                ))
              )}
            </Box>
          </>
        )}
      </Paper>
    </Box>
  );
}

export default HomePage;
