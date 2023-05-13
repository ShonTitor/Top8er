import { TextField, FormControl, Button } from '@mui/material'
import FormControlLabel from '@mui/material/FormControlLabel'
import Checkbox from '@mui/material/Checkbox'
import { Box } from '@mui/system'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import InputLabel from '@mui/material/InputLabel'
import CharacterField from './CharacterField'
import { MuiColorInput } from 'mui-color-input'

function Top8erField({ field_data, value, onChange }) {
  var field = <></>;

  const handleChange = (e) => {
    var val = e.target.value
    if (val == "None") {
      val = null
    }
    onChange(field_data.name, val, field_data.multipleIndex)
  };

  const handleChangeCheckbox = (e) => {
    const val = e.target.checked
    onChange(field_data.name, val, field_data.multipleIndex)
  };

  const handleChangeCharacterField = (name, val) => {
    onChange(field_data.name, val, field_data.multipleIndex)
  };

  const handleChangeColor = (color) => {
    onChange(field_data.name, color, field_data.multipleIndex)
  };

  const handleChangeFile = (e) => {
    const file = e.target.files[0]
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = () => {
      onChange(field_data.name, file, field_data.multipleIndex)
    }
    //console.log(file)
    //onChange(field_data.name, file, field_data.multipleIndex)
  }
  
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
      var options = field_data.options
      if (!field_data.required) {
        options = ["None"].concat(options)
      }
      field = (
        <FormControl sx={{my: 1, width: 1}} fullWidth component={Box}>
        <InputLabel color='secondary' id={labelId}>{field_data.label}</InputLabel>
        <Select
          value={value || "None"}
          name={field_data.name}
          id={field_data.id}
          onChange={handleChange}
          label={field_data.label}
          labelId={labelId}
          color="secondary"
        >
          {
            options.map((op, i) => <MenuItem key={i} value={op}>{op}</MenuItem>)
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
    case 'color':
      field = <MuiColorInput 
                format='hex'
                isAlphaHidden={true}
                value={value} 
                onChange={handleChangeColor} 
                sx={{my: 1, width: 1}}
                label={field_data.label}
                variant="outlined" 
                color="secondary"
              />
      break;
    case 'font':
      var labelId = field_data.id+"-label"
      var options = field_data.options
      if (!field_data.required) {
        options = ["None"].concat(options)
      }
      field = (
        <FormControl sx={{my: 1, width: 1}} fullWidth component={Box}>
        <InputLabel color='secondary' id={labelId}>{field_data.label}</InputLabel>
        <Select
          value={value || "None"}
          name={field_data.name}
          id={field_data.id}
          onChange={handleChange}
          label={field_data.label}
          labelId={labelId}
          color="secondary"
        >
          {
            options.map((op, i) => <MenuItem key={i} value={op}>{op}</MenuItem>)
          }
        </Select>
        </FormControl>
      )
      break;
    case 'image':
      field = (
        <FormControl sx={{ my: 1, width: 1 }}>
          <Button
            variant="contained"
            component="label"
            color="secondary"
          >
            {field_data.label}
            <input
              type="file"
              style={{ display: 'none' }}
              onChange={handleChangeFile}
            />
          </Button>
        </FormControl>
      )
      break;
    default:
      //field = <div>[unknown field type {field_data.type}]</div>
      //console.log('unknown field type ' + field_data.type)
  }

  return field
}

export default Top8erField
