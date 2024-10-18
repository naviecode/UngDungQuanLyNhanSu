from data.init_data import InitData
import configparser

class AttendanceService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)

    def insert(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        INSERT INTO attendance (
            attendance_id, 
            employee_id,
            check_in,
            check_out,
            work_date,
            status,
            TEXT
        )
        VALUES 
        (
            {input.attendance_id}, 
            {input.employee_id},
            '{input.check_in}',
            '{input.check_out}',
            '{input.work_date}',
            '{input.status}',
            '{input.TEXT}'
        )
        ''')

        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('SELECT * FROM attendance')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    def update(self, data):
        self.db.connect_database()

        # cursor = self.db.connection.cursor()
        # self.db.connection.cursor().execute(f'''
        # UPDATE employee_roles 
        # SET salary = {data.salary}, 
        # benefits = N'{data.description}'
        # WHERE contract_id = {data.contract_id}
        # ''')
        # self.db.connection.commit()

        # cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'DELETE FROM attendance WHERE attendance_id = {id}')
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        cursor.execute(f'SELECT * FROM attendance WHERE attendance_id = {id}')

        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()

        return row