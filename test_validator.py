import pytest
from validator import validate_and_execute
import sqlite3

def setup_function():
    conn = sqlite3.connect('data.db')
    conn.execute('DROP TABLE IF EXISTS users')
    conn.execute('CREATE TABLE users (id INTEGER, name TEXT)')
    conn.execute("INSERT INTO users VALUES (1, 'test')")
    conn.commit()
    conn.close()

def teardown_function():
    conn = sqlite3.connect('data.db')
    conn.execute('DROP TABLE IF EXISTS users')
    conn.commit()
    conn.close()

def test_select_valid():
    results, msg = validate_and_execute('SELECT * FROM users')
    assert results is not None

def test_delete_invalid():
    results, msg = validate_and_execute('DELETE FROM users')
    assert results is None
    assert 'Only SELECT' in msg
