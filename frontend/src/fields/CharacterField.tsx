import { useState } from 'react';
import { FormControl } from '@mui/material';
import { Box } from '@mui/system';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';

interface CharacterFieldProps {
  field_data: any;
  value: any;
  onChange: (...args: any[]) => void;
}

function CharacterField({ field_data, value, onChange }: CharacterFieldProps) {
  if (!field_data.characters) {
    console.log(field_data);
    return <></>;
  }

  if (!field_data.required) {
    field_data.characters = ["None"].concat(field_data.characters);
  }

  const char = value ? value[0] : field_data.characters[0];
  const color = value ? value[1] : 0;

  let hasColors: boolean;
  let colors: string[] | undefined;
  if (!field_data.colors || !field_data.colors[char] || field_data.colors[char].length <= 1) {
    hasColors = false;
  } else {
    hasColors = true;
    colors = field_data.colors[char];
  }

  const handleChangeChar = (e: SelectChangeEvent) => {
    if (e.target.value === "None") {
      onChange(field_data.name, null);
    } else {
      onChange(field_data.name, [e.target.value, 0]);
    }
  };

  const handleChangeColor = (e: SelectChangeEvent) => {
    const value_copy = [...value];
    value_copy[1] = e.target.value;
    onChange(field_data.name, value_copy);
  };

  const labelId = field_data.id + "-label";
  const labelIdColor = field_data.id + "-labelColor";

  const field1 = (
    <FormControl fullWidth sx={{ my: 1, width: 1, marginRight: hasColors ? 1 : 0 }} component={Box}>
      <InputLabel color='secondary' id={labelId}>{field_data.label}</InputLabel>
      <Select
        label={field_data.label}
        value={char}
        name={field_data.name}
        id={field_data.id}
        onChange={handleChangeChar}
      >
        {field_data.characters.map((c: string, i: number) => (
          <MenuItem key={i} value={c}>{c}</MenuItem>
        ))}
      </Select>
    </FormControl>
  );

  let field2 = null;
  if (hasColors && colors) {
    field2 = (
      <FormControl fullWidth sx={{ my: 1, width: 1 }} component={Box}>
        <InputLabel color='secondary' id={labelIdColor}>Color</InputLabel>
        <Select
          value={color}
          name={field_data.name + "_color"}
          id={field_data.id + "_color"}
          onChange={handleChangeColor}
        >
          {colors.map((c: string, i: number) => (
            <MenuItem key={i} value={i}>{c}</MenuItem>
          ))}
        </Select>
      </FormControl>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'row', width: 1 }}>
      {field1}
      {field2}
    </Box>
  );
}

export default CharacterField;
