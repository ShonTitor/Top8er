import { useRef } from 'react';
import { Box, Button, Chip } from '@mui/material';
import AttachFileIcon from '@mui/icons-material/AttachFile';

interface FileFieldProps {
  field_data: any;
  value: any;
  onChange: (name: string, val: { base64: string; name: string } | null, multipleIndex: any) => void;
  accept?: string;
}

function FileField({ field_data, value, onChange, accept = field_data.accept ?? '*' }: FileFieldProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
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

  const handleDelete = () => {
    onChange(field_data.name, null, field_data.multipleIndex);
    if (inputRef.current) inputRef.current.value = '';
  };

  return (
    <Box sx={{ my: 1, width: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
      <Button
        variant="outlined"
        component="label"
        color="secondary"
        startIcon={<AttachFileIcon />}
        sx={{ flexShrink: 0 }}
      >
        {field_data.label}
        <input
          ref={inputRef}
          type="file"
          hidden
          onChange={handleChange}
          accept={accept}
        />
      </Button>
      {value?.name && (
        <Chip
          label={value.name}
          onDelete={handleDelete}
          variant="outlined"
          size="small"
          sx={{ maxWidth: 1, overflow: 'hidden' }}
        />
      )}
    </Box>
  );
}

export default FileField;
