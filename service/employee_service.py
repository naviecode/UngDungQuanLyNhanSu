from data.init_data import InitData
import configparser

class EmployeeService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)
        
    def insert(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        INSERT INTO employees (
            name, 
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
        VALUES 
        (
            N'{input.name}', 
            '{input.date_of_birth}',
            {input.gender},
            N'{input.address}',
            '{input.phone_number}',
            '{input.email}',
            {input.position_id},
            {input.department_id},
            '{input.start_date}',
            '{input.id_card_number}',
            {'"1"'}
        )
        ''')

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
        self.db.connection.cursor().execute(f'''
        UPDATE employees 
        SET name = N'{data.name}', 
        date_of_birth = '{data.date_of_birth}', 
        gender = {data.gender} , 
        address = N'{data.address}',
        phone_number = '{data.phone_number}', 
        email = '{data.email}', 
        position_id = {data.position_id}, 
        department_id = {data.department_id},
        start_date = '{data.start_date}', 
        id_card_number = {data.id_card_number}
        WHERE employee_id = {data.employee_id}
        ''')
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'DELETE FROM employees WHERE employee_id = {id}')
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()

        cursor.execute(f'SELECT * FROM employees WHERE employee_id = {id}')

        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()

        return row
    def changePassword(self, id, passwordNew):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        UPDATE employees SET password = '{passwordNew}' WHERE employee_id = {id}
        ''')
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()
