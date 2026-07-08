import { useEffect, useRef, useState, Suspense } from 'react';
import { Container, Box } from '@mui/system';
import { Outlet, Link as RouterLink, useLocation } from "react-router-dom";
import Link from '@mui/material/Link';
import './Base.css';
import NavBar from './NavBar';

declare function gtag(...args: any[]): void;

// Fixed navbar height, in sync with the spacer Box below it.
const NAVBAR_HEIGHT = 64;

function Base() {
  const location = useLocation();
  const chromeRef = useRef<HTMLDivElement>(null);
  // Measured height of navbar-spacer + banner combined, kept live so pages
  // (e.g. TemplateForm's sticky sidebar) can size against "the rest of the
  // viewport" without hardcoding a guess at how tall the banner is.
  const [chromeHeight, setChromeHeight] = useState(NAVBAR_HEIGHT);

  useEffect(() => {
    gtag('event', 'page_view', { page_path: location.pathname + location.search });
  }, [location]);

  useEffect(() => {
    const el = chromeRef.current;
    if (!el) return;
    const observer = new ResizeObserver(entries => {
      setChromeHeight(entries[0].contentRect.height);
    });
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <Box
      sx={{ display: 'flex', flexDirection: 'column', height: '100vh', overflowY: 'auto' }}
      style={{ ['--chrome-height' as any]: `${chromeHeight}px` }}
    >
      <NavBar />
      <Box ref={chromeRef}>
        <Box sx={{ height: `${NAVBAR_HEIGHT}px`, flexShrink: 0 }} />
        <Box sx={{ bgcolor: '#d32f2f', color: '#fff', textAlign: 'center', py: 1, px: 2, fontSize: '0.95rem', fontWeight: 500 }}>
          🇻🇪 Venezuela earthquake relief. Please consider{' '}
          <Link href="https://www.gofundme.com/f/venezuela-fg-community-earthquake-relief" target="_blank" rel="noopener noreferrer" sx={{ color: '#fff', fontWeight: 700, textDecorationColor: '#fff' }}>
            donating to the venezuelan FGC community relief fund
          </Link>
          .
        </Box>
      </Box>
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Container sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <Suspense fallback={null}>
            <Outlet />
          </Suspense>
        </Container>
        <Box sx={{ bgcolor: 'black', minHeight: '30px', marginTop: '10px', flexShrink: 0 }}>
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
