import React, { useEffect, useState } from 'react';
import { getTransactionsByCustomerId } from '../../services/transactions.service';
import { Transaction } from '../../models/transaction.model';
import { Container, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Alert, TablePagination } from '@mui/material';

const TransactionHistory: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const customerId = '66a76ffc96415e185fc7d4b5'; // Reemplaza con el ID del cliente adecuado
        const transactions = await getTransactionsByCustomerId(customerId);
        setTransactions(transactions.sort((a, b) => {
          if (a.type === 'linking' && b.type !== 'linking') return -1;
          if (a.type !== 'linking' && b.type === 'linking') return 1;
          return a._id.localeCompare(b._id);
        }));
      } catch (error) {
        setErrorMessage('Error fetching transactions');
      }
    };

    fetchTransactions();
  }, []);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Todas las Transacciones
      </Typography>
      {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
      <Paper elevation={3}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Fondo ID</TableCell>
                <TableCell>Monto</TableCell>
                <TableCell>Tipo</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {transactions.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map(transaction => (
                <TableRow
                  key={transaction._id}
                  style={{
                    backgroundColor: transaction.type === 'unlinking' ? 'red' : transaction.type === 'linking' ? 'green' : 'inherit'
                  }}
                >
                  <TableCell>{transaction._id}</TableCell>
                  <TableCell>{transaction.fund_id}</TableCell>
                  <TableCell>{transaction.amount}</TableCell>
                  <TableCell>
                    {transaction.type === 'unlinking' ? 'Cancelada' : transaction.type === 'linking' ? 'Activa' : transaction.type}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[10, 100, 300]}
          component="div"
          count={transactions.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
    </Container>
  );
};

export default TransactionHistory;
