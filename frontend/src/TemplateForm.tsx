import { useState, useEffect, useMemo, useCallback, FormEvent } from 'react';
import {
  Button, Divider, Grid, Paper, TextField, CircularProgress, Alert, Typography,
  FormControl, InputLabel, MenuItem, IconButton,
} from '@mui/material';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { useTheme } from '@mui/material/styles';
import { Box } from '@mui/system';
import { LinearProgress } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import SaveIcon from '@mui/icons-material/Save';
import RestoreIcon from '@mui/icons-material/Restore';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import Top8erFieldAccordion from './fields/Top8erFieldAccordion';
import { useParams } from "react-router-dom";
import { TemplateData, GameData, FormState, PageState, Field, ApiError } from './types';
import { buildPlayerFields, buildInitialState, fetchImageUrlAsBase64 } from './utils';
import { apiURL, staticRoot } from './api';


const tournamentUrlPatterns = [
  /^https:\/\/(www\.)?(smash|start)\.gg\/(tournament\/)?[^/]+\/event\/[^/]+/,
  /^https:\/\/([^.]*\.)?challonge\.com\/.+/,
  /^https:\/\/tonamel\.com\/competition\/[^/]+/,
  /^https:\/\/parry\.gg\/[^/]+\/[^/]+/,
  /^https:\/\/(play\.)?limitlesstcg\.com\/tournament\/[^/]+/,
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
  const [flags, setFlags] = useState<string[]>([]);
  const theme = useTheme();

  useEffect(() => {
    fetch(apiURL + "/flags/")
      .then(res => res.json())
      .then(data => setFlags(data))
      .catch(() => {});
  }, []);

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
      setTournamentError('Unrecognized tournament URL. Supported: start.gg, challonge, tonamel, parry.gg, limitlesstcg');
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
          const isCharTupleList = (v: any) => Array.isArray(v) && v.length > 0 && v.every(isCharTuple);
          for (const key of Object.keys(next.players[i])) {
            const prevVal = prev.players[i][key];
            const nextVal = next.players[i][key];
            if (!Array.isArray(prevVal) || prevVal.length === 0) continue;
            if (nextVal === null) {
              // null → all slots null (= "None" for each slot)
              next.players[i][key] = prevVal.map(() => null);
            } else if (isCharTupleList(nextVal)) {
              // Full team (e.g. a Pokemon decklist) → fill as many slots as
              // are available, leaving the rest null
              next.players[i][key] = prevVal.map((_: any, idx: number) => nextVal[idx] ?? null);
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

  // Saved Options presets are kept in localStorage as a name → options map,
  // namespaced per template so switching templates doesn't leak one
  // template's option values into another's (they don't necessarily share
  // the same option schema), and so each template can hold several
  // independently named presets rather than a single save slot.
  const savedOptionsKey = `top8er:savedOptions:${templateName}`;
  const [savedPresets, setSavedPresets] = useState<Record<string, any>>({});
  const [presetNameInput, setPresetNameInput] = useState('');
  const [selectedPreset, setSelectedPreset] = useState('');
  const [savedOptionsStatus, setSavedOptionsStatus] = useState<'idle' | 'saved' | 'savedNoImages' | 'loaded' | 'error'>('idle');
  const [savedOptionsError, setSavedOptionsError] = useState('');

  // An image-type option value is a plain {base64, name[, url]} object (see
  // ImageField). Only ones fetched via "Image link" mode carry a url.
  const isImageValue = (v: any) => !!v && typeof v === 'object' && !Array.isArray(v) && 'base64' in v;

  const readPresets = (): Record<string, any> => {
    const raw = localStorage.getItem(savedOptionsKey);
    if (!raw) return {};
    try {
      const parsed = JSON.parse(raw);
      return parsed && typeof parsed === 'object' ? parsed : {};
    } catch {
      return {};
    }
  };

  useEffect(() => {
    setSavedPresets(readPresets());
    setSelectedPreset('');
    setSavedOptionsStatus('idle');
  }, [savedOptionsKey]);

  const presetNames = Object.keys(savedPresets);

  const handleSavePreset = () => {
    const name = presetNameInput.trim();
    if (!name) return;

    const persist = (options: Record<string, any>) => {
      const next = { ...savedPresets, [name]: options };
      localStorage.setItem(savedOptionsKey, JSON.stringify(next));
      setSavedPresets(next);
      setSelectedPreset(name);
      setPresetNameInput('');
    };

    try {
      persist(formState.options);
      setSavedOptionsStatus('saved');
      return;
    } catch (e: any) {
      // Most commonly a quota error: uploaded/linked images are embedded as
      // base64 in the options, which can push a preset past localStorage's
      // per-origin size limit (~5-10MB).
      const isQuotaError = e && (e.name === 'QuotaExceededError' || e.name === 'NS_ERROR_DOM_QUOTA_REACHED');
      if (!isQuotaError) {
        setSavedOptionsError('Could not save preset to this browser.');
        setSavedOptionsStatus('error');
        return;
      }
    }

    // Retry with images slimmed down: a url-linked image is kept as just
    // its {url, name} (tiny) instead of the full embedded base64, and an
    // uploaded image with no url is dropped entirely since there's no
    // lightweight representation for it.
    const slimOptions: Record<string, any> = {};
    let droppedAny = false;
    for (const [key, val] of Object.entries(formState.options)) {
      if (isImageValue(val)) {
        if ((val as any).url) {
          slimOptions[key] = { url: (val as any).url, name: (val as any).name };
        } else {
          droppedAny = true;
        }
      } else {
        slimOptions[key] = val;
      }
    }

    try {
      persist(slimOptions);
      setSavedOptionsError(
        droppedAny
          ? 'Some uploaded images were too large to save locally and were left out. Use an image link (URL) instead of uploading so it can be included in saved presets.'
          : 'Images were saved as URL references instead of embedded copies to fit browser storage.'
      );
      setSavedOptionsStatus('savedNoImages');
    } catch {
      setSavedOptionsError('Could not save: browser storage limit reached even after removing images.');
      setSavedOptionsStatus('error');
    }
  };

  const handleLoadPreset = async () => {
    if (!selectedPreset || !(selectedPreset in savedPresets)) return;
    const preset = savedPresets[selectedPreset];

    // A saved value that's {url, name} with no base64 was slimmed down at
    // save time (see handleSavePreset) - re-fetch it now so the form has
    // real image data to submit, same as picking it in ImageField directly.
    const resolved: Record<string, any> = { ...preset };
    const urlOnlyEntries = Object.entries(preset).filter(
      ([, v]) => v && typeof v === 'object' && !Array.isArray(v) && (v as any).url && !(v as any).base64
    );
    if (urlOnlyEntries.length > 0) {
      await Promise.all(urlOnlyEntries.map(async ([key, v]) => {
        try {
          const { base64, name } = await fetchImageUrlAsBase64((v as any).url);
          resolved[key] = { base64, name, url: (v as any).url };
        } catch {
          // Can't reconstitute this one (dead link, CORS, etc.) - leave it
          // out rather than submitting a broken value.
          delete resolved[key];
        }
      }));
    }

    setFormState(prev => ({ ...prev, options: { ...prev.options, ...resolved } }));
    setSavedOptionsStatus('loaded');
  };

  const handleDeletePreset = () => {
    if (!selectedPreset) return;
    const next = { ...savedPresets };
    delete next[selectedPreset];
    localStorage.setItem(savedOptionsKey, JSON.stringify(next));
    setSavedPresets(next);
    setSelectedPreset('');
    setSavedOptionsStatus('idle');
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
    [templateData, gameData, flags]
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
    <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
      <Grid container alignItems="flex-start" justifyContent="center" spacing={1} sx={{ flex: 1 }}>
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
                // Sticks below the navbar+banner and caps its own height to
                // whatever viewport space remains. --chrome-height is the
                // *measured* (ResizeObserver, see Base.tsx) height of the
                // navbar+banner, so this stays correct regardless of how
                // tall that content happens to be — no guessed constants,
                // and (using alignItems="flex-start" above instead of
                // "stretch") this panel no longer forces the main content
                // column to match its height or vice versa.
                '@media (min-width: 900px)': {
                  position: 'sticky',
                  top: 'calc(var(--chrome-height, 64px) + 16px)',
                  maxHeight: 'calc(100vh - var(--chrome-height, 64px) - 32px)',
                },
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
              >
                {/* Save/load named Options presets locally */}
                <Paper data-testid="saved-options-panel" variant="outlined" sx={{ p: 1.5, width: 1, mb: 1 }}>
                  <Typography variant="caption" sx={{ color: 'text.secondary', letterSpacing: 0.5, display: 'block' }}>
                    SAVED OPTIONS (THIS BROWSER)
                  </Typography>
                  <Typography variant="caption" sx={{ color: 'text.disabled', display: 'block', mb: 1 }}>
                    Save this template's Options under a name to reload later, on this device only
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-start', mb: 1 }}>
                    <TextField
                      placeholder="Preset name"
                      value={presetNameInput}
                      onChange={e => setPresetNameInput(e.target.value)}
                      onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); handleSavePreset(); } }}
                      size="small"
                      color="secondary"
                      fullWidth
                    />
                    <Button
                      type="button"
                      variant="outlined"
                      color="secondary"
                      onClick={handleSavePreset}
                      disabled={!presetNameInput.trim()}
                      startIcon={<SaveIcon />}
                      sx={{ flexShrink: 0 }}
                    >
                      Save
                    </Button>
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                    <FormControl fullWidth size="small" disabled={presetNames.length === 0}>
                      <InputLabel id="saved-presets-label" color="secondary">Saved presets</InputLabel>
                      <Select
                        labelId="saved-presets-label"
                        label="Saved presets"
                        color="secondary"
                        value={selectedPreset}
                        onChange={(e: SelectChangeEvent) => { setSelectedPreset(e.target.value); setSavedOptionsStatus('idle'); }}
                      >
                        {presetNames.map(name => (
                          <MenuItem key={name} value={name}>{name}</MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                    <Button
                      type="button"
                      variant="outlined"
                      color="secondary"
                      onClick={handleLoadPreset}
                      disabled={!selectedPreset}
                      startIcon={<RestoreIcon />}
                      sx={{ flexShrink: 0 }}
                    >
                      Load
                    </Button>
                    <IconButton
                      type="button"
                      color="secondary"
                      onClick={handleDeletePreset}
                      disabled={!selectedPreset}
                      aria-label="Delete selected preset"
                    >
                      <DeleteOutlineIcon />
                    </IconButton>
                  </Box>
                  {savedOptionsStatus === 'saved' && (
                    <Alert severity="success" sx={{ mt: 1 }}>Preset saved to this browser</Alert>
                  )}
                  {savedOptionsStatus === 'savedNoImages' && (
                    <Alert severity="warning" sx={{ mt: 1 }}>{savedOptionsError}</Alert>
                  )}
                  {savedOptionsStatus === 'loaded' && (
                    <Alert severity="success" sx={{ mt: 1 }}>Saved preset loaded</Alert>
                  )}
                  {savedOptionsStatus === 'error' && (
                    <Alert severity="error" sx={{ mt: 1 }}>{savedOptionsError}</Alert>
                  )}
                </Paper>
              </Top8erFieldAccordion>
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
                Supports: start.gg · challonge · tonamel · parry.gg · limitlesstcg
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
                  type="button"
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
    </Box>
  );
}

export default TemplateForm;
