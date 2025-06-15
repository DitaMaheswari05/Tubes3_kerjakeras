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
    
def get_applicant_profile_by_cv_path(cv_path: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT ap.first_name, ap.last_name, ap.date_of_birth, ap.address, ap.phone_number
        FROM ApplicationDetail ad
        JOIN ApplicantProfile ap ON ad.applicant_id = ap.applicant_id
        WHERE ad.cv_path = %s
        LIMIT 1
    """
    cursor.execute(query, (cv_path,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


if __name__ == "__main__":
    test_connection()