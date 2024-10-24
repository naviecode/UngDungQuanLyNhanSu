from data import InitData
import configparser

class TimeSheetService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)
        
    def search(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute(f'''
            SELECT a.employee_id, a.work_date,
            TIME_FORMAT(a.check_in, '%H:%i') AS check_in_time,
            TIME_FORMAT(a.check_out, '%H:%i') AS check_out_time,
            CASE
                WHEN lr.request_id IS NOT NULL 
                    AND a.work_date BETWEEN DATE(lr.start_date) AND DATE(lr.end_date)
                    AND lr.status = 'Approved'
                    AND TIME(lr.start_date) <= '08:00:00' 
                    AND TIME(lr.end_date) >= '12:00:00'
                    THEN 'ONLEAVE'
                WHEN a.check_in IS NULL 
                    THEN 'UNPLEAVE'
                WHEN TIME(a.check_in) <= '08:00:00' 
                    THEN 'OK'
                WHEN TIME(a.check_in) > '08:00:00' 
                    THEN 'LATE'
            END AS check_in_status,
            CASE
                WHEN lr.request_id IS NOT NULL 
                    AND a.work_date BETWEEN DATE(lr.start_date) AND DATE(lr.end_date)
                    AND lr.status = 'Approved'
                    AND TIME(lr.start_date) <= '13:30:00' 
                    AND TIME(lr.end_date) >= '17:30:00'
                    THEN 'ONLEAVE'
                WHEN a.check_out IS NULL 
                    THEN 'UNPLEAVE'
                WHEN TIME(a.check_out) < '17:30:00' 
                    THEN 'SOON'
                WHEN TIME(a.check_out) >= '17:30:00' 
                    THEN 'OK'
            END AS check_out_status
            FROM 
                attendance a
            LEFT JOIN 
                leave_requests lr 
                ON a.employee_id = lr.employee_id 
                AND a.work_date BETWEEN DATE(lr.start_date) AND DATE(lr.end_date)
                AND lr.status = 'Approved'
            WHERE 1 = 1
            AND a.employee_id = {input["emp_id"]}
                AND MONTH(a.work_date) = {input["month"]}
                AND YEAR(a.work_date) = {input["year"]};
        ''')
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.close()
        self.db.close_connection()

        return rows
    
    def dataSummarize(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute(f'''
           SELECT 
            attendance_data.employee_id,
            SUM(
                (CASE 
                    WHEN check_in_status IN ('ONLEAVE', 'OK', 'LATE') THEN 0.5
                    ELSE 0
                END) 
                +
                (CASE 
                    WHEN check_out_status IN ('ONLEAVE', 'OK', 'SOON') THEN 0.5
                    ELSE 0
                END)
            ) AS Total_Workday,
            SUM(
                (CASE 
                    WHEN check_in_status = 'LATE' THEN 1
                    ELSE 0
                END) 
                +
                (CASE 
                    WHEN check_out_status = 'SOON' THEN 1
                    ELSE 0
                END)
            ) AS Total_LateNSoonTimes,
            SUM(
                (CASE 
                    WHEN check_in_status IN ('ONLEAVE', 'UNPLEAVE') THEN 0.5
                    ELSE 0
                END) +
                (CASE 
                    WHEN check_out_status IN ('ONLEAVE', 'UNPLEAVE') THEN 0.5
                    ELSE 0
                END)
            ) AS Total_Off
        FROM 
        (
            SELECT
                a.employee_id,
                a.work_date,        
                TIME_FORMAT(a.check_in, '%H:%i') AS check_in_time,
                TIME_FORMAT(a.check_out, '%H:%i') AS check_out_time,
                CASE
                    WHEN lr.request_id IS NOT NULL 
                        AND a.work_date BETWEEN DATE(lr.start_date) AND DATE(lr.end_date)
                        AND lr.status = 'Approved'
                        AND TIME(lr.start_date) <= '08:00:00' 
                        AND TIME(lr.end_date) >= '12:00:00'
                        THEN 'ONLEAVE'
                    WHEN a.check_in IS NULL 
                        THEN 'UNPLEAVE'
                    WHEN TIME(a.check_in) <= '08:00:00' 
                        THEN 'OK'
                    WHEN TIME(a.check_in) > '08:00:00' 
                        THEN 'LATE'
                END AS check_in_status,
                CASE
                    WHEN lr.request_id IS NOT NULL 
                        AND a.work_date BETWEEN DATE(lr.start_date) AND DATE(lr.end_date)
                        AND lr.status = 'Approved'
                        AND TIME(lr.start_date) <= '13:30:00' 
                        AND TIME(lr.end_date) >= '17:30:00'
                        THEN 'ONLEAVE'
                    WHEN a.check_out IS NULL 
                        THEN 'UNPLEAVE'
                    WHEN TIME(a.check_out) < '17:30:00' 
                        THEN 'SOON'
                    WHEN TIME(a.check_out) >= '17:30:00' 
                        THEN 'OK'
                END AS check_out_status
            FROM 
                attendance a
            LEFT JOIN 
                leave_requests lr 
                ON a.employee_id = lr.employee_id 
                AND a.work_date BETWEEN DATE(lr.start_date) AND DATE(lr.end_date)
                AND lr.status = 'Approved'
            WHERE 1 = 1
            AND a.employee_id = {input["emp_id"]}
            AND MONTH(a.work_date) = {input["month"]}
            AND YEAR(a.work_date) = {input["year"]}
        ) AS attendance_data
        GROUP BY attendance_data.employee_id;


        ''')
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.close()
        self.db.close_connection()

        return rows
    
    def lateNSoonSummarize(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute(f'''
            SELECT a.employee_id,
                SUM(CASE WHEN TIME(a.check_in) > CAST('08:00:00' AS TIME) THEN 1 ELSE 0 END) AS Late_Count,
                SUM(CASE 
                    WHEN TIME(a.check_in) > CAST('08:00:00' AS TIME)
                    THEN TIMESTAMPDIFF(MINUTE, CAST('08:00:00' AS TIME), TIME(a.check_in))
                    ELSE 0 
                    END) AS Total_Late_Minutes,
                SUM(CASE WHEN TIME(a.check_out) < CAST('17:30:00' AS TIME) THEN 1 ELSE 0 END) AS Early_Out_Count,
                SUM(CASE 
                    WHEN TIME(a.check_out) < CAST('17:30:00' AS TIME)
                    THEN TIMESTAMPDIFF(MINUTE, TIME(a.check_out), CAST('17:30:00' AS TIME))
                    ELSE 0 
                    END) AS Total_Early_Out_Minutes,
                (
                    SUM(CASE 
                        WHEN TIME(a.check_in) > CAST('08:00:00' AS TIME)
                        THEN TIMESTAMPDIFF(MINUTE, CAST('08:00:00' AS TIME), TIME(a.check_in))
                        ELSE 0 
                        END)
                    + 
                    SUM(CASE 
                        WHEN TIME(a.check_out) < CAST('17:30:00' AS TIME)
                        THEN TIMESTAMPDIFF(MINUTE, TIME(a.check_out), CAST('17:30:00' AS TIME))
                        ELSE 0 
                        END)
                ) AS Total_Minutes_Late_and_Early,
                (
                    SUM(CASE WHEN TIME(a.check_in) > CAST('08:00:00' AS TIME) THEN 1 ELSE 0 END)
                    +
                    SUM(CASE WHEN TIME(a.check_out) < CAST('17:30:00' AS TIME) THEN 1 ELSE 0 END)
                ) AS Total_Late_and_Early_Out_Count
            FROM attendance a
            WHERE 1 = 1
            AND a.employee_id = {input["emp_id"]}
            AND MONTH(a.work_date) = {input["month"]}
            AND YEAR(a.work_date) = {input["year"]}
            GROUP BY a.employee_id;
        ''')
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.close()
        self.db.close_connection()

        return rows
    
    def onLeaveSummarize(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute(f'''
            SELECT attendance_data.employee_id,
                SUM(
                    (CASE 
                        WHEN check_in_status = 'ONLEAVE' THEN 0.5
                        ELSE 0
                    END) +
                    (CASE 
                        WHEN check_out_status = 'ONLEAVE' THEN 0.5
                        ELSE 0
                    END)
                ) AS Total_ONLEAVE,
                SUM(
                    (CASE 
                        WHEN check_in_status = 'UNPLEAVE' THEN 0.5
                        ELSE 0
                    END) +
                    (CASE 
                        WHEN check_out_status = 'UNPLEAVE' THEN 0.5
                        ELSE 0
                    END)
                ) AS Total_UNPLEAVE,
                SUM(
                    (CASE 
                        WHEN check_in_status = 'ONLEAVE' THEN 0.5
                        ELSE 0
                    END) +
                    (CASE 
                        WHEN check_out_status = 'ONLEAVE' THEN 0.5
                        ELSE 0
                    END)
                ) +
                SUM(
                    (CASE 
                        WHEN check_in_status = 'UNPLEAVE' THEN 0.5
                        ELSE 0
                    END) +
                    (CASE 
                        WHEN check_out_status = 'UNPLEAVE' THEN 0.5
                        ELSE 0
                    END)
                ) AS Total_LEAVE
            FROM 
            (
                SELECT
                    a.employee_id,      
                    CASE
                        WHEN lr.request_id IS NOT NULL 
                            AND a.work_date BETWEEN DATE(lr.start_date) AND DATE(lr.end_date)
                            AND lr.status = 'Approved'
                            AND TIME(lr.start_date) <= '08:00:00' 
                            AND TIME(lr.end_date) >= '12:00:00'
                            THEN 'ONLEAVE'
                        WHEN a.check_in IS NULL 
                            THEN 'UNPLEAVE'
                        WHEN TIME(a.check_in) <= '08:00:00' 
                            THEN 'OK'
                        WHEN TIME(a.check_in) > '08:00:00' 
                            THEN 'LATE'
                    END AS check_in_status,
                    CASE
                        WHEN lr.request_id IS NOT NULL 
                            AND a.work_date BETWEEN DATE(lr.start_date) AND DATE(lr.end_date)
                            AND lr.status = 'Approved'
                            AND TIME(lr.start_date) <= '13:30:00' 
                            AND TIME(lr.end_date) >= '17:30:00'
                            THEN 'ONLEAVE'
                        WHEN a.check_out IS NULL 
                            THEN 'UNPLEAVE'
                        WHEN TIME(a.check_out) < '17:30:00' 
                            THEN 'SOON'
                        WHEN TIME(a.check_out) >= '17:30:00' 
                            THEN 'OK'
                    END AS check_out_status
                FROM 
                    attendance a
                LEFT JOIN 
                    leave_requests lr 
                    ON a.employee_id = lr.employee_id 
                    AND a.work_date BETWEEN DATE(lr.start_date) AND DATE(lr.end_date)
                    AND lr.status = 'Approved'
                WHERE 1 = 1
                AND a.employee_id = {input["emp_id"]}
                AND MONTH(a.work_date) = {input["month"]}
                AND YEAR(a.work_date) = {input["year"]}
            ) AS attendance_data
                
            GROUP BY attendance_data.employee_id;

        ''')
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.close()
        self.db.close_connection()

        return rows
        