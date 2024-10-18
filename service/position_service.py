from data.init_data import InitData
import configparser

class PositionService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)

    def insert(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        INSERT INTO positions (
            position_name, 
            description,
            department_id,
            create_date                            
        )
        VALUES 
        (
            '{input.position_name}', 
            '{input.description}',
            {input.department_id},
            '{input.create_date}'
        )
        ''')

        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('''
            SELECT A.position_id, A.position_name, A.description, A.create_date, B.department_name   
            FROM positions A
            LEFT JOIN departments B ON A.department_id = B.department_id
        ''')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    def update(self, data):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        UPDATE positions 
        SET position_name = N'{data.position_name}', 
        description = N'{data.description}', 
        department_id = {data.department_id}
        WHERE position_id = {data.position_id}
        ''')
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'DELETE FROM positions WHERE position_id = {id}')
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        print(id)
        cursor.execute(f'SELECT position_id, position_name, description, department_id FROM positions WHERE position_id = {id}')

        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()

        return row
    def getCombobox(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('SELECT position_id, position_name FROM positions')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows