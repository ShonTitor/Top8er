export interface Field {
  label: string;
  name: string;
  type: 'text' | 'select' | 'checkbox' | 'character' | 'color' | 'font';
  description?: string;
  enable_image_uploading?: boolean;
  options?: string[] | string;
  image_types?: string[];
  required?: boolean | boolean[] | boolean[][];
  default?: any;
  defaults?: any[];
  multiple?: boolean;
  amount?: number | number[];
  multipleIndex?: number;
  characters?: string[];
  colors?: Record<string, string[]>;
}

export interface TemplateData {
  player_number: number;
  options: Field[];
  player_fields: Field[];
  available_fonts: Record<string, any>;
}

export interface GameData {
  characters: string[];
  colors: Record<string, string[]>;
  hasIcons?: boolean;
  iconColors?: Record<string, string[]>;
}

export interface FormState {
  players: any[];
  options: Record<string, any>;
}

export interface PageState {
  success: boolean;
  error_message: string;
  loading: boolean;
  result_img_src: string;
}
