import mysql.connector

class Database:
    def __init__(self, host, port, user, password, database, encryptor):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.encryptor = encryptor

    def get_connection(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except Exception as err:
            print(f"Database connection failed: {err}")
            raise

    def encrypt_table_columns(self, table_name, ids, columns, weak_columns=None):
        weak_columns = weak_columns or []

        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()

        for record in records:
            update_needed = False
            encrypted_values = {}

            for col in columns:
                if col in record and record[col] is not None:
                    if col in weak_columns:
                        encrypted = self.encryptor.weak_encrypt(str(record[col]))
                    else:
                        encrypted = self.encryptor.encrypt(str(record[col]))
                    encrypted_values[col] = encrypted
                    update_needed = True

            if update_needed:
                set_clause = ", ".join([f"{col} = %s" for col in encrypted_values])
                where_clause = " AND ".join([f"{id_col} = %s" for id_col in ids])
                sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
                params = list(encrypted_values.values()) + [record[id_col] for id_col in ids]
                cursor.execute(sql, params)

        conn.commit()
        cursor.close()
        conn.close()

    def run_query(self, query, params=None, decrypt_fields=None, weak_fields=None):
        weak_fields = weak_fields or []
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or [])

            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()

                if decrypt_fields:
                    for row in results:
                        for field in decrypt_fields:
                            if field in row and row[field] is not None:
                                try:
                                    if isinstance(row[field], str):
                                        if field in weak_fields:
                                            row[field] = self.encryptor.weak_decrypt(row[field])
                                        else:
                                            row[field] = self.encryptor.decrypt(row[field])
                                except Exception as e:
                                    print(f"Failed to decrypt field '{field}':", e)
                return results
            else:
                conn.commit()
                return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    def decrypt_value(self, encrypted_value, weak=False):
        if weak:
            return self.encryptor.weak_decrypt(encrypted_value)
        return self.encryptor.decrypt(encrypted_value)