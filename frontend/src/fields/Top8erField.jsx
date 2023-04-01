import { useState, useEffect } from 'react'
import { TextField, FormControl} from '@mui/material'
import FormControlLabel from '@mui/material/FormControlLabel'
import Checkbox from '@mui/material/Checkbox'
import { Box } from '@mui/system'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import InputLabel from '@mui/material/InputLabel'
import CharacterField from './CharacterField'

function Top8erField({ field_data, value, onChange }) {
  //const [value, setValue] = useState(field_data.default || "")
  var field = <></>;

  //useEffect(() => {
  //  if (field_data.default) {
  //    onChange(field_data.name, field_data.default)
  //  }
  //})

  const handleChange = (e) => {
    //setValue(e.target.value)
    onChange(field_data.name, e.target.value, field_data.multipleIndex)
  };

  const handleChangeCheckbox = (e) => {
    //setValue(e.target.value)
    const val = e.target.checked
    onChange(field_data.name, val, field_data.multipleIndex)
  };

  const handleChangeCharacterField = (name, val) => {
    //setValue(val)
    onChange(field_data.name, val, field_data.multipleIndex)
  };
  
  switch (field_data.type) {
    case 'text':
      field = (
        <TextField
          value={value}
          name={field_data.name}
          onChange={handleChange}
          sx={{my: 1, width: 1}}
          label={field_data.label}
          variant="outlined" 
          color="secondary"
        />
      )
      break;
    case 'select':
      var labelId = field_data.id+"-label"
      field = (
        <FormControl sx={{my: 1, width: 1}} fullWidth component={Box}>
        <InputLabel color='secondary' id={labelId}>{field_data.label}</InputLabel>
        <Select
          value={value}
          name={field_data.name}
          id={field_data.id}
          onChange={handleChange}
          label={field_data.label}
          labelId={labelId}
          color="secondary"
        >
          {
            field_data.options.map((op, i) => <MenuItem key={i} value={op}>{op}</MenuItem>)
          }
        </Select>
        </FormControl>
      )
      break;
      case 'checkbox':
        field = (
          <FormControlLabel control={
            <Checkbox 
            checked={value}
            name={field_data.name}
            onChange={handleChangeCheckbox}
            sx={{m: 1}}
            color="secondary"
            />
          } label={field_data.label}
        />
        )
        break;
    case 'character':
      field = <CharacterField value={value} field_data={field_data} onChange={handleChangeCharacterField}/>
      break;
    default:
      //field = <div>[unknown field type {field_data.type}]</div>
      //console.log('unknown field type ' + field_data.type)
  }

  return field
}

export default Top8erField
