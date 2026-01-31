import { TemplateData, GameData, Field, FormState } from './types';

export function buildPlayerFields(templateData: TemplateData, gameData: GameData, flags: string[]): Field[][] {
  const playerFields: Field[][] = [];
  for (let i = 0; i < templateData.player_number; i++) {
    const fields: Field[] = [];
    (templateData.player_fields || []).forEach((field: any) => {
      let betterField: any = {
        label: field.label,
        name: field.name,
        type: field.type,
        description: field.description,
        enable_image_uploading: field.enable_image_uploading,
        options: field.options,
        image_types: field.image_types,
        required: field.required,
        default: field.default,
        multiple: field.multiple
      };
      if (field.amount !== undefined) {
        betterField.amount = typeof field.amount === "number" ? field.amount : field.amount[i];
      }
      if (field.options === "flags") {
        betterField.options = flags;
      }
      if (field.type === "font") {
        betterField.options = Object.keys(templateData.available_fonts);
      }
      if (field.type === "character" && field.image_types) {
        if (field.image_types[i] === "portraits") {
          betterField.characters = gameData.characters;
          betterField.colors = gameData.colors;
        } else if (field.image_types[i] === "icons") {
          if (gameData.hasIcons && gameData.iconColors) {
            betterField.characters = Object.keys(gameData.iconColors);
            betterField.colors = gameData.iconColors;
          } else {
            return;
          }
        }
      }
      if ("defaults" in field) {
        betterField.default = field.defaults[i];
      }
      if (field.multiple) {
        for (let j = 0; j < betterField.amount; j++) {
          let finalField = { ...betterField };
          finalField.multipleIndex = j;
          finalField.name = finalField.name;
          finalField.label = `${finalField.label} ${j + 1}`;
          if ("required" in field) {
            finalField.required = field.required[i][j];
          }
          if ("image_types" in field) {
            if (field.image_types[i][j] === "portraits") {
              finalField.characters = gameData.characters;
              finalField.colors = gameData.colors;
            } else if (field.image_types[i][j] === "icons") {
              if (gameData.hasIcons && gameData.iconColors) {
                finalField.characters = Object.keys(gameData.iconColors);
                finalField.colors = gameData.iconColors;
              } else {
                return;
              }
            }
          }
          fields.push(finalField);
        }
      } else {
        fields.push(betterField);
      }
    });
    playerFields.push(fields);
  }
  return playerFields;
}

export function buildInitialState(playerFields: Field[][], templateData: TemplateData, gameData: GameData, options: Field[]): FormState {
  const initial_state: FormState = { players: [], options: {} };
  initial_state.players = [...Array(playerFields.length).keys()].map(() => ({}));
  for (let i = 0; i < playerFields.length; i++) {
    for (let j = 0; j < playerFields[i].length; j++) {
      const fieldName = playerFields[i][j].name;
      const k = playerFields[i][j].multipleIndex;
      if (playerFields[i][j].multiple && initial_state.players[i][fieldName] === undefined) {
        const amount = playerFields[i][j].amount;
        initial_state.players[i][fieldName] = [...Array(amount).keys()].map(() => null);
      }
      let field_initial = playerFields[i][j].default;
      if (!field_initial) {
        switch (playerFields[i][j].type) {
          case "text":
            field_initial = "";
            break;
          case "select":
            field_initial = null;
            break;
          case "checkbox":
            field_initial = false;
            break;
          case "character":
            const chars = playerFields[i][j].characters;
            const firstChar = Array.isArray(chars) && chars.length > 0 ? chars[0] : null;
            field_initial = playerFields[i][j].required ? [firstChar, 0] : null;
            break;
          case "color":
            field_initial = "#111111";
            break;
          case "font":
            field_initial = null;
            break;
        }
      }
      if (playerFields[i][j].multiple && typeof k === 'number' && Array.isArray(initial_state.players[i][fieldName])) {
        initial_state.players[i][fieldName][k] = field_initial;
      } else {
        initial_state.players[i][fieldName] = field_initial;
      }
    }
  }
  initial_state.options = {};
  for (let i = 0; i < options.length; i++) {
    let field_initial = options[i].default;
    if (!field_initial) {
      switch (options[i].type) {
        case "text":
          field_initial = "";
          break;
        case "select":
          field_initial = null;
          break;
        case "checkbox":
          field_initial = false;
          break;
        case "character":
          const chars = playerFields[i][0]?.characters;
          const firstChar = Array.isArray(chars) && chars.length > 0 ? chars[0] : null;
          field_initial = options[i].required ? [firstChar, 0] : null;
          break;
        case "color":
          field_initial = "#000000";
          break;
        case "font":
          field_initial = null;
          options[i].options = Object.keys(templateData.available_fonts);
          break;
      }
    }
    initial_state.options[options[i].name] = field_initial;
  }
  return initial_state;
}
