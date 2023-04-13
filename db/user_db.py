from db.db_config import db


class UserDBModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, name: str, phone_number: str, login: str, password: str) -> None:
        self.name = name
        self.phone_number = phone_number
        self.login = login
        self.password = password



