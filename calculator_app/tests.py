import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_calculator.settings')

from django.test import TestCase
from django.urls import reverse

class CalculatorViewsTest(TestCase):

    def test_standard_calculator_get(self):
        response = self.client.get(reverse('calculator_app:standard_calculator'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Standard Calculator')

    def test_standard_calculator_post_valid(self):
        response = self.client.post(reverse('calculator_app:standard_calculator'), {'expression': '2+3*4'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '14')

    def test_standard_calculator_post_invalid(self):
        response = self.client.post(reverse('calculator_app:standard_calculator'), {'expression': '2++3'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid calculation')

    def test_interest_calculator_get(self):
        response = self.client.get(reverse('calculator_app:interest_calculator'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Interest Calculator')

    def test_interest_calculator_post_valid(self):
        data = {'principal': '1000', 'rate': '5', 'time': '2'}
        response = self.client.post(reverse('calculator_app:interest_calculator'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '100.00')  # Interest = 1000*5*2/100 = 100

    def test_interest_calculator_post_invalid(self):
        data = {'principal': 'abc', 'rate': '5', 'time': '2'}
        response = self.client.post(reverse('calculator_app:interest_calculator'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter valid numbers')

    def test_installment_calculator_get(self):
        response = self.client.get(reverse('calculator_app:installment_calculator'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Installment Calculator')

    def test_installment_calculator_post_valid(self):
        data = {'principal': '10000', 'annual_rate': '13', 'months': '6'}
        response = self.client.post(reverse('calculator_app:installment_calculator'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Monthly EMI')

    def test_installment_calculator_post_invalid(self):
        data = {'principal': '-10000', 'annual_rate': '13', 'months': '6'}
        response = self.client.post(reverse('calculator_app:installment_calculator'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Principal must be positive')

    def test_installment_calculator_post_invalid_rate(self):
        data = {'principal': '10000', 'annual_rate': '10', 'months': '6'}
        response = self.client.post(reverse('calculator_app:installment_calculator'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rate must be 13 or 15')

    def test_installment_calculator_post_invalid_months(self):
        data = {'principal': '10000', 'annual_rate': '13', 'months': '20'}
        response = self.client.post(reverse('calculator_app:installment_calculator'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'months between 2 and 12')
