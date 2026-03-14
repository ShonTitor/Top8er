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
  tournament_aliases?: {
    player: Record<string, string[]>;
    options: Record<string, string[]>;
  };
  game_defaults?: Record<string, string | [string, number]>;
}

export interface GameData {
  characters: string[];
  colors: Record<string, string[]>;
  hasIcons?: boolean;
  iconColors?: Record<string, string[]>;
  defaultLayoutColors?: string[];
  blackSquares?: boolean;
}

export interface ApiError {
  scope: 'root' | 'options' | 'player_fields';
  field: string;
  message: string;
  player_index?: number;
}

export interface FormState {
  players: any[];
  options: Record<string, any>;
}

export interface PageState {
  success: boolean;
  errors: ApiError[];
  loading: boolean;
  result_img_src: string;
}
