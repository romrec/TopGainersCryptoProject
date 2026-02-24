import unittest
import sqlite3
import tempfile
import os
import sys
from unittest.mock import patch, Mock

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import init_db, save_to_db


class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Set up test database"""
        # Create a temporary database file for testing
        self.test_db_path = tempfile.mktemp(suffix='.db')
        # Patch the DB_PATH in the db module
        self.db_patch = patch('db.DB_PATH', self.test_db_path)
        self.db_patch.start()
    
    def tearDown(self):
        """Clean up test database"""
        self.db_patch.stop()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_init_db_creates_table(self):
        """Test that init_db creates the top_movers table"""
        # Initialize the database
        init_db()
        
        # Check if the table exists
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='top_movers'")
        table_exists = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(table_exists, "Table 'top_movers' should exist after init_db()")
        self.assertEqual(table_exists[0], 'top_movers')
    
    def test_init_db_table_structure(self):
        """Test that the top_movers table has the correct structure"""
        # Initialize the database
        init_db()
        
        # Check table structure
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(top_movers)")
        columns = cursor.fetchall()
        conn.close()
        
        # Expected columns: id, symbol, name, price, volume, change_24h, timestamp
        expected_columns = [
            (0, 'id', 'INTEGER', 0, None, 1),  # PRIMARY KEY AUTOINCREMENT
            (1, 'symbol', 'TEXT', 1, None, 0),  # NOT NULL
            (2, 'name', 'TEXT', 1, None, 0),  # NOT NULL
            (3, 'price', 'REAL', 1, None, 0),  # NOT NULL
            (4, 'volume', 'REAL', 1, None, 0),  # NOT NULL
            (5, 'change_24h', 'REAL', 1, None, 0),  # NOT NULL
            (6, 'timestamp', 'DATETIME', 0, 'CURRENT_TIMESTAMP', 0)
        ]
        
        self.assertEqual(len(columns), len(expected_columns))
        for i, (actual, expected) in enumerate(zip(columns, expected_columns)):
            self.assertEqual(actual[0], expected[0], f"Column {i} cid mismatch")
            self.assertEqual(actual[1], expected[1], f"Column {i} name mismatch")
            self.assertEqual(actual[2], expected[2], f"Column {i} type mismatch")
            self.assertEqual(actual[3], expected[3], f"Column {i} notnull mismatch")
            self.assertEqual(actual[5], expected[5], f"Column {i} pk mismatch")
    
    def test_save_to_db_inserts_record(self):
        """Test that save_to_db inserts a record into the database"""
        # Initialize the database
        init_db()
        
        # Save a record
        save_to_db('BTC', 'Bitcoin', 50000.0, 1000000.0, 5.5)
        
        # Check if the record was inserted
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT symbol, name, price, volume, change_24h FROM top_movers")
        record = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(record, "Record should be inserted into the database")
        self.assertEqual(record[0], 'BTC')
        self.assertEqual(record[1], 'Bitcoin')
        self.assertEqual(record[2], 50000.0)
        self.assertEqual(record[3], 1000000.0)
        self.assertEqual(record[4], 5.5)
    
    def test_save_to_db_multiple_records(self):
        """Test that save_to_db can insert multiple records"""
        # Initialize the database
        init_db()
        
        # Save multiple records
        save_to_db('BTC', 'Bitcoin', 50000.0, 1000000.0, 5.5)
        save_to_db('ETH', 'Ethereum', 3000.0, 800000.0, 3.2)
        save_to_db('LTC', 'Litecoin', 200.0, 500000.0, 2.1)
        
        # Check if all records were inserted
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM top_movers")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 3, "Three records should be inserted into the database")
    
    def test_save_to_db_with_timestamp(self):
        """Test that save_to_db sets the timestamp automatically"""
        # Initialize the database
        init_db()
        
        # Save a record
        save_to_db('BTC', 'Bitcoin', 50000.0, 1000000.0, 5.5)
        
        # Check if the timestamp was set
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp FROM top_movers WHERE symbol='BTC'")
        timestamp = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(timestamp, "Timestamp should be set automatically")
        self.assertIsNotNone(timestamp[0], "Timestamp value should not be None")
    
    @patch('db.sqlite3.connect')
    def test_save_to_db_handles_database_error(self, mock_connect):
        """Test that save_to_db handles database errors gracefully"""
        # Mock database error
        mock_connect.side_effect = sqlite3.Error("Database error")
        
        # This should not raise an exception
        try:
            save_to_db('BTC', 'Bitcoin', 50000.0, 1000000.0, 5.5)
        except Exception as e:
            self.fail(f"save_to_db raised an exception: {e}")
    
    def test_init_db_is_idempotent(self):
        """Test that calling init_db multiple times doesn't cause errors"""
        # Initialize the database multiple times
        init_db()
        init_db()
        init_db()
        
        # Check if the table still exists and has the correct structure
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='top_movers'")
        table_exists = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(table_exists, "Table 'top_movers' should still exist after multiple init_db() calls")
        self.assertEqual(table_exists[0], 'top_movers')


if __name__ == '__main__':
    unittest.main()