import sqlite3
import re
import logging
from schema import get_schema

logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s - %(message)s')

def validate_and_execute(sql):
    conn = sqlite3.connect('data.db')
    
    if not sql.strip().upper().startswith('SELECT'):
        msg = 'Only SELECT allowed'
        logging.error(msg)
        conn.close()
        return None, msg
    
    match = re.search(r'FROM\s+(\w+)', sql, re.IGNORECASE)
    if not match:
        msg = 'No table found'
        logging.error(msg)
        conn.close()
        return None, msg
    
    table = match.group(1)
    
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    if not cursor.fetchone():
        msg = f'Table {table} not found'
        logging.error(msg)
        conn.close()
        return None, msg
    
    valid_cols = [col['name'] for col in get_schema(table)]
    valid_cols_lower = [c.lower() for c in valid_cols]
    
    # Skip column check if SELECT *
    if '*' not in sql:
        # Find column names (letters and underscores, not SQL keywords)
        keywords = {'select', 'from', 'where', 'and', 'or', 'not', 'in', 'like', 'order', 'by', 'group', 'limit', 'join', 'on', 'as', 'null', 'true', 'false', 'inner', 'left', 'right'}
        words = re.findall(r'\b[a-z_][a-z0-9_]*\b', sql.lower())
        potential_cols = [w for w in words if w not in keywords and not w.isdigit()]
        
        for col in potential_cols:
            if col not in valid_cols_lower:
                msg = f"Column '{col}' not found in table {table}"
                logging.error(msg)
                conn.close()
                return None, msg
    
    try:
        cursor = conn.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return results, 'Success'
    except Exception as e:
        logging.error(str(e))
        conn.close()
        return None, str(e)
