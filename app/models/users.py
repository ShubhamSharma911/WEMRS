from app.models.user_enum import UserRole, EmpCategory

class User:
    def __init__(self, id: int, name: str, email: str, role: UserRole, emp_category: EmpCategory):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.emp_category = emp_category
