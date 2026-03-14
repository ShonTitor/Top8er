import { TextField as MuiTextField } from '@mui/material';

interface TextFieldProps {
  field_data: any;
  value: any;
  onChange: (name: string, val: string | null, multipleIndex: any) => void;
}

function TextField({ field_data, value, onChange }: TextFieldProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let val: string | null = e.target.value;
    if (val === 'None') val = null;
    onChange(field_data.name, val, field_data.multipleIndex);
  };

  return (
    <MuiTextField
      value={value}
      name={field_data.name}
      onChange={handleChange}
      sx={{ my: 1, width: 1 }}
      label={field_data.label}
      variant="outlined"
      color="secondary"
    />
  );
}

export default TextField;
