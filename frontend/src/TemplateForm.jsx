import { useState, useEffect } from 'react'
import { Button, Grid, Paper } from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { Box } from '@mui/system'
import { LinearProgress } from '@mui/material'
import Top8erFieldAccordion from './fields/Top8erFieldAccordion'
import { useParams } from "react-router-dom";

function TemplateForm() {
  const [formState, setFormState] = useState({})
  const [pageState, setPageState] = useState({
    success: true,
    error_message: "",
    loading: false,
    result_img_src: "https://i.imgur.com/dOjahqX.png"
  })
  const { template } = useParams();
  const templateName = template;
  //const [templateName, setTemplateName] = useState("top1er")
  const [templateData, setTemplateData] = useState(null)
  const [gameName, setGameName] = useState("ssbu")
  const [gameData, setGameData] = useState(null)

  const theme = useTheme()

  const apiURL = "https://www.top8er.com/api/"

  // GET template_data
  useEffect(() => {
    fetch(apiURL + "template_data/" + templateName + "/", {
      method: 'GET',
      headers: {'Content-type': 'application/json; charset=UTF-8'}
    })
    .then((res) => res.json())
    .then((data) => {
      setTemplateData(data)
    })
    .catch((err) => {
      console.log(err)
    });
  }, [templateName])

  // GET game_data
  useEffect(() => {
    fetch(apiURL + "game_data/" + gameName + "/", {
      method: 'GET',
      headers: {'Content-type': 'application/json; charset=UTF-8'}
    })
    .then((res) => res.json())
    .then((data) => {
      setGameData(data)
    })
    .catch((err) => {
      console.log(err)
    });
  }, [gameName])

  const handleSubmit = (e) => {
    e.preventDefault()
    setPageState({...pageState, ['loading']: true})
    fetch(apiURL + "generate/" + templateName + "/" + gameName + "/", {
      method: 'POST',
      body: JSON.stringify(formState),
      headers: {'Content-type': 'application/json; charset=UTF-8'}
    })
    .then((res) => res.json())
    .then((data) => {
      if ("base64_img" in data) {
        var base64_img = data["base64_img"]
        setPageState({
          ...pageState,
          ['result_img_src']: 'data:image/png;base64,' + base64_img,
          ['success']: true,
          ['error_message']: "",
          ['loading']: false
        })
      }
      else {
        setPageState({
          ...pageState,
          ['success']: false,
          ['error_message']: JSON.stringify(data),
          ['loading']: false
        })
      }
    })
    .catch((err) => {
      console.log(err)
      setPageState({
        ...pageState,
        ['success']: false,
        ['error_message']: "Server error. Plase contact the administrator",
        ['loading']: false
      })
    });
  };

  const readyLoading = !!(templateData && gameData)

  const playerNumber = readyLoading ? templateData.player_number : 0
  const options = readyLoading ? templateData.options : []

  // turn this into a flags endpoint
  const flags =  ['None', 'Abkhazia', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antartica',
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
                  'Non-binary', 'Pansexual Pride', 'Polyamory Pride', 'Polysexual Pride', 'Transgender Pride']

  var playerFields = [];
  for (var i=0; i < playerNumber; i++) {
    var fields = [];
    (templateData.player_fields || []).forEach(field => {
      var betterField = {
        "label": field.label,
        "name": field.name,
        "type": field.type,
        "description": field.description,
        "enable_image_uploading": field.enable_image_uploading,
        "options": field.options,
        "image_types": field.image_types,
        "required": field.required,
        "default": field.default,
        "multiple": field.multiple,
        "amount": field.amount
      }
  
      if (field.options == "flags") {
        field.options = flags
      }
  
      if (field.type == "character" && field.image_types) {
        if (field.image_types[i] == "portraits") {
          betterField.characters = gameData.characters
          betterField.colors = gameData.colors
        }
        else if (field.image_types[i] == "icons") {
          if (gameData.hasIcons) {
            betterField.characters = Object.keys(gameData.iconColors)
            betterField.colors = gameData.iconColors
          }
        }
      }

      if ("defaults" in field) {
        betterField.default = field.defaults[i]
      }
  
      if (field.multiple) {
        for (var j=0; j < field.amount[i]; j++) {
          var finalField = {...betterField}
          finalField.multipleIndex = j
          finalField.name = finalField.name
          finalField.label =  `${finalField.label} ${j+1}`
          if ("required_multiple" in field) {
            finalField.required = field.required_multiple[j]
          }
          if ("image_types_multiple" in field) {
            if (field.image_types_multiple[i][j] == "portraits") {
              finalField.characters = gameData.characters
              finalField.colors = gameData.colors
            }
            else if (field.image_types_multiple[i][j] == "icons") {
              if (gameData.hasIcons) {
                finalField.characters = Object.keys(gameData.iconColors)
                finalField.colors = gameData.iconColors
              }
            }
          }
          fields.push(finalField)
        }
      }
      else {
        fields.push(betterField)
      }
      
    })
    playerFields.push(fields)
  }

  // Initial form state
  var initial_state = {}

  initial_state["players"] = [...Array(playerNumber).keys()].map(() => {return {}})

  for (var i=0; i < playerFields.length; i++) {
    for (var j=0; j < playerFields[i].length; j++) {
      const fieldName = playerFields[i][j].name
      const k = playerFields[i][j].multipleIndex
      if (playerFields[i][j].multiple && initial_state["players"][i][fieldName] == undefined) {
        const amount = playerFields[i][j].amount
        initial_state["players"][i][fieldName] = 
          [...Array(amount).keys()].map(() => {return null})
      }

      var field_initial = playerFields[i][j].default
      if (!field_initial) {
        switch (playerFields[i][j].type) {
          case "text":
            field_initial = ""
            break
          case "select":
            field_initial = ""
            break
          case "checkbox":
            field_initial = false
            break
          case "character":
            field_initial = null
            break
        }
      }
      if (playerFields[i][j].multiple) {
        initial_state["players"][i][fieldName][k] = field_initial
      }
      else {
        initial_state["players"][i][fieldName] = field_initial
      }
      
    }
  }

  initial_state["options"] = {}
  for (var i=0; i < options.length; i++) {
    initial_state["options"][options[i].name] = options[i].default || ""
  }

  useEffect(() => {
    setFormState(initial_state)
  }, [templateData, gameData])

  const handleChange = (name, value, playerIndex, multipleIndex) => {
    var stateCopy = JSON.parse(JSON.stringify(formState))
    if (playerIndex != undefined) {
      stateCopy["players"][playerIndex] = value
      value = stateCopy["players"]
      setFormState({
        ...formState,
        ["players"]: value
      })
    }
    else {
      setFormState({
        ...formState,
        [name]: value
      })
    }
    console.log("DEEP STATE", formState)

  };

  if (!readyLoading) {
    return <></>
  }

  return (
    <form  onSubmit={handleSubmit}>
    <Grid container alignItems="stretch" justifyContent="center">

      <Grid
            item 
            component={Paper}
            elevation={2}
            separation={2}
            xs={12}
            md={6}> 
        
        <Box
        margin="normal" 
        variant="filled" 
        sx={{display: 'flex', flexDirection: 'column',
            overflow: 'hidden', overflowY: "auto",
            alignItems: 'center',
            '@media (min-width: 900px)': {
              height: 'calc(100vh - 120px)'
            }
          }}
        >

            <h2>Enter your data</h2>
            {
              ([...Array(playerNumber).keys()]).map((field_data, i) => (
                <Top8erFieldAccordion 
                  key={i}
                  playerIndex={i}
                  name={"players"}
                  summary={"Player "+(i+1)} 
                  fields={playerFields[i]}
                  onChange={handleChange}
                  value={formState["players"][i]}
                />
              ))
            }
            <Top8erFieldAccordion 
                defaultExpanded={false} 
                name="options" 
                summary="Options" 
                fields={templateData.options || []}
                onChange={handleChange}
                value={formState["options"]}
            />

        </Box>

      </Grid>

      <Grid item xs={12} md={6}>

        <Box
            margin="normal" 
            variant="filled" 
            sx={{display: 'flex', flexDirection: 'column',
                overflow: "hidden", alignItems: 'center'
                }}
        > 

            <Button type='submit' sx={{m: 1, width: 7/10}}
                    variant="contained" disabled={pageState.loading} >
            Generate
            </Button>
            
            <LinearProgress sx={{ width: '80%', visibility: (pageState.loading ? "visible": "hidden") }} />
            {pageState.success 
            ?
            <img id="result-img" fit='scale-down' src={pageState.result_img_src}/>
            :
            <>
            <h1>An error occurred</h1>
            <Paper elevation={1} sx={{ width: '100%', height: 1, overflowy: "auto"}}>
              <code>{pageState.error_message}</code>
            </Paper>
            </>}
        </Box>

      </Grid>

    </Grid>
    </form>
  )
}

export default TemplateForm
