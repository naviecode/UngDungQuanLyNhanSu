from data import InitData
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
            employee_id,
            start_date, 
            end_date,
            salary,
            benefits                            
        )
        VALUES 
        (
            {input["employee_id"]},
            '{input["start_date"]}',
            '{input["end_date"]}',
            {input["salary"]},
            N'{input["benefits"]}'
        )
        ''')

        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute("""
        SELECT A.contract_id,         
        B.name, CONCAT(FORMAT(A.salary, 0), ' VND'), 
        DATE_FORMAT(A.start_date, '%d/%m/%Y') AS start_date, DATE_FORMAT(A.end_date, '%d/%m/%Y') AS end_date               
        FROM contracts A
        LEFT JOIN employees B on A.employee_id = B.employee_id
        """)
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    def update(self, data):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        UPDATE contracts 
        SET salary = {data["salary"]}, 
        benefits = N'{data["benefits"]}'
        WHERE contract_id = {data["contract_id"]}
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
        columns_name = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()
        row_dict = dict(zip(columns_name, row))
        return row_dict