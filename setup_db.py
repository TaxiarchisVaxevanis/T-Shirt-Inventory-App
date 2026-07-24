import sqlite3

def create_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS shirts')
    cursor.execute('''
        CREATE TABLE shirts ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            color TEXT,
            size TEXT,
            initial_qty INTEGER,
            sold_qty INTEGER
        )
    ''')

    thanasis_data = [
        ("ΜΠΟΡΝΤΟ", "2XL", 2, 1), ("ΜΠΟΡΝΤΟ", "XL", 3, 3),
        ("ΜΠΟΡΝΤΟ", "L", 3, 1), ("ΜΠΟΡΝΤΟ", "M", 3, 3), ("ΜΠΟΡΝΤΟ", "S", 1, 1),
        ("ΜΠΕΖ", "XL", 2, 0), ("ΜΠΕΖ", "L", 2, 0), ("ΜΠΕΖ", "M", 2, 1), ("ΜΠΕΖ", "S", 1, 0),
        ("ΛΕΥΚΑ", "XL", 3, 2), ("ΛΕΥΚΑ", "L", 3, 0), ("ΛΕΥΚΑ", "M", 3, 1),
        ("ΛΕΥΚΑ", "S", 3, 0), ("ΛΕΥΚΑ", "9-10", 3, 0),
        ("ΜΑΥΡΑ", "2XL", 3, 0), ("ΜΑΥΡΑ", "XL", 7, 3), ("ΜΑΥΡΑ", "L", 3, 1),
        ("ΜΑΥΡΑ", "M", 3, 2), ("ΜΑΥΡΑ", "S", 3, 2), ("ΜΑΥΡΑ", "9-10", 3, 0), ("ΜΑΥΡΑ", "3XL", 2, 1)
    ]

    cursor.executemany('INSERT INTO shirts (color, size, initial_qty, sold_qty) VALUES (?,?,?,?)', thanasis_data)
    conn.commit()
    conn.close()
    print("Η βάση δημιουργήθηκε επιτυχώς")

if __name__ == "__main__":
    create_db()