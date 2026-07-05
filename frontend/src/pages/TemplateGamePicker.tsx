import { useState, useEffect } from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { apiURL, staticRoot } from '../api';
import { TemplateData } from '../types';
import GameBrowser, { Category, Game } from '../GameBrowser';

function TemplateGamePicker() {
  const { template } = useParams();
  const templateName = template as string;
  const navigate = useNavigate();

  const [templateMeta, setTemplateMeta] = useState<TemplateData | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    document.title = `Top8er | ${templateName}`;
  }, [templateName]);

  useEffect(() => {
    setLoading(true);
    // Fetched by exact name (not the browsable /templates/ list) so hidden
    // templates still resolve correctly when reached directly via their link.
    Promise.all([
      fetch(apiURL + '/template_data/' + templateName + '/').then(r => r.json()),
      fetch(apiURL + '/games/').then(r => r.json()),
    ]).then(([tmplData, gamesData]: [TemplateData, Category[]]) => {
      setTemplateMeta(tmplData);
      setCategories(gamesData);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [templateName]);

  const requiresIcons = templateMeta?.requiresIcons ?? false;

  const handleGameClick = (game: Game) => {
    navigate(`/template/${templateName}/game/${game.slug || game.path}`);
  };

  return (
    <Box sx={{ py: { xs: 2, sm: 4 }, px: { xs: 1, sm: 0 }, maxWidth: 1000, mx: 'auto' }}>

      {/* Selected template */}
      <Paper variant="outlined" sx={{ p: { xs: 1.5, sm: 2 }, mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Box
          component="img"
          src={`${staticRoot}/static/template_samples/${templateName}.png`}
          alt={templateMeta?.label ?? templateName}
          sx={{ width: { xs: 60, sm: 80 }, height: 'auto', borderRadius: 0.5, flexShrink: 0 }}
          onError={(e: React.SyntheticEvent<HTMLImageElement>) => {
            e.currentTarget.style.display = 'none';
          }}
        />
        <Box>
          <Typography variant="overline" color="text.secondary" letterSpacing={1} display="block">
            Template
          </Typography>
          <Typography variant="h6">{templateMeta?.label ?? templateName}</Typography>
        </Box>
      </Paper>

      <Typography variant="overline" color="text.secondary" letterSpacing={1} display="block" mb={1}>
        Pick a game
      </Typography>
      {requiresIcons && (
        <Typography variant="caption" color="text.disabled" sx={{ fontStyle: 'italic', display: 'block', mb: 1 }}>
          Only games with icon support are shown
        </Typography>
      )}

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

export default TemplateGamePicker;
