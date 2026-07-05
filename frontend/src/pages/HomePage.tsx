import { useState, useEffect } from 'react';
import {
  Box, Typography, ToggleButton, ToggleButtonGroup,
  Paper,
} from '@mui/material';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/top8er_square_white.svg';
import { apiURL, staticRoot } from '../api';
import GameBrowser, { Category, Game } from '../GameBrowser';

interface TemplateMeta {
  name: string;
  label: string;
  player_number: number;
  requiresIcons: boolean;
}

function HomePage() {
  useEffect(() => { document.title = 'Top8er | Tournament Graphic Generator'; }, []);
  const navigate = useNavigate();

  const [templates, setTemplates] = useState<TemplateMeta[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedTemplate, setSelectedTemplate] = useState('top8er');

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
    navigate(`/template/${selectedTemplate}/game/${game.slug || game.path}`);
  };

  return (
    <Box sx={{ py: { xs: 2, sm: 4 }, px: { xs: 1, sm: 0 }, maxWidth: 1000, mx: 'auto' }}>

      {/* Hero */}
      <Box sx={{ textAlign: 'center', mb: { xs: 3, sm: 5 } }}>
        <Box
          component="img"
          src={logo}
          alt="Top8er logo"
          sx={{ width: { xs: 60, sm: 80 }, height: { xs: 60, sm: 80 }, mb: 2, opacity: 0.9 }}
        />
        <Typography variant="h3" fontWeight={800} letterSpacing={2} gutterBottom
          sx={{ fontSize: { xs: '1.8rem', sm: '3rem' } }}
        >
          Top8er.com
        </Typography>
        <Typography variant="h6" color="text.secondary" fontWeight={300}
          sx={{ fontSize: { xs: '0.95rem', sm: '1.25rem' } }}
        >
          Tournament graphic generator for the competitive gaming community
        </Typography>
      </Box>

      {/* Template selector */}
      <Paper variant="outlined" sx={{ p: { xs: 1.5, sm: 2 }, mb: 3 }}>
        <Typography variant="overline" color="text.secondary" display="block" mb={1.5} letterSpacing={1}>
          Template
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1, flexWrap: 'wrap' }}>
          <AutoFixHighIcon color="secondary" sx={{ mt: 0.5 }} />
          <Box sx={{ overflowX: 'auto', flex: 1 }}>
            <ToggleButtonGroup
              value={selectedTemplate}
              exclusive
              onChange={handleTemplateChange}
              size="small"
              sx={{ flexWrap: 'nowrap' }}
            >
              {templates.map(t => (
                <ToggleButton key={t.name} value={t.name} sx={{ px: 1, py: 0.75, flexDirection: 'column', gap: 0.5 }}>
                  <Box
                    component="img"
                    src={`${staticRoot}/static/template_samples/${t.name}.png`}
                    alt={t.label}
                    sx={{ width: { xs: 80, sm: 120 }, height: 'auto', display: 'block', borderRadius: 0.5 }}
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
          </Box>
        </Box>
        {requiresIcons && (
          <Typography variant="caption" color="text.disabled" sx={{ fontStyle: 'italic', display: 'block', mt: 1 }}>
            Only games with icon support are shown
          </Typography>
        )}
      </Paper>

      {/* Game browser */}
      <GameBrowser
        categories={categories}
        loading={loading}
        requiresIcons={requiresIcons}
        onSelect={handleGameClick}
      />
    </Box>
  );
}

export default HomePage;
