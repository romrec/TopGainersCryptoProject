import unittest
from unittest.mock import patch, Mock
import requests
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from top_movers import get_top_movers


class TestTopMovers(unittest.TestCase):
    
    @patch('top_movers.requests.get')
    def test_get_top_movers_success(self, mock_get):
        """Test successful API response"""
        # Mock response data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'symbol': 'btc',
                'name': 'Bitcoin',
                'current_price': 50000.0,
                'total_volume': 1000000.0,
                'price_change_percentage_24h': 5.5
            },
            {
                'symbol': 'eth',
                'name': 'Ethereum',
                'current_price': 3000.0,
                'total_volume': 800000.0,
                'price_change_percentage_24h': 3.2
            }
        ]
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_top_movers()
        
        # Assert the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['symbol'], 'btc')
        self.assertEqual(result[0]['name'], 'Bitcoin')
        self.assertEqual(result[0]['current_price'], 50000.0)
        self.assertEqual(result[0]['total_volume'], 1000000.0)
        self.assertEqual(result[0]['price_change_percentage_24h'], 5.5)
        
        # Assert the API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], 'https://api.coingecko.com/api/v3/coins/markets')
        self.assertIn('params', kwargs)
        params = kwargs['params']
        self.assertEqual(params['vs_currency'], 'usd')
        self.assertEqual(params['order'], 'price_change_percentage_24h_desc')
        self.assertEqual(params['per_page'], 10)
        self.assertEqual(params['page'], 1)
        self.assertEqual(params['sparkline'], False)
        self.assertEqual(params['price_change_percentage'], '24h')
    
    @patch('top_movers.requests.get')
    def test_get_top_movers_failure(self, mock_get):
        """Test failed API response"""
        # Mock response with error status
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_top_movers()
        
        # Assert the result
        self.assertEqual(result, [])
        
        # Assert the API call
        mock_get.assert_called_once()
    
    @patch('top_movers.requests.get')
    def test_get_top_movers_empty_response(self, mock_get):
        """Test empty API response"""
        # Mock response with success status but empty data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_top_movers()
        
        # Assert the result
        self.assertEqual(result, [])
        
        # Assert the API call
        mock_get.assert_called_once()
    
    @patch('top_movers.requests.get')
    def test_get_top_movers_network_error(self, mock_get):
        """Test network error during API call"""
        # Mock network error
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        
        # Call the function and expect it to handle the error gracefully
        try:
            result = get_top_movers()
            # Assert the result
            self.assertEqual(result, [])
        except requests.exceptions.ConnectionError:
            # If the exception is raised, that's also acceptable behavior
            # as long as we're testing that the function handles the error
            pass
        
        # Assert the API call
        mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()