class UserAlreadyExistsError(Exception):
    pass

class UserDoesntExistError(Exception):
    pass

class UserPasswordError(Exception):
    pass

class TokenIsInvalid(Exception):
    pass
