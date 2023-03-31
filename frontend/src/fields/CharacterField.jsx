import { useState} from 'react'
import { FormControl } from '@mui/material'
import { Box } from '@mui/system'
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';

function CharacterField({ field_data, onChange }) {
  if (!field_data.characters) {
    return <></>
  }

  if (!field_data.required) {
    field_data.characters = ["None"].concat(field_data.characters)
  }
  const [char, setChar] = useState(field_data.characters ? field_data.characters[0] : "")
  const [color, setColor] = useState(0)

  var hasColors
  var colors
  if (!field_data.colors || !field_data.colors[char] || field_data.colors[char].length <= 1) {
    hasColors = false
  }
  else {
    hasColors = true;
    colors = field_data.colors[char]
  }

  if (!field_data.required) {
    
  }

  const handleChangeChar = (e) => {
    setChar(e.target.value)
    setColor(0)
    onChange(field_data.id, [e.target.value, 0])
  };

  const handleChangeColor = (e) => {
    setColor(e.target.value)
    onChange(field_data.id, [char, e.target.value])
  };

  const labelId = field_data.id+"-label"
  const labelIdColor = field_data.id+"-labelColor"

  const field1 = (
    <FormControl fullWidth sx={{my: 1, width: 1, marginRight: 1}} component={Box}>
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
            <MenuItem color='secondary' key={i} value={i}>{op}</MenuItem>)
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
