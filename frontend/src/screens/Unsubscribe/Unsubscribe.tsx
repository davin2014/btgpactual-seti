import React, { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import { getTransactionsByCustomerId, updateTransaction } from '../../services/transactions.service';
import { fetchFundNames } from '../../services/funds.service';
import { customerById, updateCustomer } from '../../services/customers.service';
import { Transaction } from '../../models/transaction.model';
import { Container, Typography, Paper, List, ListItem, ListItemText, Button, Alert } from '@mui/material';
import { Customer } from '../../models/customer.model';

const Unsubscribe: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [fundNames, setFundNames] = useState<{ [key: string]: string }>({});
  const [errorMessage, setErrorMessage] = useState('');
  const [customer, setCustomer] = useState<Customer | null>(null);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const customerId = '66a76ffc96415e185fc7d4b5';
        const transactions = await getTransactionsByCustomerId(customerId);
        setTransactions(transactions);

        const fundIds = transactions.map(transaction => transaction.fund_id);
        const fundNamesMap = await fetchFundNames(fundIds);
        setFundNames(fundNamesMap);

        const customer = await customerById(customerId);
        setCustomer(customer);
      } catch (error) {
        setErrorMessage('Error fetching transactions or fund names');
      }
    };

    fetchTransactions();
  }, []);

  const handleUnsubscribe = async (transaction: Transaction) => {
    try {
      if (!transaction || !customer) {
        setErrorMessage('Transaction or customer not found');
        return;
      }
      const newTransaction = { ...transaction, type: 'unlinking' };
      // Unlink the transaction
      await updateTransaction(newTransaction._id, newTransaction);

      // Update customer balance
      const newBalance = customer.balance + transaction.amount;
      await updateCustomer(customer._id, { ...customer, balance: newBalance });

      // Update local state
      setTransactions(transactions.filter(t => t._id !== newTransaction._id));
      setCustomer({ ...customer, balance: newBalance });

      setErrorMessage('');
      toast.success('el fondo se ha desvinculado correctamente'); 
    } catch (error) {
      setErrorMessage('Error unlinking transaction');
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Salirse de un fondo actual
      </Typography>
      {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
      <Paper elevation={3}>
        <List>
          {transactions
            .filter(transaction => transaction.type === 'linking')
            .map(transaction => (
              <ListItem key={transaction._id} divider>
                <ListItemText
                  primary={`Fondo: ${fundNames[transaction.fund_id] || transaction.fund_id}`}
                  secondary={`Monto: ${transaction.amount}`}
                />
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={() => handleUnsubscribe(transaction)}
                >
                  Cancelar suscripción
                </Button>
              </ListItem>
            ))}
        </List>
      </Paper>
    </Container>
  );
};

export default Unsubscribe;