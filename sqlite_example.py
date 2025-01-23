import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('medicine.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# SQL command to create the medicines table
create_table_query = '''
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);
'''

# Execute the SQL command
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")




