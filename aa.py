import sqlite3

# Establish connection to SQLite database
conn = sqlite3.connect('app_data.db')
cursor = conn.cursor()

# Create admin table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')

# Insert admin credentials
admin_username = 'ad'
admin_password = 'admin12'

try:
    cursor.execute('''
        INSERT INTO admin (username, password)
        VALUES (?, ?)
    ''', (admin_username, admin_password))
    conn.commit()
    print("Admin credentials created successfully!")
except sqlite3.IntegrityError:
    print("Admin credentials already exist!")

conn.close()
