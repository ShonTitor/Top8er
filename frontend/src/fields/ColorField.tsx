import { FormControl } from '@mui/material';
import { MuiColorInput } from 'mui-color-input';

interface ColorFieldProps {
  field_data: any;
  value: any;
  onChange: (name: string, val: string, multipleIndex: any) => void;
}

function ColorField({ field_data, value, onChange }: ColorFieldProps) {
  const handleChange = (color: string) => {
    onChange(field_data.name, color, field_data.multipleIndex);
  };

  return (
    <FormControl sx={{ my: 1, width: 1 }}>
      <MuiColorInput
        value={value ?? ''}
        onChange={handleChange}
        label={field_data.label}
        format="hex"
      />
    </FormControl>
  );
}

export default ColorField;
