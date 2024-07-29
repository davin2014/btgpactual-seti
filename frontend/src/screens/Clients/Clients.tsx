import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { CLIENT } from '../../models/client.model';
import { getAllClients } from '../../services/clients.service';
import '../../assets/css/Clients.css';

export default function Clients() {
  const [clients, setClients] = useState<CLIENT[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await getAllClients();
      setClients(response);
    };

    fetchData();
  }, []);

  return (
    <TableContainer component={Paper} className="tableContainer">
      <Table className="table" aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell className="tableCell tableHeadCell">Id</TableCell>
            <TableCell className="tableCell tableHeadCell">Nombre</TableCell>
            <TableCell className="tableCell tableHeadCell">Apellido</TableCell>
            <TableCell className="tableCell tableHeadCell">Ciudad</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {clients.map((row) => (
            <TableRow
              key={row.id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell className="tableCell tableBodyCell">{row.id}</TableCell>
              <TableCell className="tableCell tableBodyCell">{row.name}</TableCell>
              <TableCell className="tableCell tableBodyCell">{row.lastname}</TableCell>
              <TableCell className="tableCell tableBodyCell">{row.city}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}