from data.init_data import InitData
import configparser

class ContractService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)

    def insert(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        INSERT INTO contracts (
            contract_id, 
            employee_id,
            start_date, 
            end_date,
            salary,
            benefits                            
        )
        VALUES 
        (
            {input.contract_id}, 
            {input.employee_id},
            '{input.start_date}',
            '{input.end_date}',
            {input.salary},
            '{input.benefits}'
        )
        ''')

        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('SELECT * FROM contracts')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    def update(self, data):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        UPDATE contracts 
        SET salary = {data.salary}, 
        benefits = N'{data.description}'
        WHERE contract_id = {data.contract_id}
        ''')
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'DELETE FROM contracts WHERE contract_id = {id}')
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        cursor.execute(f'SELECT * FROM contracts WHERE contract_id = {id}')

        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()

        return row