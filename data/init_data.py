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
        """Tạo bảng employees nếu nó chưa tồn tại."""
        try:
            cursor = self.connection.cursor()
            create_table_employee_query = """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INT PRIMARY KEY AUTO_INCREMENT, 
                name NVARCHAR(100) NOT NULL,
                date_of_birth DATE,
                gender TINYINT CHECK (gender IN(0, 1)),
                address NVARCHAR(100),
                phone_number VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL,
                position_id INT NOT NULL,
                department_id INT NOT NULL,
                start_date DATE NOT NULL,
                id_card_number VARCHAR(50) NOT NULL,
                password VARCHAR(50)
            );
            """

            cursor.execute(create_table_employee_query)
            self.connection.commit()
            print("Bảng employees đã được tạo thành công.")
        except Error as e:
            print(f"Error while creating table: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Kết nối đến cơ sở dữ liệu đã được đóng.")