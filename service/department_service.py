from data import InitData
import configparser

class DepartMentService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)

    def insert(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        self.db.connection.cursor().execute(f'''
        INSERT INTO departments (
            department_name, 
            description,
            location, 
            manager_id,
            create_date                            
        )
        VALUES 
        (
            '{input["department_name"]}', 
            '{input["description"]}',
            '{input["location"]}',
            {input["manager_id"]},
            CURDATE()
        )
        ''')

        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self, filter = None):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('''
            SELECT A.department_id, A.department_name, A.description, A.location, DATE_FORMAT( A.create_date, '%d/%m/%Y') as create_date,
            B.name
            FROM departments A
            LEFT JOIN employees B ON A.manager_id = B.employee_id
        ''')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    def update(self, data):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        UPDATE departments 
        SET department_name = N'{data["department_name"]}', 
        description = N'{data["description"]}', 
        location = N'{data["location"]}' , 
        manager_id = {data["manager_id"]}
        WHERE department_id = {data["department_id"]}
        ''')
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'DELETE FROM departments WHERE department_id = {id}')
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        cursor.execute(f'SELECT department_id, department_name, description, location, manager_id FROM departments WHERE department_id = {id}')
        columns_name = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()
        row_dict = dict(zip(columns_name, row))
        return row_dict
    
    def getCombobox(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('''
            SELECT department_id, department_name
            FROM departments
        ''')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows