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
                    contract_id INT PRIMARY KEY AUTO_INCREMENT,     -- Mã hợp đồng
                    employee_id INT NOT NULL,                       -- Mã nhân viên (Foreign Key)
                    start_date DATE NOT NULL,                       -- Ngày bắt đầu hợp đồng
                    end_date DATE,                                  -- Ngày kết thúc hợp đồng (nếu có)
                    salary DECIMAL(10, 2) NOT NULL,                 -- Mức lương
                    benefits TEXT,                                    -- Quyền lợi (nếu có)
                    check_in_time TIME NOT NULL,                             -- Giờ vào
                    check_out_time TIME NOT NULL                             -- Giờ ra
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

            create_table_license_query = """
                CREATE TABLE IF NOT EXISTS leave_requests (
                    request_id INT AUTO_INCREMENT PRIMARY KEY, -- Mã đơn xin nghỉ (ID duy nhất)
                    employee_id INT NOT NULL,                  -- Mã nhân viên liên kết
                    reason TEXT NOT NULL,                      -- Lý do xin nghỉ
                    start_date DATE NOT NULL,                  -- Ngày bắt đầu nghỉ
                    end_date DATE NOT NULL,                    -- Ngày kết thúc nghỉ
                    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending', -- Trạng thái của đơn
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Ngày tạo đơn
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Ngày cập nhật
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) -- Liên kết với bảng nhân viên
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
                cursor.execute("INSERT INTO departments(department_name, description, location, create_date)VALUES(N'Admin', N'Không', 'HCM',CURDATE())")
                cursor.execute("INSERT INTO positions (position_name, description, department_id, create_date)VALUES('Admin', 'Admin', 1, CURDATE())")
                cursor.execute("INSERT INTO employees(name, date_of_birth, gender, address, phone_number, email, position_id, start_date, id_card_number, password, username)VALUES('ADMIN', CURDATE(), 1, 'HCM', '999', 'admin@gmail.com', 1, CURDATE(), '888', '1', 'admin')")
                cursor.execute("INSERT INTO employees(name, date_of_birth, gender, address, phone_number, email, position_id, start_date, id_card_number, password, username)VALUES('sonnq', CURDATE(), 1, 'HCM', '999', 'sonnq@gmail.com', 1, CURDATE(), '888', '1', 'sonnq')")

                cursor.execute("INSERT INTO roles(role_name, description) VALUES('Admin', N'Toàn quyền truy cập và quản lý hệ thống')")
                cursor.execute("INSERT INTO roles(role_name, description) VALUES('Manager', N'Quản lý nhân viên và phòng ban và duyệt đơn xin nghỉ')")
                cursor.execute("INSERT INTO roles(role_name, description) VALUES('User', N'Chấm công, đơn xin nghỉ, xem bảng chấm công')")
                cursor.execute("INSERT INTO employee_roles(employee_id, role_id)VALUES(1, 1)")
                cursor.execute("INSERT INTO employee_roles(employee_id, role_id)VALUES(2, 2)")
                cursor.execute("INSERT INTO employee_roles(employee_id, role_id)VALUES(3, 3)")
            cursor.execute("INSERT INTO attendance (employee_id, check_in, check_out, work_date, status, remarks)VALUES(1, '2024-09-02 08:00:00', '2024-09-02 17:30:00', '2024-09-02', 'OK', 'On time'),(1, '2024-09-03 08:15:00', '2024-09-03 17:30:00', '2024-09-03', 'LATE', '15 minutes late'),(1, '2024-09-04 08:05:00', '2024-09-04 17:00:00', '2024-09-04', 'LATE', 'Left early'),(1, '2024-09-05 08:00:00', '2024-09-05 17:30:00', '2024-09-05', 'OK', 'On time'),(1, NULL, NULL, '2024-09-06', 'UNPLEAVE', 'Absent without leave'),(1, '2024-09-09 08:00:00', '2024-09-09 17:30:00', '2024-09-09', 'OK', 'On time'),(1, '2024-09-10 08:20:00', '2024-09-10 17:30:00', '2024-09-10', 'LATE', '20 minutes late'),(1, '2024-09-11 08:00:00', '2024-09-11 17:30:00', '2024-09-11', 'OK', 'On time'),(1, '2024-09-12 08:30:00', '2024-09-12 16:30:00', '2024-09-12', 'LATE', 'Late and left early'),(1, '2024-09-13 08:00:00', '2024-09-13 17:30:00', '2024-09-13', 'OK', 'On time'),(1, '2024-09-16 08:00:00', '2024-09-16 17:30:00', '2024-09-16', 'OK', 'On time'),(1, '2024-09-17 08:05:00', '2024-09-17 17:30:00', '2024-09-17', 'LATE', '5 minutes late'),(1, '2024-09-18 08:00:00', '2024-09-18 17:30:00', '2024-09-18', 'OK', 'On time'),(1, '2024-09-19 08:10:00', '2024-09-19 17:00:00', '2024-09-19', 'LATE', 'Late and left early'),(1, '2024-09-20 08:00:00', '2024-09-20 17:30:00', '2024-09-20', 'OK', 'On time'),(1, '2024-09-23 08:00:00', '2024-09-23 17:30:00', '2024-09-23', 'OK', 'On time'),(1, '2024-09-24 08:40:00', '2024-09-24 17:30:00', '2024-09-24', 'LATE', '40 minutes late'),(1, '2024-09-25 08:00:00', '2024-09-25 17:30:00', '2024-09-25', 'OK', 'On time'),(1, '2024-09-26 08:00:00', '2024-09-26 16:30:00', '2024-09-26', 'OK', 'Left early'),(1, '2024-09-27 08:00:00', '2024-09-27 17:30:00', '2024-09-27', 'OK', 'On time'),(1, '2024-09-30 08:10:00', '2024-09-30 17:30:00', '2024-09-30', 'LATE', '10 minutes late');")
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