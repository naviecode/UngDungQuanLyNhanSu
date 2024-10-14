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
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employees (
                name VARCHAR(100) NOT NULL,
                address VARCHAR(50) NOT NULL
            );
            """
            cursor.execute(create_table_query)
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