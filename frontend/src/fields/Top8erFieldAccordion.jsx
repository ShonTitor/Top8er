import { useState} from 'react'
import { useTheme } from '@mui/material/styles'
import Accordion from '@mui/material/Accordion'
import AccordionSummary from '@mui/material/AccordionSummary'
import AccordionDetails from '@mui/material/AccordionDetails'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import Top8erField from './Top8erField'

function Top8erFieldAccordion({ fields, onChange, summary, name, defaultExpanded }) {
  const [state, setState] = useState({})
  const [expanded, setExpanded] = useState(defaultExpanded != undefined ? defaultExpanded : true)
  const theme = useTheme()

  const handleChangeAccordion = (e) => {
    setExpanded(!expanded)
  }

  const handleChange = (field_name, val) => {
    const new_state = {...state, [field_name]: val}
    setState(new_state)
    onChange(name, new_state)
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
      fields.map((field_data, i) => 
        <Top8erField key={i} field_data={field_data} onChange={handleChange}></Top8erField>
      )
    }
    </AccordionDetails>
  </Accordion>
  )
}

export default Top8erFieldAccordion

