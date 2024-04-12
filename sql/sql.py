# -*- coding: utf-8 -*-

import sqlite3
import argparse
import os

def search_all_tables(database_path, search_value):
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

    conn.close()

def main():
    a_path = None
    a_key = None

    parser = argparse.ArgumentParser(description='Search for a key in every entity of the SQLite database.')
    parser.add_argument('path', help='The path of the SQLite file. Supports .sqlite and .db files')
    parser.add_argument('-k', '--key', type=int, help='The key to search for in the database.')
    
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