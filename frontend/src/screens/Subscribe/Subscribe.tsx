import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { fetchFunds } from '../../services/funds.service';
import { Fund } from '../../models/fund.model';
import {
  Container,
  Title,
  Label,
  Select,
  Input,
  Button,
  ErrorMessage,
  Balance
} from '../../assets/js/css/Subscribe.styles';
import { Customer } from '../../models/customer.model';
import { customerById, updateCustomer } from '../../services/customers.service';
import { createTransaction } from '../../services/transactions.service';
import { Transaction } from '../../models/transaction.model';
import { NumberFormatValues, NumericFormat } from 'react-number-format';


const initialBalance = 500000; // COP $500.000

const Subscribe: React.FC = () => {
  const [balance, setBalance] = useState(initialBalance);
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [funds, setFunds] = useState<Fund[]>([]);
  const [selectedFund, setSelectedFund] = useState('');
  const [investmentAmount, setInvestmentAmount] = useState<number | string>('');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const loadCustomerData = async () => {
      try {
        const id = '66a76ffc96415e185fc7d4b5';
        const customer: Customer = await customerById(id);
        setCustomer(customer);
        setBalance(customer.balance);
      } catch (error) {
        console.error('Error loading customer data:', error);
      }
    };

    const loadFunds = async () => {
      try {
        const fetchedFunds = await fetchFunds();
        setFunds(fetchedFunds);
        if (fetchedFunds.length > 0) {
          setSelectedFund(fetchedFunds[0].name);
          setInvestmentAmount(fetchedFunds[0].minimum_amount);
        }
      } catch (error) {
        console.error('Error loading funds:', error);
      }
    };

    loadCustomerData();
    loadFunds();
  }, []);

  useEffect(() => {
    const fund = funds.find(f => f.name === selectedFund);
    if (fund) {
      setInvestmentAmount(fund.minimum_amount);
    }
  }, [selectedFund, funds]);

  

  const updateCustomerBalance = async (newBalance: number) => {
    if (customer) {
      try {
        const updatedCustomer: Customer = await updateCustomer(customer._id, { ...customer, balance: newBalance });
        setBalance(updatedCustomer.balance);
      } catch (error) {
        console.error('Error updating balance:', error);
        setErrorMessage('Failed to update balance');
      }
    }
  };

  const handleSubscribe = async () => {
    
    const fund = funds.find(f => f.name === selectedFund);
    const amount = typeof investmentAmount === 'string' ? parseFloat(investmentAmount) : investmentAmount;
  
    if (fund) {
      if (amount < fund.minimum_amount) {
        toast.error(`El monto es menor al mínimo requerido para el fondo ${selectedFund}`);
        setErrorMessage('');
      } else if (balance < amount) {
        toast.error('No tiene saldo disponible'); 
        setErrorMessage('');
      } else {
        try {
          await updateCustomerBalance(balance - amount);

          const transaction: Transaction = {
            _id: '',
            fund_id: fund._id,
            customer_id: customer!._id,
            amount: amount,
            type: 'linking'
          };

          const createdTransaction = await createTransaction(transaction);
          console.log(`Transaction created: ${createdTransaction}`);
          setErrorMessage('');
          toast.success('La inversión fue guardada correctamente'); 
        } catch (error) {
          console.error('Error creating transaction:', error);
          setErrorMessage('Failed to create transaction');
        }
      }
    } else {
      setErrorMessage('Fondo seleccionado no encontrado');
    }
  };

  const handleAmountChange = (values: NumberFormatValues) => {
    const { value } = values;
    if (!isNaN(Number(value)) && Number(value) >= 0) {
      setInvestmentAmount(value);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(amount);
  };

  

  return (
    <Container>
      <Title>Suscribirse a un nuevo fondo</Title>
      <div>
        <Label htmlFor="fund">Seleccione un fondo:</Label>
        <Select
          id="fund"
          value={selectedFund}
          onChange={(e) => setSelectedFund(e.target.value)}
        >
          {funds.map((fund) => (
            <option key={fund.name} value={fund.name}>
              {fund.name} (Mínimo: COP ${fund.minimum_amount})
            </option>
          ))}
        </Select>
      </div>
      <div>
        <Label htmlFor="amount">Monto a invertir:</Label>
        <NumericFormat
          id="amount"
          value={investmentAmount}
          thousandSeparator={true}
          decimalScale={2}
          fixedDecimalScale={true}
          onValueChange={handleAmountChange}
          prefix="COP "
          customInput={Input}
        />
      </div>
      <Button onClick={handleSubscribe}>Suscribirse</Button>
      {errorMessage && <ErrorMessage>{errorMessage}</ErrorMessage>}
      <Balance>Saldo disponible: {formatCurrency(balance)}</Balance>
    </Container>
  );
};

export default Subscribe;