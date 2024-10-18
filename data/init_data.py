import mysql.connector
from mysql.connector import Error
class InitData:
    def __init__(self, config):
        self.host = config['database']['host']
        self.user = config['database']['user']
        self.password = config['database']['password']
        self.database = config['database']['database']
        self.connection = None

    def connect_database(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Kết nối thành công đến cơ sở dữ liệu.")
        except Error  as e:
            print(f"Error while connecting to MySQL: {e}")
    
    def create_table(self):
        try:
            cursor = self.connection.cursor()
            create_table_department_query =""" 
                CREATE TABLE IF NOT EXISTS departments (
                    department_id INT PRIMARY KEY AUTO_INCREMENT,
                    department_name VARCHAR(100) NOT NULL,
                    description VARCHAR(500) NULL,
                    location VARCHAR(200) NULL,
                    create_date DATE NOT NULL,
                    manager_id INT NOT NULL
                )
            """
            create_table_position_query = """
                CREATE TABLE IF NOT EXISTS positions (
                    position_id INT PRIMARY KEY AUTO_INCREMENT,
                    position_name VARCHAR(100) NOT NULL,
                    description VARCHAR(500) NULL,
                    create_date DATE NOT NULL,
                    department_id INT NULL 
                )
            """
            create_table_employee_query = """
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id INT PRIMARY KEY AUTO_INCREMENT, 
                    name VARCHAR(100) NOT NULL,
                    date_of_birth DATE,
                    gender TINYINT CHECK (gender IN(0, 1)),
                    address VARCHAR(100),
                    phone_number VARCHAR(50) NOT NULL,
                    email VARCHAR(50) NOT NULL,
                    position_id INT NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NULL,
                    id_card_number VARCHAR(50) NOT NULL,
                    password VARCHAR(50),
                    username VARCHAR(50) NOT NULL
                )                
            """

            create_table_contracts_query = """
                CREATE TABLE IF NOT EXISTS contracts (
                    contract_id INT PRIMARY KEY AUTO_INCREMENT,     -- Mã hợp đồng
                    employee_id INT NOT NULL,                       -- Mã nhân viên (Foreign Key)
                    start_date DATE NOT NULL,                       -- Ngày bắt đầu hợp đồng
                    end_date DATE,                                  -- Ngày kết thúc hợp đồng (nếu có)
                    salary DECIMAL(10, 2) NOT NULL,                 -- Mức lương
                    benefits TEXT                                   -- Quyền lợi (nếu có)
                )
            
            """

            create_table_attendance_query = """
                CREATE TABLE IF NOT EXISTS attendance (
                    attendance_id INT PRIMARY KEY AUTO_INCREMENT,   -- ID chấm công
                    employee_id INT NOT NULL,                       -- Mã nhân viên (Foreign Key)
                    check_in DATETIME NOT NULL,                     -- Thời gian vào làm
                    check_out DATETIME,                             -- Thời gian ra về
                    work_date DATE NOT NULL,                        -- Ngày làm việc
                    status VARCHAR(50),                             -- Trạng thái chấm công (Ví dụ: "Đi làm", "Nghỉ phép", "Đi muộn")
                    remarks TEXT                                   -- Ghi chú (nếu có)
                )
            """

            create_table_role_query = """
                CREATE TABLE IF NOT EXISTS roles (
                    role_id INT PRIMARY KEY AUTO_INCREMENT,   
                    role_name VARCHAR(50) NOT NULL,           
                    description VARCHAR(255)                  
                )
            """

            create_table_employee_role_query = """
                CREATE TABLE IF NOT EXISTS employee_roles (
                    employee_role_id INT PRIMARY KEY AUTO_INCREMENT, 
                    employee_id INT,                          
                    role_id INT                              
                )
            """

            cursor.execute(create_table_department_query)
            cursor.execute(create_table_position_query)
            cursor.execute(create_table_employee_query)
            cursor.execute(create_table_contracts_query)
            cursor.execute(create_table_attendance_query)
            cursor.execute(create_table_role_query)
            cursor.execute(create_table_employee_role_query)
            self.connection.commit()
        except Error as e:
            self.connection.rollback()
            print(f"Error while creating table: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Kết nối đến cơ sở dữ liệu đã được đóng.")