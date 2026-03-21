import { useRef, useState } from 'react';
import {
  Box, Button, Chip, Divider, FormControl, InputLabel, MenuItem,
  ToggleButton, ToggleButtonGroup, Tooltip,
} from '@mui/material';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import FileUploadIcon from '@mui/icons-material/FileUpload';

type Mode = 'list' | 'upload';

interface SelectFieldProps {
  field_data: any;
  value: any;
  onChange: (name: string, val: string | null | { base64: string; name: string }, multipleIndex: any) => void;
}

function SelectField({ field_data, value, onChange }: SelectFieldProps) {
  const isUploaded = value && typeof value === 'object' && 'base64' in value;
  const [mode, setMode] = useState<Mode>(isUploaded ? 'upload' : 'list');
  const inputRef = useRef<HTMLInputElement>(null);
  const enableUpload = field_data.enable_image_uploading;

  const handleModeChange = (_: React.MouseEvent, newMode: Mode | null) => {
    if (!newMode) return;
    setMode(newMode);
    onChange(field_data.name, null, field_data.multipleIndex);
    if (inputRef.current) inputRef.current.value = '';
  };

  const handleSelectChange = (e: SelectChangeEvent<string>) => {
    let val: string | null = e.target.value;
    if (val === '__none__') val = null;
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

  const toggle = enableUpload ? (
    <ToggleButtonGroup value={mode} exclusive onChange={handleModeChange} size="small">
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
    </ToggleButtonGroup>
  ) : null;

  const header = (
    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.75 }}>
      <Box sx={{ fontSize: 12, color: 'text.secondary', fontWeight: 500, letterSpacing: 0.5 }}>
        {field_data.label}
      </Box>
      {toggle}
    </Box>
  );

  if (mode === 'upload' && enableUpload) {
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
            <input ref={inputRef} type="file" hidden accept="image/*" onChange={handleFileChange} />
          </Button>
          {value?.name
            ? <Chip label={value.name} onDelete={handleFileDelete} variant="outlined" size="small" sx={{ minWidth: 0, flex: 1 }} />
            : <Box sx={{ color: 'text.disabled', fontSize: 13, flex: 1 }}>No file chosen</Box>
          }
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ width: 1, my: 1 }}>
      {header}
      <FormControl fullWidth>
        <InputLabel color="secondary">{field_data.label}</InputLabel>
        <Select
          value={value ?? '__none__'}
          name={field_data.name}
          label={field_data.label}
          onChange={handleSelectChange}
          color="secondary"
        >
          <MenuItem value="__none__"><em>None</em></MenuItem>
          <Divider />
          {Array.isArray(field_data.options) && field_data.options.map((option: string, idx: number) => (
            <MenuItem key={idx} value={option}>{option}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
}

export default SelectField;
