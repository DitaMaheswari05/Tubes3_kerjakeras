import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",      # atau "127.0.0.1"
        port=3306,
        user="root",
        password="root",
        database="tubes3db"
    )

# Contoh query
def test_connection():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    for (table_name,) in cursor.fetchall():
        print(table_name)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    test_connection()