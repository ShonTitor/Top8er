import { useRef, useState } from 'react';
import {
  Box, Button, Chip, CircularProgress, FormControl, InputLabel, MenuItem,
  TextField, ToggleButton, ToggleButtonGroup, Tooltip,
} from '@mui/material';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import LinkIcon from '@mui/icons-material/Link';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

type Mode = 'list' | 'upload' | 'link';

interface CharacterFieldProps {
  field_data: any;
  value: any;
  onChange: (...args: any[]) => void;
}

function ModeToggle({ mode, onChange }: { mode: Mode; onChange: (_: React.MouseEvent, v: Mode | null) => void }) {
  return (
    <ToggleButtonGroup value={mode} exclusive onChange={onChange} size="small">
      <Tooltip title="Select from list">
        <ToggleButton value="list" sx={{ px: 0.75, py: 0.25 }}>
          <FormatListBulletedIcon fontSize="small" />
        </ToggleButton>
      </Tooltip>
      <Tooltip title="Upload image">
        <ToggleButton value="upload" sx={{ px: 0.75, py: 0.25 }}>
          <FileUploadIcon fontSize="small" />
        </ToggleButton>
      </Tooltip>
      <Tooltip title="Image link">
        <ToggleButton value="link" sx={{ px: 0.75, py: 0.25 }}>
          <LinkIcon fontSize="small" />
        </ToggleButton>
      </Tooltip>
    </ToggleButtonGroup>
  );
}

function CharacterField({ field_data, value, onChange }: CharacterFieldProps) {
  // All hooks at the top — Rules of Hooks
  const [mode, setMode] = useState<Mode>('list');
  const [linkUrl, setLinkUrl] = useState('');
  const [linkStatus, setLinkStatus] = useState<'idle' | 'loading' | 'ok' | 'error'>('idle');
  const inputRef = useRef<HTMLInputElement>(null);

  if (!field_data.characters) {
    return <></>;
  }

  const characters: string[] = field_data.required
    ? field_data.characters
    : ['None'].concat(field_data.characters);

  const handleModeChange = (_: React.MouseEvent, newMode: Mode | null) => {
    if (!newMode) return;
    setMode(newMode);
    setLinkUrl('');
    setLinkStatus('idle');
    onChange(field_data.name, null);
    if (inputRef.current) inputRef.current.value = '';
  };

  // — List mode —
  const char = value?.[0] ?? characters[0];
  const color = value?.[1] ?? 0;
  const hasColors = !!field_data.colors?.[char] && field_data.colors[char].length > 1;
  const colors: string[] | undefined = hasColors ? field_data.colors[char] : undefined;

  const handleChangeChar = (e: SelectChangeEvent) => {
    onChange(field_data.name, e.target.value === 'None' ? null : [e.target.value, 0]);
  };

  const handleChangeColor = (e: SelectChangeEvent) => {
    onChange(field_data.name, [value[0], e.target.value]);
  };

  // — Upload mode —
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      const result = reader.result as string;
      const base64 = result.includes(',') ? result.split(',')[1] : result;
      onChange(field_data.name, { base64, name: file.name });
    };
  };

  const handleFileDelete = () => {
    onChange(field_data.name, null);
    if (inputRef.current) inputRef.current.value = '';
  };

  // — Link mode —
  const fetchAsBase64 = async (url: string) => {
    if (!url) return;
    setLinkStatus('loading');
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error();
      const blob = await res.blob();
      const base64 = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = () => {
          const result = reader.result as string;
          resolve(result.includes(',') ? result.split(',')[1] : result);
        };
        reader.onerror = reject;
      });
      const name = url.split('/').pop() || 'image';
      onChange(field_data.name, { base64, name });
      setLinkStatus('ok');
    } catch {
      onChange(field_data.name, null);
      setLinkStatus('error');
    }
  };

  const handleLinkChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLinkUrl(e.target.value);
    setLinkStatus('idle');
    onChange(field_data.name, null);
  };

  const handleLinkBlur = () => fetchAsBase64(linkUrl);
  const handleLinkKeyDown = (e: React.KeyboardEvent) => { if (e.key === 'Enter') fetchAsBase64(linkUrl); };

  const toggle = <ModeToggle mode={mode} onChange={handleModeChange} />;
  const header = (
    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.75 }}>
      <Box sx={{ fontSize: 12, color: 'text.secondary', fontWeight: 500, letterSpacing: 0.5 }}>
        {field_data.label}
      </Box>
      {toggle}
    </Box>
  );

  if (mode === 'list') {
    return (
      <Box sx={{ width: 1, my: 1 }}>
        {header}
        <Box sx={{ display: 'flex', gap: 1 }}>
          <FormControl fullWidth>
            <InputLabel color="secondary">Character</InputLabel>
            <Select
              label="Character"
              value={char}
              name={field_data.name}
              onChange={handleChangeChar}
            >
              {characters.map((c: string, i: number) => (
                <MenuItem key={i} value={c}>{c}</MenuItem>
              ))}
            </Select>
          </FormControl>
          {hasColors && colors && (
            <FormControl fullWidth>
              <InputLabel color="secondary">Color</InputLabel>
              <Select
                label="Color"
                value={color}
                name={field_data.name + '_color'}
                onChange={handleChangeColor}
              >
                {colors.map((c: string, i: number) => (
                  <MenuItem key={i} value={i}>{c}</MenuItem>
                ))}
              </Select>
            </FormControl>
          )}
        </Box>
      </Box>
    );
  }

  if (mode === 'upload') {
    return (
      <Box sx={{ width: 1, my: 1 }}>
        {header}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Button
            variant="outlined"
            component="label"
            color="secondary"
            startIcon={<FileUploadIcon />}
            sx={{ flexShrink: 0 }}
          >
            Choose file
            <input ref={inputRef} type="file" hidden onChange={handleFileChange} accept="image/*" />
          </Button>
          {value?.name
            ? <Chip label={value.name} onDelete={handleFileDelete} variant="outlined" size="small" sx={{ minWidth: 0, flex: 1 }} />
            : <Box sx={{ color: 'text.disabled', fontSize: 13, flex: 1 }}>No file chosen</Box>
          }
        </Box>
      </Box>
    );
  }

  const linkAdornment = {
    idle: null,
    loading: <CircularProgress size={18} color="secondary" />,
    ok: <CheckCircleOutlineIcon fontSize="small" color="success" />,
    error: <Tooltip title="Could not load image (check URL or CORS)"><ErrorOutlineIcon fontSize="small" color="error" /></Tooltip>,
  }[linkStatus];

  return (
    <Box sx={{ width: 1, my: 1 }}>
      {header}
      <TextField
        value={linkUrl}
        onChange={handleLinkChange}
        onBlur={handleLinkBlur}
        onKeyDown={handleLinkKeyDown}
        placeholder="https://..."
        variant="outlined"
        color="secondary"
        fullWidth
        InputProps={{ endAdornment: linkAdornment }}
      />
    </Box>
  );
}

export default CharacterField;
