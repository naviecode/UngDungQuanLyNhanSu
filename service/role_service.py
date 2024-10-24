from data import InitData
import configparser

class RoleService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)

    def insert(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        self.db.connection.cursor().execute(f'''
        INSERT INTO roles (
            role_name,
            description                           
        )
        VALUES 
        (
            N'{input["role_name"]}',
            N'{input["description"]}'
        )
        ''')

        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self, filter = None):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('SELECT * FROM roles')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    def update(self, data):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        UPDATE roles 
        SET role_name = '{data["role_name"]}', 
        description = N'{data["description"]}'
        WHERE role_id = {data["role_id"]}
        ''')
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'DELETE FROM roles WHERE role_id = {id}')
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        cursor.execute(f'SELECT role_id, role_name, description FROM roles WHERE role_id = {id}')
        columns_name = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()
        row_dict = dict(zip(columns_name, row))
        return row_dict
    def getCombobox(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('SELECT role_id, role_name FROM roles')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows