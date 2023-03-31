import { useState, useEffect, useRef } from 'react'
import { TextField, Button, Grid, Paper, Card, List } from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { Box } from '@mui/system'
import { LinearProgress } from '@mui/material'
import Top8erField from './fields/Top8erField'

function TestAPI() {
  const [state, setState] = useState({
    url: "",
    json_data: "",
    result_img_src: "https://i.imgur.com/dOjahqX.png"
  })
  const [pageState, setPageState] = useState({
    success: true,
    error_message: "",
    loading: false
  })
  const theme = useTheme()

  const handleChange = (e) => {
    setState({
      ...state,
      [e.target.name]: e.target.value
    })
  };

  const handleSubmit = (e) => {
    e.preventDefault()
    setPageState({...pageState, ['loading']: true})
    fetch(state.url, {
      method: 'POST',
      body: state.json_data,
      headers: {'Content-type': 'application/json; charset=UTF-8'}
    })
    .then((res) => res.json())
    .then((data) => {
      if ("base64_img" in data) {
        var base64_img = data["base64_img"]
        setState({
          ...state,
          ['result_img_src']: 'data:image/png;base64,' + base64_img,
        })
        setPageState({success: true, error_message: "", loading: false})
      }
      else {
        setPageState({success: false, error_message: JSON.stringify(data), loading: false})
      }
    })
    .catch((err) => {
      setPageState({success: false, error_message: "Server error. Plase contact the administrator", loading: false})
    });
  };

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
            },
            width: 1
            }}
        >

            <h2>API Explorer</h2>

            <TextField  value={state.url}
                        name="url"
                        onChange={handleChange}
                        sx={{m: 1, width: 9/10}}
                        id="url" 
                        label="URL" 
                        variant="outlined" 
                        color="secondary"/>

            <TextField  value={state.json_data}
                        name="json_data"
                        onChange={handleChange}
                        sx={{m: 1, width: 9/10}}
                        id="json" 
                        label="JSON" 
                        variant="outlined" 
                        color="secondary" 
                        multiline 
                        minRows={20}
                        maxRows={20}/>
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
              <img id="result-img" fit='scale-down' src={state.result_img_src}/>
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

export default TestAPI
