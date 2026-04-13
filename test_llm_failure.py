import pytest
from validator import validate_and_execute
import sqlite3

def setup_function():
    conn = sqlite3.connect('data.db')
    conn.execute('DROP TABLE IF EXISTS people')
    conn.execute('CREATE TABLE people (id INTEGER, name TEXT, years INTEGER)')
    conn.execute("INSERT INTO people VALUES (1, 'Alice', 30)")
    conn.commit()
    conn.close()

def teardown_function():
    conn = sqlite3.connect('data.db')
    conn.execute('DROP TABLE IF EXISTS people')
    conn.commit()
    conn.close()

def test_llm_wrong_column():
    bad_sql_from_llm = "SELECT * FROM people WHERE age > 25"
    
    results, msg = validate_and_execute(bad_sql_from_llm)
    
    assert results is None, "Validator should block bad SQL"
    assert "no such column" in msg.lower() or "age" in msg.lower()
    
    print("\n[LLM FAILURE CASE]")
    print("LLM generated SQL: " + bad_sql_from_llm)
    print("Validator error: " + msg)
    print("Result: Query was blocked because column 'age' does not exist in table 'people'")
