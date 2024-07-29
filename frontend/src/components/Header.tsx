import React from 'react';
import { AppBar, Toolbar, Typography, IconButton } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import '../assets/css/Header.css';

interface HeaderProps {
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  return (
    <AppBar className="appBar">
      <Toolbar>
        <Typography variant="h6" className="typography">
        <img src="https://www.btgpactual.com/assets/images/svg/btg-logo-white.svg" alt="BTG Logo" className="logo" />
        </Typography>
        <IconButton edge="end" color="inherit" aria-label="menu" onClick={onMenuClick}>
          <MenuIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default Header;