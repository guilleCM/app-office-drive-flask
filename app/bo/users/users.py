from app.models.users.users import Users, Roles
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

class AuthenticationError(Exception):
    pass


class UsersBO:
    def __init__(self):
        self._ORM = None
        self.username = ""
        self.password = ""
        self.company_ref = ""
        self.email = ""
        self.name = ""
        self.address = ""
        self.city = ""
        self.nif = ""
        self.tel = ""
        self.roles = None
        self.c_date = None
        self.access_token = None
        self.refresh_token = None

    def insert(self):
        roles_collection = []
        for rol in self.roles:
            embedded_rol = Roles(
                description=rol['description'],
                name=rol['name']
            )
            roles_collection.append(embedded_rol)
        user = Users(
            username=self.username,
            password=self.generate_hash(self.password),
            company_ref=self.company_ref,
            email=self.email,
            name=self.name,
            address=self.address,
            city=self.city,
            nif=self.nif,
            tel=self.tel,
            roles=roles_collection,
        )
        user.save()
        self.c_date = user.c_date
        self._ORM = user

    def get_id(self):
        return self._ORM.id

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def login(self, username, password):
        user = Users.objects(username=username).first()
        if user is not None and self.verify_hash(password, user.password):
            self.access_token = create_access_token(identity=username)
            self.refresh_token = create_access_token(identity=username)
            self._ORM = user
            self._set_data_from_ORM()
        else:
            raise AuthenticationError("Not valid credentials.")

    def _set_data_from_ORM(self):
        self.username = self._ORM.username
        self.password = self._ORM.password
        self.company_ref = self._ORM.company_ref
        self.email = self._ORM.email
        self.name = self._ORM.name
        self.address = self._ORM.address
        self.city = self._ORM.city
        self.nif = self._ORM.nif
        self.tel = self._ORM.tel
        self.roles = self._ORM.roles
        self.c_date = self._ORM.c_date
