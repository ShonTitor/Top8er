import FileField from './FileField';

interface ImageFieldProps {
  field_data: any;
  value: any;
  onChange: (name: string, val: { base64: string; name: string }, multipleIndex: any) => void;
}

function ImageField({ field_data, value, onChange }: ImageFieldProps) {
  return <FileField field_data={field_data} value={value} onChange={onChange} accept="image/*" />;
}

export default ImageField;
