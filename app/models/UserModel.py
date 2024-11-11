from models.BaseModel import BaseModel

class UserModel(BaseModel):
    table_name = "User"

    def __init__(self):
        super().__init__()

    def create_user(self, name: str, email: str, pwd: str,balance:str):
        data = {
            "name": name,
            "email": email,
            "pwd": pwd,
            "balance": balance,
        }
        return self.save(data)

    def get_by_email(self, email: str):
        sql = f"SELECT * FROM {self.table_name} WHERE email = %s"
        self.cursor.execute(sql, (email,))
        return self.cursor.fetchone()
