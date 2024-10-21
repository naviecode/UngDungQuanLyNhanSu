from data.init_data import InitData
import configparser

class AttendanceService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)

    def handle(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()

        query = f"""
        SELECT * 
        FROM attendance
        WHERE employee_id = {input.employee_id} 
        AND work_date = CURDATE() 
        AND check_out IS NULL
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
        # Nếu có bản ghi check-in mà chưa check-out thì cập nhật lại
            update_query = f"""
            UPDATE attendance
            SET check_out = '{input.check_out}'
            WHERE employee_id = {input.employee_id} 
            AND work_date = CURDATE() 
            AND check_out IS NULL
            """
            cursor.execute(update_query)
        else:
            # Nếu không tìm thấy bản ghi, thực hiện check-in mới
            self.db.connection.cursor().execute(f'''
            INSERT INTO attendance (
                employee_id,
                check_in,
                work_date,
                status,
                remarks
            )
            VALUES 
            (
                 {input.employee_id},
                '{input.check_in}',
                '{input.work_date}',
                '{input.status}',
                '{input.remarks}'
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

    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        cursor.execute(f'SELECT * FROM attendance WHERE attendance_id = {id}')

        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()

        return row