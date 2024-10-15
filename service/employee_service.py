
class EmployeeService:
    def __init__(self, db):
        self.db = db
        
        
    def insert(self, input):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute('''
        INSERT INTO employees (name, 
            date_of_birth,
            gender, 
            address, 
            phone_number, 
            email,
            position_id,
            department_id,
            start_date,
            id_card_number,
            password                                 
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (input.name, 
            input.date_of_birth,
            input.gender,
            input.address,
            input.phone_number,
            input.email,
            input.position_id,
            input.department_id,
            input.start_date,
            input.id_card_number,
            "1"
        ))
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('SELECT employee_id, name, address, gender, position_id, department_id FROM employees')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    def update(self, data):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute('''
        UPDATE employees 
        SET name = ?, date_of_birth = ? , gender = ? , address = ?,
        phone_number = ?, email = ?, position_id = ?, department_id = ?,
        start_date = ?, id_card_number = ?
        WHERE employee_id = ?
        ''', (data.name,data.date_of_birth,data.gender,data.address,
        data.phone_number, data.email, data.position_id, data.department_id,
        data.start_date,data.id_card_number, data.employee_id))
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute('DELETE FROM employees WHERE employee_id = ?',(id,))
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()

        cursor.execute('SELECT * FROM employees WHERE employee_id = ?',(id,))

        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()

        return row
    def changePassword(self, id, passwordNew):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute('''
        UPDATE employees SET password = ? WHERE employee_id = ?
        ''', (passwordNew, id))
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()
