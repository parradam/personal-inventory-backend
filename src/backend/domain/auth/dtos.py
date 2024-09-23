from attrs import define


@define
class RegisterUserDTO:
    username: str
    email: str
    password: str
