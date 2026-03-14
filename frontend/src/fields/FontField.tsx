import { useRef, useState } from 'react';
import {
  Box, Button, Chip, FormControl, InputLabel, MenuItem,
  ToggleButton, ToggleButtonGroup, Tooltip,
} from '@mui/material';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import FileUploadIcon from '@mui/icons-material/FileUpload';

type Mode = 'select' | 'upload';

interface FontFieldProps {
  field_data: any;
  value: any;
  onChange: (name: string, val: any, multipleIndex: any) => void;
}

function FontField({ field_data, value, onChange }: FontFieldProps) {
  const [mode, setMode] = useState<Mode>('select');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleModeChange = (_: React.MouseEvent, newMode: Mode | null) => {
    if (!newMode) return;
    setMode(newMode);
    onChange(field_data.name, null, field_data.multipleIndex);
    if (inputRef.current) inputRef.current.value = '';
  };

  const handleSelectChange = (e: SelectChangeEvent) => {
    const val = e.target.value === '__auto__' ? null : e.target.value;
    onChange(field_data.name, val, field_data.multipleIndex);
  };

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

  const fonts: string[] = field_data.options ?? [];

  const toggle = (
    <ToggleButtonGroup value={mode} exclusive onChange={handleModeChange} size="small">
      <Tooltip title="Select from list">
        <ToggleButton value="select" sx={{ px: 0.75, py: 0.25 }}>
          <FormatListBulletedIcon fontSize="small" />
        </ToggleButton>
      </Tooltip>
      <Tooltip title="Upload font file">
        <ToggleButton value="upload" sx={{ px: 0.75, py: 0.25 }}>
          <FileUploadIcon fontSize="small" />
        </ToggleButton>
      </Tooltip>
    </ToggleButtonGroup>
  );

  const header = (
    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.75 }}>
      <Box sx={{ fontSize: 12, color: 'text.secondary', fontWeight: 500, letterSpacing: 0.5 }}>
        {field_data.label}
      </Box>
      {toggle}
    </Box>
  );

  if (mode === 'select') {
    return (
      <Box sx={{ width: 1, my: 1 }}>
        {header}
        <FormControl fullWidth>
          <InputLabel color="secondary">Font</InputLabel>
          <Select
            label="Font"
            value={value ?? '__auto__'}
            onChange={handleSelectChange}
            color="secondary"
          >
            <MenuItem value="__auto__"><em>Auto</em></MenuItem>
            {fonts.map((f: string, i: number) => (
              <MenuItem key={i} value={f}>{f}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
    );
  }

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
          <input ref={inputRef} type="file" hidden onChange={handleFileChange} accept=".ttf,.otf,.woff,.woff2" />
        </Button>
        {value?.name
          ? <Chip label={value.name} onDelete={handleFileDelete} variant="outlined" size="small" sx={{ minWidth: 0, flex: 1 }} />
          : <Box sx={{ color: 'text.disabled', fontSize: 13, flex: 1 }}>No file chosen</Box>
        }
      </Box>
    </Box>
  );
}

export default FontField;
