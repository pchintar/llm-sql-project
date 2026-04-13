import sqlite3
import pandas as pd
from schema import get_schema

def load_csv(csv_path, table_name):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect('data.db')
    
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
    
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    table_exists = cursor.fetchone() is not None
    
    if table_exists:
        existing_schema = get_schema(table_name)
        existing_cols = [col['name'].lower() for col in existing_schema]
        new_cols = [col.lower() for col in df.columns]
        
        if 'id' in existing_cols:
            existing_cols.remove('id')
        
        if existing_cols == new_cols:
            print(f"Table '{table_name}' schema matches. Appending data.")
            for _, row in df.iterrows():
                placeholders = ','.join(['?' for _ in df.columns])
                col_names = ','.join([f'"{c}"' for c in df.columns])
                conn.execute(f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})', tuple(row))
            conn.commit()
            conn.close()
            print(f"Appended {len(df)} rows to {table_name}")
            return
        else:
            print(f"Schema mismatch for '{table_name}'.")
            choice = input("(o)verwrite, (s)kip, (r)ename: ").lower()
            if choice == 's':
                conn.close()
                return
            elif choice == 'r':
                table_name = input("Enter new table name: ")
            elif choice == 'o':
                conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    
    cols = []
    for col in df.columns:
        if df[col].dtype == 'int64':
            cols.append(f'"{col}" INTEGER')
        elif df[col].dtype == 'float64':
            cols.append(f'"{col}" REAL')
        else:
            cols.append(f'"{col}" TEXT')
    
    conn.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {", ".join(cols)})')
    
    for _, row in df.iterrows():
        placeholders = ','.join(['?' for _ in df.columns])
        col_names = ','.join([f'"{c}"' for c in df.columns])
        conn.execute(f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})', tuple(row))
    
    conn.commit()
    conn.close()
    print(f"Loaded {len(df)} rows into {table_name}")
