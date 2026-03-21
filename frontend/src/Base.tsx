import { useEffect } from 'react';
import { Container, Box } from '@mui/system';
import { Outlet, Link as RouterLink, useLocation } from "react-router-dom";
import Link from '@mui/material/Link';
import './Base.css';
import NavBar from './NavBar';

declare function gtag(...args: any[]): void;

function Base() {
  const location = useLocation();

  useEffect(() => {
    gtag('event', 'page_view', { page_path: location.pathname + location.search });
  }, [location]);
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <NavBar />
      <Box sx={{ height: '80px', flexShrink: 0 }} />
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Container sx={{ flex: 1 }}>
          <Outlet />
        </Container>
        <Box sx={{ bgcolor: 'black', minHeight: '30px', marginTop: '10px' }}>
          <Container sx={{ textAlign: "center", py: 0.75, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
            <span>
              Top8er is a passion project developed by <Link color="secondary" href='https://twitter.com/Riokaru' target="_blank" rel="noopener noreferrer">Riokaru</Link>.
              Consider donating on <Link color="secondary" href='https://ko-fi.com/riokaru' target="_blank" rel="noopener noreferrer">ko-fi</Link> or <Link color="secondary" href='https://www.patreon.com/Riokaru' target="_blank" rel="noopener noreferrer">Patreon</Link> if you like it.
            </span>
            <Link component={RouterLink} to="/privacy" color="secondary" variant="body2" sx={{ opacity: 0.7 }}>
              Privacy Policy
            </Link>
          </Container>
        </Box>
      </Box>
    </Box>
  );
}

export default Base;
