class BaseUser:
    def __init__(self, username, email, password, is_admin, id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def get_info(self):
        return {
                "id": self.id,
                "username": self.username,
                "email": self.email,
                "is_admin": self.is_admin,
                }