import { useState, useEffect } from 'react'
import { useTheme } from '@mui/material/styles'
import Accordion from '@mui/material/Accordion'
import AccordionSummary from '@mui/material/AccordionSummary'
import AccordionDetails from '@mui/material/AccordionDetails'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import Top8erField from './Top8erField'

function Top8erFieldAccordion({ fields, value, onChange, summary, name, defaultExpanded, playerIndex }) {
  const [expanded, setExpanded] = useState(defaultExpanded != undefined ? defaultExpanded : true)
  const theme = useTheme()

  const handleChangeAccordion = (e) => {
    setExpanded(!expanded)
  }

  const handleChange = (field_name, val, multiple_index) => {
    if (multiple_index == undefined) {
      onChange(name, {...value, [field_name]: val}, playerIndex)
    }
    else {
      var stateCopy = JSON.parse(JSON.stringify(value))
      stateCopy[field_name][multiple_index] = val
      onChange(name, stateCopy, playerIndex, multiple_index)
    }
    
  }

  var ready = !!value
  if (ready) {
    for (var i=0; i < fields.length; i++) {
      if (!(fields[i].name in value)) {
        ready = false
        break
      }
    }
  }
  
  if (!ready) {
    return <></>
  }

  return (
  <Accordion sx={{width: 1}} expanded={expanded} onChange={handleChangeAccordion}>
    <AccordionSummary
      sx={{backgroundColor: theme.palette.primary.main}}
      expandIcon={<ExpandMoreIcon />}
    >
      {summary}
    </AccordionSummary>
    <AccordionDetails>
    {
      fields.map((field_data, i) => {
        return <Top8erField 
                  key={i}
                  value={
                    field_data.multiple
                    ?
                    value[field_data.name][field_data.multipleIndex]
                    :
                    value[field_data.name]
                  }
                  field_data={field_data}
                  onChange={handleChange}
                />
      })
    }
    </AccordionDetails>
  </Accordion>
  )
}

export default Top8erFieldAccordion

