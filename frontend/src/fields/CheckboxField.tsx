import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';

interface CheckboxFieldProps {
  field_data: any;
  value: any;
  onChange: (name: string, val: boolean, multipleIndex: any) => void;
}

function CheckboxField({ field_data, value, onChange }: CheckboxFieldProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(field_data.name, e.target.checked, field_data.multipleIndex);
  };

  return (
    <FormControlLabel
      control={
        <Checkbox
          checked={!!value}
          onChange={handleChange}
          color="secondary"
          size="small"
        />
      }
      label={field_data.label}
      sx={{ width: '50%', my: 0.25, '& .MuiFormControlLabel-label': { fontSize: 14 } }}
    />
  );
}

export default CheckboxField;
