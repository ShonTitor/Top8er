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
    <>
      <NavBar />
      <Box sx={{ height: '80px' }} />
      <Box>
        <Container sx={{ minHeight: 'calc(100vh - 120px)', overflow: "hidden" }}>
          <Outlet />
        </Container>
        <Box sx={{ bgcolor: 'black', minHeight: '30px', marginTop: '10px' }}>
          <Container sx={{ textAlign: "center", py: 0.75, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
            <span>
              Top8er is a passion project developed by <Link color="secondary" href='https://twitter.com/Riokaru'>Riokaru</Link>.
              Consider donating on <Link color="secondary" href='https://ko-fi.com/riokaru'>ko-fi</Link> or <Link color="secondary" href='https://www.patreon.com/Riokaru'>Patreon</Link> if you like it.
            </span>
            <Link component={RouterLink} to="/beta/privacy" color="secondary" variant="body2" sx={{ opacity: 0.7 }}>
              Privacy Policy
            </Link>
          </Container>
        </Box>
      </Box>
    </>
  );
}

export default Base;
