class employee_model:
    def __init__(self, employee_id, name, date_of_birth, gender, address, phone_number, email, position, department, start_date, id_card_number):
        self.employee_id = employee_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.position = position
        self.department = department
        self.start_date = start_date
        self.id_card_number = id_card_number
    
    def __str__(self):
        return f"Employee({self.employee_id}, {self.name}, {self.position}, {self.department})"
    
    def get_full_info(self):
        return {
            "Employee ID": self.employee_id,
            "Name": self.name,
            "Date of Birth": self.date_of_birth,
            "Gender": self.gender,
            "Address": self.address,
            "Phone Number": self.phone_number,
            "Email": self.email,
            "Position": self.position,
            "Department": self.department,
            "Start Date": self.start_date,
            "ID Card Number": self.id_card_number,
            "Notes": self.notes
        }