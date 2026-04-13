from db_setup_loader import load_csv
from service import query

def main():
    while True:
        line = input('> ').strip()
        if line == 'exit':
            break
        elif line.startswith('load '):
            parts = line.split(maxsplit=2)
            if len(parts) == 3:
                load_csv(parts[1], parts[2])
        elif line.startswith('ask '):
            parts = line.split(maxsplit=2)
            if len(parts) == 3:
                results, sql, msg = query(parts[2], parts[1])
                print(f'SQL: {sql}')
                print(f'Message: {msg}')
                if results is not None:
                    print(f'Results: {results}')
        else:
            print('Commands: load <csv_path> <table_name> | ask <table> <question> | exit')

if __name__ == '__main__':
    main()
