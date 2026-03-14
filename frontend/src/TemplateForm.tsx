import { useState, useEffect, useMemo, useCallback, FormEvent } from 'react';
import { Button, Divider, Grid, Paper, TextField, CircularProgress, Alert, Typography } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { Box } from '@mui/system';
import { LinearProgress } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import Top8erFieldAccordion from './fields/Top8erFieldAccordion';
import { useParams } from "react-router-dom";
import { TemplateData, GameData, FormState, PageState, Field, ApiError } from './types';
import { buildPlayerFields, buildInitialState } from './utils';

const flags = [
  'Abkhazia', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antartica',
  'Antigua and Barbuda', 'Argentina', 'Armenia', 'Artsakh', 'Australia', 'Austria',
  'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium',
  'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil',
  'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada',
  'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia',
  'Comoros', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic',
  'Democratic Republic of Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic',
  'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
  'Eswatini', 'Ethiopia', 'Federated States of Micronesia', 'Fiji', 'Finland', 'France',
  'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala',
  'Guinea-Bissau', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India',
  'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan',
  'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia',
  'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar',
  'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius',
  'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
  'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'North Korea',
  'North Macedonia', 'Northern Cyprus', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama',
  'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar',
  'Republic of China (Taiwan)', 'Republic of Congo', 'Romania', 'Russia', 'Rwanda',
  'Sahrawi Arab Democratic Republic', 'Saint Kitts and Nevis', 'Saint Lucia',
  'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Saudi Arabia', 'Scania', 'Scotland',
  'Senegal', 'Serbia',
  'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia',
  'Somaliland', 'South Africa', 'South Korea', 'South Ossetia', 'South Sudan', 'Spain', 'Sri Lanka',
  'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'São Tomé and Príncipe', 'Tajikistan',
  'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Transnistria', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
  'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States',
  'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Wales', 'Yemen', 'Zambia', 'Zimbabwe',
  'Agender Pride', 'Aromantic Pride', 'Asexual Pride', 'Bigender Pride', 'Bisexual Pride', 'Demiromantic Pride',
  'Demisexual Pride', 'Gay Pride', 'Gender Fluid', 'Genderqueer Pride', 'Intersex Pride', 'Lesbian Pride',
  'Non-binary', 'Pansexual Pride', 'Polyamory Pride', 'Polysexual Pride', 'Transgender Pride'
];

const tournamentUrlPatterns = [
  /^https:\/\/(www\.)?(smash|start)\.gg\/(tournament\/)?[^/]+\/event\/[^/]+/,
  /^https:\/\/([^.]*\.)?challonge\.com\/.+/,
  /^https:\/\/tonamel\.com\/competition\/[^/]+/,
  /^https:\/\/parry\.gg\/[^/]+\/[^/]+/,
];
const isValidTournamentUrl = (url: string) => tournamentUrlPatterns.some(re => re.test(url));

function TemplateForm() {
  const [formState, setFormState] = useState<FormState>({ players: [], options: {} });
  const [pageState, setPageState] = useState<PageState>({
    success: true,
    errors: [],
    loading: false,
    result_img_src: ""
  });
  const { template, gameName } = useParams();
  const templateName = template as string;

  useEffect(() => {
    document.title = gameName ? `Top8er | ${gameName.toUpperCase()}` : 'Top8er | Graphic Generator';
  }, [gameName]);
  const [templateData, setTemplateData] = useState<TemplateData | null>(null);
  const [gameData, setGameData] = useState<GameData | null>(null);
  const theme = useTheme();
  const apiURL = import.meta.env.VITE_TOP8ER_API_URL;
  const staticRoot = (apiURL as string).replace(/\/api$/, '');

  useEffect(() => {
    fetch(apiURL + "/template_data/" + templateName + "/", {
      method: 'GET',
      headers: { 'Content-type': 'application/json; charset=UTF-8' }
    })
      .then((res) => res.json())
      .then((data) => {
        setTemplateData(data);
      })
      .catch(() => {
        setPageState(prev => ({ ...prev, success: false, errors: [{ scope: 'root', field: '', message: 'Failed to fetch template data' }] }));
      });
  }, [templateName]);

  useEffect(() => {
    fetch(apiURL + "/game_data/" + gameName + "/", {
      method: 'GET',
      headers: { 'Content-type': 'application/json; charset=UTF-8' }
    })
      .then((res) => res.json())
      .then((data) => {
        setGameData(data);
      })
      .catch(() => {});
  }, [gameName]);

  const [tournamentUrl, setTournamentUrl] = useState('');
  const [tournamentStatus, setTournamentStatus] = useState<'idle' | 'loading' | 'ok' | 'error'>('idle');
  const [tournamentError, setTournamentError] = useState('');

  const handleLoadTournament = async () => {
    if (!tournamentUrl) return;
    if (!isValidTournamentUrl(tournamentUrl)) {
      setTournamentStatus('error');
      setTournamentError('Unrecognized tournament URL. Supported: start.gg, challonge, tonamel, parry.gg');
      return;
    }
    setTournamentStatus('loading');
    setTournamentError('');
    try {
      const params = new URLSearchParams({ url: tournamentUrl, game: gameName ?? '' });
      const res = await fetch(`${apiURL}/tournament_data/?${params}`);
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error ?? 'Failed to load tournament data');
      }

      const playerAliases: Record<string, string[]> = templateData?.tournament_aliases?.player ?? {};
      const optionAliases: Record<string, string[]> = templateData?.tournament_aliases?.options ?? {};

      const applyAliases = (target: Record<string, any>, aliases: Record<string, string[]>, source: Record<string, any>) => {
        for (const [apiKey, candidates] of Object.entries(aliases)) {
          if (!(apiKey in source)) continue;
          const match = candidates.find(c => c in target);
          if (match) target[match] = source[apiKey];
        }
      };

      setFormState(prev => {
        const next = JSON.parse(JSON.stringify(prev));
        (data.players as any[]).forEach((apiPlayer: any, i: number) => {
          if (i >= next.players.length) return;
          applyAliases(next.players[i], playerAliases, apiPlayer);
          // Fix multiple fields (arrays of slots) that received a single value from the API
          const isCharTuple = (v: any) => Array.isArray(v) && v.length === 2 && typeof v[0] === 'string' && typeof v[1] === 'number';
          for (const key of Object.keys(next.players[i])) {
            const prevVal = prev.players[i][key];
            const nextVal = next.players[i][key];
            if (!Array.isArray(prevVal) || prevVal.length === 0) continue;
            if (nextVal === null) {
              // null → all slots null (= "None" for each slot)
              next.players[i][key] = prevVal.map(() => null);
            } else if (isCharTuple(nextVal)) {
              // Single char tuple → first slot filled, rest null
              next.players[i][key] = [nextVal, ...prevVal.slice(1).map(() => null)];
            }
          }
        });
        applyAliases(next.options, optionAliases, data);
        return next;
      });

      setTournamentStatus('ok');
    } catch (e: any) {
      setTournamentError(e.message ?? 'Unknown error');
      setTournamentStatus('error');
    }
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setPageState(prev => ({ ...prev, loading: true }));

    fetch(apiURL + "/generate/" + templateName + "/" + gameName + "/", {
      method: 'POST',
      body: JSON.stringify(formState),
      headers: { 'Content-type': 'application/json; charset=UTF-8' }
    })
      .then((res) => res.json())
      .then((data) => {
        if ("base64_img" in data) {
          const base64_img = data["base64_img"];
          setPageState(prev => ({
            ...prev,
            result_img_src: 'data:image/png;base64,' + base64_img,
            success: true,
            errors: [],
            loading: false
          }));
        } else {
          setPageState(prev => ({
            ...prev,
            success: false,
            errors: Array.isArray(data) ? data as ApiError[] : [{ scope: 'root' as const, field: '', message: JSON.stringify(data) }],
            loading: false
          }));
        }
      })
      .catch(() => {
        setPageState(prev => ({
          ...prev,
          success: false,
          errors: [{ scope: 'root', field: '', message: 'Server error. Please contact the administrator.' }],
          loading: false
        }));
      });
  };

  const readyLoading = !!(templateData && gameData);
  const playerNumber = readyLoading ? templateData.player_number : 0;
  const options = readyLoading ? templateData.options : [];
  const playerFields: Field[][] = useMemo(
    () => templateData && gameData ? buildPlayerFields(templateData, gameData, flags) : [],
    [templateData, gameData]
  );

  useEffect(() => {
    if (readyLoading && templateData && gameData) {
      setFormState(buildInitialState(playerFields, templateData, gameData, options));
    }
  }, [templateData, gameData]);

  const handleChange = useCallback((name: string, value: any, playerIndex?: number) => {
    setFormState(prev => {
      if (playerIndex !== undefined) {
        const players = [...prev.players];
        players[playerIndex] = value;
        return { ...prev, players };
      }
      return { ...prev, [name]: value };
    });
  }, []);

  if (!readyLoading) {
    return <></>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <Grid container alignItems="stretch" justifyContent="center" spacing={1}>
        {/* Left panel — player data */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ width: '100%', overflow: 'hidden' }}>
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                overflowY: 'auto',
                p: 1,
                gap: 0.5,
                '@media (min-width: 900px)': { height: 'calc(100vh - 128px)' },
              }}
            >
              {([...Array(playerNumber).keys()]).map((_field_data, i) => (
                <Top8erFieldAccordion
                  key={i}
                  playerIndex={i}
                  name="players"
                  summary={'Player ' + (i + 1)}
                  fields={playerFields[i]}
                  onChange={handleChange}
                  value={formState['players'][i]}
                  defaultExpanded={true}
                />
              ))}
              <Top8erFieldAccordion
                defaultExpanded={false}
                name="options"
                summary="Options"
                fields={templateData.options || []}
                onChange={handleChange}
                value={formState['options']}
                playerIndex={undefined}
              />
            </Box>
          </Paper>
        </Grid>

        {/* Right panel — controls + result */}
        <Grid item xs={12} md={6}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5, px: 1 }}>

            {/* Generate */}
            <Box>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={pageState.loading}
                startIcon={<AutoFixHighIcon />}
                sx={{ fontWeight: 700, letterSpacing: 1 }}
              >
                Generate
              </Button>
              <LinearProgress sx={{ mt: 0.5, visibility: pageState.loading ? 'visible' : 'hidden' }} />
            </Box>

            {/* Load from tournament */}
            <Paper variant="outlined" sx={{ p: 1.5 }}>
              <Typography variant="caption" sx={{ color: 'text.secondary', letterSpacing: 0.5, display: 'block' }}>
                LOAD FROM TOURNAMENT URL
              </Typography>
              <Typography variant="caption" sx={{ color: 'text.disabled', display: 'block', mb: 1 }}>
                Supports: start.gg · challonge · tonamel · parry.gg
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-start' }}>
                <TextField
                  placeholder="https://start.gg/..."
                  value={tournamentUrl}
                  onChange={e => { setTournamentUrl(e.target.value); setTournamentStatus('idle'); }}
                  onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); handleLoadTournament(); } }}
                  size="small"
                  color="secondary"
                  fullWidth
                />
                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={handleLoadTournament}
                  disabled={tournamentStatus === 'loading' || !tournamentUrl}
                  startIcon={tournamentStatus === 'loading' ? <CircularProgress size={16} color="inherit" /> : <DownloadIcon />}
                  sx={{ flexShrink: 0 }}
                >
                  Load
                </Button>
              </Box>
              {tournamentStatus === 'error' && (
                <Alert severity="error" sx={{ mt: 1 }}>{tournamentError}</Alert>
              )}
              {tournamentStatus === 'ok' && (
                <Alert severity="success" sx={{ mt: 1 }}>Tournament data loaded successfully</Alert>
              )}
            </Paper>

            {/* Result */}
            <Divider />
            {pageState.success ? (
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1 }}>
                <img
                  id="result-img"
                  style={{ maxWidth: '100%', objectFit: 'scale-down' }}
                  src={pageState.result_img_src || `${staticRoot}/static/template_samples/${templateName}.png`}
                />
                {pageState.result_img_src && (
                  <Button
                    variant="contained"
                    component="a"
                    href={pageState.result_img_src}
                    download="top8er.png"
                    startIcon={<DownloadIcon />}
                    sx={{ backgroundColor: '#5e0a00', '&:hover': { backgroundColor: '#7a0d00' } }}
                  >
                    Download Graphic
                  </Button>
                )}
              </Box>
            ) : (
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.75 }}>
                <Typography variant="h6" color="error" gutterBottom>An error occurred</Typography>
                {pageState.errors.map((err, idx) => {
                  let label = '';
                  if (err.scope === 'player_fields' && err.player_index !== undefined) {
                    label = `Player ${err.player_index + 1} · ${err.field}`;
                  } else if (err.scope === 'options') {
                    label = `Options · ${err.field}`;
                  }
                  return (
                    <Alert key={idx} severity="error" sx={{ py: 0 }}>
                      {label && <strong>{label}: </strong>}{err.message}
                    </Alert>
                  );
                })}
              </Box>
            )}
          </Box>
        </Grid>
      </Grid>
    </form>
  );
}

export default TemplateForm;
