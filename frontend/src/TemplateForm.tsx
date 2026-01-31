import { useState, useEffect, FormEvent } from 'react';
import { Button, Grid, Paper } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { Box } from '@mui/system';
import { LinearProgress } from '@mui/material';
import Top8erFieldAccordion from './fields/Top8erFieldAccordion';
import { useParams } from "react-router-dom";
import { TemplateData, GameData, FormState, PageState, Field } from './types';
import { buildPlayerFields, buildInitialState } from './utils';

function TemplateForm() {
  const [formState, setFormState] = useState<FormState>({ players: [], options: {} });
  const [pageState, setPageState] = useState<PageState>({
    success: true,
    error_message: "",
    loading: false,
    result_img_src: "https://i.imgur.com/iH2jz30.png"
  });
  const { template, gameName } = useParams();
  const templateName = template as string;
  const [templateData, setTemplateData] = useState<TemplateData | null>(null);
  const [gameData, setGameData] = useState<GameData | null>(null);
  const theme = useTheme();
  const apiURL = import.meta.env.VITE_TOP8ER_API_URL;

  useEffect(() => {
    fetch(apiURL + "/template_data/" + templateName + "/", {
      method: 'GET',
      headers: { 'Content-type': 'application/json; charset=UTF-8' }
    })
      .then((res) => res.json())
      .then((data) => {
        setTemplateData(data);
      })
      .catch(() => {
        setPageState({ ...pageState, success: false, error_message: "Failed to fetch template data" });
      });
  }, [templateName]);

  useEffect(() => {
    fetch(apiURL + "/game_data/" + gameName + "/", {
      method: 'GET',
      headers: { 'Content-type': 'application/json; charset=UTF-8' }
    })
      .then((res) => res.json())
      .then((data) => {
        setGameData(data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [gameName]);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setPageState({ ...pageState, loading: true });


    const dataToSend = JSON.parse(JSON.stringify(formState));
    for (const [key, value] of Object.entries(dataToSend.options)) {
      console.log(key, typeof value, value);
        if (value && typeof value === 'object' && 'base64' in value) {
          dataToSend.options[key] = value;
      }
    }
    for (let i = 0; i < dataToSend.players.length; i++) {
      for (const [key, value] of Object.entries(dataToSend.players[i])) {
          if (value && typeof value === 'object' && 'base64' in value) {
            dataToSend.players[i][key] = value;
        } else if (Array.isArray(value)) {
          for (let j = 0; j < value.length; j++) {
              if (value[j] && typeof value[j] === 'object' && 'base64' in value[j]) {
                dataToSend.players[i][key][j] = value[j];
            }
          }
        }
      }
    }

    console.log(JSON.stringify(dataToSend.options));
    fetch(apiURL + "/generate/" + templateName + "/" + gameName + "/", {
      method: 'POST',
      body: JSON.stringify(dataToSend),
      headers: { 'Content-type': 'application/json; charset=UTF-8' }
    })
      .then((res) => res.json())
      .then((data) => {
        if ("base64_img" in data) {
          const base64_img = data["base64_img"];
          setPageState({
            ...pageState,
            result_img_src: 'data:image/png;base64,' + base64_img,
            success: true,
            error_message: "",
            loading: false
          });
        } else {
          setPageState({
            ...pageState,
            success: false,
            error_message: JSON.stringify(data),
            loading: false
          });
        }
      })
      .catch(() => {
        setPageState({
          ...pageState,
          success: false,
          error_message: "Server error. Plase contact the administrator",
          loading: false
        });
      });
  };

  const readyLoading = !!(templateData && gameData);
  const playerNumber = readyLoading ? templateData.player_number : 0;
  const options = readyLoading ? templateData.options : [];
  const flags = [
    'Abkhazia', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antartica',
    'Antigua and Barbuda', 'Argentina', 'Armenia', 'Artsakh', 'Australia', 'Austria', 
    'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 
    'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 
    'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 
    'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 
    'Comoros', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 
    'Democratic Republic of Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 
    'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 
    'Eswatini', 'Ethiopia', 'Federated States of Micronesia', 'Fiji', 'Finland', 'France', 
    'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 
    'Guinea-Bissau', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 
    'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 
    'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 
    'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 
    'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 
    'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 
    'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'North Korea',
    'North Macedonia', 'Northern Cyprus', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 
    'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 
    'Republic of China (Taiwan)', 'Republic of Congo', 'Romania', 'Russia', 'Rwanda', 
    'Sahrawi Arab Democratic Republic', 'Saint Kitts and Nevis', 'Saint Lucia', 
    'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Saudi Arabia', 'Scania', 'Scotland',
    'Senegal', 'Serbia', 
    'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 
    'Somaliland', 'South Africa', 'South Korea', 'South Ossetia', 'South Sudan', 'Spain', 'Sri Lanka', 
    'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'São Tomé and Príncipe', 'Tajikistan', 
    'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Transnistria', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 
    'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 
    'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Wales', 'Yemen', 'Zambia','Zimbabwe', 
    'Agender Pride', 'Aromantic Pride', 'Asexual Pride', 'Bigender Pride', 'Bisexual Pride', 'Demiromantic Pride', 
    'Demisexual Pride', 'Gay Pride', 'Gender Fluid', 'Genderqueer Pride', 'Intersex Pride', 'Lesbian Pride', 
    'Non-binary', 'Pansexual Pride', 'Polyamory Pride', 'Polysexual Pride', 'Transgender Pride'
  ];
  const playerFields: Field[][] = readyLoading && templateData && gameData
    ? buildPlayerFields(templateData, gameData, flags)
    : [];

  useEffect(() => {
    if (readyLoading && templateData && gameData) {
      setFormState(buildInitialState(playerFields, templateData, gameData, options));
    }
  }, [templateData, gameData]);

  const handleChange = (name: string, value: any, playerIndex?: number, multipleIndex?: number) => {
    setFormState(prev => {
      const copy = JSON.parse(JSON.stringify(prev));
      if (playerIndex !== undefined) {
        copy.players[playerIndex] = value;
        return { ...prev, players: copy.players };
      } else {
        return { ...prev, [name]: value };
      }
    });
  };

  if (!readyLoading) {
    return <></>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <Grid container alignItems="stretch" justifyContent="center">
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ width: '100%' }}>
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden',
                overflowY: "auto",
                alignItems: 'center',
                '@media (min-width: 900px)': {
                  height: 'calc(100vh - 120px)'
                }
              }}
            >
            <h2>Enter your data</h2>
            {([...Array(playerNumber).keys()]).map((field_data, i) => (
              <Top8erFieldAccordion
                key={i}
                playerIndex={i}
                name={"players"}
                summary={"Player " + (i + 1)}
                fields={playerFields[i]}
                onChange={handleChange}
                value={formState["players"][i]}
                defaultExpanded={true}
              />
            ))}
            <Top8erFieldAccordion
              defaultExpanded={false}
              name="options"
              summary="Options"
              fields={templateData.options || []}
              onChange={handleChange}
              value={formState["options"]}
              playerIndex={undefined}
            />
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Box sx={{ display: 'flex', flexDirection: 'column', overflow: "hidden", alignItems: 'center' }}>
            <Button type='submit' sx={{ m: 1, width: '70%' }} variant="contained" disabled={pageState.loading}>
              Generate
            </Button>
            <LinearProgress sx={{ width: '80%', visibility: pageState.loading ? "visible" : "hidden" }} />
            {pageState.success ? (
              <img id="result-img" style={{ objectFit: 'scale-down' }} src={pageState.result_img_src} />
            ) : (
              <>
                <h1>An error occurred</h1>
                <Paper elevation={1} sx={{ width: '100%', height: 1, overflowY: "auto" }}>
                  <code>{pageState.error_message}</code>
                </Paper>
              </>
            )}
          </Box>
        </Grid>
      </Grid>
    </form>
  );
}

export default TemplateForm;
