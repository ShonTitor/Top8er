import { Divider, FormControl, ListSubheader } from '@mui/material';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';

interface SelectFieldProps {
  field_data: any;
  value: any;
  onChange: (name: string, val: string | null, multipleIndex: any) => void;
}

function SelectField({ field_data, value, onChange }: SelectFieldProps) {
  const handleChange = (e: SelectChangeEvent<string>) => {
    let val: string | null = e.target.value;
    if (val === '__none__') val = null;
    onChange(field_data.name, val, field_data.multipleIndex);
  };

  return (
    <FormControl sx={{ my: 1, width: 1 }}>
      <InputLabel color="secondary">{field_data.label}</InputLabel>
      <Select
        value={value ?? '__none__'}
        name={field_data.name}
        label={field_data.label}
        onChange={handleChange}
        color="secondary"
      >
        {Array.isArray(field_data.options) && field_data.options.map((option: string, idx: number) => (
          <MenuItem key={idx} value={option}>{option}</MenuItem>
        ))}
        <Divider />
        <MenuItem value="__none__"><em>None</em></MenuItem>
      </Select>
    </FormControl>
  );
}

export default SelectField;
