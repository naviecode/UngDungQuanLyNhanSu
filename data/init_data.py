import sqlite3

class InitData:
    def __init__(self, config):
        self.database = config['database']['database']
        self.connection = None

    def connect_database(self):
        """Kết nối đến cơ sở dữ liệu MySQL."""
        try:
            self.connection = sqlite3.connect(self.database)
            print("Kết nối thành công đến cơ sở dữ liệu.")
        except sqlite3.Error as e:
            print(f"Error while connecting to MySQL: {e}")
    
    def create_table(self):
        """Tạo bảng employees nếu nó chưa tồn tại."""
        try:
            cursor = self.connection.cursor()
            create_table_employee_query = """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name VARCHAR(100) NOT NULL,
                date_of_birth DATE,
                gender INTEGER CHECK (gender IN(0, 1)),
                address VARCHAR(100),
                phone_number VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL,
                position_id INTEGER NOT NULL,
                department_id INTEGER NOT NULL,
                start_date DATE NOT NULL,
                id_card_number VARCHAR(50) NOT NULL,
                password VARCHAR(50)
            );
            """
            cursor.execute(create_table_employee_query)
            self.connection.commit()
            print("Bảng employees đã được tạo thành công.")
        except sqlite3.Error as e:
            print(f"Error while creating table: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        """Đóng kết nối đến cơ sở dữ liệu."""
        self.connection.close()
        print("Kết nối đến cơ sở dữ liệu đã được đóng.")