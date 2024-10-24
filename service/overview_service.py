from data import InitData
import configparser

class OverviewService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)

    def pie_department_data(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('''
            SELECT A.department_name, COUNT(C.employee_id) AS SoLuongNV
            FROM departments A
            LEFT JOIN positions B ON A.department_id = B.department_id
            LEFT JOIN employees C ON B.position_id = C.position_id
            GROUP BY A.department_name
        ''')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    
    def pie_position_data(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('''
            SELECT A.position_name, COUNT(B.employee_id) AS SoLuongNV
            FROM positions A
            LEFT JOIN employees B ON B.position_id = A.position_id
            GROUP BY A.position_name
        ''')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    
    def pie_employee_in_department_data(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('''
            SELECT A.department_id, A.department_name, ROUND(COALESCE(COALESCE(SUM(C.SO_LAN_DI_TRE), 0) / NULLIF(D.SoLuongNV, 0),0)) AS TONG
            FROM departments A
            LEFT JOIN positions B ON A.department_id = B.department_id
            LEFT JOIN 
            (
                SELECT NV.employee_id, NV.position_id, COALESCE(ATD.SO_LAN_DI_TRE, 0) as SO_LAN_DI_TRE
                FROM employees NV
                LEFT JOIN (
                    SELECT EMP_IN.employee_id, COUNT(*) AS SO_LAN_DI_TRE
                    FROM (
                    SELECT A.employee_id, A.work_date, MIN(check_in) as CHECK_IN
                    FROM attendance A
                    GROUP BY A.employee_id, A.work_date) EMP_IN
                    LEFT JOIN (
                    SELECT A.employee_id, A.work_date, MIN(check_out) as CHECK_OUT
                    FROM attendance A
                    GROUP BY A.employee_id, A.work_date) EMP_OUT ON EMP_IN.employee_id = EMP_OUT.employee_id AND EMP_IN.work_date = EMP_OUT.work_date
                    LEFT JOIN contracts CTS ON EMP_IN.employee_id = CTS.employee_id
                    WHERE CTS.check_in_time  < TIME(EMP_IN.CHECK_IN)
                    GROUP BY EMP_IN.employee_id
                )ATD ON NV.employee_id = ATD.employee_id                   
            )           
            C ON B.position_id = C.position_id
            LEFT JOIN (
                SELECT A.department_id, COUNT(C.employee_id) AS SoLuongNV 
                FROM departments A
                LEFT JOIN positions B ON A.department_id = B.department_id
                LEFT JOIN employees C ON B.position_id = C.position_id
                GROUP BY A.department_id           
            )
            D ON A.department_id = D.department_id
            GROUP BY A.department_id, A.department_name              
        ''')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    
    def pie_employee_data(self, employee_id =None):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute(f'''
            SELECT EMP_IN.employee_id,EMP_IN.work_date, TIMESTAMPDIFF(MINUTE, STR_TO_DATE(CONCAT(EMP_IN.work_date, ' ', CTS.check_in_time), '%Y-%m-%d %H:%i:%s'), EMP_IN.CHECK_IN) AS Minutes
            FROM (
            SELECT A.employee_id, A.work_date, MIN(check_in) as CHECK_IN
            FROM attendance A
            GROUP BY A.employee_id, A.work_date) EMP_IN
            LEFT JOIN contracts CTS ON EMP_IN.employee_id = CTS.employee_id
            WHERE CTS.check_in_time  < TIME(EMP_IN.CHECK_IN)
            AND EMP_IN.employee_id = '{employee_id}'
            AND MONTH(EMP_IN.work_date) = MONTH(CURRENT_DATE())
            AND YEAR(EMP_IN.work_date) = YEAR(CURRENT_DATE())
        ''')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows