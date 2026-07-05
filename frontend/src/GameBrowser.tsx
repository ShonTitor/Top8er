import { useState } from 'react';
import {
  Box, Typography, TextField, Paper, CircularProgress, InputAdornment, Tabs, Tab, Tooltip,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { staticRoot } from './api';

export interface Game {
  slug: string;
  path: string;
  full_name: string;
  hasIcons: boolean;
}

export interface Category {
  category_name: string;
  games: Game[];
}

function GameCard({ game, onClick }: { game: Game; onClick: () => void }) {
  const logoSrc = `${staticRoot}/static/logos/${game.path}.png`;

  return (
    <Tooltip title={game.full_name} placement="top" enterDelay={400}>
      <Paper
        variant="outlined"
        onClick={onClick}
        sx={{
          width: '100%',
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
          sx={{ width: '100%', maxWidth: 64, height: 64, objectFit: 'contain', display: 'block' }}
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

interface GameBrowserProps {
  categories: Category[];
  loading: boolean;
  requiresIcons: boolean;
  onSelect: (game: Game) => void;
}

function GameBrowser({ categories, loading, requiresIcons, onSelect }: GameBrowserProps) {
  const [search, setSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState(0);

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
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs
                value={activeCategory}
                onChange={(_, v) => setActiveCategory(v)}
                variant="scrollable"
                scrollButtons="auto"
                allowScrollButtonsMobile
                textColor="secondary"
                indicatorColor="secondary"
                sx={{ px: 1 }}
              >
                {categories.map(cat => {
                  const count = filterGames(cat.games).length;
                  return (
                    <Tab
                      key={cat.category_name}
                      label={`${cat.category_name} (${count})`}
                      sx={{ fontSize: { xs: 11, sm: 13 }, minWidth: { xs: 'auto', sm: 90 }, px: { xs: 1, sm: 2 } }}
                    />
                  );
                })}
              </Tabs>
            </Box>
          )}

          {isSearching && (
            <Typography variant="caption" color="text.secondary" sx={{ px: 2, pt: 1, display: 'block' }}>
              {searchResults.length} result{searchResults.length !== 1 ? 's' : ''}
            </Typography>
          )}

          <Box
            sx={{
              p: { xs: 1, sm: 2 },
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(80px, 1fr))',
              gap: 1,
              minHeight: 160,
              alignContent: 'flex-start',
            }}
          >
            {currentGames.length === 0 ? (
              <Typography color="text.disabled" sx={{ alignSelf: 'center', mx: 'auto', py: 4, gridColumn: '1 / -1' }}>
                No games found
              </Typography>
            ) : (
              currentGames.map(game => (
                <GameCard
                  key={game.path}
                  game={game}
                  onClick={() => onSelect(game)}
                />
              ))
            )}
          </Box>
        </>
      )}
    </Paper>
  );
}

export default GameBrowser;
