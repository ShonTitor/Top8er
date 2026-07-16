import { useRef, useState } from 'react';
import {
  Box, Button, Chip, CircularProgress, TextField, ToggleButton, ToggleButtonGroup, Tooltip,
} from '@mui/material';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import LinkIcon from '@mui/icons-material/Link';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import { fetchImageUrlAsBase64 } from '../utils';

type Mode = 'upload' | 'link';

interface ImageFieldProps {
  field_data: any;
  value: any;
  onChange: (...args: any[]) => void;
}

function ModeToggle({ mode, onChange }: { mode: Mode; onChange: (_: React.MouseEvent, v: Mode | null) => void }) {
  return (
    <ToggleButtonGroup value={mode} exclusive onChange={onChange} size="small">
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

function ImageField({ field_data, value, onChange }: ImageFieldProps) {
  // All hooks at the top — Rules of Hooks
  const [mode, setMode] = useState<Mode>('upload');
  const [linkUrl, setLinkUrl] = useState('');
  const [linkStatus, setLinkStatus] = useState<'idle' | 'loading' | 'ok' | 'error'>('idle');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleModeChange = (_: React.MouseEvent, newMode: Mode | null) => {
    if (!newMode) return;
    setMode(newMode);
    setLinkUrl('');
    setLinkStatus('idle');
    onChange(field_data.name, null, field_data.multipleIndex);
    if (inputRef.current) inputRef.current.value = '';
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
      onChange(field_data.name, { base64, name: file.name }, field_data.multipleIndex);
    };
  };

  const handleFileDelete = () => {
    onChange(field_data.name, null, field_data.multipleIndex);
    if (inputRef.current) inputRef.current.value = '';
  };

  // — Link mode — fetched client-side and converted to base64, same as an
  // upload, so the server never has to fetch a user-supplied URL itself.
  // The original url is kept alongside the base64 (not sent to the server,
  // but used by the Saved Options preset mechanism: a url is a lightweight
  // reference it can store instead of the full embedded image when the
  // preset would otherwise be too large for localStorage).
  const fetchAsBase64 = async (url: string) => {
    if (!url) return;
    setLinkStatus('loading');
    try {
      const { base64, name } = await fetchImageUrlAsBase64(url);
      onChange(field_data.name, { base64, name, url }, field_data.multipleIndex);
      setLinkStatus('ok');
    } catch {
      onChange(field_data.name, null, field_data.multipleIndex);
      setLinkStatus('error');
    }
  };

  const handleLinkChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLinkUrl(e.target.value);
    setLinkStatus('idle');
    onChange(field_data.name, null, field_data.multipleIndex);
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

export default ImageField;
