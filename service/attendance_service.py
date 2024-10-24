from datetime import datetime
from data.init_data import InitData
import configparser

class AttendanceService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)

    from datetime import datetime

    def handle(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()

        # Lấy thời gian hiện tại
        now = datetime.now()
        current_time = now.time()

        # Định nghĩa các mốc thời gian
        checkin_end_time = datetime.strptime('09:30', '%H:%M').time()
        checkout_start_time = datetime.strptime('15:30', '%H:%M').time()

        # Kiểm tra thời gian hiện tại có trong khoảng cho phép check-in hoặc check-out
        if input.check_in:
            # Điều kiện cho check-in
            if current_time > checkin_end_time:
                print("Không được check-in sau 9h30 sáng.")
                return
            else:
                # Thực hiện check-in
                insert_query = f"""
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
                """
                cursor.execute(insert_query)

        elif input.check_out:
            # Kiểm tra xem có bản ghi check-in cho ngày hôm đó không
            query = f"""
            SELECT * 
            FROM attendance
            WHERE employee_id = {input.employee_id} 
            AND work_date = CURDATE()
            """
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                # Nếu đã có bản ghi check-in, chỉ cập nhật check-out
                if current_time < checkout_start_time:
                    print("Chưa đến giờ check-out.")
                    return
                else:
                    update_query = f"""
                    UPDATE attendance
                    SET check_out = '{input.check_out}'
                    WHERE employee_id = {input.employee_id} 
                    AND work_date = CURDATE()
                    """
                    cursor.execute(update_query)
            else:
                # Nếu không có bản ghi, thực hiện insert mới
                insert_query = f"""
                INSERT INTO attendance (
                    employee_id,
                    work_date,
                    check_out,
                    status,
                    remarks
                )
                VALUES 
                (
                    {input.employee_id},
                    '{input.work_date}',
                    '{input.check_out}',
                    '{input.status}',
                    '{input.remarks}'
                )
                """
                cursor.execute(insert_query)

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