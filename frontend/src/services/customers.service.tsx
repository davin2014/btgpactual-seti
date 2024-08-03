import { Customer } from "../models/customer.model";


import { API_BASE_URL } from "../config/config";
export const customerById = async (id : string): Promise<Customer> => {
    try {
      const response = await fetch(`${API_BASE_URL}customers/customers/${id}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching funds:', error);
      throw error;
    }
  };

  
export const updateCustomer = async (id: string, customer: Customer): Promise<Customer> => {
    try {
        const response = await fetch(`${API_BASE_URL}customers/customers/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(customer)
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
