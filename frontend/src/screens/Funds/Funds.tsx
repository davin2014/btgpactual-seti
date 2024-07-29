import React, { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


import { fetchFunds } from '../../services/funds.service';
import { Fund } from '../../models/fund.model';

import '../../assets/css/Funds.css';

const Funds: React.FC = () => {
  const [funds, setFunds] = useState<Fund[]>([]);

  useEffect(() => {
    const getFunds = async () => {
      try {
        const data = await fetchFunds();
        setFunds(data);
      } catch (error) {
        console.error('Error fetching funds:', error);
      }
    };

    getFunds();
  }, []);

  return (
    <div>
      <h1>Lista de Fondos</h1>
      <TableContainer component={Paper} className="tableContainer">
        <Table className="table" aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell className="tableCell tableHeadCell">No.</TableCell>
              <TableCell className="tableCell tableHeadCell">Nombre</TableCell>
              <TableCell className="tableCell tableHeadCell">Monto Mínimo</TableCell>
              <TableCell className="tableCell tableHeadCell">Categoría</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {funds.map((fund, index) => (
              <TableRow
                key={fund._id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell className="tableCell tableBodyCell">{index + 1}</TableCell>
                <TableCell className="tableCell tableBodyCell">{fund.name}</TableCell>
                <TableCell className="tableCell tableBodyCell">{fund.minimum_amount}</TableCell>
                <TableCell className="tableCell tableBodyCell">{fund.category}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default Funds;