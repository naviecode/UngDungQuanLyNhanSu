from data.init_data import InitData
import configparser

class EmployeeRoleService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)

    def insert(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        print(input)
        self.db.connection.cursor().execute(f'''
        INSERT INTO employee_roles (
            employee_id, 
            role_id                         
        )
        VALUES 
        (
            {input["employee_id"]}, 
            {input["role_id"]}
        )
        ''')

        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('''
            SELECT A.employee_role_id, B.name, C.role_name
            FROM employee_roles A
            LEFT JOIN employees B ON A.employee_id = B.employee_id
            LEFT JOIN roles C ON A.role_id = C.role_id
        ''')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    def update(self, data):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        UPDATE employee_roles 
        SET employee_id = {data["employee_id"]}, 
        role_id = {data["role_id"]}
        WHERE employee_role_id = {data["employee_role_id"]}
        ''')
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'DELETE FROM employee_roles WHERE employee_role_id = {id}')
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        cursor.execute(f'SELECT employee_role_id, employee_id, role_id  FROM employee_roles WHERE employee_role_id = {id}')
        columns_name = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()
        row_dict = dict(zip(columns_name, row))
        return row_dict