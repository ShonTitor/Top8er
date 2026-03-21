export const apiURL = import.meta.env.VITE_TOP8ER_API_URL as string;
export const staticRoot = apiURL.replace(/\/api$/, '');
