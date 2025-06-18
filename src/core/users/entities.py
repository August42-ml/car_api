class BaseUser:
    def __init__(self, username, email, password, is_admin):
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def get_info(self):
        return {
                "username": self.username,
                "email": self.email,
                "is_admin": self.is_admin,
                }