 # -*- coding: utf-8 -*-

"""
Nome del file: sql.py
Autore: Alessandro Di Roberto
Data: 01 Aprile 2024
Descrizione: Ricerca in ogni entità di un database (.db oppure .sqlite), la chiave indicata chiave.
             - Per ricercare una chiave:    sql.py - k "chiave" percorso_file
             - Per la stampa della guida:   sql.py -h 

Modulo richiesti:

- sqlite3
- argparse
- os

"""

import sqlite3
import argparse
import os

def search_all_tables(database_path, search_value):
    occurrence = 0

    if not os.path.exists(database_path):
        print(f"Error: the file {database_path} does not exist.")
        return

    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table = table[0]
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]

            for column in columns:
                query = f"SELECT * FROM {table} WHERE {column} LIKE ?"
                cursor.execute(query, (f"%{search_value}%",))
                results = cursor.fetchall()
                for result in results:
                    print(f"Found {search_value} in table {table}, column {column}")
                    occurrence += 1

        if occurrence == 0:
            print("Not found")
        else:
            print(f"Number of occurrences: {occurrence}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")

    finally:
        if conn:
            conn.close()

def main():
    a_path = None
    a_key = None

    parser = argparse.ArgumentParser(description='Search for a key in every entity of the SQLite database.')
    parser.add_argument('path', help='The path of the SQLite file. Supports .sqlite and .db files')
    parser.add_argument('-k', '--key', help='The key to search for in the database.')
    
    args = parser.parse_args()
    a_path = args.path
    a_key = args.key   

    if a_path is None or a_key is None:
        print("Error: no args!")
        print("For more information, use the -h option.")
        return
    
    if not os.path.exists(a_path):
        print(f"Error: the file {a_path} does not exist.")
        print("For more information, use the -h option.")
        return

    if a_key is None:
        print("Error: no key has been specified.")
        print("For more information, use the -h option.")
        return

    search_all_tables(a_path, a_key)

if __name__ == "__main__":
    main()