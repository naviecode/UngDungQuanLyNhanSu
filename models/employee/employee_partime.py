from models.employee import Employee

class PartTimeEmployee(Employee):
    def __init__(self, employee_id, name, date_of_birth, gender, address, phone_number, email, position, department, start_date, id_card_number, hourly_wage, hours_worked, notes=None):
        super().__init__(employee_id, name, date_of_birth, gender, address, phone_number, email, position, department, start_date, id_card_number, notes)
        self.hourly_wage = hourly_wage      # Thêm thuộc tính lương theo giờ cho nhân viên part-time
        self.hours_worked = hours_worked    # Thêm thuộc tính số giờ làm
    
    def get_full_info(self):
        info = super().get_full_info()      # Kế thừa thông tin từ lớp cha
        info["Hourly Wage"] = self.hourly_wage
        info["Hours Worked"] = self.hours_worked
        return info