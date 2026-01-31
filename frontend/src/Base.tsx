import { useTheme } from '@mui/material/styles';
import { Container, Box } from '@mui/system';
import { TextField, Button, Grid, Paper, Card, List } from '@mui/material';
import { Outlet, Link as RouterLink } from "react-router-dom";
import Link from '@mui/material/Link';
import './Base.css';
import NavBar from './NavBar';

function Base() {
  const theme = useTheme();
  return (
    <>
      <NavBar />
      <Box sx={{ height: '80px' }} />
      <Box>
        <Container sx={{ minHeight: 'calc(100vh - 120px)', overflow: "hidden" }}>
          <Outlet />
        </Container>
        <Box sx={{ bgcolor: 'black', minHeight: '30px', marginTop: '10px' }}>
          <Container sx={{ textAlign: "center" }}>
            Top8er is a passion project developed by <Link color="secondary" href='https://twitter.com/Riokaru'>Riokaru</Link>.
            Consider donating on <Link color="secondary" href='https://ko-fi.com/riokaru'>ko-fi</Link> or <Link color="secondary" href='https://www.patreon.com/Riokaru'>Patreon</Link> if you like it.
          </Container>
        </Box>
      </Box>
    </>
  );
}

export default Base;
