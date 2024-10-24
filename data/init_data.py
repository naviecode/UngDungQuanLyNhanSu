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
                    manager_id INT NULL
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
                    id_card_number VARCHAR(50) NOT NULL,
                    password VARCHAR(50),
                    username VARCHAR(50) NOT NULL
                )                
            """

            create_table_contracts_query = """
                CREATE TABLE IF NOT EXISTS contracts (
                    contract_id INT PRIMARY KEY AUTO_INCREMENT,     
                    employee_id INT NOT NULL,                       
                    start_date DATE NOT NULL,                       
                    end_date DATE,                                  
                    salary DECIMAL(18, 0) NOT NULL,                 
                    benefits TEXT,                                   
                    check_in_time TIME NOT NULL,                            
                    check_out_time TIME NOT NULL                             
                )
            
            """

            create_table_attendance_query = """
                CREATE TABLE IF NOT EXISTS attendance (
                    attendance_id INT PRIMARY KEY AUTO_INCREMENT,   
                    employee_id INT NOT NULL,                      
                    check_in DATETIME NOT NULL,                    
                    check_out DATETIME,                            
                    work_date DATE NOT NULL,                       
                    status VARCHAR(50),                            
                    remarks TEXT                                  
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

            create_table_license_query = """
                CREATE TABLE IF NOT EXISTS leave_requests (
                    request_id INT AUTO_INCREMENT PRIMARY KEY, 
                    employee_id INT NOT NULL,                  
                    reason TEXT NOT NULL,                      
                    start_date DATE NOT NULL,                  
                    end_date DATE NOT NULL,                    
                    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending', 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) 
                )
            """

            cursor.execute(create_table_department_query)
            cursor.execute(create_table_position_query)
            cursor.execute(create_table_employee_query)
            cursor.execute(create_table_contracts_query)
            cursor.execute(create_table_attendance_query)
            cursor.execute(create_table_role_query)
            cursor.execute(create_table_employee_role_query)
            cursor.execute(create_table_license_query)

            self.connection.commit()
        except Error as e:
            self.connection.rollback()
            print(f"Error while creating table: {e}")
        finally:
            cursor.close()

    def create_data(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees")
            result = cursor.fetchone()
            if result[0] == 0:
                cursor.execute("INSERT INTO employees(name, date_of_birth, gender, address, phone_number, email, position_id, start_date, id_card_number, password, username)VALUES('ADMIN', CURDATE(), 1, 'HCM', '999', 'admin@gmail.com', 0, CURDATE(), '888', '1', 'admin')")
                
                cursor.execute("INSERT INTO roles(role_name, description) VALUES('Admin', N'Toàn quyền truy cập và quản lý hệ thống')")
                cursor.execute("INSERT INTO roles(role_name, description) VALUES('Manager', N'Quản lý nhân viên và phòng ban và duyệt đơn xin nghỉ')")
                cursor.execute("INSERT INTO roles(role_name, description) VALUES('User', N'Chấm công, đơn xin nghỉ, xem bảng chấm công')")
                cursor.execute("INSERT INTO employee_roles(employee_id, role_id)VALUES(1, 1)")


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