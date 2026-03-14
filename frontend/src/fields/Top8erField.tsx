import { memo, useCallback } from 'react';
import TextField from './TextField';
import SelectField from './SelectField';
import CheckboxField from './CheckboxField';
import CharacterField from './CharacterField';
import ColorField from './ColorField';
import FileField from './FileField';
import ImageField from './ImageField';
import FontField from './FontField';

interface Top8erFieldProps {
  field_data: any;
  value: any;
  onChange: (...args: any[]) => void;
}

function Top8erField({ field_data, value, onChange }: Top8erFieldProps) {
  const handleChangeCharacterField = useCallback((_name: string, val: any) => {
    onChange(field_data.name, val, field_data.multipleIndex);
  }, [onChange, field_data.name, field_data.multipleIndex]);

  switch (field_data.type) {
    case 'text':
      return <TextField field_data={field_data} value={value} onChange={onChange} />;
    case 'select':
      return <SelectField field_data={field_data} value={value} onChange={onChange} />;
    case 'checkbox':
      return <CheckboxField field_data={field_data} value={value} onChange={onChange} />;
    case 'character':
      return <CharacterField field_data={field_data} value={value} onChange={handleChangeCharacterField} />;
    case 'color':
      return <ColorField field_data={field_data} value={value} onChange={onChange} />;
    case 'file':
      return <FileField field_data={field_data} value={value} onChange={onChange} />;
    case 'image':
      return <ImageField field_data={field_data} value={value} onChange={onChange} />;
    case 'font':
      return <FontField field_data={field_data} value={value} onChange={onChange} />;
    default:
      return <></>;
  }
}

export default memo(Top8erField);
