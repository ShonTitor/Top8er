import { TextField, FormControl, Button, Box } from '@mui/material';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import CharacterField from './CharacterField';
import { MuiColorInput } from 'mui-color-input';

interface Top8erFieldProps {
  field_data: any;
  value: any;
  onChange: (...args: any[]) => void;
}

function Top8erField({ field_data, value, onChange }: Top8erFieldProps) {
  let field = <></>;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | { value: unknown }>) => {
    let val: string | null = (e.target as HTMLInputElement).value;
    if (val === "None") {
      val = null;
    }
    onChange(field_data.name, val, field_data.multipleIndex);
  };

  const handleSelectChange = (e: SelectChangeEvent<string>) => {
    let val: string | null = e.target.value;
    if (val === "None") {
      val = null;
    }
    onChange(field_data.name, val, field_data.multipleIndex);
  };

  const handleChangeCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.checked;
    onChange(field_data.name, val, field_data.multipleIndex);
  };

  const handleChangeCharacterField = (name: string, val: any) => {
    onChange(field_data.name, val, field_data.multipleIndex);
  };

  const handleChangeColor = (color: string) => {
    onChange(field_data.name, color, field_data.multipleIndex);
  };

  const handleChangeFile = (e: React.ChangeEvent<HTMLInputElement>) => {
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

  switch (field_data.type) {
    case 'text':
      field = (
        <TextField
          value={value}
          name={field_data.name}
          onChange={handleChange}
          sx={{ my: 1, width: 1 }}
          label={field_data.label}
          variant="outlined"
          color="secondary"
        />
      );
      break;
    case 'select':
      field = (
        <FormControl sx={{ my: 1, width: 1 }}>
          <InputLabel>{field_data.label}</InputLabel>
          <Select
            value={value ?? ''}
            name={field_data.name}
            label={field_data.label}
            onChange={handleSelectChange}
            color="secondary"
          >
            {Array.isArray(field_data.options) && field_data.options.map((option: string, idx: number) => (
              <MenuItem key={idx} value={option}>{option}</MenuItem>
            ))}
            <MenuItem value="None">None</MenuItem>
          </Select>
        </FormControl>
      );
      break;
    case 'checkbox':
      field = (
        <FormControlLabel
          control={
            <Checkbox
              checked={!!value}
              onChange={handleChangeCheckbox}
              color="secondary"
            />
          }
          label={field_data.label}
          sx={{ my: 1, width: '32%' }}
        />
      );
      break;
    case 'character':
      field = (
        <CharacterField
          field_data={field_data}
          value={value}
          onChange={handleChangeCharacterField}
        />
      );
      break;
    case 'color':
      field = (
        <FormControl sx={{ my: 1, width: 1 }}>
          <MuiColorInput
            value={value ?? ''}
            onChange={handleChangeColor}
            label={field_data.label}
            format="hex"
          />
        </FormControl>
      );
      break;
    case 'file':
      field = (
        <Box sx={{ my: 1, width: 1 }}>
          <Button
            variant="outlined"
            component="label"
            color="secondary"
            sx={{ width: 1 }}
          >
            {field_data.label}
            <input
              type="file"
              hidden
              onChange={handleChangeFile}
              accept={field_data.accept || '*'}
            />
          </Button>
          {value && value.name && (
            <Box sx={{ mt: 1, fontSize: 14 }}>{value.name}</Box>
          )}
        </Box>
      );
      break;
    case 'image':
      field = (
        <Box sx={{ my: 1, width: 1 }}>
          <Button
            variant="outlined"
            component="label"
            color="secondary"
            sx={{ width: 1 }}
          >
            {field_data.label}
            <input
              type="file"
              hidden
              onChange={handleChangeFile}
              accept="image/*"
            />
          </Button>
          {value && value.name && (
            <Box sx={{ mt: 1, fontSize: 14 }}>{value.name}</Box>
          )}
        </Box>
      );
      break;
    default:
      field = <></>;
      break;
  }

  return field;
}

export default Top8erField;
