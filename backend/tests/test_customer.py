import unittest
import sys
import os
from unittest.mock import patch, AsyncMock

# Añadir el directorio raíz del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.crud.customer import get_customer_by_name, create_customer, update_customer, delete_customer, get_customers, get_customer_by_id
from app.models.customer import Customer, CustomerCreate, CustomerUpdate

class TestCustomer(unittest.TestCase):

    def setUp(self):
        # Configuración inicial para las pruebas
        self.customer_data = CustomerCreate(name="John Doe", email="john.doe@example.com")
        self.customer = Customer(id="123", name="John Doe", email="john.doe@example.com")

    @patch('app.crud.customer.customer_collection.insert_one', new_callable=AsyncMock)
    @patch('app.crud.customer.customer_collection.find_one', new_callable=AsyncMock)
    async def test_create_customer(self, mock_find_one, mock_insert_one):
        # Configurar el mock
        mock_insert_one.return_value.inserted_id = "123"
        mock_find_one.return_value = self.customer.dict()

        created_customer = await create_customer(self.customer_data)
        self.assertEqual(created_customer.name, self.customer.name)
        self.assertEqual(created_customer.email, self.customer.email)

    @patch('app.crud.customer.customer_collection.find_one', new_callable=AsyncMock)
    async def test_get_customer_by_id(self, mock_find_one):
        # Configurar el mock
        mock_find_one.return_value = self.customer.dict()

        customer = await get_customer_by_id("123")
        self.assertEqual(customer.name, self.customer.name)
        self.assertEqual(customer.email, self.customer.email)

    @patch('app.crud.customer.customer_collection.find_one', new_callable=AsyncMock)
    async def test_get_customer_by_name(self, mock_find_one):
        # Configurar el mock
        mock_find_one.return_value = self.customer.dict()

        customer = await get_customer_by_name("John Doe")
        self.assertEqual(customer.name, self.customer.name)
        self.assertEqual(customer.email, self.customer.email)

    @patch('app.crud.customer.customer_collection.update_one', new_callable=AsyncMock)
    @patch('app.crud.customer.customer_collection.find_one', new_callable=AsyncMock)
    async def test_update_customer(self, mock_find_one, mock_update_one):
        # Configurar el mock
        mock_find_one.return_value = self.customer.dict()
        mock_update_one.return_value.modified_count = 1

        customer_update = CustomerUpdate(email="john.new@example.com")
        updated_customer = await update_customer("123", customer_update)
        self.assertEqual(updated_customer.email, "john.new@example.com")

    @patch('app.crud.customer.customer_collection.delete_one', new_callable=AsyncMock)
    @patch('app.crud.customer.customer_collection.find_one', new_callable=AsyncMock)
    async def test_delete_customer(self, mock_find_one, mock_delete_one):
        # Configurar el mock
        mock_find_one.return_value = self.customer.dict()

        deleted_customer = await delete_customer("123")
        self.assertEqual(deleted_customer.name, self.customer.name)
        self.assertEqual(deleted_customer.email, self.customer.email)

if __name__ == '__main__':
    unittest.main()