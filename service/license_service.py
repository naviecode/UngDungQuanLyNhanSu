from data.init_data import InitData
import configparser

class LicenseService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)
        
    def insert(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        print(input)
        self.db.connection.cursor().execute(f'''
        INSERT INTO leave_requests (
            employee_id, 
            reason,
            start_date, 
            end_date
        )
        VALUES 
        (
            {input["employee_id"]}, 
            '{input["reason"]}',
            '{input["start_date"]}',
            '{input["end_date"]}'
        )
        ''')

        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self, filters = None):
        self.db.connect_database()
        cursor = self.db.connection.cursor()

        if filters is None:
            cursor.execute(f'''
            SELECT A.request_id, B.name, A.reason, DATE_FORMAT(A.start_date, '%d/%m/%Y') AS start_date, 
            DATE_FORMAT(A.end_date, '%d/%m/%Y') AS end_date, A.status
            FROM leave_requests A           
            LEFT JOIN employees B ON A.employee_id = B.employee_id
            ''')
        else:
            cursor.execute(f'''
            SELECT A.request_id, B.name, A.reason, DATE_FORMAT(A.start_date, '%d/%m/%Y') AS start_date, 
            DATE_FORMAT(A.end_date, '%d/%m/%Y') AS end_date, A.status
            FROM leave_requests A           
            LEFT JOIN employees B ON A.employee_id = B.employee_id
            WHERE A.employee_id = {filters["employee_id"]}
        ''')
        
        
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    
    

    def update(self, data):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        UPDATE leave_requests 
        SET status = N'{data["status"]}'
        WHERE request_id = {data["request_id"]}
        ''')
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'DELETE FROM leave_requests WHERE request_id = {id}')
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()

        cursor.execute(f'''
        SELECT request_id, employee_id, reason, start_date, end_date, status
        FROM leave_requests                        
        WHERE request_id = {id}
        ''')

        columns_name = [desc[0] for desc in cursor.description]

        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()

        row_dict = dict(zip(columns_name, row))
        return row_dict
    