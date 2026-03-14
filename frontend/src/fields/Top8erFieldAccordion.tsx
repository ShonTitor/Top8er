import { memo, useState, useCallback } from 'react';
import { useTheme } from '@mui/material/styles';
import { Typography } from '@mui/material';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Top8erField from './Top8erField';

interface Top8erFieldAccordionProps {
  fields: any[];
  value: any;
  onChange: (...args: any[]) => void;
  summary: React.ReactNode;
  name: string;
  defaultExpanded?: boolean;
  playerIndex?: number;
}

function Top8erFieldAccordion({ fields, value, onChange, summary, name, defaultExpanded, playerIndex }: Top8erFieldAccordionProps) {
  const [expanded, setExpanded] = useState(defaultExpanded !== undefined ? defaultExpanded : true);
  const theme = useTheme();

  const handleChangeAccordion = useCallback(() => {
    setExpanded(e => !e);
  }, []);

  const handleChange = useCallback((field_name: string, val: any, multiple_index?: number) => {
    if (multiple_index === undefined) {
      onChange(name, { ...value, [field_name]: val }, playerIndex);
    } else {
      const newArr = [...value[field_name]];
      newArr[multiple_index] = val;
      onChange(name, { ...value, [field_name]: newArr }, playerIndex, multiple_index);
    }
  }, [onChange, name, value, playerIndex]);

  let ready = !!value;
  if (ready) {
    for (let i = 0; i < fields.length; i++) {
      if (!(fields[i].name in value)) {
        ready = false;
        break;
      }
    }
  }

  if (!ready) {
    return <></>;
  }

  return (
    <Accordion
      sx={{ width: 1, '&:before': { display: 'none' }, borderRadius: '4px !important', mb: 0.5 }}
      expanded={expanded}
      onChange={handleChangeAccordion}
      disableGutters
    >
      <AccordionSummary
        sx={{
          backgroundColor: theme.palette.primary.main,
          borderRadius: expanded ? '4px 4px 0 0' : '4px',
          minHeight: 44,
          '& .MuiAccordionSummary-content': { my: 0.75 },
        }}
        expandIcon={<ExpandMoreIcon />}
      >
        <Typography variant="subtitle2" fontWeight={600} letterSpacing={0.5}>
          {summary}
        </Typography>
      </AccordionSummary>
      <AccordionDetails sx={{ display: 'flex', flexWrap: 'wrap', px: 2, pt: 0.5, pb: 1.5 }}>
        {fields.map((field_data, i) => (
          <Top8erField
            key={i}
            value={field_data.multiple ? value[field_data.name][field_data.multipleIndex] : value[field_data.name]}
            field_data={field_data}
            onChange={handleChange}
          />
        ))}
      </AccordionDetails>
    </Accordion>
  );
}

export default memo(Top8erFieldAccordion);
