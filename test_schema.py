import pytest
import sqlite3
from schema import get_schema, table_exists

def setup_function():
    conn = sqlite3.connect('data.db')
    conn.execute('DROP TABLE IF EXISTS users')
    conn.execute('CREATE TABLE users (id INTEGER, name TEXT)')
    conn.commit()
    conn.close()

def teardown_function():
    conn = sqlite3.connect('data.db')
    conn.execute('DROP TABLE IF EXISTS users')
    conn.commit()
    conn.close()

def test_get_schema():
    schema = get_schema('users')
    assert len(schema) == 2
    assert schema[0]['name'] == 'id'
    assert schema[1]['name'] == 'name'

def test_table_exists():
    assert table_exists('users') == True
    assert table_exists('fake') == False
