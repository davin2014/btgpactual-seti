import { Transaction } from "../models/transaction.model";

import { API_BASE_URL } from "../config/config";


export const createTransaction = async ( transaction: Transaction): Promise<Transaction> => {
    try {
        const response = await fetch(`${API_BASE_URL}transactions/transactions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(transaction)
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error updating customer:', error);
        throw error;
    }
};


export const getTransactionsByCustomerId = async (customerId: string): Promise<Transaction[]> => {
    try {
      const response = await fetch(`${API_BASE_URL}transactions/transactions/customer/${customerId}`, {
        method: 'GET',
        headers: {
          'accept': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching transactions:', error);
      throw error;
    }
  };


  export const updateTransaction = async (id: string, transaction: Transaction): Promise<Transaction> => {
    try {
        const response = await fetch(`${API_BASE_URL}transactions/transactions/${id}`,
            {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(transaction)
            });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error updating transaction:', error);
        throw error;
    }
}
