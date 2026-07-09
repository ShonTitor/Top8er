import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import TwitterIcon from '@mui/icons-material/Twitter';
import SvgIcon, { SvgIconProps } from '@mui/material/SvgIcon';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import Icon from '@mui/material/Icon';
import logo from './assets/top8er_square_white.svg';
import { Link as RouterLink, useLocation, useMatch } from 'react-router-dom';

function BlueskyIcon(props: SvgIconProps) {
  return (
    <SvgIcon {...props} viewBox="0 0 24 24">
      <path d="M5.202 2.857C7.954 4.922 10.913 9.11 12 11.358c1.087-2.247 4.046-6.436 6.798-8.501C20.783 1.366 24 .213 24 3.883c0 .732-.42 6.156-.667 7.037-.856 3.061-3.978 3.842-6.755 3.37 4.854.826 6.089 3.562 3.422 6.299-5.065 5.196-7.28-1.304-7.847-2.97-.104-.305-.152-.448-.153-.327 0-.121-.05.022-.153.327-.568 1.666-2.782 8.166-7.847 2.97-2.667-2.737-1.432-5.473 3.422-6.3-2.777.473-5.899-.308-6.755-3.369C.42 10.04 0 4.615 0 3.883c0-3.67 3.217-2.517 5.202-1.026" />
    </SvgIcon>
  );
}

const pages = [
  { label: 'Home', path: '/' },
  { label: 'About', path: '/about' },
  { label: 'Special Thanks', path: '/special-thanks' },
  { label: 'Blog', path: '/blog' },
  { label: 'Contact', path: '/contact' },
];

function NavBar() {
  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
  const location = useLocation();
  const templateMatch = useMatch('/template/:template/game/:gameName');
  const classicSiteHref = templateMatch?.params.gameName
    ? `/old/${templateMatch.params.gameName}`
    : '/old/ssbu';

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
            <img src={logo} alt="Top8er logo" />
          </Icon>
          <Typography
            variant="h6"
            noWrap
            component={RouterLink}
            to="/"
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
              <MenuItem onClick={handleCloseNavMenu} component="a" href={classicSiteHref}>
                <Typography textAlign="center">Classic Site</Typography>
              </MenuItem>
            </Menu>
          </Box>

          {/* Mobile: centered logo + title */}
          <Icon sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }}>
            <img src={logo} alt="Top8er logo" />
          </Icon>
          <Typography
            variant="h6"
            noWrap
            component={RouterLink}
            to="/"
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
            <Button
              component="a"
              href={classicSiteHref}
              sx={{
                color: 'white',
                fontWeight: 400,
                opacity: 0.75,
                borderBottom: '2px solid transparent',
                borderRadius: 0,
                px: 1.5,
                '&:hover': { opacity: 1, bgcolor: 'rgba(255,255,255,0.08)' },
              }}
            >
              Classic Site
            </Button>
          </Box>

          <IconButton
            component="a"
            href="https://x.com/Top8er"
            target="_blank"
            rel="noopener noreferrer"
            color="inherit"
            aria-label="Top8er on Twitter/X"
          >
            <TwitterIcon />
          </IconButton>
          <IconButton
            component="a"
            href="https://bsky.app/profile/top8er.bsky.social"
            target="_blank"
            rel="noopener noreferrer"
            color="inherit"
            aria-label="Top8er on Bluesky"
          >
            <BlueskyIcon fontSize="small" />
          </IconButton>

        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default NavBar;
