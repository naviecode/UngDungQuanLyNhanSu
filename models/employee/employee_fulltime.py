from models.employee import Employee

class FullTimeEmployee(Employee):
    def __init__(self, employee_id, name, date_of_birth, gender, address, phone_number, email, position, department, start_date, id_card_number, salary, notes=None):
        super().__init__(employee_id, name, date_of_birth, gender, address, phone_number, email, position, department, start_date, id_card_number, notes)
        self.salary = salary  # Thêm thuộc tính lương cho nhân viên full-time
    
    def get_full_info(self):
        info = super().get_full_info()  # Kế thừa thông tin từ lớp cha
        info["Salary"] = self.salary    # Thêm thông tin lương vào
        return info