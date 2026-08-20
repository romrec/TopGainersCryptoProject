import unittest
import os
import sys
from unittest.mock import patch, Mock, MagicMock

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import init_db, save_to_db, get_top_movers_from_db, get_latest_by_symbol


class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        # Mock the database connection
        self.conn_patcher = patch('db.get_db_connection')
        self.mock_get_conn = self.conn_patcher.start()
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.mock_get_conn.return_value = self.mock_conn

    def tearDown(self):
        """Clean up test environment"""
        self.conn_patcher.stop()

    def test_init_db_creates_table(self):
        """Test that init_db creates the top_movers table"""
        init_db()

        # Verify the CREATE TABLE query was executed
        self.mock_cursor.execute.assert_called_once()
        create_query = self.mock_cursor.execute.call_args[0][0]
        self.assertIn('CREATE TABLE IF NOT EXISTS top_movers', create_query)
        self.mock_conn.commit.assert_called_once()
        self.mock_conn.close.assert_called_once()

    def test_init_db_is_idempotent(self):
        """Test that calling init_db multiple times doesn't cause errors"""
        init_db()
        init_db()
        init_db()

        # Verify the CREATE TABLE query was executed 3 times
        self.assertEqual(self.mock_cursor.execute.call_count, 3)
        self.assertEqual(self.mock_conn.commit.call_count, 3)

    def test_init_db_table_structure(self):
        """Test that the top_movers table has the correct structure"""
        init_db()

        # Verify the CREATE TABLE query contains all expected columns
        create_query = self.mock_cursor.execute.call_args[0][0]
        expected_columns = ['id', 'symbol', 'name', 'price', 'volume', 'change_24h', 'timestamp']
        for col in expected_columns:
            self.assertIn(col, create_query, f"Column '{col}' should be in CREATE TABLE query")

    def test_save_to_db_inserts_record(self):
        """Test that save_to_db inserts a record into the database"""
        self.mock_cursor.rowcount = 1
        result = save_to_db('BTC', 'Bitcoin', 50000.0, 1000000.0, 5.5)

        self.assertTrue(result)
        self.mock_cursor.execute.assert_called_once()
        query, params = self.mock_cursor.execute.call_args[0]
        self.assertIn('INSERT INTO top_movers', query)
        self.assertEqual(params, ('BTC', 'Bitcoin', 50000.0, 1000000.0, 5.5))
        self.mock_conn.commit.assert_called_once()
        self.mock_conn.close.assert_called_once()

    def test_save_to_db_multiple_records(self):
        """Test that save_to_db can insert multiple records"""
        self.mock_cursor.rowcount = 1
        result1 = save_to_db('BTC', 'Bitcoin', 50000.0, 1000000.0, 5.5)
        result2 = save_to_db('ETH', 'Ethereum', 3000.0, 800000.0, 3.2)
        result3 = save_to_db('LTC', 'Litecoin', 200.0, 500000.0, 2.1)

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertEqual(self.mock_cursor.execute.call_count, 3)
        self.assertEqual(self.mock_conn.commit.call_count, 3)

    def test_save_to_db_with_timestamp(self):
        """Test that save_to_db inserts a record (timestamp is set by DB default)"""
        self.mock_cursor.rowcount = 1
        result = save_to_db('BTC', 'Bitcoin', 50000.0, 1000000.0, 5.5)

        self.assertTrue(result)
        # Verify the INSERT query doesn't include timestamp (DB default NOW())
        query, params = self.mock_cursor.execute.call_args[0]
        self.assertNotIn('timestamp', query, "Timestamp should be set by DB default")

    def test_save_to_db_handles_database_error(self):
        """Test that save_to_db handles database errors gracefully"""
        self.mock_cursor.execute.side_effect = Exception("Database error")

        # This should not raise an exception
        try:
            result = save_to_db('BTC', 'Bitcoin', 50000.0, 1000000.0, 5.5)
            self.assertFalse(result, "save_to_db should return False on error")
        except Exception as e:
            self.fail(f"save_to_db raised an exception: {e}")

    def test_get_top_movers_from_db(self):
        """Test that get_top_movers_from_db returns records"""
        self.mock_cursor.fetchall.return_value = [
            {'symbol': 'BTC', 'name': 'Bitcoin', 'price': 50000.0, 'volume': 1000000.0, 'change_24h': 5.5, 'timestamp': '2024-01-01'}
        ]

        result = get_top_movers_from_db()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['symbol'], 'BTC')
        self.mock_cursor.execute.assert_called_once()
        query, params = self.mock_cursor.execute.call_args[0]
        self.assertIn('SELECT', query)
        self.assertIn('ORDER BY timestamp DESC', query)
        self.assertEqual(params, (10,))

    def test_get_latest_by_symbol(self):
        """Test that get_latest_by_symbol returns the latest record for a symbol"""
        self.mock_cursor.fetchone.return_value = {
            'symbol': 'BTC', 'name': 'Bitcoin', 'price': 50000.0, 'volume': 1000000.0, 'change_24h': 5.5, 'timestamp': '2024-01-01'
        }

        result = get_latest_by_symbol('BTC')

        self.assertIsNotNone(result)
        self.assertEqual(result['symbol'], 'BTC')
        self.mock_cursor.execute.assert_called_once()
        query, params = self.mock_cursor.execute.call_args[0]
        self.assertIn('WHERE symbol = %s', query)
        self.assertEqual(params, ('BTC',))


if __name__ == '__main__':
    unittest.main()