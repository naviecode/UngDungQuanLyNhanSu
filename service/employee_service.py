
class EmployeeService:
    def __init__(self, db):
        self.db = db
        
        
    def insert(self, input):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute('''
        INSERT INTO employees (name, address) VALUES (?, ?)
        ''', (input.name, input.address))
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()

        cursor.execute('SELECT *, oid FROM employees')

        rows = cursor.fetchall()

        for row in rows:
            print(row)

        cursor.close()
        self.db.close_connection()

        return rows
    def update(self, id, name, address):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute('''
        UPDATE employees SET name = ?, address = ? WHERE ID = ?
        ''', (name, address, id))
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute('''
        DELETE FROM employees WHERE ID = ?
        ''', (id))
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
