import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import Icon from '@mui/material/Icon';
import logo from './assets/top8er_square_white.svg';
import { Link as RouterLink, useLocation } from 'react-router-dom';

const pages = [
  { label: 'Home', path: '/beta/' },
  { label: 'About', path: '/beta/about' },
  { label: 'Special Thanks', path: '/beta/special-thanks' },
];

function NavBar() {
  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
  const location = useLocation();

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <AppBar enableColorOnDark position="fixed">
      <Container maxWidth="xl">
        <Toolbar disableGutters>

          {/* Desktop: logo + title */}
          <Icon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }}>
            <img src={logo} />
          </Icon>
          <Typography
            variant="h6"
            noWrap
            component={RouterLink}
            to="/beta/"
            sx={{
              mr: 3,
              display: { xs: 'none', md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            Top8er.com
          </Typography>

          {/* Mobile: hamburger menu */}
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton size="large" onClick={handleOpenNavMenu} color="inherit">
              <MenuIcon />
            </IconButton>
            <Menu
              anchorEl={anchorElNav}
              anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
              keepMounted
              transformOrigin={{ vertical: 'top', horizontal: 'left' }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{ display: { xs: 'block', md: 'none' } }}
            >
              {pages.map(page => (
                <MenuItem
                  key={page.label}
                  onClick={handleCloseNavMenu}
                  component={RouterLink}
                  to={page.path}
                  selected={isActive(page.path)}
                >
                  <Typography textAlign="center">{page.label}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>

          {/* Mobile: centered logo + title */}
          <Icon sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }}>
            <img src={logo} />
          </Icon>
          <Typography
            variant="h6"
            noWrap
            component={RouterLink}
            to="/beta/"
            sx={{
              flexGrow: 1,
              display: { xs: 'flex', md: 'none' },
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            Top8er.com
          </Typography>

          {/* Desktop: nav links */}
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' }, gap: 0.5 }}>
            {pages.map(page => (
              <Button
                key={page.label}
                component={RouterLink}
                to={page.path}
                sx={{
                  color: 'white',
                  fontWeight: isActive(page.path) ? 700 : 400,
                  opacity: isActive(page.path) ? 1 : 0.75,
                  borderBottom: isActive(page.path) ? '2px solid rgba(255,255,255,0.8)' : '2px solid transparent',
                  borderRadius: 0,
                  px: 1.5,
                  '&:hover': { opacity: 1, bgcolor: 'rgba(255,255,255,0.08)' },
                }}
              >
                {page.label}
              </Button>
            ))}
          </Box>

        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default NavBar;
