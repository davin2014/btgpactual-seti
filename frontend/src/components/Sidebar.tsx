import React from 'react';
import { Drawer, List, ListItemText, ListItemButton } from '@mui/material';
import { NavLink } from 'react-router-dom';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
  navLink: {
    textDecoration: 'none',
    color: 'inherit',
  },
  listItem: {
    '&.active': {
      backgroundColor: '#f0f0f0',
    },
  },
});

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const classes = useStyles();

  return (
    <Drawer anchor="right" open={open} onClose={onClose}>
      <List>
        <ListItemButton component={NavLink} to="/" className={`${classes.navLink} ${classes.listItem}`} onClick={onClose}>
          <ListItemText primary="Inicio" />
        </ListItemButton>
        <ListItemButton component={NavLink} to="/subscribe" className={`${classes.navLink} ${classes.listItem}`} onClick={onClose}>
          <ListItemText primary="Suscribirse a un fondo" />
        </ListItemButton>
        <ListItemButton component={NavLink} to="/unsubscribe" className={`${classes.navLink} ${classes.listItem}`} onClick={onClose}>
          <ListItemText primary="Cancelar suscripción" />
        </ListItemButton>
        <ListItemButton component={NavLink} to="/transaction-history" className={`${classes.navLink} ${classes.listItem}`} onClick={onClose}>
          <ListItemText primary="Historial de transacciones" />
        </ListItemButton>
        <ListItemButton component={NavLink} to="/funds" className={`${classes.navLink} ${classes.listItem}`} onClick={onClose}>
          <ListItemText primary="Fondos" />
        </ListItemButton>
      </List>
    </Drawer>
  );
};

export default Sidebar;