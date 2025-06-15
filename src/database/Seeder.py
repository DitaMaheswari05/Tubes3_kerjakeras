from Database import Database
from Encryptor import Encryptor
import time
import mysql.connector

for _ in range(10):
    try:
        mysql.connector.connect(
            host="db", port=3306, user="root", password="root", database="tubes3db"
        ).close()
        break
    except mysql.connector.Error:
        time.sleep(2)
else:
    exit(1)

encryptor = Encryptor(password="TUBES")
db = Database(
    host="db",
    port=3306,
    user="root",
    password="root",
    database="tubes3db",
    encryptor=encryptor,
)

with open("seed.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

conn = db.get_connection()
cursor = conn.cursor()

for stmt in statements:
    cursor.execute(stmt)

conn.commit()
cursor.close()
conn.close()

db.encrypt_table_columns(
    table_name="ApplicantProfile",
    ids=["applicant_id"],
    columns=["first_name", "last_name", "address", "phone_number"],
    weak_columns=["phone_number"]
)

db.encrypt_table_columns(
    table_name="ApplicationDetail",
    ids=["detail_id", "applicant_id"],
    columns=["application_role", "cv_path"]
)