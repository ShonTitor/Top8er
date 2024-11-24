import { useState} from 'react'
import { FormControl } from '@mui/material'
import { Box } from '@mui/system'
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';

function CharacterField({ field_data, value, onChange }) {
  if (!field_data.characters) {
    console.log(field_data)
    return <></>
  }

  if (!field_data.required) {
    field_data.characters = ["None"].concat(field_data.characters)
  }
  
  const char = value ? value[0] : field_data.characters[0]
  const color = value ? value[1] : 0

  var hasColors
  var colors
  if (!field_data.colors || !field_data.colors[char] || field_data.colors[char].length <= 1) {
    hasColors = false
  }
  else {
    hasColors = true;
    colors = field_data.colors[char]
  }

  if (field_data.required && value == null) {
    //onChange(field_data.name, [char, color])
  }

  const handleChangeChar = (e) => {
    if (e.target.value == "None") {
      onChange(field_data.name, null)
    }
    else {
      onChange(field_data.name, [e.target.value, 0])
    }
  };

  const handleChangeColor = (e) => {
    var value_copy = [...value]
    value_copy[1] = e.target.value
    onChange(field_data.name, value_copy)
  };

  const labelId = field_data.id+"-label"
  const labelIdColor = field_data.id+"-labelColor"

  const field1 = (
    <FormControl fullWidth sx={{my: 1, width: 1, marginRight: (hasColors ? 1 : 0)}} component={Box}>
      <InputLabel color='secondary' id={labelId}>{field_data.label}</InputLabel>
      <Select
        value={char}
        name={field_data.name}
        id={field_data.id}
        onChange={handleChangeChar}
        label={field_data.label}
        labelId={labelId}
        color="secondary"
      >
        {
          field_data.characters.map((op, i) => 
            <MenuItem color='secondary' key={i} value={op}>{op}</MenuItem>)
        }
      </Select>
    </FormControl>
  )

  const field2 = (
    <FormControl sx={{my: 1, width: 1, px: 0}} component={Box}>
      <InputLabel color='secondary' id={labelIdColor}>{field_data.label + " Skin"}</InputLabel>
      <Select
        value={color}
        name={field_data.name}
        id={field_data.id}
        onChange={handleChangeColor}
        label={field_data.label}
        labelId={labelIdColor}
        color="secondary"
      >
        {
          (colors || []).map((op, i) => 
            <MenuItem color='secondary' key={i} value={i}>{i}: {op}</MenuItem>)
        }
      </Select>
    </FormControl>
  )

  return (
    <Box sx={{display: "flex", px: 0}}>
    
    {field1}
    {hasColors ? field2 : <></>}

    </Box>
  )
}

export default CharacterField
